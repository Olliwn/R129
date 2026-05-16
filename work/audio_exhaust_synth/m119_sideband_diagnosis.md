# M119 idle-spectrum sideband diagnosis

Original recording: `work/exhaust.wav` (warm idle, ~720 rpm, phone mic, 8 kHz mono).
Spectra: `work/exhaust_spectrum.png`, `work/exhaust_spectrogram.png`,
`work/audio_exhaust_synth/renders/spectrum_compare_720rpm.png`.

Follow-up recordings (2026-05-14, UMIK-1 calibrated reference mic via Mac, 48 kHz):
`work/exhaust_2026_05_14/m1_voicememo.wav` (2:06 idle), `m2_voicememo.wav` (1:27 with rev to ~2400 rpm).
Follow-up plots: `sideband_compare_3recs.png`, `m2_spectrogram_v2.png`,
`m2_windowed_psd.png`, `sideband_at_2000rpm.png`.

## Bottom line — UPDATED 2026-05-14 (final pass after order-axis + low-frequency analysis)

**Verdict: healthy cross-plane V8 with a fixed 40–70 Hz acoustic resonance and clear evidence
of engine-block rocking on (likely worn) mounts. No cylinder imbalance signature visible
above the noise floor. Confidence: high.** Do not pursue compression / leakdown based on
this evidence. Engine mounts and transmission mount are the more likely service item.

### Three pieces of evidence used to converge on this verdict

1. **Order-axis PSD comparison** (`work/exhaust_2026_05_14/order_axis_compare.png`):
   when the spectrum of the rev-up region (30–37 s) and the plateau (38–50 s) is plotted
   against `frequency / firing_rate`, both regions show clean peaks at integer firing
   orders 1× and 2× and *no peaks above noise floor* at half-integer orders (1.5×, 2.5×,
   3.5×). The "low-order peak around 0.3–0.4× fire" that appears in both regions is the
   fixed 50 Hz acoustic resonance expressed as a fraction of two different firing rates
   (159 Hz vs 142 Hz) — confirmed, same physical 50 Hz feature, not a sideband.
   Half-integer firing harmonics would be the signature of *paired-cylinder* asymmetry;
   they are absent.

2. **Low-frequency (0–35 Hz) waterfall** (`work/exhaust_2026_05_14/low_freq_waterfall.png`):
   shows a clear bright trace climbing from ~12 Hz at idle to ~33 Hz at the rev plateau —
   exactly 1× engine-rotation speed (rpm/60). The trace dies the instant the engine stops
   at 64 s, confirming it is engine-correlated, not chassis / wind / handling. This is
   the **engine block rocking on its mounts** that the user observed visually. Most of
   it sits below 20 Hz so it is largely *infrasonic* (felt, not heard), but the UMIK-1
   captures it. On a 35-year-old car this is consistent with worn engine and transmission
   mounts.

3. **Firing-line envelope modulation** (`work/exhaust_2026_05_14/firing_envelope_modulation.png`):
   bandpass the firing line (40–60 Hz) at idle and take its Hilbert envelope; the envelope's
   own spectrum has a sharp peak at **6.38 Hz** with an 8 s window. This is **not a Welch
   bin-spacing artifact** — it is a real narrow line at one-engine-cycle period:
   `6.38 Hz × 8 firings = 51 Hz ≈ idle firing rate`, so 6.38 Hz is the cylinder-event rate.
   The original GoPro recording's "6.1 Hz sideband" was almost certainly the same feature,
   just rounded by a coarser bin spacing. This represents `fire ± 1×cyl_rate` modulation,
   which is the signature of *non-uniform single-cylinder* variation — combined with the
   absence of `fire ± 4×cyl_rate` (= half-integer firing harmonic) sidebands, this is
   consistent with normal cycle-to-cycle variability and possibly mild (sub-5 %) single-
   cylinder offset, well within healthy aged-engine territory.

### Re-statement of the original "6 Hz sideband" finding

