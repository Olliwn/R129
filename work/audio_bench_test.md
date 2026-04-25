# Audio Chain Bench Test — BE2210 → UP 6DSP → Sub + Fronts

Opportunistic end-to-end bench test of the complete audio chain before the permanent install. Purpose: prove the signal path, the DSP auto-wake behaviour, and the absence of ground-loop hum, using a minimum of temporary wiring that can be torn down in ten minutes.

**First-use context:** Sunday evening, 2026-04-26, only if the subwoofer carcass is sealed and drying per `work/subwoofer_enclosure/README.md`. Not a blocker — skip cleanly if tired.

**Cross-references:**
- BE2210 pinout + tap rationale: `work/center_console_refresh/README.md` §4
- Sub enclosure state expected: carcass assembled, terminal cup wired, driver NOT yet mounted (can sit loose on the bench)
- DSP power source: Biltema 84-574 CCA kit, see `docs/parts_to_order.md` Priority 6B

---

## 1. What the test proves (and doesn't)

### Proves

- The UP 6DSP receives signal from the BE2210 via the high-level CAT6 tap.
- DC-offset-sense auto-wake turns the DSP on within ~1 s of BE2210 signal and off within ~60 s of silence.
- Channel assignment is correct end-to-end (L stays L, R stays R, sub receives both summed via DSP mixer).
- Driver polarity is correct per coil (subwoofer pulls then pushes on a LF test tone, not the reverse).
- No ground-loop hum with engine **off** and engine **on**. Engine-on hum, if present, localises to alternator noise vs shield termination error.
- Approximate channel levels before the permanent level-matching pass.

### Does NOT prove

- Sealed-box acoustic response (driver is loose, not in the finished box with polyfill — expect thin, chesty, low-Q sub sound).
- Permanent wiring behaviour (temporary ground, temporary route — moves when the car does).
- Door-speaker installation fit (all speakers loose on the bench for this test).
- Final DSP EQ + crossover tuning (the test preset is minimum-safe, not optimised).

---

## 2. Topology

```
BE2210 ISO speaker-out pair (front L+/L−, front R+/R−)
        │
        │  CAT6 #1, 3 m, solid-core shielded F/UTP (stripped BOTH ends for this test)
        │    · Blue pair  → LF+/LF− at DSP
        │    · Orange pair → RF+/RF− at DSP
        │    · Green + Brown pairs: unused, twisted shorts to themselves
        │    · Overall foil shield + drain wire: grounded at DSP end only,
        │       floating (insulated, heat-shrunk stub) at BE2210 end
        │
        ▼
    UP 6DSP high-level input
        ▲
        │  Power:
        │   +12 V  ← CCA 8 mm² red (Biltema) ← 40 A AGU fuse holder inline ← battery +
        │   GND    ← CCA 8 mm² black (Biltema) → cubby chassis bolt (bare metal, star washer)
        │
        │  Outputs (all short runs, Biltema 2.5 mm² speaker cable from the 84-574 kit):
        │   Ch 1 ── tweeter L  (Hertz MP 28.3, loose on bench)
        │   Ch 2 ── tweeter R  (Hertz MP 28.3, loose on bench)
        │   Ch 3 ── woofer L   (Hertz MP 165P.3, loose on bench)
        │   Ch 4 ── woofer R   (Hertz MP 165P.3, loose on bench)
        │   Ch 5 ── sub COIL A (Helix IK S10-DVC2 via terminal cup, driver loose or taped to mock-up)
        │   Ch 6 ── sub COIL B (same driver, other coil)
```

Key clarifications:

- **One** CAT6 gets stripped for this test. The second 3 m CAT6 stays intact as a spare for the permanent run.
- Strip 80–100 mm of outer jacket at each end. Leave the pair twist intact to within ~13 mm of termination. Don't untwist the pairs for "tidy routing" — the noise rejection is in the twist.
- The shield drain at the BE2210 end gets heat-shrunk over itself (insulated stub) — NOT left floating bare inside the ISO pigtail, NOT grounded at that end.
- CCA kit lugs for this bench test: **hex-crimped**, dielectric grease in the cup, as per the Apr 24 decision. Even temporary, practice the real install protocol so the procedure is familiar.

---

## 3. Pre-flight checks — before any 12 V touches anything

