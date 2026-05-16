"""
Exhaust synth prototype runner.

Two main subcommands:

  preview  — Gate 0. Drive the V8 synth from a synthetic RPM curve
             (hold / idle / sweep / stab). Plays through default audio
             output (sounddevice) and/or writes a WAV.

  track    — Gate 1. Drive the V8 synth from a recorded exhaust WAV by
             passing it through the engine tracker. Writes diagnostic
             outputs (synth-only, downmix of mic+synth, side-by-side
             stereo) for offline A/B listening.

Other utilities:

  compare      — Render every preset back-to-back into one long WAV so
                 you can audition them in sequence.
  make-clip    — Synthesise a "fake exhaust" WAV by running the synth
                 with sport preset + room reverb + mic noise. Useful for
                 testing the Gate 1 tracker before you have a real
                 recording from the M119.

Audio output is optional — if sounddevice isn't installed, --out FILE is
used as the sole output. The prototype never plays louder than the synth's
internal soft-limiter ceiling (≈ -3 dBFS).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np

from v8_synth import V8Synth, available_presets, PRESETS
from rpm_source import SyntheticSource, WavFileSource
from engine_tracker import EngineTracker


SAMPLE_RATE_DEFAULT = 48000
BLOCK_DEFAULT = 512   # ≈ 10.7 ms @ 48 kHz, fits within the plan's latency budget


def _try_import_sounddevice():
    try:
        import sounddevice as sd  # type: ignore
        return sd
    except Exception:
        return None


def _try_import_soundfile():
    try:
        import soundfile as sf  # type: ignore
        return sf
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────
# Rendering helpers
# ─────────────────────────────────────────────────────────────────────

def render_synthetic(
    *,
    preset: str,
    mode: str,
    rpm: float,
    start: float,
    end: float,
    duration: float,
    intensity: float,
    sample_rate: int,
    block: int,
    total_seconds: float,
) -> np.ndarray:
    """Render Gate 0 audio. Returns (n_total, 2) float32."""
    src = SyntheticSource(
        mode=mode, rpm=rpm, start=start, end=end, duration=duration
    )
    synth = V8Synth(sample_rate=sample_rate, preset=preset)
    synth.set_intensity(intensity)
    synth.set_engaged(True)

    n_total = int(total_seconds * sample_rate)
    out = np.zeros((n_total, 2), dtype=np.float32)
    cursor = 0
    while cursor < n_total:
        n = min(block, n_total - cursor)
        rpm_block = src.render(n, sample_rate)
        audio = synth.render(rpm_block.rpm, rpm_block.crank_phase, rpm_block.confidence)
        out[cursor : cursor + n] = audio
        cursor += n
    return out


def render_tracked(
    *,
    wav_path: str,
    preset: str,
    intensity: float,
    block: int,
    total_seconds: float,
    work_sample_rate: int = 48000,
) -> dict:
    """Run Gate 1 tracker on a WAV. Returns dict of named float32 arrays.

    work_sample_rate
        Sample rate that tracker, synth, and output run at. The input WAV
        is resampled to this rate on load — lets us audition an 8 kHz phone
        recording through the living-room rig at full bandwidth on the
        synth side.

    Keys:
      mic       (n, 2) original mic, stereo-duplicated
      synth     (n, 2) synth output, phase-locked to mic
      downmix   (n, 2) mic + synth at relative levels (mic at -6 dBFS, synth -9 dBFS)
      side      (n, 2) [L = mic mono, R = synth mono] for visual alignment
      rpm       (n,)   tracker RPM estimate
      conf      (n,)   tracker confidence
    """
    sf = _try_import_soundfile()
    if sf is None:
        raise RuntimeError("soundfile not installed; pip install -r requirements.txt")

    sr = int(work_sample_rate)
    tracker = EngineTracker(sample_rate=sr)
    src = WavFileSource(wav_path, tracker, loop=True, target_sample_rate=sr)
    synth = V8Synth(sample_rate=sr, preset=preset)
    synth.set_intensity(intensity)
    synth.set_engaged(True)
    sample_rate = sr

    n_total = int(total_seconds * sample_rate)
    mic_out = np.zeros((n_total, 1), dtype=np.float32)
    synth_out = np.zeros((n_total, 2), dtype=np.float32)
    rpm_out = np.zeros(n_total, dtype=np.float32)
    conf_out = np.zeros(n_total, dtype=np.float32)

    cursor = 0
    while cursor < n_total:
        n = min(block, n_total - cursor)
        rpm_block = src.render(n, sample_rate)
        audio = synth.render(rpm_block.rpm, rpm_block.crank_phase, rpm_block.confidence)
        mic_out[cursor : cursor + n, 0] = rpm_block.mic if rpm_block.mic is not None else 0.0
        synth_out[cursor : cursor + n] = audio
        rpm_out[cursor : cursor + n] = rpm_block.rpm
        conf_out[cursor : cursor + n] = rpm_block.confidence
        cursor += n

    # Downmix: mic at -6 dBFS-ish, synth at -9 dBFS-ish — roughly what the
    # in-car DSP gain staging target will look like.
    mic_gain = 0.5
    synth_gain = 0.355
    mic_stereo = np.repeat(mic_out, 2, axis=1)
    downmix = (mic_stereo * mic_gain + synth_out * synth_gain).astype(np.float32)
    # Final soft limit to keep |downmix| ≤ 0.7
    downmix = np.tanh(downmix * 1.2).astype(np.float32) * 0.7

    # Side-by-side: left = mic, right = synth (mono-summed)
    side = np.concatenate(
        [mic_stereo[:, :1] * 0.7, synth_out.mean(axis=1, keepdims=True) * 0.7],
        axis=1,
    ).astype(np.float32)

    return dict(
        sample_rate=sample_rate,
        mic=mic_stereo.astype(np.float32),
        synth=synth_out,
        downmix=downmix,
        side=side,
        rpm=rpm_out,
        conf=conf_out,
    )


# ─────────────────────────────────────────────────────────────────────
# Output / playback helpers
# ─────────────────────────────────────────────────────────────────────

def write_wav(path: str, audio: np.ndarray, sample_rate: int) -> None:
    sf = _try_import_soundfile()
    if sf is None:
        raise RuntimeError("soundfile not installed; pip install -r requirements.txt")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, audio, sample_rate, subtype="PCM_24")
    print(f"  wrote {path}  ({len(audio)/sample_rate:.2f}s @ {sample_rate} Hz)")


def play_audio(audio: np.ndarray, sample_rate: int) -> bool:
    """Play through default device. Returns True on success.

    Always honours the synth's internal soft-limit ceiling — no extra gain
    applied here. If sounddevice isn't installed, returns False so the
    caller can fall back to WAV-only output.
    """
    sd = _try_import_sounddevice()
    if sd is None:
        print("  sounddevice not installed; skipping playback (use --out to write a WAV)")
        return False
    print(f"  playing {len(audio)/sample_rate:.2f}s through default output…")
    try:
        sd.play(audio, sample_rate, blocking=True)
        sd.wait()
        return True
    except Exception as exc:
        print(f"  playback failed: {exc}")
        return False


# ─────────────────────────────────────────────────────────────────────
# Subcommands
# ─────────────────────────────────────────────────────────────────────

def cmd_preview(args: argparse.Namespace) -> int:
    print(
        f"Gate 0 preview — preset={args.preset!r}, mode={args.mode!r}, "
        f"duration={args.duration:.1f}s, intensity={args.intensity:.2f}"
    )
    audio = render_synthetic(
        preset=args.preset,
        mode=args.mode,
        rpm=args.rpm,
        start=args.start,
        end=args.end,
        duration=args.cycle if args.mode == "sweep" else args.duration,
        intensity=args.intensity,
        sample_rate=args.sample_rate,
        block=args.block,
        total_seconds=args.duration,
    )
    if args.out:
        write_wav(args.out, audio, args.sample_rate)
    if not args.no_play:
        play_audio(audio, args.sample_rate)
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    print("Gate 0 preset comparison — sweep on each preset, back to back.")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for preset in available_presets():
        if preset == "off":
            continue
        print(f"  rendering preset={preset}")
        audio = render_synthetic(
            preset=preset,
            mode="sweep",
            rpm=1500.0,
            start=args.start,
            end=args.end,
            duration=args.cycle,
            intensity=args.intensity,
            sample_rate=args.sample_rate,
            block=args.block,
            total_seconds=args.seconds_per_preset,
        )
        write_wav(str(out_dir / f"compare_{preset}.wav"), audio, args.sample_rate)
        # Silence gap between presets for the joined version
        gap = np.zeros((int(0.5 * args.sample_rate), 2), dtype=np.float32)
        parts.append(audio)
        parts.append(gap)
    if parts:
        joined = np.concatenate(parts, axis=0)
        write_wav(str(out_dir / "compare_all.wav"), joined, args.sample_rate)
        if not args.no_play:
            play_audio(joined, args.sample_rate)
    return 0


def cmd_track(args: argparse.Namespace) -> int:
    print(
        f"Gate 1 tracker — wav={args.wav!r}, preset={args.preset!r}, "
        f"duration={args.duration:.1f}s, intensity={args.intensity:.2f}"
    )
    result = render_tracked(
        wav_path=args.wav,
        preset=args.preset,
        intensity=args.intensity,
        block=args.block,
        total_seconds=args.duration,
        work_sample_rate=args.work_sr,
    )
    sr = result["sample_rate"]
    if args.synth_out:
        write_wav(args.synth_out, result["synth"], sr)
    if args.downmix_out:
        write_wav(args.downmix_out, result["downmix"], sr)
    if args.side_out:
        write_wav(args.side_out, result["side"], sr)

    # Brief tracker stats
    conf = result["conf"]
    rpm = result["rpm"]
    lock_frac = float(np.mean(conf > 0.5))
    print(
        f"  tracker: rpm range {rpm.min():.0f}..{rpm.max():.0f}, "
        f"mean confidence {conf.mean():.2f}, locked-fraction {lock_frac*100:.0f}%"
    )
    if not args.no_play:
        # Default playback choice: downmix (most representative of in-car)
        which = args.play
        audio = result.get(which)
        if audio is None or audio.ndim != 2:
            print(f"  --play={which} not available; choose synth | downmix | side")
        else:
            play_audio(audio, sr)
    return 0


def cmd_make_clip(args: argparse.Namespace) -> int:
    """Synthesise a 'fake exhaust' WAV for testing the tracker.

    Uses the V8 synth itself with the sport preset, then post-processes
    with bandpass + saturation + noise to roughly mimic a mic-captured
    exhaust signal. Not a substitute for a real recording, but enough to
    exercise the Gate 1 tracker pipeline end-to-end.
    """
    sr = args.sample_rate
    audio = render_synthetic(
        preset="sport",
        mode="sweep",
        rpm=1500.0,
        start=args.start,
        end=args.end,
        duration=args.cycle,
        intensity=1.0,
        sample_rate=sr,
        block=args.block,
        total_seconds=args.duration,
    )
    mono = audio.mean(axis=1)
    # Add ambient mic noise (-50 dBFS hiss)
    noise = np.random.default_rng(123).standard_normal(len(mono)).astype(np.float32) * 0.003
    # Gentle compression to mimic a phone mic AGC + saturation
    mono = np.tanh(mono * 1.8 + noise).astype(np.float32) * 0.6
    out = np.stack([mono, mono], axis=1)
    write_wav(args.out, out, sr)
    print(
        f"  synthetic exhaust clip written. Note: this is *not* a real M119 capture; "
        f"it lets you verify the tracker chain before you have a real recording."
    )
    return 0


# ─────────────────────────────────────────────────────────────────────
# Argument parsing
# ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="prototype",
        description="R129 exhaust synth prototype (Gates 0 & 1).",
    )
    p.add_argument("--sample-rate", type=int, default=SAMPLE_RATE_DEFAULT)
    p.add_argument("--block", type=int, default=BLOCK_DEFAULT)
    sub = p.add_subparsers(dest="cmd", required=True)

    presets = available_presets()

    # preview
    pv = sub.add_parser("preview", help="Gate 0: synthetic-RPM preview")
    pv.add_argument("--preset", choices=presets, default="luxury")
    pv.add_argument("--mode", choices=("hold", "idle", "sweep", "stab"), default="sweep")
    pv.add_argument("--rpm", type=float, default=2000.0, help="hold-mode RPM")
    pv.add_argument("--start", type=float, default=800.0, help="sweep low end RPM")
    pv.add_argument("--end", type=float, default=3000.0, help="sweep high end RPM")
    pv.add_argument("--cycle", type=float, default=8.0,
                    help="sweep/stab cycle period in seconds")
    pv.add_argument("--duration", type=float, default=10.0,
                    help="total playback duration in seconds")
    pv.add_argument("--intensity", type=float, default=0.8)
    pv.add_argument("--out", type=str, help="write rendered audio to this WAV")
    pv.add_argument("--no-play", action="store_true")
    pv.set_defaults(func=cmd_preview)

    # compare
    cmp = sub.add_parser("compare", help="Gate 0: render every preset back-to-back")
    cmp.add_argument("--out-dir", default="renders/compare")
    cmp.add_argument("--seconds-per-preset", type=float, default=10.0)
    cmp.add_argument("--start", type=float, default=800.0)
    cmp.add_argument("--end", type=float, default=3000.0)
    cmp.add_argument("--cycle", type=float, default=8.0)
    cmp.add_argument("--intensity", type=float, default=0.8)
    cmp.add_argument("--no-play", action="store_true")
    cmp.set_defaults(func=cmd_compare)

    # track
    tk = sub.add_parser("track", help="Gate 1: tracker-driven render from a WAV")
    tk.add_argument("--wav", required=True, help="input exhaust WAV")
    tk.add_argument("--preset", choices=presets, default="luxury")
    tk.add_argument("--duration", type=float, default=15.0)
    tk.add_argument("--intensity", type=float, default=0.8)
    tk.add_argument("--synth-out", type=str, help="write synth-only WAV here")
    tk.add_argument("--downmix-out", type=str, help="write mic+synth downmix WAV here")
    tk.add_argument("--side-out", type=str, help="write L=mic R=synth WAV here")
    tk.add_argument("--play", choices=("synth", "downmix", "side"), default="downmix")
    tk.add_argument("--work-sr", type=int, default=48000,
                    help="working sample rate for tracker + synth + output")
    tk.add_argument("--no-play", action="store_true")
    tk.set_defaults(func=cmd_track)

    # make-clip
    mk = sub.add_parser("make-clip", help="Synthesise a fake exhaust WAV for tracker testing")
    mk.add_argument("--out", default="renders/fake_exhaust.wav")
    mk.add_argument("--duration", type=float, default=20.0)
    mk.add_argument("--start", type=float, default=800.0)
    mk.add_argument("--end", type=float, default=3000.0)
    mk.add_argument("--cycle", type=float, default=8.0)
    mk.set_defaults(func=cmd_make_clip)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
