"""
RPM source abstraction — keeps the synth sensor-agnostic.

A RpmSource yields, per audio block:
  - rpm         (n,) instantaneous crank RPM per sample
  - crank_phase (n,) wrapped crank phase in radians
  - confidence  scalar, 0..1

This is the key abstraction the plan calls out: same V8 synth code works
with a synthetic RPM curve, a WAV file + mic tracker, an accelerometer,
or eventually a CAN/ignition-pulse RPM signal. New sources just implement
``render``.

Two sources land here:
  - SyntheticSource — Gate 0. Drives the synth from a slider / sweep /
    idle wobble / throttle stab pattern. Phase is integrated internally.
  - WavFileSource — Gate 1. Pulls samples from a WAV (e.g. a phone-recorded
    exhaust clip) and runs them through engine_tracker.EngineTracker to
    derive rpm + crank_phase from the audio.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional  # noqa: F401  (used by WavFileSource type hints)

import numpy as np


@dataclass
class RpmBlock:
    rpm: np.ndarray         # (n,) float32, crank RPM per sample
    crank_phase: np.ndarray # (n,) float32, wrapped to [0, 2π)
    confidence: float       # scalar 0..1
    mic: Optional[np.ndarray] = None  # (n,) mono — set by mic-based sources


class RpmSource:
    """Abstract source. Implementations must define ``render``."""

    def render(self, n_samples: int, sample_rate: int) -> RpmBlock:
        raise NotImplementedError

    def reset(self) -> None:
        """Optional hook for sources that hold time-based state."""


class SyntheticSource(RpmSource):
    """Drives the synth from a parameterised RPM curve.

    Modes:
      hold(rpm)        : constant
      idle()           : wobbling idle around 800 rpm
      sweep(a, b, T)   : triangle 800↔3000-style sweep with period T sec
      stab(low, high, T): periodic throttle stab (low → high → low) every T sec
    """

    def __init__(
        self,
        mode: str = "hold",
        rpm: float = 1500.0,
        start: float = 800.0,
        end: float = 3000.0,
        duration: float = 8.0,
        stab_low: float = 900.0,
        stab_high: float = 4000.0,
    ):
        if mode not in ("hold", "idle", "sweep", "stab"):
            raise ValueError(f"unknown mode {mode!r}")
        self.mode = mode
        self.rpm = float(rpm)
        self.start = float(start)
        self.end = float(end)
        self.duration = float(duration)
        self.stab_low = float(stab_low)
        self.stab_high = float(stab_high)
        self._t = 0.0
        self._phase = 0.0   # crank phase accumulator (radians)

    def reset(self) -> None:
        self._t = 0.0
        self._phase = 0.0

    def render(self, n_samples: int, sample_rate: int) -> RpmBlock:
        dt = 1.0 / sample_rate
        t = self._t + np.arange(n_samples, dtype=np.float64) * dt
        self._t = float(t[-1] + dt) if n_samples else self._t

        if self.mode == "hold":
            rpm = np.full(n_samples, self.rpm, dtype=np.float32)

        elif self.mode == "idle":
            # 800 rpm with a slow ±30 rpm wobble (engine-mount + idle valve)
            wobble = 30.0 * np.sin(2.0 * np.pi * 0.7 * t)
            rpm = (800.0 + wobble).astype(np.float32)

        elif self.mode == "sweep":
            # Triangle 0..1..0 over `duration` seconds, then loops.
            ph = (t % self.duration) / self.duration
            tri = 1.0 - 2.0 * np.abs(ph - 0.5)
            rpm = (self.start + (self.end - self.start) * tri).astype(np.float32)

        else:  # stab
            # Half-period ramp up, half-period ramp down, repeats.
            ph = (t % self.duration) / self.duration
            up = self.stab_low + (self.stab_high - self.stab_low) * (ph / 0.5)
            dn = self.stab_high - (self.stab_high - self.stab_low) * ((ph - 0.5) / 0.5)
            rpm = np.where(ph < 0.5, up, dn).astype(np.float32)
            rpm = np.clip(rpm, 600.0, 6500.0).astype(np.float32)

        crank_freq = rpm / 60.0
        dphase = 2.0 * np.pi * crank_freq.astype(np.float64) / sample_rate
        phase = self._phase + np.cumsum(dphase)
        if n_samples:
            self._phase = float(phase[-1] % (2.0 * np.pi))
        crank_phase = (phase % (2.0 * np.pi)).astype(np.float32)

        return RpmBlock(rpm=rpm, crank_phase=crank_phase, confidence=1.0)


class WavFileSource(RpmSource):
    """Streams a recorded exhaust WAV through an engine tracker.

    The tracker derives instantaneous firing-order frequency and provides
    a phase-locked output for the synth. Mono-sums multichannel files.

    Loops the file by default so a 30-second idle clip can be played
    back continuously while the user tweaks presets.
    """

    def __init__(
        self,
        wav_path: str,
        tracker,
        loop: bool = True,
        target_sample_rate: Optional[int] = None,
    ):
        """Load a recorded exhaust clip and prepare it for tracker streaming.

        target_sample_rate
            If set and different from the file's native rate, resample to
            this rate (polyphase filter). Useful so a low-rate phone
            recording (e.g. 8 kHz) can run through a 48 kHz tracker/synth
            pipeline for audition through the living-room rig at full
            stereo bandwidth on the synth side.
        """
        import soundfile as sf  # lazy: only needed if a WAV source is used
        data, file_sr = sf.read(wav_path, dtype="float32", always_2d=True)
        mono = np.mean(data, axis=1).astype(np.float32)
        self.file_sr = int(file_sr)
        if target_sample_rate is not None and int(target_sample_rate) != self.file_sr:
            from scipy.signal import resample_poly  # lazy
            from math import gcd
            tgt = int(target_sample_rate)
            g = gcd(tgt, self.file_sr)
            up = tgt // g
            down = self.file_sr // g
            mono = resample_poly(mono, up, down).astype(np.float32)
            self.sample_rate = tgt
        else:
            self.sample_rate = self.file_sr

        # Seamless-loop preprocessing. Raw concatenation of clip end → clip
        # start gives a single-sample step at every wrap (verified
        # audibly as a click at t = N·duration). We bake an equal-power
        # crossfade of length `fade_len` between the clip's tail and head,
        # then trim the tail. After this transform, looping is
        # mathematically continuous because the cross-faded head meets the
        # last unchanged body sample at the exact original adjacency, with
        # no derivative discontinuity. Crossfade length is short enough
        # (~30 ms) that it doesn't disturb the engine-cycle content used
        # by the tracker.
        if loop and mono.size > 0:
            fade_len = max(8, min(int(0.030 * self.sample_rate), mono.size // 8))
            fade = (0.5 * (1.0 - np.cos(
                np.pi * np.arange(fade_len, dtype=np.float32) / fade_len
            ))).astype(np.float32)
            head = mono[:fade_len].copy()
            tail = mono[-fade_len:].copy()
            mono = mono.copy()
            mono[:fade_len] = head * fade + tail * (1.0 - fade)
            mono = mono[:-fade_len]

        self.audio = mono
        self.tracker = tracker
        self.loop = bool(loop)
        self._cursor = 0
        self.last_confidence: float = 0.0

    def reset(self) -> None:
        self._cursor = 0
        self.tracker.reset()

    def render(self, n_samples: int, sample_rate: int) -> RpmBlock:
        if sample_rate != self.sample_rate:
            # The tracker is configured for the WAV source's working rate at
            # construction time; the prototype runner ensures they match.
            raise ValueError(
                f"WAV source rate {self.sample_rate} != requested sr "
                f"{sample_rate}; rebuild the tracker at the source rate"
            )

        n_total = len(self.audio)
        if n_total == 0:
            block = np.zeros(n_samples, dtype=np.float32)
        elif self._cursor + n_samples <= n_total:
            block = self.audio[self._cursor : self._cursor + n_samples]
            self._cursor += n_samples
        elif self.loop:
            # Wrap to start
            head = self.audio[self._cursor :]
            need = n_samples - len(head)
            tail = self.audio[: need % n_total]
            block = np.concatenate([head, tail]).astype(np.float32)
            self._cursor = need % n_total
        else:
            head = self.audio[self._cursor :]
            block = np.concatenate(
                [head, np.zeros(n_samples - len(head), dtype=np.float32)]
            ).astype(np.float32)
            self._cursor = n_total

        rpm, phase, conf = self.tracker.process(block)
        self.last_confidence = float(conf)
        return RpmBlock(rpm=rpm, crank_phase=phase, confidence=conf, mic=block)