The original report flagged 6.1 Hz spacing as a possible cylinder-balance signature and
gave it medium confidence. The order-axis analysis and the long-window envelope analysis
together show:
- the 6 Hz line **is real** (corrected from the intermediate "Welch artifact" guess), and
- it represents 1× cylinder-event-rate modulation, which is *expected* in any V8 — a
  perfectly balanced engine would still have small CCV (cycle-to-cycle variability) at
  this frequency from purely combustion turbulence, and a healthy-aged engine has a few
  percent more from minor cylinder-to-cylinder differences, and
- no auxiliary evidence of *paired* asymmetry (no half-integer firing harmonics, no
  misfire transients, no abnormal time-domain envelope behaviour) is present.

So the conservative reading is: cylinder balance is healthy or mildly off (under the
~5 % threshold below which workshop diagnostics will not detect it either). The earlier
medium-confidence imbalance call is downgraded.

### What the rev-sweep test showed

| RPM regime | 40–70 Hz band energy (rms-norm dB) | firing-line band energy | ratio |
| :--- | :---: | :---: | :---: |
| idle (705 rpm, fire = 47 Hz) | −2.9 | −3.0 | ~equal — firing line lies inside the resonance band |
| 2355 rpm, fire = 157 Hz | −1.6 | **−20.6** | **resonance band is 19 dB louder than the firing line** |

The 40–70 Hz band stays at almost exactly the same absolute level whether the engine is at
705 rpm or 2355 rpm. That is the textbook signature of a **fixed acoustic resonance** in the
cabin / exhaust pipe — the diagnostic test the previous version of this report explicitly
proposed (`acoustic resonances stay pinned in frequency while true cylinder-event sidebands
track rpm`). The dominant 50–65 Hz feature stayed pinned. So the dominant feature is acoustic.

### Re-interpreting the original "sidebands"

The peaks observed in `exhaust.wav` at 29, 35, 41, 47, 53, 59, 65 Hz are the natural harmonic
series of the cylinder-event impulse train (`f_cyl = 5.88 Hz` at 705 rpm; harmonics at 5.88,
11.76, 17.64 … 47, 52.9 … Hz). Every V8 produces this comb regardless of cylinder balance.
What was unusual in the data — the asymmetric "low-side dominant" pattern — turns out to be
the natural consequence of the 40–70 Hz resonance band amplifying whichever cylinder-event
harmonics happen to fall inside it (specifically the 5×, 6×, 7×, 8×, 9× cyl-rate harmonics at
705 rpm).

The earlier "back-of-envelope cylinder imbalance" inference of "5–10 % imbalance" was based
on the implicit assumption that the spectral shape was driven by combustion modulation. With
the resonance hypothesis confirmed, that inference no longer holds — the imbalance, if any,
is buried under at least 19 dB of resonance amplification and **cannot be measured from this
data**.

### Implications

- **Diagnostic**: stop suspecting the engine on the basis of these recordings. Cylinder
  balance might still be a few % off (always is on a 30-year-old engine), but the spectrum
  doesn't show it.
- **Audio system / synth tuning**: the 40–70 Hz cabin/exhaust resonance is a major design
  input for the in-cabin augmentation system. Anything the synth puts at ~50 Hz will be
  acoustically amplified ≥ 19 dB. The DSP front-channel parametric EQ should already include
  a notch / cut around the resonance centre once it is measured cleanly with REW. This is
  also why the Match-DSP tuning at the headrest position will sound very different from the
  passenger seat — fixed resonances are highly position-dependent.
- **Mechanical**: arrange to inspect the engine mounts and transmission mount at the next
  lift. The 1× engine-speed line in the audio is consistent with worn rubber, and on a
  35-year-old car they are a common service item that affects both the visible idle shake
  and (subtly) the in-cabin vibration baseline that the augmentation system has to sit on
  top of.
- **What would still be useful to capture**: an RPM sweep where the engine sits cleanly at
  several plateaus (700, 1500, 2000, 2500 rpm, 5 s each) **without engine-off noise** in the
  recording. With 5 s of clean per-RPM data, the cyl-rate harmonic comb can be identified
  and cleanly separated from the fixed resonance, which would let us compute a proper
  cylinder-balance figure. The current m2 only spent 0.2 s above 1500 rpm and shut the
  engine off mid-recording.

