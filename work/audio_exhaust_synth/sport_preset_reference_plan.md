# Sport-preset reference clip — what to source, what to listen for

**Status as of 2026-05-14 (afternoon update — sport preset now tuned):** a
reference clip was sourced and the sport preset has been retuned against it.
The reference is a YouTube clip of an SL500 R129 with MG Motorsport custom
exhaust, captured to `work/exhaust_2026_05_14/ref_mgmotorsport_sl500.wav`.
A second clip (`ref_eisenmann_sl280.wav`) is on disk too but is an SL280
(M104 inline-6, wrong cylinder count and firing-rate geometry) so it is not
used as a primary reference — kept only for cross-checking the broadband
muffler-character envelope. The match achieved against the MG Motorsport
reference at 900 rpm idle (fire = 60 Hz):

| Order / band | M119 sport REF | synth sport |
| :--- | :---: | :---: |
| 1× fire | 0 dB | 0 dB |
| 1.5× fire | −11 dB | −13 dB |
| 2× fire | −10 dB | −9 dB |
| 2.5× fire | −15 dB | −14 dB |
| 3× fire | −10 dB | −25 dB *(structural — synth has no `tonal_o3` term)* |
| 4× fire | −34 dB | −20 dB *(pulse-train residue, mild excess)* |
| 200–400 Hz energy (rel fire band) | −15 dB | −18 dB |
| 400–1 kHz energy | −23 dB | −26 dB |
| 1–4 kHz energy | −24 dB | −30 dB |

The half-integer firing harmonics (1.5×, 2.5×) — which are the **strongest
"non-OEM" tells** of the sport exhaust character — are now within 2 dB of
the reference. They were achieved by adding dedicated `tonal_1p5` and
`tonal_2p5` parallel sine terms in the synth (these are exhaust-resonance-
driven peaks in the real engine, not bank-rate sidebands; no amount of pulse-
train shaping can produce them so a direct tonal injection is the right model).

The 3×/4× imbalance is a structural limitation: the synth currently has
`tonal_fund / tonal_1p5 / tonal_o2 / tonal_2p5 / tonal_o4` but no
`tonal_o3`, and the pulse-train naturally puts more energy into 4× than 3×
for a narrow Hann pulse. Adding `tonal_o3` is a one-line change if it ever
becomes audibly important. For the current listening test it is not.

Original document below preserved (search strategy + tuning-lever map +
PSD targets), now mostly historical but useful when sourcing future
reference clips for other preset variants.

---

Status as of early 2026-05-14: the OEM and Luxury synth presets are quantitatively
tuned against the real M119 idle (m1 UMIK-1 reference). The AMG preset is a
midpoint extrapolation. The Sport preset's target signature — **M119 with X-pipe
and bypassed final silencer** — has no direct reference clip yet. This document
describes (a) what kind of reference we should source, (b) what spectral
characteristics we want to validate against, and (c) what tuning levers in
`v8_synth.py` map to which acoustic features.

## What we want as a reference

A 10-30 second stationary capture of a 5.0 L M119 (M119.960 from the R129
500SL or W124/W126 500E, or M119.970/.974 sport variants from the SL 600 platform
where the displacement is 6.0 L — close enough at idle) with **as little exhaust
muffling as possible after the cats**. Specifically:

| Configuration | Why it's relevant |
| :--- | :--- |
| OEM cats kept (street legal, ~99 % of M119 reference clips will have these) | Cats absorb very high-frequency hash but leave the firing-rate/harmonic signature intact — fine. |
| **X-pipe** between the two banks (replacing the OEM H-pipe / OEM mid-section) | Couples the two banks acoustically, makes the firing rate sound "tighter" / more even. Shifts upper-harmonic balance noticeably. |
| **Bypassed or removed final silencer** ("muffler delete" or "straight pipe out the back") | This is the *raspy* flag. Removes the chamber-resonator absorption of 200–800 Hz energy. The "raspy" character lives in this band. |
| Microphone position outside the car, ~1–3 m from tailpipe, idle (steady RPM ≈ 700) and 2000–2500 rpm hold | Matches our m1/m2 capture geometry — comparable PSDs. |

Configurations to **avoid**:

- Open headers (no cats, no muffler at all): too much high-frequency content,
  doesn't represent any street-driven M119.
- Carbureted / pre-CIS / pre-KE-Jetronic: different fuelling spectrum,
  different combustion characteristic.
- Huge displacement (M275 6.0 V12 etc.): different cylinder count, different
  firing rate harmonic comb.
- Dyno videos with a fan running on the recording: contaminated noise floor.
- Heavily stylised / edited car magazine YouTube clips: compression and
  dynamic-range mangling will skew the PSD analysis.

## What to listen for / measure

Once a candidate clip is captured (extract audio with `yt-dlp` + `ffmpeg`,
trim to a stationary segment), the existing `spectrum_compare.py` tool should
produce a PSD with these expected differences vs the OEM-muffled m1 reference:

