# Listening Guide — Gate 0 + Gate 1 Renders (synth v3)

All files live in [`renders/`](renders/). The folder is gitignored so
re-running the prototype is non-destructive to history. Play these
through the living-room Genelec G3 + SVS sub.

All output is 48 kHz / stereo / float-32 inside a 24-bit PCM WAV.
Internal soft-limiter ceiling is ≈ −3 dBFS (`SAFETY_PEAK = 0.7`) so
nothing here will overshoot, but treat `sport` clips as the loudest in
the set when you set system volume.

## What changed in v3 (spectrum-matched)

After Gate 0/1 v2 you flagged two problems that survived the Hann
rewrite:

1. **Clicks in Gate 1 only** — the synth itself was clean (Gate 0
   measured 6× lower 2nd-derivative spikes), but Gate 1 still had
   clicks at multiples of the clip length. Localisation showed steps
   at t=9.09 s and t=18.17 s in the *downmix* (i.e. the mic side).
   Root cause: `WavFileSource` was looping by raw concatenation of
   tail → head with a single-sample step at each wrap.
   **Fix in `rpm_source.py`:** a 30 ms equal-power crossfade baked
   into the audio at load time. Measured d² peak on the new downmix
   dropped from 0.18 → 0.005 (36× lower), zero step-events anywhere
   across the 20-second loop.

2. **Tone still too synthetic.** Approached this as a spectrum-A/B
   exercise — see `spectrum_compare.py` and
   `renders/spectrum_compare_720rpm.png`. The Welch PSD overlay of
   real M119 idle vs the v2 synth presets at 720 rpm revealed three
   structural mismatches that the v3 synth now corrects:

   | Band | Real | v2 luxury | v3 luxury |
   | --- | --- | --- | --- |
   | fire fundamental | −1.0 | −8.0 | **−0.8** |
   | fire ± cyl-rate sidebands | −0.5 | −7.6 | **−0.4** |
   | 0.5× fire (engine cycle) | −24.2 | −12.7 | **−21.7** |
   | 4× fire | −35.4 | −21.1 | **−33.3** |

   The fundamental and (crucially) the *discrete cylinder-rate
   sidebands* — fire ± k·cyl_rate (= 6.1 Hz at idle) — now match the
   real engine. These sidebands are the spectral signature of the
   8-cylinder pressure-difference pattern repeating once per engine
   cycle, which v2's random per-pulse jitter could not produce
   (random jitter creates broadband floor, not discrete sidebands).

## v3 architecture in one diagram

```
crank_phase ──▶ unwrap & bridge ──▶ continuous phase θ(t)
                                         │
                          ┌──────────────┼────────────────┐
                          ▼              ▼                ▼
                  sin(θ_fire)     Hann pulse train     crank-rate
                  + sin(2θ_fire)  at firing rate       sub pulse → LP
                  + sin(4θ_fire)  (width = preset)         │
                          │              │                 │
                  × cyl-signature       × cyl-signature    │
                  (amp @ 1×, ph @ 1×)   (amp + jitter)    │
                          │              │                 │
                          └──────┬───────┴────┬────────────┘
                                 ▼            ▼
                          tonal core    pulse + sub-pulse
                                 │            │
                                 └──── + ─────┘
                                       │
                                  + sustained_noise (state-preserved LP)
                                  + pulsed_noise (× pulse env)
                                       │
                                 [pipe bandpass biquad, wet/dry]
                                       │
                                  tanh saturator (low drive)
                                       │
                              engaged-fade envelope
                                       │
                               ±SAFETY_PEAK clip
```

The "cyl-signature" tables are 8 deterministic numbers (one per
cylinder) that repeat each engine cycle. Slow per-cylinder drift
(10-second time constant) prevents the sidebands from sounding
mechanically locked.

## Gate 0 — procedural V8 driven by synthetic RPM

Pure synth. No M119 in these renders. This is the answer to "is the
roar worth pursuing on its own?"

Listen in this order:

| # | File | What it is | What to listen for |
| :-: | :--- | :--- | :--- |
| 1 | `gate0_luxury_idle.wav` | 6 s ~800 rpm idle with ±30 rpm wobble | Lopey idle character. No clicks. Slight cross-plane "ba-da-bum" should be audible. |
| 2 | `gate0_luxury_sweep.wav` | 12 s, 800↔3500 rpm triangle sweep | Timbre coherence across firing rates. No zipper / aliasing. |
| 3 | `gate0_luxury_stab.wav` | 12 s of throttle-stab cycles 900↔4500 rpm | Transient response on fast RPM swings. |
| 4 | `gate0_oem_*.wav` | OEM+ preset — muffled refinement | "Miss it when off" tier. Quiet but present. |
| 5 | `gate0_amg_*.wav` | More upper-mid bark, less pipe smoothing | "Noticeable character" tier. |
| 6 | `gate0_sport_*.wav` | Open-exhaust reference (x-pipe, no final silencer) | Sharp narrow pulses, broadband roar, heavy saturation. |

### Gate 0 pass criterion

> The `luxury` sweep should sound plausibly like a refined V8 —
> engaging, not cartoonish, not obviously a sawtooth.
> The `sport` sweep should sound aggressively like a deleted exhaust:
> sharp blat per firing, rich high-frequency content, audible burble.