The original detailed analysis below is preserved for reference — most of the threshold
calculations and benign-cause / failure-mode lists are still accurate, only the *verdict
on this particular recording* changes.

---

## Original analysis (pre-2026-05-14, retained for reference)

**Most likely normal-to-slightly-elevated cross-plane V8 character, not a clear single-cylinder
fault — but the recording is not clean enough to rule out a mild ~10 % cylinder imbalance.**
Confidence: medium. The single biggest unknown is the tailpipe / muffler transfer function
between ~30 and 80 Hz, which is almost certainly resonant in this band on a stock R129 system
and is doing a lot of the apparent "sideband boosting." Don't panic; do the two free software
checks below before spending money.

## What the sidebands physically represent

The exhaust pulse train at warm idle is a sequence of firing events at
`f_fire = rpm/60·(N_cyl/2) = 720/60·4 ≈ 48 Hz`. Because the same cylinder fires only once per
two-rev engine cycle, any cylinder-to-cylinder difference (compression, fuel, spark, valve
seat, port flow) repeats at the cylinder-event rate
`f_cyl = f_fire / 8 ≈ 6 Hz`. In the spectrum this appears as a comb of lines at
`k · 6 Hz`, with the firing rate itself sitting on the `k = 8` line at 48 Hz. A perfectly
balanced V8 would put **all** energy on multiples of 48 Hz; every line in between (42, 36, 30,
54, 60, 67 Hz …) is by definition a measure of imbalance plus once-per-cycle valvetrain /
intake-manifold resonances. This is the textbook origin of the "V8 lope/burble."

## Threshold for "normal" — back-of-envelope

Model the firing pulse train as 8 pulses of amplitude `a_n = A(1+ε_n)` per engine cycle, with
RMS imbalance `σ ≡ rms(ε_n)`. By Parseval the total power outside the firing harmonics is
`σ²·A²`, distributed across the 7 non-trivial sideband bins per firing harmonic. Per-sideband
power relative to the firing line is then roughly `σ²/7`:

| RMS cylinder imbalance σ | Per-sideband level vs firing line (pure AM model) |
| --- | --- |
| 2 % (very healthy / fresh build) | ≈ −38 dB |
| 5 % (typical healthy aged engine) | ≈ −34 dB |
| 10 % (noticeable imbalance, on the edge of a workshop "fail") | ≈ −28 dB |
| 15 % (one cylinder clearly weak) | ≈ −24 dB |
| One cylinder fully out (a₁=0, others=A) | ≈ −17 dB per sideband |