- [ ] Sub terminal cup continuity per `work/subwoofer_enclosure/README.md` §6.3 confirmed
  - `COIL A +` ↔ driver A+: ~0 Ω
  - `COIL A +` ↔ `COIL B +`: **open** (isolation check — this is the one that kills the DSP if wrong)
  - Each coil DCR: ~2 Ω
- [ ] AGU fuse **OUT** of the fuse holder
- [ ] Multimeter on 20 V DC, probes on DSP `+12V` and `GND` screw terminals → should read 0 V (no path to battery yet, fuse is out)
- [ ] CAT6 pair assignment labelled on both ends with tape (Blue = LF, Orange = RF) — easy to swap by accident during strip-and-land
- [ ] Shield drain: ring-terminaled at DSP end, heat-shrunk stub at BE2210 end
- [ ] All speaker-cable polarity marked at both ends with tape or heat-shrink (red sleeve = +, black = −) — easy to cross under pressure
- [ ] Ignition: **OFF, key out**. All doors closed. No charger connected to battery.

---

## 4. Power-up sequence

Order matters — ground always first, fuse always last, so no live lead ever waves around.

1. **DSP ground** to cubby chassis bolt. Torque snug, not aggressive.
2. **DSP +12 V** to the CCA red output side of the AGU fuse holder.
3. **AGU fuse holder +12 V input** to the battery +. Holder empty.
4. Quick visual on everything. No shorts, no pinched insulation, no stray strands.
5. **Insert the 40 A AGU fuse.**
6. Expect: DSP power LED ON within 1–2 s, no turn-on pop. Listen for click/relay noise inside the DSP housing — that's the auto-sense board standing ready.
7. If fuse blows: pull it, recheck step 1–4 for a ground/+ short. Do **not** fit a higher-rated fuse to "solve" it.

---

## 5. First signal test — BE2210 on, minimum-safe preset loaded

### 5.1 DSP PC-Tool preset (load before hardware test)

Connect laptop to UP 6DSP via USB, Audiotec Fischer DSP PC-Tool. Load or manually set:

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| Input source | `High-Level` | Uses the front-pair CAT6 tap as input, not USB or line-in. |
| Turn-on mode | `High-Level (DC offset sense)` | Auto-wake on BE2210 signal, no remote wire needed. |
| Turn-on delay | Default (~1 s) | |
| Turn-off delay | 60 s | Sleep after BE2210 goes silent. |
| Channel 1 HP | 2.5 kHz, 24 dB/oct LR | Tweeter L — **−10 dB** gain trim. |
| Channel 2 HP | 2.5 kHz, 24 dB/oct LR | Tweeter R — −10 dB. |
| Channel 3 BP | 80 Hz HP, 2.5 kHz LP, 24 dB/oct LR | Woofer L — −10 dB. |
| Channel 4 BP | 80 Hz HP, 2.5 kHz LP, 24 dB/oct LR | Woofer R — −10 dB. |
| Channel 5 LP | 80 Hz, 24 dB/oct LR | Sub coil A — −10 dB. |
| Channel 6 LP | 80 Hz, 24 dB/oct LR | Sub coil B — −10 dB. |
| All EQ bands | flat | No tuning yet. |
| Sub mix (Ch 5/6) | L+R sum from Ch 3/4 source | Sub gets mono L+R. |

Save as preset `bench_test_v1`. The −10 dB across-the-board is insurance against a wiring error blowing a driver before the level is sanity-checked.

### 5.2 Sound checks — stepwise

1. **BE2210 off (power button off).** DSP should be in standby after ~60 s. Power LED dim or off depending on UP 6DSP firmware.
2. **BE2210 on, volume at zero, tune to an FM station with good signal.** DSP auto-wakes within ~1 s of un-muting. Power LED full on.
3. **Volume up to a low-moderate level (say FM volume setting ~10 / 30).**
4. Listen to each channel in turn by plugging speakers one-at-a-time, or by panning the BE2210 balance/fader:
   - Tweeter L — expect high-frequency content, no low-frequency thumping. Centered on one ear.
   - Tweeter R — same, other ear.
   - Woofer L — midbass through upper-midrange. No tweeter content (crossover working), no sub rumble (80 Hz HP).
   - Woofer R — same.
   - Sub — continuous low rumble on a bass-heavy track, both coils moving the driver cone in the **same direction** on a bass beat (visually confirm — uneven movement = coil polarity error on one of A/B).
