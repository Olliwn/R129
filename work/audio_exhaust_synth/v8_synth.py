"""
Procedural V8 synth — Gate 0 of the exhaust augmentation prototype.

Design (v3.1, validated against UMIK-1 reference of the actual car):

Architecture is unchanged from v3 (tonal core + Hann pulse train +
deterministic 8-element cylinder signature + low-frequency drift).
v3.1 reflects what we now know about the real M119 character after the
2026-05-14 UMIK-1 / order-axis / low-frequency analysis (see
`m119_sideband_diagnosis.md`):

  • The real engine has a clean 1× and 2× firing-rate spectrum with
    NO half-integer firing harmonics above noise floor. Our cylinder
    signature already produces that — `fire ± 1×cyl_rate` sidebands
    only, no `fire ± 4×cyl_rate` content. Confirmed correct.
  • The 6.4 Hz envelope modulation of the firing line at idle, which
    was at one point thought to be a Welch artifact, is real and is
    exactly the cylinder-event rate (`fire/8`). Our mod-8 cylinder
    signature produces exactly this. Confirmed correct.
  • The dominant 40–70 Hz feature in the real recordings is a **fixed
    acoustic resonance** of the cabin / exhaust system, not combustion.
    The synth must NOT model it — it will be re-introduced acoustically
    by the cabin. (If anything, the in-car DSP front-channel parametric
    EQ should put a notch / cut around the resonance centre once REW
    measures it.)
  • There is a real 1× engine-speed line at ~12 Hz (idle) climbing
    through the rev — engine-block rocking on (likely worn) mounts.
    This is largely infrasonic. The synth must NOT inject any content
    here — wasted subwoofer headroom. v3.1 adds a **24 Hz subsonic
    high-pass** at the synth output to enforce this.
  • bank_asymmetry stays small (0.03–0.12) because we now know the real
    engine's 0.5× firing line sits at noise floor.

Implementation pieces:

  • Continuous (unwrapped) crank phase, bridged across blocks.
  • Tonal core = a clean fundamental sinusoid at the firing rate +
    selected harmonics (2nd/4th) with preset-controlled levels.
    Carries the dominant spectral peaks cleanly.
  • Hann pulse train = the transient "blat" that gives the V8 its
    pulsed character and supplies higher-order harmonic content. Pulse
    width is preset-controlled.
  • Cylinder signature = an 8-element table (one entry per cylinder in
    the firing order) of (amplitude, phase_offset) pairs. Indexed by
    `floor(firing_count) mod 8`. Plus low-frequency per-cylinder drift.
  • Sub-band rumble = a low-passed Hann pulse at the crank rate.
  • Bank-asymmetry modulation (much weaker than v2).
  • Continuous turbulence noise (state-preserved LP) + firing-gated
    burst noise.
  • Exhaust-pipe bandpass biquad (state-preserved) with preset Q.
  • Light tanh saturator (gentler than v2).
  • Subsonic high-pass (24 Hz, 2nd order) at the synth output — keeps
    the rocking-mode region clean.
  • Engaged-fade envelope (one-pole towards target).
  • Hard ±SAFETY_PEAK safety clip on the final output.

Phase convention is unchanged: crank_phase wraps to [0, 2π) at the
input but the synth keeps an internal continuous (unwrapped) phase so
fractional orders never half-wave-rectify.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi


# ─────────────────────────────────────────────────────────────────────
# Preset palette
# ─────────────────────────────────────────────────────────────────────

@dataclass
class PresetSpec:
    """Per-preset synth parameters. See module docstring for the
    architecture each parameter plugs into. Levels chosen so that the
    luxury preset roughly matches the real M119 spectrum at idle
    (firing fundamental dominant, weak harmonics, present sidebands).

    tonal_fund      Linear gain on the clean firing-rate sinusoid. This
                    is the main carrier of the spectral peak.
    tonal_1p5       Gain on a 1.5×-firing sine. Models exhaust standing-
                    wave resonances that boost odd half-integer firing
                    harmonics in open / sport exhausts; OEM mufflers
                    damp these out. Sport target sits this at ~0.18
                    (−15 dB rel fundamental); OEM keeps it at ~0.0.
    tonal_o2        Gain on the 2nd-order sinusoid (8× crank). Real
                    M119 OEM idle puts this 35 dB below the fundamental
                    (so ~0.02), sport target ~10 dB below (~0.32).
    tonal_2p5       Gain on a 2.5×-firing sine. Same role as tonal_1p5
                    one octave up — only used in sport-style presets
                    where exhaust resonances pump the 2.5× line.
    tonal_o4        Gain on the 4th-order. Tiny at idle for OEM
                    (~0.005); somewhat larger for sport (~0.05).
    pulse_gain      Gain on the Hann pulse train. Provides upper-
                    harmonic colour and the audible "blat".
    pulse_width     Hann pulse width as a fraction of the firing-rate
                    period (0.05..0.6). Narrow ⇒ broadband ⇒ sharp.
    pulse_jitter    Stddev of the residual random per-firing amplitude
                    jitter (broadband noise floor).
    cyl_amp_spread  Stddev of the deterministic 8-cylinder amplitude
                    signature. The cylinder signature is what produces
                    the real engine's discrete fire ± k·cyl-rate
                    sidebands.
    cyl_phase_spread Stddev of the per-cylinder phase nudge (radians at
                    firing rate). Adds a tiny FM contribution.
    bank_asymmetry  Strength of the slow 2nd-order amplitude modulation
                    representing cross-plane bank-firing unevenness.
                    Real M119 idle is small (~0.05–0.10) — v2 used 5×
                    that and over-energised the engine-cycle line.
    sub_pulse_gain  Amplitude of the crank-rate sub-pulse (low-passed
                    rumble below the firing fundamental).
    sustained_noise Continuous combustion turbulence floor.
    pulsed_noise    Firing-rate-gated burst noise.
    pipe_f0_hz      Exhaust-pipe bandpass centre frequency.
    pipe_q          Bandpass Q. Sport keeps this low (open pipe).
    pipe_mix        Wet/dry mix of the pipe filter.
    sat_drive       Pre-gain into the tanh saturator.
    master          Preset master gain into the safety clip.
    """

    tonal_fund: float
    tonal_1p5: float
    tonal_o2: float
    tonal_2p5: float
    tonal_o4: float
    pulse_gain: float
    pulse_width: float
    pulse_jitter: float
    cyl_amp_spread: float
    cyl_phase_spread: float
    bank_asymmetry: float
    sub_pulse_gain: float
    sustained_noise: float
    pulsed_noise: float
    pipe_f0_hz: float
    pipe_q: float
    pipe_mix: float
    sat_drive: float
    master: float


PRESETS: dict[str, PresetSpec] = {
    "off": PresetSpec(
        tonal_fund=0.0, tonal_1p5=0.0, tonal_o2=0.0, tonal_2p5=0.0, tonal_o4=0.0,
        pulse_gain=0.0, pulse_width=0.35, pulse_jitter=0.0,
        cyl_amp_spread=0.0, cyl_phase_spread=0.0, bank_asymmetry=0.0,
        sub_pulse_gain=0.0, sustained_noise=0.0, pulsed_noise=0.0,
        pipe_f0_hz=120.0, pipe_q=2.0, pipe_mix=0.0,
        sat_drive=1.0, master=0.0,
    ),
    "oem": PresetSpec(
        # Quiet, well-muffled. Real M119 measurement (m1 UMIK-1) shows
        # cyl-rate envelope modulation depth ≈ 0.6 % (envelope-spectrum
        # peak at 6 Hz sits at −45 dB rel passband). cyl_amp_spread and
        # bank_asymmetry tuned to that level — earlier values of
        # 0.10–0.20 produced an audibly dramatic 6/12 Hz pulse-amplitude
        # variation that the real engine doesn't have.
        tonal_fund=0.55, tonal_1p5=0.0, tonal_o2=0.012, tonal_2p5=0.0, tonal_o4=0.002,
        pulse_gain=0.022, pulse_width=0.65, pulse_jitter=0.005,
        cyl_amp_spread=0.015, cyl_phase_spread=0.010, bank_asymmetry=0.008,
        sub_pulse_gain=0.06, sustained_noise=0.012, pulsed_noise=0.018,
        pipe_f0_hz=85.0, pipe_q=2.8, pipe_mix=0.60,
        sat_drive=1.0, master=0.42,
    ),
    "luxury": PresetSpec(
        # Closest spectral match to a real M119 with stock-ish exhaust.
        # cyl_amp_spread/bank_asymmetry kept near OEM levels — both
        # presets target a healthy V8, the difference between them is
        # broadband presence, not cylinder-balance audibility.
        tonal_fund=0.62, tonal_1p5=0.0, tonal_o2=0.018, tonal_2p5=0.0, tonal_o4=0.004,
        pulse_gain=0.030, pulse_width=0.60, pulse_jitter=0.008,
        cyl_amp_spread=0.020, cyl_phase_spread=0.012, bank_asymmetry=0.012,
        sub_pulse_gain=0.10, sustained_noise=0.022, pulsed_noise=0.025,
        pipe_f0_hz=95.0, pipe_q=2.4, pipe_mix=0.55,
        sat_drive=1.05, master=0.55,
    ),
    "amg": PresetSpec(
        # Sport-character but still tonal. Mid-way between luxury (clean
        # firing-rate-and-harmonics signature) and sport (open-pipe
        # rasp). Modest half-integer content — represents a sport
        # muffler with some residual chamber damping. Cylinder-balance
        # audibility kept at near-luxury level so the character comes
        # from the harmonics, not from cylinder-pulse asymmetry.
        tonal_fund=0.65, tonal_1p5=0.06, tonal_o2=0.10, tonal_2p5=0.05, tonal_o4=0.03,
        pulse_gain=0.20, pulse_width=0.25, pulse_jitter=0.015,
        cyl_amp_spread=0.025, cyl_phase_spread=0.015, bank_asymmetry=0.020,
        sub_pulse_gain=0.22, sustained_noise=0.08, pulsed_noise=0.20,
        pipe_f0_hz=140.0, pipe_q=1.5, pipe_mix=0.30,
        sat_drive=1.25, master=0.70,
    ),
    "sport": PresetSpec(
        # Aftermarket sport exhaust on M119. Reference: MG Motorsport
        # SL500 R129 idle clip (2026-05-14). The first sport tune used a
        # very narrow, mostly-dry Hann pulse plus strong firing-gated
        # noise, which measured OK spectrally but sounded like a tick
        # train: the 500 Hz high-pass trace showed isolated impulses at
        # every firing event. This version keeps the sport harmonic
        # signature but treats the pulse as a wider pressure wave, moves
        # rasp into sustained turbulence, and lets more of the pulse pass
        # through the pipe resonance instead of the dry path.
        tonal_fund=0.66, tonal_1p5=0.18, tonal_o2=0.26, tonal_2p5=0.16, tonal_o4=0.040,
        pulse_gain=0.12, pulse_width=0.34, pulse_jitter=0.020,
        cyl_amp_spread=0.030, cyl_phase_spread=0.020, bank_asymmetry=0.025,
        sub_pulse_gain=0.30, sustained_noise=0.58, pulsed_noise=0.16,
        pipe_f0_hz=220.0, pipe_q=0.9, pipe_mix=0.25,
        sat_drive=1.30, master=0.85,
    ),
}


def available_presets() -> list[str]:
    return list(PRESETS.keys())


# ─────────────────────────────────────────────────────────────────────
# Pulse-shape primitives
# ─────────────────────────────────────────────────────────────────────

def _hann_pulse(phase_mod: np.ndarray, width_frac: float) -> np.ndarray:
    """Hann-shaped pulse of fractional width within a 2π cycle.

    phase_mod : (n,) wrapped phase ∈ [0, 2π)
    width_frac : 0..1 fraction of the cycle the pulse occupies

    Returns: (n,) in [0, 1], smooth start, smooth end, zero between
    pulses. Zero derivative at both ends → no click whatever the
    firing rate.
    """
    w = max(1e-4, min(1.0, float(width_frac))) * (2.0 * np.pi)
    out = np.zeros_like(phase_mod)
    mask = phase_mod < w
    inside = phase_mod[mask]
    out[mask] = 0.5 * (1.0 - np.cos(2.0 * np.pi * inside / w))
    return out


# ─────────────────────────────────────────────────────────────────────
# V8 synth
# ─────────────────────────────────────────────────────────────────────

class V8Synth:
    """Procedural cross-plane V8 synth, block-rate vectorised on NumPy."""

    SAFETY_PEAK = 0.70
    FADE_TAU_SEC = 0.05

    def __init__(self, sample_rate: int = 48000, preset: str = "luxury", seed: int = 42):
        if preset not in PRESETS:
            raise ValueError(f"unknown preset {preset!r}; choose from {available_presets()}")
        self.fs = int(sample_rate)
        self.preset_name = preset
        self.preset: PresetSpec = PRESETS[preset]
        self.master_gain = 1.0
        self._rng = np.random.default_rng(seed)

        self._fade = 0.0
        self._target_fade = 1.0

        # Unwrapped crank-phase accumulator (preserved across blocks).
        self._unwrapped_phase: float = 0.0
        self._last_block_phase: Optional[float] = None

        # Cylinder-signature tables. The 8-element amplitude table is
        # what produces the discrete fire ± k·cyl-rate sidebands in the
        # real spectrum. It is *deterministic* — every engine cycle
        # plays the same 8 amplitudes in firing order, which is exactly
        # what makes the modulation periodic at the cylinder-event rate
        # (and therefore line-spectrum-producing rather than broadband).
        # Random per-pulse jitter sits on top for the noise floor.
        self._n_cylinders = 8
        self._cyl_amp = self._rng.standard_normal(self._n_cylinders).astype(np.float32)
        self._cyl_phase = self._rng.standard_normal(self._n_cylinders).astype(np.float32)
        # Slow per-cylinder long-term drift (one engine-cycle period).
        self._cyl_drift_target = self._cyl_amp.copy()
        self._cyl_drift_state = self._cyl_amp.copy()
        # Long random-per-pulse jitter table for the broadband floor.
        self._jitter_table_len = 512
        self._jitter_table = self._rng.standard_normal(self._jitter_table_len).astype(np.float32)

        # State-preserving filter chains. Built once, kept warm.
        self._noise_lp_b, self._noise_lp_a = butter(
            2, 4000.0, btype="low", fs=self.fs, output="ba"
        )
        self._noise_lp_zi = lfilter_zi(self._noise_lp_b, self._noise_lp_a) * 0.0

        self._sub_lp_b, self._sub_lp_a = butter(
            2, 110.0, btype="low", fs=self.fs, output="ba"
        )
        self._sub_lp_zi = lfilter_zi(self._sub_lp_b, self._sub_lp_a) * 0.0

        self._pipe_b, self._pipe_a = self._design_pipe_filter()
        self._pipe_zi = lfilter_zi(self._pipe_b, self._pipe_a) * 0.0

        # Subsonic high-pass at 24 Hz. Removes any sub-audible content
        # the synth might radiate into the subwoofer (the real-car
        # 1×-rev rocking line at 12-30 Hz that the M2 recording shows
        # is mechanical, infrasonic, and should not be reproduced).
        self._sub_hp_b, self._sub_hp_a = butter(
            2, 24.0, btype="high", fs=self.fs, output="ba"
        )
        self._sub_hp_zi = lfilter_zi(self._sub_hp_b, self._sub_hp_a) * 0.0

        # Half-integer-harmonic phase-noise state. The 1.5× and 2.5×
        # firing harmonics emerge in real engines from bank-firing
        # alternation + manifold/exhaust resonance, both of which jitter
        # cycle-to-cycle. If we synthesise them as *pure phase-coherent
        # sines* against the fundamental they beat at exactly 0.5×fire
        # (=24 Hz at idle), producing an audible "loud-quiet" pulse
        # alternation. Slow random phase walks (OU process, ~3 Hz BW,
        # stationary RMS ~1.5 rad) broaden these lines into ~5 Hz-wide
        # peaks that match the real spectrum, while breaking the rigid
        # beat. State preserved across blocks for continuity.
        self._half_int_phase = np.zeros(2, dtype=np.float64)  # [1.5x, 2.5x]
        self._half_int_phase_lp = np.zeros(2, dtype=np.float64)
        self._half_int_bw_hz = 3.0
        self._half_int_rms_rad = 1.5

    # ── public API ────────────────────────────────────────────────────

    def set_preset(self, name: str) -> None:
        if name not in PRESETS:
            raise ValueError(f"unknown preset {name!r}; choose from {available_presets()}")
        self.preset_name = name
        self.preset = PRESETS[name]
        # Pipe filter depends on preset.
        self._pipe_b, self._pipe_a = self._design_pipe_filter()
        # Keep current zi state (zeros) — filter will warm up over a few ms.
        self._pipe_zi = lfilter_zi(self._pipe_b, self._pipe_a) * 0.0

    def set_intensity(self, intensity: float) -> None:
        self.master_gain = float(np.clip(intensity, 0.0, 1.0))

    def set_engaged(self, engaged: bool) -> None:
        self._target_fade = 1.0 if engaged else 0.0

    def reset(self) -> None:
        self._fade = 0.0
        self._target_fade = 1.0
        self._unwrapped_phase = 0.0
        self._last_block_phase = None
        self._noise_lp_zi[:] = 0.0
        self._sub_lp_zi[:] = 0.0
        self._pipe_zi[:] = 0.0
        self._sub_hp_zi[:] = 0.0
        self._cyl_drift_state[:] = self._cyl_amp
        self._half_int_phase[:] = 0.0
        self._half_int_phase_lp[:] = 0.0

    def render(
        self,
        rpm: np.ndarray,
        crank_phase: np.ndarray,
        confidence: float = 1.0,
    ) -> np.ndarray:
        """Render one stereo block. See module docstring for inputs.

        Returns float32 (n, 2).
        """
        crank_phase = np.asarray(crank_phase, dtype=np.float32)
        rpm = np.asarray(rpm, dtype=np.float32)
        n = int(crank_phase.shape[0])
        if rpm.shape[0] != n:
            raise ValueError("rpm and crank_phase must have the same length")
        if n == 0:
            return np.zeros((0, 2), dtype=np.float32)

        p = self.preset

        # ── 1. Continuous (unwrapped) crank phase across blocks ────
        phase64 = crank_phase.astype(np.float64)
        unwrapped_local = np.unwrap(phase64)
        if self._last_block_phase is not None:
            bridge = (phase64[0] - self._last_block_phase) % (2.0 * np.pi)
            unwrapped_local = (
                unwrapped_local - unwrapped_local[0]
                + self._unwrapped_phase + bridge
            )
        else:
            unwrapped_local = unwrapped_local - unwrapped_local[0] + self._unwrapped_phase
        self._unwrapped_phase = float(unwrapped_local[-1])
        self._last_block_phase = float(phase64[-1])

        firing_phase = 4.0 * unwrapped_local              # rad
        firing_count = firing_phase * (1.0 / (2.0 * np.pi))

        # ── 2. Cylinder signature — deterministic per-cylinder values
        # repeating once per engine cycle (8 firings). This creates the
        # discrete fire ± k·cyl-rate sidebands seen in the real spectrum.
        #
        # IMPORTANT: continuously interpolate between the 8 cylinder
        # entries instead of holding each constant. A piecewise-constant
        # modulation puts a step discontinuity in amp_sig (and phase_sig)
        # at every firing transition (= 48 Hz at idle). When that
        # multiplies / phase-shifts the continuous tonal sine, each step
        # is an audible click whose 8-cylinder pattern repeats at the
        # cylinder-event rate ≈ 6 Hz at idle. Linear interp removes the
        # value discontinuities, leaving a piecewise-linear modulation
        # whose harmonic content rolls off as 1/k² instead of 1/k —
        # inaudible at the levels we use.
        cyl_pos = (firing_count % self._n_cylinders).astype(np.float32)
        i0 = np.floor(cyl_pos).astype(np.int64) % self._n_cylinders
        i1 = (i0 + 1) % self._n_cylinders
        frac = np.clip(cyl_pos - i0.astype(np.float32), 0.0, 1.0)
        cyl_amp_norm = (
            (1.0 - frac) * self._cyl_drift_state[i0]
            + frac * self._cyl_drift_state[i1]
        )
        cyl_phase_norm = (
            (1.0 - frac) * self._cyl_phase[i0]
            + frac * self._cyl_phase[i1]
        )
        amp_sig = 1.0 + p.cyl_amp_spread * cyl_amp_norm
        phase_sig = p.cyl_phase_spread * cyl_phase_norm
        # Per-firing random residual jitter for broadband noise floor.
        # This one CAN stay piecewise-constant because it is only ever
        # multiplied with the Hann pulse, which is exactly zero at every
        # firing transition (the pulse closes between firings). The
        # discontinuity therefore lands on a zero crossing and is silent.
        jit_idx = np.floor(firing_count).astype(np.int64) % self._jitter_table_len
        amp_residual = 1.0 + p.pulse_jitter * self._jitter_table[jit_idx]
        # Apply slow drift to the cylinder-signature targets between blocks
        # so the sidebands are not perfectly stationary. Drift constant
        # picked so the targets walk on a time scale of ~10 s.
        drift_alpha = float(np.clip(n / (10.0 * self.fs), 1e-5, 0.1))
        self._cyl_drift_state += drift_alpha * (
            self._rng.standard_normal(self._n_cylinders).astype(np.float32) * 0.4
            - self._cyl_drift_state
        )

        # ── 3. Clean tonal core — sine harmonics on continuous phase.
        # This is what carries the dominant fundamental peak. Apply the
        # cylinder-amplitude signature to the fundamental so the
        # sidebands appear in the line spectrum exactly where the real
        # engine has them.
        # Sample-rate slow random phase walk for the half-integer
        # harmonics. We integrate LP-filtered Gaussian noise into a
        # leaky accumulator (OU process). The block-rate update is a
        # simple linear ramp of the per-block start/end values — fine
        # for 3 Hz BW, since the per-sample variation is tiny relative
        # to the 1.5×fire rate (>50 Hz). Random walk is generated only
        # if either half-integer level is non-zero.
        if (p.tonal_1p5 != 0.0) or (p.tonal_2p5 != 0.0):
            dt = float(n) / float(self.fs)
            k_decay = 2.0 * np.pi * self._half_int_bw_hz
            sigma_step = self._half_int_rms_rad * np.sqrt(2.0 * k_decay * dt)
            # OU update for the two harmonics independently
            new_phase = np.zeros(2, dtype=np.float64)
            for h in (0, 1):
                step = float(self._rng.standard_normal()) * sigma_step
                new_phase[h] = (
                    self._half_int_phase[h] * np.exp(-k_decay * dt) + step
                )
            # Ramp from old to new across the block (smooth, no glitch).
            phase_walk_15 = np.linspace(
                self._half_int_phase[0], new_phase[0], n, dtype=np.float64
            )
            phase_walk_25 = np.linspace(
                self._half_int_phase[1], new_phase[1], n, dtype=np.float64
            )
            self._half_int_phase[:] = new_phase
        else:
            phase_walk_15 = np.zeros(n, dtype=np.float64)
            phase_walk_25 = np.zeros(n, dtype=np.float64)

        sin_fund = np.sin(firing_phase + phase_sig.astype(np.float64))
        sin_1p5  = np.sin(1.5 * firing_phase + phase_walk_15)
        sin_o2   = np.sin(2.0 * firing_phase)
        sin_2p5  = np.sin(2.5 * firing_phase + phase_walk_25)
        sin_o4   = np.sin(4.0 * firing_phase)
        tonal = (
            p.tonal_fund * sin_fund.astype(np.float32) * amp_sig
            + p.tonal_1p5 * sin_1p5.astype(np.float32)
            + p.tonal_o2 * sin_o2.astype(np.float32)
            + p.tonal_2p5 * sin_2p5.astype(np.float32)
            + p.tonal_o4 * sin_o4.astype(np.float32)
        )

        # ── 4. Hann pulse train — supplies upper harmonics + blat ──
        fp_mod = np.mod(firing_phase, 2.0 * np.pi).astype(np.float32)
        pulse = _hann_pulse(fp_mod, p.pulse_width) * amp_sig * amp_residual

        # Weak 2nd-order amplitude modulation — cross-plane V8 lopiness.
        # Real M119 idle has 0.5× line ≈ −24 dB; v2's bank_asymmetry of
        # 0.25–0.50 over-energised this. The luxury preset's 0.07 here
        # lines up with the measured target.
        if p.bank_asymmetry > 0.0:
            mod = 0.5 + 0.5 * np.cos(unwrapped_local.astype(np.float64))
            mod = (1.0 - p.bank_asymmetry) + p.bank_asymmetry * mod
            pulse = pulse * mod.astype(np.float32)
            tonal = tonal * mod.astype(np.float32)

        # ── 5. Sub-band rumble — one Hann pulse per crank rev, LP'd ─
        crank_mod = np.mod(unwrapped_local, 2.0 * np.pi).astype(np.float32)
        sub_pulse = _hann_pulse(crank_mod, 0.55) * p.sub_pulse_gain
        sub_pulse, self._sub_lp_zi = lfilter(
            self._sub_lp_b, self._sub_lp_a, sub_pulse, zi=self._sub_lp_zi
        )

        # ── 6. Continuous turbulence noise (state-preserving LP) ───
        raw_noise = self._rng.standard_normal(n).astype(np.float32) * 0.35
        smoothed_noise, self._noise_lp_zi = lfilter(
            self._noise_lp_b, self._noise_lp_a, raw_noise, zi=self._noise_lp_zi
        )
        smoothed_noise = smoothed_noise.astype(np.float32)
        rpm_norm = np.clip(rpm / 3000.0, 0.2, 2.0).astype(np.float32)
        sustained = smoothed_noise * p.sustained_noise * rpm_norm
        pulsed = smoothed_noise * p.pulsed_noise * pulse

        # ── 7. Dry mix ─────────────────────────────────────────────
        dry = (tonal + p.pulse_gain * pulse + sub_pulse + sustained + pulsed)
        dry *= p.master * self.master_gain

        # ── 8. Pipe resonance (wet/dry) ────────────────────────────
        if p.pipe_mix > 1e-3:
            wet, self._pipe_zi = lfilter(
                self._pipe_b, self._pipe_a, dry, zi=self._pipe_zi
            )
            mix = float(np.clip(p.pipe_mix, 0.0, 1.0))
            sig = wet.astype(np.float32) * mix + dry * (1.0 - mix)
        else:
            sig = dry

        # ── 9. Saturator ──────────────────────────────────────────
        sig = np.tanh(sig * p.sat_drive).astype(np.float32)

        # ── 10. Subsonic high-pass — never radiate <24 Hz content.
        # The real M119 has a strong 1×-rev infrasonic rocking line
        # (12–33 Hz across the rev range, see m2 low-frequency
        # waterfall) that is mechanical, inaudible, and would just
        # waste subwoofer headroom if synthesised. Strip it here.
        sig, self._sub_hp_zi = lfilter(
            self._sub_hp_b, self._sub_hp_a, sig, zi=self._sub_hp_zi
        )
        sig = sig.astype(np.float32)

        # ── 11. Engaged/confidence fade ────────────────────────────
        target = float(np.clip(self._target_fade * confidence, 0.0, 1.0))
        fade_env = self._make_fade_env(n, target)
        sig = sig * fade_env

        # ── 12. Safety ceiling ─────────────────────────────────────
        sig = np.clip(sig, -1.0, 1.0).astype(np.float32) * self.SAFETY_PEAK

        return np.stack([sig, sig], axis=1).astype(np.float32)

    @property
    def fade_level(self) -> float:
        return float(self._fade)

    # ── internals ─────────────────────────────────────────────────────

    def _design_pipe_filter(self) -> tuple[np.ndarray, np.ndarray]:
        """Bandpass biquad approximating an exhaust pipe resonance.

        Note: we use a 2nd-order Butterworth bandpass with bandwidth set
        by the requested Q. Not a "true" resonator (no high-Q peak),
        but enough to add audible pipe colour without ringing into
        instability.
        """
        f0 = float(np.clip(self.preset.pipe_f0_hz, 30.0, 1000.0))
        q = float(np.clip(self.preset.pipe_q, 0.4, 8.0))
        bw = max(10.0, f0 / q)
        f_lo = max(20.0, f0 - 0.5 * bw)
        f_hi = min(self.fs * 0.45, f0 + 0.5 * bw)
        if f_hi <= f_lo + 1.0:
            f_hi = f_lo + 1.0
        return butter(2, [f_lo, f_hi], btype="band", fs=self.fs, output="ba")

    def _make_fade_env(self, n: int, target: float) -> np.ndarray:
        if n == 0:
            return np.empty(0, dtype=np.float32)
        tau_samples = max(1.0, self.FADE_TAU_SEC * self.fs)
        alpha = 1.0 - float(np.exp(-1.0 / tau_samples))
        decay = (1.0 - alpha) ** np.arange(n, dtype=np.float64)
        env = target + (self._fade - target) * decay
        self._fade = float(env[-1])
        return env.astype(np.float32)