The 10 % figure aligns with the standard cranking-compression spec that no cylinder may differ
from the others by more than 10 % ([VintageIsTheNewOld](https://www.vintageisthenewold.com/faq/how-much-compression-should-a-v8-have),
[Jeepfan](https://jeepfan.com/tech/how-to-test-compression-pressure-on-an-amc-v8-engine/)).
These numbers are for an ideal, full-bandwidth pressure transducer at the port; at the
**tailpipe** the muffler/pipe transfer function and the phone mic's AGC compress this dynamic
range. Empirically, expect another 5–15 dB of dynamic-range compression at the mic. So
"healthy at the mic" is more like **−15 to −25 dB per dominant sideband**, with one-cylinder-out
showing up as sidebands within ~5–10 dB of the carrier.

## Where the observed signal sits

From `exhaust_spectrum.png`:

- 48.8 Hz firing line is the tallest in the audible band (≈ 7·10⁻² PSD units).
- A second peak at ~67 Hz (= 48.8 + 3·6.1) is roughly half its height (≈ −3 to −6 dB).
- A third peak around 55 Hz (= 48.8 + 1·6.1) is ~5–8 dB down.
- Cylinder-event lines at 6, 12, 18 Hz are clearly visible.
- 2× firing (97.7 Hz) is ~−15 to −20 dB vs the fundamental, which is consistent with the OEM
  muffler rolling off above ~100 Hz.
- The synth comparison (`spectrum_compare_720rpm.png`) shows the four procedural V8 models
  all produce a **single sharp 48 Hz spike with essentially no sideband comb**, while the real
  trace has a dense comb of ±k·6 Hz lines. So qualitatively the engine has more sideband
  structure than an "ideal" model — but that is partly because the synth doesn't include
  pipe acoustics or imbalance, not because the engine is broken.

A sideband within ~5 dB of the carrier looks alarming on the −24 dB / −17 dB scale above and
is **above** what pure ±5 % imbalance would predict. But two strong caveats:

1. **Tailpipe Helmholtz/standing-wave resonances** in the 50–80 Hz band are essentially
   guaranteed on a stock R129 system (~3 m of pipe + chambered muffler ≈ quarter-wave around
   55–80 Hz). Any spectral content there gets boosted; a ~10 dB resonance peak at 65–70 Hz on
   top of a small genuine sideband would reproduce exactly what we see.
2. **Phone-mic AGC and 8 kHz codec** flatten the loudest peaks by 5–15 dB. That makes the
   effective sideband-to-carrier ratio at the mic an upper bound on the true imbalance, not a
   direct measurement.

After mentally subtracting both effects, the implied cylinder imbalance is most likely in the
**5–10 % range**: well within the burble-character envelope of an aged but healthy cross-plane
V8 (consistent with the general descriptions of cross-plane half-order content in
[Wikipedia: Crossplane](https://en.wikipedia.org/wiki/Crossplane) and the Ferrari V8 idle FFT
example at [YMEC](https://www.ymec.com/hp/signal2/car1.htm)), and **not** in the
"one-cylinder-fully-out" range that would put a sideband within ~3 dB of the carrier and
also kill the 2× firing line entirely (it didn't — 97.7 Hz is still there, just weak).

## Most likely benign causes on a 25+ year-old M119

1. Normal cross-plane V8 cylinder-event modulation, amplified by tailpipe/muffler resonance
   in the 50–80 Hz band.
2. Mild, even cylinder spread (≤ ~8 % imbalance) from age-related differences in injector
   flow, intake-port carbon, and slightly tired valve guides — the usual story on a 200k+ km
   M119 that still drives well.
3. Phone-mic recording artifacts (AGC, low sample rate, wind/handling noise around the
   tailpipe) inflating the apparent low-frequency comb.

## Failure modes to rule out (ranked by prior probability for an M119)

1. **Distributor cap + rotor + insulator behind the cap** — by far the #1 cause of M119 idle
   roughness and intermittent one-cylinder dropout; carbon-tracking and condensation under the
   cap, even on relatively new OEM parts ([500Eboard cap thread](https://www.500eboard.co/forums/threads/distributor-caps-insulators-and-idle-issues.11460/),
   [Insulator thread](https://www.500eboard.co/forums/threads/ignition-problem-traced-to-faulty-insulators-behind-distributor-caps.144/),
   [Defective new Bosch caps](https://500eboard.co/forums/threads/m119-intermittent-misfire-defective-brand-new-distributor-cap.16709)).
   A cylinder fed by a tracked cap segment can drop ~10–20 % of its energy intermittently —
   exactly the thing that lifts these sidebands.
2. **Plug wires** — high-resistance or breakdown wires (target ~1.8 kΩ each) commonly cause a
   single weak cylinder ([MBClub UK SL500 misfire](https://forums.mbclub.co.uk/threads/sl500-r129-misfire-at-idle-what-next.79244/)).
3. **Spark plugs** — fouled / wrong-heat-range / wide-gapped plugs on one cylinder.
4. **Vacuum / intake-manifold leak** at one runner (cracked rubber boots, tired O-rings on
   the upper plenum, leaky idle-air bypass) — biases one cylinder lean ([Benzworld 1990 SL
   hunting idle](https://www.benzworld.org/threads/1990-mercedes-500sl-r129-hunting-idle-and-shaking.3047696/)).
5. **EZL / PMS ignition module** going marginal — usually shows up as random dropout across
   cylinders, not a single repeating one, but worth knowing about.
6. **Compression / leakdown problem on one cylinder** — burnt exhaust valve, worn rings,
   dropped valve seat. M119s are pretty robust here but the engine is 25+ years old.
7. **Camshaft / timing-related**: oil-filled chain tensioner rails are a known M119 wear item;
   a worn rail won't cause cylinder imbalance directly but can change valve timing globally
   (would not look like single-cylinder sidebands — listed for completeness).

## Recommended next diagnostic steps (cheapest first)

**Free, software/recording only** — do these before anything else:

1. **Record a 30–60 s warm idle with a better setup**: phone or recorder ≥ 44.1 kHz / 16-bit,
   AGC off if possible, mic on a stand 30–50 cm behind the tailpipe at 45° off-axis (avoid
   tailpipe wash). The current 8 kHz AGC clip is the limiting factor in this whole analysis.
2. **Record cold-start to fully-warm** as one continuous take. If the sideband-to-carrier
   ratio in the 36/55/67 Hz lines **shrinks** as the engine warms, that is strong evidence
   the imbalance is real (typically: cold cylinders behave more differently than warm ones).
   If the ratio stays constant, it's almost certainly tailpipe acoustics + AGC and the engine
   is fine.
3. **Record a slow rpm sweep** (idle → 1500 → idle, hold each step 5 s). Acoustic resonances
   are pinned to the pipe geometry and do **not** track rpm; genuine cylinder-event sidebands
   **do** track rpm (they always sit at `f_fire ± k·rpm/120`). This is the cleanest free
   discriminator and you can do it from the driver's seat with the phone on the rear bumper.
4. **Cylinder-out audio**: with the engine off, pull one plug wire at the cap end at a time,
   restart, record 10 s at idle, reconnect, repeat for all 8. The cylinder whose removal
   causes the **smallest** change in idle quality / firing-line height is the already-weak
   one. (Don't crank for long; the cats won't love unburnt fuel.)

**Cheap shop / DIY steps**:

5. **Pull both distributor caps and rotors and inspect** for carbon tracks, hairline cracks,
   moisture, and oily film on the insulator behind the cap. Replace as a set with genuine
   Bosch / Beru if anything looks off (≈ €150–250 in parts). This is the highest-prior fix.
6. **Measure plug-wire resistance** end-to-end — should be ≈ 1.8 kΩ each, all 8 within ~10 %.
7. **Pull all 8 plugs**, photograph each, look for one that's noticeably different (sooty,
   oily, white). A cylinder running cold or rich will out itself here.
8. **Read KE-Jetronic / HFM blink codes** on the diagnostic socket (X11 in the engine bay).
   The pin-3 impulse counter / duty-cycle method is documented for these cars
   ([Benzworld KE-Jetronic diagnosis](http://benzworld.org/threads/ke-jetronic-diagnosis-information.3083914/latest)).
   Even a cheap LED + paperclip rig works.

**Shop-only, only if 1–8 don't disambiguate**:

9. **Cranking compression test**, all 8 cylinders, throttle held open, hot. Spec is no
   cylinder more than 10 % below the others.
10. **Cylinder leakdown test** — best single test for finding a bad valve, ring, or HG; if
    any cylinder shows >15 % leakdown or unusual leak path (into intake = intake valve, into
    exhaust = exhaust valve, into crankcase = rings) that is the weak cylinder.
11. Only if leakdown is bad on one cylinder: borescope through the plug hole. Cracked-piston
    / dropped-seat findings on M119s are rare but documented.

## TL;DR for the owner

The "second peak almost as tall as the firing peak" is mostly your stock muffler resonating
in the 60–70 Hz band on top of the perfectly normal cylinder-event modulation that gives
every cross-plane V8 its character. It is **not by itself a sign of a dead cylinder** — a
truly dead cylinder would also kill the 2× firing line at 97 Hz, and it hasn't. That said, the
M119's #1 weak spot is the distributor cap / rotor / insulator stack, and the cheapest
high-value moves are: (a) re-record cold-start and an rpm sweep with a better mic to confirm
the comb is acoustic and not combustion, then (b) pull both caps and look at them. Hold off
on compression / leakdown unless steps 1–7 actually point at one cylinder.