5. **Polarity sanity check:** put a hand on the sub cone while a low bass note hits. First movement should be **outward** (toward you). Inward-first = swap one coil's polarity.
6. **Level sanity check:** at a mid-level BE2210 setting, woofers + tweeters should balance at normal listening volume. Sub should be audible but not dominant (−10 dB trim is intentionally conservative). No clipping, no distortion.

### 5.3 Pass/fail table

| Observation | Expected | If not ... |
| :--- | :--- | :--- |
| DSP wakes on signal within 2 s | ✓ | Check PC-Tool turn-on mode is `DC offset sense`, not `Remote`. Check the CAT6 tap actually has signal (multimeter on AC 2 V scale at the DSP high-level input — should read 0.1–1 V AC when music plays). |
| L/R not swapped on fronts | ✓ | Check CAT6 pair labelling. Blue pair = LF, Orange = RF per §4 convention. Easy to reverse at strip-and-land. |
| Sub moves air | ✓ | If silent: check Ch 5/6 levels in PC-Tool, check DVC2 terminal cup continuity, check LP is 80 Hz not 8 Hz (UI typo). |
| Sub cone moves out-first on bass | ✓ | Swap one coil's polarity at the terminal cup (NOT at the DSP — confusing once installed). |
| No hum engine-off | ✓ | Check DSP ground quality. Scrape bare metal if needed — paint under a ground lug is the usual first failure. |
| No hum engine-on | ✓ | See §6 below — this is the alternator-noise test. |
| DSP sleeps ~60 s after BE2210 off | ✓ | Check turn-off delay in PC-Tool. |

---

## 6. Engine-on test — alternator noise isolation

Worth running as a separate step because the fix is distinctive if it fails.

- Start engine, let it settle at warm idle (post-Saturday the engine is warm from the ATF cycle).
- Listen at normal volume, then **volume to zero, BE2210 on, DSP awake**.
- **Listen for high-frequency whine** that changes pitch with engine RPM. Blip the throttle (safely, with the car still on stands and in Park) and listen for the whine's pitch tracking.

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| Steady 50/60-Hz-ish hum, engine off AND on | Ground loop | Check DSP ground is a solid chassis bolt on bare metal. Disconnect all signal cables except CAT6; if hum persists → power ground issue, if hum stops → signal ground issue. |
| Whine that tracks engine RPM, only engine-on | Alternator noise on the CAT6 tap, shield not terminated correctly | Confirm shield is grounded **at DSP end only**, floating at BE2210 end. Both-ends grounded = ground loop back through the shield, same RPM-tracking symptom. Per `work/center_console_refresh/README.md` §4. |
| Buzz on bass notes only | DSP clipping or MDF panel resonance — neither possible at bench-test levels | Skip; revisit in the final tune. |
| Noise only when headlights on | Shared-ground with the headlight circuit | DSP ground needs its own star-point return to battery −, not via chassis. Re-plan permanent routing. |

Log the engine-on result. If clean → the shield strategy works and can be committed to the permanent install. If noisy → fix before closing the console.

---

## 7. Teardown

1. BE2210 off, let DSP sleep.
2. **Pull the 40 A AGU fuse first** — kills all 12 V downstream immediately.
3. Disconnect DSP +12 V. Disconnect DSP GND. (Opposite order of build-up.)
4. Unplug all speaker leads and the CAT6. Coil loosely for re-use.
5. Mark the CAT6 cable as "bench-test stripped, retire from intact spare use — becomes the permanent BE2210 tap cable next weekend."
6. Note any observations in the 2026-04-26 diary entry. Things worth recording: whether auto-wake was reliable, any hum (and which version solved it), driver polarity on each coil confirmed, any channel that sounded wrong.

---

## 8. Artifacts to produce from the test

On the way out, before packing up, take these so the permanent install doesn't have to re-derive them:

- [ ] Photo of the full bench topology
- [ ] Saved PC-Tool preset `bench_test_v1.cfg` — starting point for Phase 3 tuning
- [ ] Diary note on DSP auto-wake + auto-sleep timing (actual vs spec)
- [ ] Diary note on hum status (engine off / engine on / engine on with headlights)
- [ ] Measured AC voltage on the CAT6 tap at the DSP end with music at normal BE2210 volume — useful for sanity-checking the permanent install if it ever seems "quiet"

---

*Created 2026-04-24 as a weekend-prep artifact. Procedure execution 2026-04-26 (opportunistic).*
