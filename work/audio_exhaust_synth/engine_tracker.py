"""
Engine-order tracker — Gate 1.

Estimates the dominant V8 firing order from a mic / WAV signal and
maintains a phase-locked oscillator the synth can ride.

Pipeline:

  audio block ──▶ bandpass 20..350 Hz ──▶ windowed FFT ──▶ peak finder
                                                          │
                              SNR-vs-in-band-noise        │
                                  ──▶ confidence  ◀───────┘
                                                          │
                              slew-rate-limited           │
                              one-pole tracker  ◀─────────┘
                                          │
                                          ▼
                              phase integrator @ crank rate
                                          │
                                          ▼
                              (rpm, crank_phase, confidence)

Design notes (per the plan):
  • Track the firing rate (4 × crank) because it is the strongest line in a
    V8 acoustic spectrum and sits in 40–333 Hz for 600–5000 rpm — well
    inside what a phone or UMIK-1 can capture and bandpass cleanly.
  • PLL frequency is slew-rate limited so transient noise spikes can't yank
    the phase. Synth lag is acceptable for steady-state and gentle revs;
    sharp throttle stabs lag visibly. This is explicitly accepted in the
    plan's latency budget (50–150 ms target).
  • Confidence is a normalised SNR of the peak vs in-band noise floor.
    Below threshold the prototype fades the synth out instead of free-
    running on a stale RPM.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi


class EngineTracker:
    """Block-rate firing-order tracker.

    Construct once with the audio sample rate, then feed mono blocks via
    ``process`` and read back (rpm, crank_phase, confidence) per block.
    """

    def __init__(
        self,
        sample_rate: int = 48000,
        rpm_min: float = 500.0,
        rpm_max: float = 5500.0,
        analysis_bw_hz: tuple[float, float] = (20.0, 380.0),
        analysis_window_sec: float = 0.085,
        snr_min_db: float = 6.0,
        snr_full_db: float = 18.0,
        slew_hz_per_sec: float = 800.0,
        pll_alpha: float = 0.45,
    ):
        self.fs = int(sample_rate)
        self.rpm_min = float(rpm_min)
        self.rpm_max = float(rpm_max)
        self.snr_min_db = float(snr_min_db)
        self.snr_full_db = float(snr_full_db)
        # Slew limit is per-second (RPM-rate-of-change shaped); the per-block
        # cap is derived from this and the block length so behaviour is
        # independent of caller block size.
        self.slew_hz_per_sec = float(slew_hz_per_sec)
        self.pll_alpha = float(pll_alpha)

        f_lo, f_hi = analysis_bw_hz
        # SOS bandpass keeps the in-band magnitude flat and gives a stable
        # filter state for streaming use.
        self._sos = butter(4, [f_lo, f_hi], btype="band", fs=self.fs, output="sos")
        self._zi = sosfilt_zi(self._sos) * 0.0

        # Firing-rate search window in Hz
        self.firing_min = rpm_min * 4.0 / 60.0
        self.firing_max = rpm_max * 4.0 / 60.0

        # Internal analysis buffer. The FFT runs on this longer window
        # regardless of the caller's block size — required so the bin
        # spacing is fine enough to discriminate adjacent V8 orders
        # (≈ 50 Hz apart at idle). 85 ms @ 48 kHz → ~12 Hz bins, well
        # inside the safety margin.
        self._win_n = max(1024, int(analysis_window_sec * self.fs))
        # Round up to power of two for FFT speed.
        n = 1
        while n < self._win_n:
            n *= 2
        self._win_n = n
        self._buf = np.zeros(self._win_n, dtype=np.float32)
        self._win = np.hanning(self._win_n).astype(np.float32)
        self._freqs = np.fft.rfftfreq(self._win_n, 1.0 / self.fs)
        self._band_mask = (self._freqs >= self.firing_min) & (
            self._freqs <= self.firing_max
        )

        # PLL state — start near idle firing rate (800 rpm → 53 Hz).
        self._pll_freq = 800.0 * 4.0 / 60.0
        self._pll_phase = 0.0   # firing-rate phase, integrated across blocks
        self._confidence = 0.0

    def reset(self) -> None:
        self._zi[:] = 0.0
        self._buf[:] = 0.0
        self._pll_freq = 800.0 * 4.0 / 60.0
        self._pll_phase = 0.0
        self._confidence = 0.0

    # ── public API ────────────────────────────────────────────────────

    @property
    def confidence(self) -> float:
        return float(self._confidence)

    @property
    def rpm_estimate(self) -> float:
        return float(self._pll_freq * 60.0 / 4.0)

    def process(self, audio_block: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
        """Process one mono block.

        Returns (rpm, crank_phase, confidence):
          rpm          (n,) float32, repeated PLL estimate (constant within block)
          crank_phase  (n,) float32, wrapped to [0, 2π)
          confidence   scalar 0..1
        """
        block = np.asarray(audio_block, dtype=np.float32)
        n = block.shape[0]
        if n == 0:
            return (
                np.empty(0, dtype=np.float32),
                np.empty(0, dtype=np.float32),
                self._confidence,
            )

        # Bandpass (state-preserving across blocks).
        filtered, self._zi = sosfilt(self._sos, block, zi=self._zi)

        # Slide the analysis buffer and append the new bandpassed samples.
        if n >= self._win_n:
            self._buf[:] = filtered[-self._win_n :]
        else:
            self._buf[:-n] = self._buf[n:]
            self._buf[-n:] = filtered

        # Windowed FFT on the longer analysis buffer — gives the bin
        # resolution needed to discriminate adjacent V8 orders.
        spec = np.fft.rfft(self._buf * self._win)
        mag = np.abs(spec)

        if not self._band_mask.any():
            new_conf = 0.0
            peak_freq = self._pll_freq
        else:
            band_mag = mag[self._band_mask]
            band_freqs = self._freqs[self._band_mask]
            peak_idx = int(np.argmax(band_mag))
            peak_mag = float(band_mag[peak_idx])

            # Parabolic interpolation around the peak for sub-bin accuracy.
            if 0 < peak_idx < len(band_mag) - 1:
                a = float(band_mag[peak_idx - 1])
                b = float(peak_mag)
                c = float(band_mag[peak_idx + 1])
                denom = (a - 2.0 * b + c)
                offset = 0.5 * (a - c) / denom if abs(denom) > 1e-12 else 0.0
                offset = float(np.clip(offset, -1.0, 1.0))
            else:
                offset = 0.0
            bin_df = float(band_freqs[1] - band_freqs[0]) if len(band_freqs) > 1 else 0.0
            peak_freq = float(band_freqs[peak_idx] + offset * bin_df)

            # Robust noise-floor estimate: median of in-band bins excluding
            # ±2 bins around the peak (otherwise the peak dominates the
            # median for narrow analysis windows + concentrated spectra).
            lo = max(0, peak_idx - 2)
            hi = min(len(band_mag), peak_idx + 3)
            kept = np.concatenate([band_mag[:lo], band_mag[hi:]])
            noise = float(np.median(kept)) + 1e-9 if kept.size else 1e-9
            snr_db = 20.0 * np.log10(max(peak_mag, 1e-9) / noise)
            new_conf = float(
                np.clip(
                    (snr_db - self.snr_min_db) / max(1e-6, self.snr_full_db - self.snr_min_db),
                    0.0,
                    1.0,
                )
            )

        # Smooth confidence with a one-pole.
        self._confidence = 0.6 * self._confidence + 0.4 * new_conf

        # Slew-rate-limited PLL on the firing-rate measurement. Slew limit
        # scales with the block duration so behaviour is invariant to the
        # caller's chosen block size.
        block_sec = n / self.fs
        slew_block = self.slew_hz_per_sec * block_sec
        if self._confidence > 0.20:
            delta = float(np.clip(peak_freq - self._pll_freq, -slew_block, slew_block))
            self._pll_freq += self.pll_alpha * delta

        # Clamp PLL to sane RPM bounds.
        self._pll_freq = float(
            np.clip(self._pll_freq, self.firing_min, self.firing_max)
        )

        # Integrate phase at the crank rate (= firing_rate / 4) so the
        # caller can multiply by harmonic order N to get the Nth-order
        # phase.
        crank_freq = self._pll_freq / 4.0
        dphase = 2.0 * np.pi * crank_freq / self.fs
        phase_arr = self._pll_phase + np.arange(n, dtype=np.float64) * dphase
        self._pll_phase = float((phase_arr[-1] + dphase) % (2.0 * np.pi))
        crank_phase = (phase_arr % (2.0 * np.pi)).astype(np.float32)

        rpm_value = float(crank_freq * 60.0)
        rpm_arr = np.full(n, rpm_value, dtype=np.float32)

        return rpm_arr, crank_phase, float(self._confidence)
