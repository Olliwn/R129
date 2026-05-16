"""
Spectrum A/B — real M119 recording vs procedural synth.

Produces a single PNG with the Welch PSD of the real exhaust clip and
of each synth preset rendered at the same nominal RPM, overlaid on the
same axes so it is easy to read off:

  • Where the synth puts energy that the real engine does NOT
  • Where the real engine has energy the synth lacks
  • The cylinder-event sideband structure around the firing fundamental
    (real V8 spectra are not a clean line + harmonics — cylinder-to-
    cylinder pressure variation modulates the firing line at the
    cylinder-rate ≈ rpm / 60 / 2 in V8 4-stroke, producing dense
    sidebands ±cyl-rate around the fundamental.)

Usage
-----
  python3 spectrum_compare.py \\
      --real ../exhaust.wav \\
      --rpm 720 \\
      --out renders/spectrum_compare_720rpm.png

Set ``--rpm`` to the steady-state RPM in the reference clip — for the
current `work/exhaust.wav`, the tracker locks at ≈ 720 rpm so 720 is
the right choice.

The script also prints summary band energies for quick eyeballing.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import welch

from rpm_source import SyntheticSource
from v8_synth import V8Synth, available_presets


# ─────────────────────────────────────────────────────────────────────
# Rendering helpers
# ─────────────────────────────────────────────────────────────────────

def render_synth_hold(preset: str, rpm: float, dur_sec: float, sr: int) -> np.ndarray:
    """Render a constant-RPM synth signal. Returns mono float32."""
    src = SyntheticSource(mode="hold", rpm=float(rpm))
    synth = V8Synth(sample_rate=sr, preset=preset, seed=11)
    synth.set_engaged(True)
    synth.set_intensity(0.9)
    n_total = int(dur_sec * sr)
    out = np.zeros(n_total, dtype=np.float32)
    cur = 0
    while cur < n_total:
        n = min(512, n_total - cur)
        block = src.render(n, sr)
        rendered = synth.render(block.rpm, block.crank_phase, block.confidence)
        out[cur : cur + n] = rendered[:, 0]
        cur += n
    return out


def load_mono(path: str) -> tuple[np.ndarray, int]:
    a, sr = sf.read(path, dtype="float32", always_2d=True)
    return a.mean(axis=1).astype(np.float32), int(sr)


# ─────────────────────────────────────────────────────────────────────
# Spectrum + summary
# ─────────────────────────────────────────────────────────────────────

def welch_psd(sig: np.ndarray, sr: int, n_per_seg: int) -> tuple[np.ndarray, np.ndarray]:
    """RMS-normalised Welch PSD. RMS-normalisation lets us compare a
    real signal (whose absolute level is arbitrary) against the synth's
    fixed-ceiling output without being misled by gain."""
    rms = float(np.sqrt(np.mean(sig.astype(np.float64) ** 2)) + 1e-12)
    f, p = welch(
        sig.astype(np.float64) / rms,
        fs=sr,
        window="hann",
        nperseg=n_per_seg,
        noverlap=n_per_seg // 2,
        detrend=False,
        scaling="density",
    )
    return f, p


def summarise(name: str, freqs: np.ndarray, psd: np.ndarray, firing_hz: float) -> None:
    cyl = firing_hz / 8.0       # cylinder-event rate
    bands = [
        ("0.5×fire (eng cycle)", 0.7 * firing_hz / 2, 1.3 * firing_hz / 2),
        ("fire fundamental",     0.9 * firing_hz,     1.1 * firing_hz),
        ("fire ±cyl-rate band",  firing_hz - 1.5 * cyl, firing_hz + 1.5 * cyl),
        ("2× fire",              1.8 * firing_hz,     2.2 * firing_hz),
        ("4× fire",              3.8 * firing_hz,     4.2 * firing_hz),
        ("noise floor 200-400 Hz", 200.0, 400.0),
        ("upper band 400-1k Hz",   400.0, 1000.0),
        ("upper band 1-4 kHz",     1000.0, 4000.0),
    ]
    print(f"\n  {name}")
    for label, f1, f2 in bands:
        sel = (freqs >= f1) & (freqs < f2)
        if not sel.any():
            continue
        e = 10.0 * np.log10(np.sum(psd[sel] * (freqs[1] - freqs[0])) + 1e-15)
        print(f"    {label:28s}  {e:+6.1f} dB (rms-normalised)")


# ─────────────────────────────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────────────────────────────

def plot_overlay(
    real_path: str,
    real_psd: tuple[np.ndarray, np.ndarray],
    synth_psds: dict[str, tuple[np.ndarray, np.ndarray]],
    rpm: float,
    out_png: str,
    f_lo: float = 5.0,
    f_hi: float = 1500.0,
) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fire = rpm * 4.0 / 60.0
    cyl = rpm / 60.0 / 2.0   # cylinder-event rate (V8 4-stroke)

    fig, ax = plt.subplots(figsize=(12, 7))
    # Real
    f, p = real_psd
    ax.semilogy(f, p, color="black", lw=1.6, label=f"real M119 — {Path(real_path).name}")
    # Synth presets
    colours = {"oem": "#1f77b4", "luxury": "#2ca02c",
               "amg":  "#ff7f0e", "sport":  "#d62728"}
    for preset, (fs, ps) in synth_psds.items():
        ax.semilogy(fs, ps, color=colours.get(preset, "#888"), lw=1.1,
                    alpha=0.85, label=f"synth {preset}")

    # Reference vertical lines
    for k, lbl in [(0.5, "½×fire"), (1.0, "1×fire"), (2.0, "2×"),
                   (3.0, "3×"), (4.0, "4×"), (8.0, "8×")]:
        x = fire * k
        if f_lo <= x <= f_hi:
            ax.axvline(x, color="#888", lw=0.5, ls="--", alpha=0.6)
            ax.text(x, ax.get_ylim()[1] * 0.5, lbl, color="#666",
                    fontsize=8, rotation=90, va="top", ha="right")
    # Cylinder-event sideband markers
    for n in range(-3, 4):
        if n == 0:
            continue
        x = fire + n * cyl
        if f_lo <= x <= f_hi:
            ax.axvline(x, color="#c44", lw=0.4, ls=":", alpha=0.5)

    ax.set_xlim(f_lo, f_hi)
    ax.set_xscale("log")
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("PSD (rms-normalised, log)")
    ax.set_title(
        f"R129 exhaust — real vs synth, hold @ {rpm:.0f} rpm "
        f"(fire = {fire:.1f} Hz, cyl-rate = {cyl:.2f} Hz)\n"
        f"red dotted lines = firing ± k·cyl-rate sidebands"
    )
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="upper right")
    fig.tight_layout()
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=110)
    plt.close(fig)
    print(f"\n  wrote {out_png}")


# ─────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--real", required=True, help="reference exhaust WAV/m4a (resampled if needed)")
    p.add_argument("--rpm", type=float, default=720.0,
                   help="nominal RPM for the synth holds")
    p.add_argument("--sr", type=int, default=48000)
    p.add_argument("--dur", type=float, default=6.0,
                   help="synth render duration (seconds)")
    p.add_argument("--nperseg", type=int, default=8192,
                   help="Welch segment size in samples (8192 @ 48 kHz → 5.9 Hz bins)")
    p.add_argument("--out", default="renders/spectrum_compare.png")
    p.add_argument("--presets", nargs="+", default=available_presets(),
                   help="which presets to overlay")
    args = p.parse_args()

    # Real clip
    real, real_sr = load_mono(args.real)
    print(f"loaded real clip: {len(real)/real_sr:.2f}s @ {real_sr} Hz")
    # Welch on real at its native rate for best bin spacing in the
    # important low-frequency band. If file_sr < args.sr, the upper
    # synth bands won't have a corresponding real-clip line — that's
    # what motivates capturing a wider-bandwidth M119 reference next.
    nperseg_real = min(args.nperseg, len(real))
    real_psd = welch_psd(real, real_sr, nperseg_real)

    # Synth presets
    synth_psds = {}
    for preset in args.presets:
        if preset == "off":
            continue
        sig = render_synth_hold(preset, args.rpm, args.dur, args.sr)
        synth_psds[preset] = welch_psd(sig, args.sr, args.nperseg)
        print(f"  rendered synth {preset!r} at {args.rpm:.0f} rpm "
              f"({args.dur:.1f}s, sr={args.sr})")

    firing_hz = args.rpm * 4.0 / 60.0
    summarise("real M119", *real_psd, firing_hz=firing_hz)
    for preset, psd in synth_psds.items():
        summarise(f"synth {preset}", *psd, firing_hz=firing_hz)

    plot_overlay(args.real, real_psd, synth_psds, args.rpm, args.out,
                 f_hi=min(real_sr * 0.5, 4000.0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