If only `oem` is bearable and everything above sounds fake, the synth
needs more iteration (extend the harmonic spectrum, add a second
formant, or move to a hybrid sample / granular model). If `luxury`
and `amg` both feel musical, you're past Gate 0.

## Gate 1 — synth phase-locked to the real M119 recording

These renders run the engine tracker against `work/exhaust.wav` (the
9 s clip extracted from `pics/exhaust.m4a`). Tracker locks at
**~720 rpm / 48 Hz firing rate**, 100 % confidence throughout. Renders
loop the clip ~2× to cover 20 s of playback.

Listen in this order:

| # | File | What it is | What to listen for |
| :-: | :--- | :--- | :--- |
| 1 | `gate1_oem_downmix.wav` | M119 idle + oem synth | Does the synth blend with the recording, or sit on top? |
| 2 | `gate1_luxury_downmix.wav` | M119 idle + luxury synth | The "what would the cabin sound like" target. |
| 3 | `gate1_amg_downmix.wav` | M119 idle + amg synth | More obvious augmentation. |
| 4 | `gate1_sport_downmix.wav` | M119 idle + sport synth | Over-the-top end. |
| 5 | `gate1_luxury_synth.wav` | Synth alone, phase-locked to mic | Compare against `gate0_luxury_idle.wav` to confirm tracker-driven phase doesn't introduce warble. |
| 6 | `gate1_luxury_side.wav` | L = mic only, R = synth only | Pan-balance check. Solo each channel — both should pulse together. |

### Gate 1 pass criterion

> The `luxury` downmix should sound like *one coherent exhaust*, not
> two stacked signals.

The source is an 8 kHz phone recording — the mic content is lo-fi
(silence above 4 kHz), the synth is full bandwidth at 48 kHz. So you
should hear:

- The familiar M119 idle burble (mic side, low and rough)
- A coherent harmonic fill *at the same phase / pitch* (synth side)

If the synth drifts against the mic, that's a tracker phase issue —
re-run with longer `--duration` or open the side WAV in Audacity to
inspect.

If the synth is at a different pitch (e.g. an octave off), the tracker
locked onto a harmonic rather than the firing rate. Known risk on idle
recordings with strong 2nd-order content — next iteration would add
Goertzel-bank harmonic verification.

## Spectral analysis tool

The synth is now backed by a measurement tool — run it any time you
want to A/B against the reference clip after a tuning pass:

```bash
python3 spectrum_compare.py --real ../exhaust.wav --rpm 720 \
    --out renders/spectrum_compare_720rpm.png
```

It produces:

- A log-log PSD plot of real vs each preset, with reference vertical
  lines at ½×, 1×, 2×, 3×, 4×, 8× firing and at the cylinder-rate
  sideband positions.
- A per-band energy summary (rms-normalised dB) for fundamental,
  sidebands, ½× fire, 2× fire, 4× fire, and three noise-floor bands.

When you get a real M119 *with sports exhaust* reference clip — your
suggested next data — re-run with `--real path/to/that_clip.wav` and
update preset tuning to chase the new target. The `sport` preset
parameters in `v8_synth.py` are the obvious starting point; the most
impactful knobs are `pulse_width`, `pulse_gain`, `pipe_q`, `pipe_mix`,
`sustained_noise`.

## What's still missing from Gate 1

The current `exhaust.wav` is a steady idle. To answer "does this add
value while *driving*", capture a second clip:

```bash
# In the car, parked, engine running. Place phone or UMIK-1 near the
# tailpipe or on the rear bumper, ~30 cm away, wind-shielded.
# Record 30 seconds of:
#   - 10 s idle
#   - 10 s slow rev from idle to 2500 rpm and back
#   - 10 s of two-three throttle stabs
# Save as work/exhaust_rev.m4a (or .wav)
```

Then convert (if needed) and run:

```bash
ffmpeg -i ../exhaust_rev.m4a -ac 1 -ar 8000 ../exhaust_rev.wav
python3 prototype.py track --wav ../exhaust_rev.wav --preset luxury \
    --duration 30 --downmix-out renders/gate1_rev_luxury_downmix.wav --no-play
```

That second recording lets us audition the synth across a range of
firing rates rather than only at idle, and is what actually answers
the "does this add value at speed?" question.

## Regenerating the pack

```bash
# Gate 0 only
for p in oem luxury amg sport; do
  python3 prototype.py preview --preset $p --mode sweep \
    --start 800 --end 3500 --cycle 8 --duration 12 \
    --out renders/gate0_${p}_sweep.wav --no-play
  python3 prototype.py preview --preset $p --mode idle \
    --duration 6 --out renders/gate0_${p}_idle.wav --no-play
  python3 prototype.py preview --preset $p --mode stab \
    --duration 12 --out renders/gate0_${p}_stab.wav --no-play
done

# Gate 1 only (real M119 recording)
for p in oem luxury amg sport; do
  python3 prototype.py track --wav ../exhaust.wav --preset $p --duration 20 \
    --synth-out renders/gate1_${p}_synth.wav \
    --downmix-out renders/gate1_${p}_downmix.wav \
    --side-out renders/gate1_${p}_side.wav --no-play
done
```