| Spectral feature | OEM (m1) measured | Open-pipe target |
| :--- | :---: | :---: |
| Firing fundamental (48 Hz @ idle) | 0 dB | 0 dB (same — fundamental survives muffling) |
| 2× firing (96 Hz @ idle) | −34.6 dB | **−10 to −20 dB** (much stronger — open pipes don't damp the second harmonic) |
| 3× firing (144 Hz) | mostly noise floor | **clearly visible**, around −15 to −25 dB |
| 4×–8× firing (200-400 Hz region) | −45 dB | **−25 to −35 dB** ("raspy" energy lives here) |
| Mid-band 400 Hz – 1 kHz | quieter than firing band | **comparable** to firing band — the raspy-rasp is broadband mid-frequency turbulence |
| Cyl-rate sidebands at fire ± 6 Hz | visible just above floor | similar (cylinder balance unchanged by exhaust mods) |

The single number that captures "rasp" is the **400 Hz – 1 kHz / firing
fundamental** ratio: OEM has it 40+ dB below fundamental, an X-piped/bypassed
M119 will have it within 25 dB of fundamental.

## Search strategy for the reference clip

Concrete candidate searches (in order of preference):

1. **YouTube** searches:
   - `"M119 X-pipe" idle` / `M119.960 straight pipe` / `500SL muffler delete idle`
   - `R129 M119 X-pipe rev` (needs to include some idle, not just a launch)
   - `400E muffler delete M119` / `500E straight pipe`
   - Channels worth checking: SLShop UK, M-B veteran community channels,
     individual M119 enthusiasts on AMG.de or Benzworld threads who post
     short clips.
2. **Forum-hosted clips**: Benzworld `r129/discussions`, MB-W124.de,
   500eboard.com, AMGforum.com — niche but the audio is often unedited.
3. **Cold-start vs warm-idle**: warm idle is easier to compare to m1.
   A cold start has higher RPM (~1100) and a higher fuel-rich pulse
   character; useful but not first-pass.

Once a candidate URL is identified, the workflow is:

```bash
# inside work/audio_exhaust_synth/.venv:
yt-dlp -x --audio-format wav -o reference_sport.%\(ext\)s "<URL>"
# Trim to a 10-30 s stationary idle window (audacity / sox / ffmpeg)
ffmpeg -i reference_sport.wav -ss 00:00:12 -t 20 reference_sport_idle.wav
# Compare:
.venv/bin/python spectrum_compare.py \
    --real reference_sport_idle.wav --rpm 720 \
    --out renders/spectrum_compare_sport_ref.png
```

The PSD print-out from `spectrum_compare.py` is the quantitative target. The
existing sport preset's numbers should then be adjusted to match.

## Tuning levers in `v8_synth.py` for the Sport preset

Mapping each acoustic feature to the parameter that controls it most directly:

| Acoustic feature in the reference | Parameter to adjust |
| :--- | :--- |
| Stronger 2× firing (–10 to –20 dB) | `tonal_o2` ↑, `pulse_gain` ↑, `pulse_width` ↓ (narrower) |
| Stronger 3×/4× firing | narrower `pulse_width` (= broader spectrum), higher `sat_drive` |
| Mid-band rasp 400 Hz – 1 kHz | higher `pulsed_noise`, narrower pipe filter (lower `pipe_q`), higher `sustained_noise`, slight `sat_drive` bump |
| Less acoustic damping above 200 Hz (= "open" character) | `pipe_mix` ↓ (less bandpass smoothing), `pipe_f0_hz` ↑ (less low-pass character) |
| Brighter overall tone but same fundamental level | keep `tonal_fund` ≈ luxury, raise `master` only if reference is louder |

The current sport preset in `v8_synth.py` is a heuristic guess at these
values and is intentionally over-the-top until validated. Expect material
changes once a reference clip lands.

## Open questions to settle with the reference

1. Does X-pipe vs H-pipe change the *deterministic* cylinder-signature
   sideband structure, or only the broadband level? (Probably only the
   broadband level — coupling between banks doesn't change cylinder-to-
   cylinder pressure variation.)
2. How much of the "rasp" survives the in-cabin acoustic transfer function?
   The cabin's own 40-70 Hz resonance amplifies the firing band; the upper
   "rasp" band 400 Hz – 1 kHz is attenuated by cabin acoustics. We may need
   to **deliberately** boost the synth's mid-band content above what an
   outside-the-car reference shows, so the in-cabin result still reads as
   raspy. This is best determined empirically once we have a Pi-driven
   in-car listening test.
3. Should there be intermediate presets between Luxury and Sport?
   ("Sport-light" = OEM resonators removed but cats kept, similar to a
   Borla / Magnaflow muffler change.) Decide after evaluating the gap
   between Luxury and tuned Sport.
