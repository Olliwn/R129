"""
FFT analysis of engine exhaust audio.

Goal: Verify R129 V8 idle (~600 rpm) is clean by looking for the 40 Hz
firing-frequency tone and its harmonics, and checking for any half-order
(20 Hz) content that would indicate a misfire (one cylinder firing weakly
once per revolution => 10 Hz on a per-cyl basis, but the dominant
misfire signature is the 1/2-engine-order at 1*rev = 10 Hz and odd
multiples / sub-harmonics of the firing frequency).

Engine orders for a 4-stroke V8 at idle (600 rpm => 10 rev/s):
    0.5x  =  5 Hz   (per-cylinder rate)
    1.0x  = 10 Hz   (crank rev / "half engine order")
    2.0x  = 20 Hz   (1/2 firing order; classic single-cyl misfire signature)
    4.0x  = 40 Hz   (firing frequency, V8)
    8.0x  = 80 Hz   (2nd harmonic of firing)
   12.0x  =120 Hz   (3rd harmonic)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import get_window, welch, spectrogram
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "pics" / "exhaust.m4a"
WAV = HERE / "exhaust.wav"
OUT_SPECTRUM = HERE / "exhaust_spectrum.png"
OUT_SPECTROGRAM = HERE / "exhaust_spectrogram.png"


def extract_wav(src: Path, dst: Path, target_sr: int = 8000) -> None:
    """Decode m4a -> mono PCM WAV via ffmpeg.

    8 kHz is plenty: we care about <500 Hz where engine orders live, and a
    lower sample rate gives us better FFT bin spacing for the same window
    size.
    """
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-ac", "1",
        "-ar", str(target_sr),
        "-sample_fmt", "s16",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def load_mono(path: Path) -> tuple[int, np.ndarray]:
    sr, x = wavfile.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x.astype(np.float64)
    x /= max(abs(x.max()), abs(x.min()), 1.0)
    return sr, x


def trim_steady(x: np.ndarray, sr: int, head: float = 0.5, tail: float = 0.5) -> np.ndarray:
    """Drop a bit from each end (handle clicks / phone-handling noise)."""
    n0 = int(head * sr)
    n1 = len(x) - int(tail * sr)
    return x[n0:n1] if n1 > n0 + sr else x


def welch_spectrum(x: np.ndarray, sr: int, fmax: float = 500.0):
    """Welch PSD with a Hann window. Window length set to give sub-Hz bins."""
    nperseg = 1 << int(np.log2(sr * 4))   # ~4 s window -> ~0.25 Hz bins @ 8 kHz
    nperseg = min(nperseg, len(x))
    noverlap = nperseg // 2
    f, pxx = welch(
        x, fs=sr,
        window=get_window("hann", nperseg),
        nperseg=nperseg, noverlap=noverlap,
        detrend="constant", scaling="density", average="median",
    )
    mask = f <= fmax
    return f[mask], pxx[mask]


def db(p: np.ndarray) -> np.ndarray:
    return 10.0 * np.log10(np.maximum(p, 1e-20))


def find_local_peaks(f: np.ndarray, p_db: np.ndarray, min_prominence_db: float = 6.0):
    peaks = []
    for i in range(2, len(p_db) - 2):
        if p_db[i] > p_db[i - 1] and p_db[i] > p_db[i + 1]:
            window = p_db[max(0, i - 40):i + 41]
            if p_db[i] - np.median(window) >= min_prominence_db:
                peaks.append((f[i], p_db[i]))
    return peaks


def estimate_idle_rpm(f: np.ndarray, pxx: np.ndarray, cylinders: int = 8,
                       search=(25.0, 60.0)):
    """Find the dominant peak in the firing-frequency search band, return rpm."""
    band = (f >= search[0]) & (f <= search[1])
    if not band.any():
        return None, None
    fb, pb = f[band], pxx[band]
    i = int(np.argmax(pb))
    f_fire = float(fb[i])
    rpm = f_fire * 60.0 * 2.0 / cylinders   # firing freq -> rpm for 4-stroke
    return f_fire, rpm


def main() -> int:
    if not SRC.exists():
        print(f"missing source audio: {SRC}", file=sys.stderr)
        return 1
    print(f"[1/4] extracting wav from {SRC.name}")
    extract_wav(SRC, WAV)

    print(f"[2/4] loading {WAV.name}")
    sr, x = load_mono(WAV)
    print(f"      sample rate: {sr} Hz, length: {len(x)/sr:.2f} s")
    x = trim_steady(x, sr)

    print("[3/4] computing Welch PSD")
    f, pxx = welch_spectrum(x, sr, fmax=500.0)
    p_db = db(pxx)

    f_fire, rpm = estimate_idle_rpm(f, pxx, cylinders=8, search=(30.0, 55.0))
    print(f"      dominant firing peak: {f_fire:.2f} Hz  ->  {rpm:.0f} rpm (V8 4-stroke)")

    # Order multiples of the detected firing frequency.
    orders = {
        "0.5x rev (1/8 firing) — per-cyl": f_fire / 8.0,
        "1.0x rev (1/4 firing) — crank":   f_fire / 4.0,
        "2.0x rev (1/2 firing) — MISFIRE": f_fire / 2.0,
        "4.0x rev (1x firing)":            f_fire,
        "8.0x rev (2x firing)":            2 * f_fire,
       "12.0x rev (3x firing)":            3 * f_fire,
       "16.0x rev (4x firing)":            4 * f_fire,
    }

    print("\n[4/4] level at engine-order frequencies (dB re full-scale^2/Hz):")
    print(f"  {'order':<38s}{'f [Hz]':>10s}{'level [dB]':>14s}")
    ref = None
    for name, ff in orders.items():
        i = int(np.argmin(abs(f - ff)))
        lvl = p_db[i]
        if ref is None:
            ref = lvl  # use first (per-cyl rate) as anchor
        print(f"  {name:<38s}{ff:>10.2f}{lvl:>14.1f}")

    # Misfire heuristic: half-firing-order vs firing-order.
    i_fire = int(np.argmin(abs(f - f_fire)))
    i_half = int(np.argmin(abs(f - f_fire / 2.0)))
    delta_db = p_db[i_half] - p_db[i_fire]
    print(f"\n  half-firing/firing ratio: {delta_db:+.1f} dB")
    if delta_db > -10.0:
        print("  WARNING: half-firing order is within 10 dB of firing — "
              "possible misfire / uneven combustion.")
    else:
        print("  half-firing order is well below firing order — no misfire signature.")

    peaks = find_local_peaks(f, p_db, min_prominence_db=6.0)
    print(f"\n  prominent peaks (>=6 dB above local median):")
    for pf, pl in peaks[:25]:
        print(f"    {pf:7.2f} Hz   {pl:6.1f} dB")

    # ---- spectrum plot ----
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.semilogy(f, pxx, lw=1.0)
    ax.set_xlim(0, 300)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("PSD [arb²/Hz]")
    ax.set_title(f"R129 exhaust — Welch PSD (Hann, ~0.25 Hz bins)\n"
                  f"firing peak {f_fire:.1f} Hz  ≈  {rpm:.0f} rpm  (V8, 4-stroke)")
    ax.grid(True, which="both", alpha=0.3)
    for name, ff in orders.items():
        if ff > 300:
            continue
        ax.axvline(ff, color="C3" if "MISFIRE" in name else "C2",
                   ls=":" if "MISFIRE" in name else "--",
                   alpha=0.6, lw=1)
        ax.text(ff, ax.get_ylim()[1] * 0.6, f"{ff:.1f}",
                rotation=90, va="top", ha="right", fontsize=7,
                color="C3" if "MISFIRE" in name else "C2")
    fig.tight_layout()
    fig.savefig(OUT_SPECTRUM, dpi=140)
    print(f"\n  wrote {OUT_SPECTRUM.relative_to(HERE.parent)}")

    # ---- spectrogram (verify steadiness over time) ----
    nperseg = 1 << int(np.log2(sr * 1))    # ~1 s
    f_s, t_s, Sxx = spectrogram(
        x, fs=sr, window=get_window("hann", nperseg),
        nperseg=nperseg, noverlap=nperseg // 2, scaling="density",
    )
    band = f_s <= 300
    Sdb = db(Sxx[band, :])
    vmax = float(np.percentile(Sdb, 99.5))
    vmin = vmax - 60.0
    fig, ax = plt.subplots(figsize=(11, 4.5))
    im = ax.pcolormesh(t_s, f_s[band], Sdb,
                       shading="auto", cmap="magma", vmin=vmin, vmax=vmax)
    ax.set_xlabel("time [s]")
    ax.set_ylabel("frequency [Hz]")
    ax.set_title("exhaust spectrogram (Hann, 1 s window)")
    for ff, name in [(f_fire / 2, "1/2 firing"), (f_fire, "firing"),
                     (2 * f_fire, "2x firing"), (3 * f_fire, "3x firing")]:
        ax.axhline(ff, color="cyan", ls="--", alpha=0.5, lw=0.7)
        ax.text(t_s[-1] * 1.005, ff, name, color="cyan", fontsize=7, va="center")
    fig.colorbar(im, ax=ax, label="PSD [dB]")
    fig.tight_layout()
    fig.savefig(OUT_SPECTROGRAM, dpi=140)
    print(f"  wrote {OUT_SPECTROGRAM.relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
