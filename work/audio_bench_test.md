# Audio Chain Bench Test — BE2210 → UP 6DSP → Sub + Fronts

Opportunistic end-to-end bench test of the complete audio chain before the permanent install. Purpose: prove the signal path, the DSP auto-wake behaviour, and the absence of ground-loop hum, using a minimum of temporary wiring that can be torn down in ten minutes.

**Status (2026-05-01):** ✅ **Executed via the USB-based variant** documented in §9 below — Windows PC → MEC HD-USB → UP 6DSP → all four Hertz speakers + Helix sub. All hardware confirmed functional, channel assignment + polarity correct, configuration persisted to DSP via Save & Store. The original BE2210 + high-level CAT6 procedure (§3–§8) remains intact for the in-car install's auto-wake / shield-termination / engine-on noise validation, none of which the USB bench test exercised. **First-time readers: read §9.3 "Gotchas" before powering anything on.**

**First-use context:** Originally targeted for Sunday evening, 2026-04-26 if the subwoofer carcass was sealed and drying per `work/subwoofer_enclosure/README.md`. Revised 2026-04-25 evening: dropped from the weekend plan in favour of in-car DSP power wiring + BE2210 console-out tap (see `docs/diary/2026-04.md` April 25 evening). Re-revived 2026-05-01 evening as a USB-based variant — see §9 and `docs/diary/2026-05.md` May 1 entry. The §3–§8 BE2210 procedure remains valuable as a fallback diagnostic if the in-car install surfaces a signal-path issue we want to isolate from the install variables — keep the procedure intact for future use.

**DSP location note (2026-04-25):** The permanent DSP location is the **rear passenger-side cubby**, not driver-side. The bench test itself happens on a bench/floor rather than in either cubby, so the procedure below is unchanged; the only consequence is that "cubby chassis bolt" (Step 4 ground reference) refers to the passenger-side cubby once we move from bench to car.

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

## 9. USB-based bench test variant (executed 2026-05-01)

The procedure in §3–§8 above assumes the BE2210 head unit is the signal source. On Friday evening 2026-05-01 the bench test was executed in a different topology — **PC → MEC HD-USB → DSP** — because the goal was end-of-day low-effort progress with the car untouched, the BE2210 was still in the dash, and the MEC HD-USB module was already installed in the DSP. This variant proves nearly all the same things the BE2210 path proves (signal flow, channel assignment, crossovers, polarity, hardware integrity); the explicit exception is that the auto-wake DC-offset path was *not* exercised — REM was tied directly to +12 V instead.

### 9.1 Topology delta

```
PC laptop (Windows 10)
    │
    │  USB cable (control)        →  UP 6DSP main USB port (PC-Tool tuning)
    │  USB cable (audio)          →  MEC HD-USB module port (audio stream)
    │
UP 6DSP
    │  +12 V  ← Varta H3 100Ah (old battery, ~12.5 V resting) via 40 A AGU fuse
    │  GND    ← battery negative direct
    │  REM    ← jumper wire to +12 V (forces amp ON without DC-offset auto-detect)
    │
    │  Outputs: same channel assignment as §2 (Ch 1/2 = tweeters, Ch 3/4 = mid-woofers, Ch 5/6 = sub coils)
```

### 9.2 What was different from §5

- **No BE2210 in the loop** — input source is the PC's USB audio output, presented to Windows as `HD-AUDIO USB-INTERFACE FS`. No driver install needed (FS = Full Speed, up to 96 kHz / 32-bit, class-compliant USB audio).
- **Auto-wake disabled** — physical "Auto Remote" switch on the UP 6DSP chassis flipped to **OFF**, REM tied to +12 V. Rationale: with no BE2210 in the loop there is no DC offset on the high-level inputs, so the auto-detect circuit has nothing to wake on.
- **Sub driver loose, in temporary cardboard/MDF mock-up box** — final enclosure still curing; not yet wrapped/finished.
- **Crossover defaults bumped slightly:** tweeter HP set to 3 kHz / 24 dB/oct LR (vs 2.5 kHz spec) for bench-test safety with loose speakers and no enclosure acoustics. Drop back to 2.5 kHz once in the car with measurements in hand.
- **Bench location:** living-room floor on a carpet (battery on parquet). Distance from battery to amp ~1.5 m on the floor.

### 9.3 Gotchas — every one of these cost real time, document so it doesn't happen twice

These four traps are the "every first-time UP 6DSP installer hits these" set. They are not mentioned in the §3–§5 procedure above because that procedure assumed BE2210 auto-wake. **For any future bench test or first-power-on of an Audiotec Fischer DSP without a head unit, read this list first.**

1. **Save & Store is mandatory.** Every change you make in the PC-Tool — IO routing matrix, DCM source priority, channel filters, gains — is **preview-only** until you click the **Save & Store** (disk icon) button at the top of the PC-Tool. Symptom when forgotten: the DSP appears configured correctly in the UI, but outputs are silent because the running configuration on the DSP is still the previous (or factory default) state. This single gotcha consumed roughly 30 minutes of debugging on 2026-05-01.

2. **Auto Remote switch must be OFF for bench operation.** The UP 6DSP has a small physical slide switch on the chassis (near the screw terminals) labeled **"Auto Remote"**. When ON, the amp ignores the REM screw terminal and waits for DC-offset on the high-level inputs to wake up. For bench testing without a head unit, set this to **OFF** and tie REM to +12 V with a jumper wire. **Power-cycle the DSP after flipping this switch** — the position is only read at boot.

3. **HEC/AUX Routing is a separate matrix from Main Routing.** In the IO menu, there are (at least) two routing tabs: **Main Routing** (for analog/high-level inputs from a head unit) and **HEC / AUX Routing** (for the MEC card audio). When the DCM source priority switches the active source from Main to HEC/AUX, the DSP also switches *which routing matrix it consults*. A populated Main matrix and an empty HEC/AUX matrix → silence. **Both matrices must be configured if both source paths will be used.**

4. **DSP PC-Tool has no internal signal generator.** The PC-Tool **cannot generate test tones internally** — it has only an analyzer (RTA) for an external microphone. To bench-test a UP 6DSP you *must* provide an external audio source (BE2210, MEC HD-USB, or a stripped 3.5 mm AUX cable into the high-level inputs).

Honourable mentions:
- The PC-Tool's Master Volume slider lives at the bottom edge of the Outputs screen and is easy to miss the first time. Same for the channel level meters (left/right edges of the Outputs screen, only animate when audio is actively flowing through that channel post-routing).
- Windows 10 default audio format on the MEC HD-USB device should be left at 48 kHz / 24-bit unless deliberately needed otherwise — sample-rate mismatches with the DSP's internal 48 kHz processing would show up as silent dropouts.

### 9.4 Result (2026-05-01)

- **All hardware confirmed functional:** UP 6DSP, MEC HD-USB card, both Hertz MP 28.3 tweeters, both Hertz MP 165P.3 mid-woofers, Helix IK S10-DVC2 sub driver and terminal cup.
- **Signal path proven end-to-end:** Windows USB → MEC HD-USB → DSP processing (per `bench_test_v1` preset) → all 6 amp output channels → speakers.
- **Channel assignment correct** (L stays L, R stays R, sub gets summed mono L+R).
- **Crossover defaults applied:** tweeter HP 3 kHz / 24 dB/oct LR, woofer BP 80 Hz HP / 3 kHz LP / 24 dB/oct LR, sub LP 80 Hz / 24 dB/oct LR. All channels at −10 dB safety trim.
- **Sub polarity:** cone moves outward first on bass — both DVC2 coils correctly in phase, no terminal-cup polarity swap needed.
- **Subjective audio quality** on speakers loose on the carpet (no enclosures, no door panels, sub in temporary mock-up): "already pretty good on some material." Mid-bass thin (no door reinforcement) and sub a bit boomy and uneven (no proper enclosure or polyfill yet), but the system clearly responds to good source material with character that the BE2210-only baseline never had.
- **Configuration persisted to DSP non-volatile memory** via Save & Store. Survives power-cycle; ready to be the starting preset for the in-car tuning pass.
- **Bench setup photo:** `pics/F4D28352-6753-491F-8D2E-B9FAEDD892F1_1_102_o.jpeg`.

### 9.5 What this variant does NOT prove (vs §1)

- **Auto-wake on DC offset** — REM was tied to +12 V, so the DC-offset detection circuit was not exercised. This must still be confirmed during the in-car install when the BE2210 high-level tap is wired up (per `work/center_console_refresh/README.md` §4).
- **Engine-on alternator noise rejection** — bench was on an old Varta H3, not the car's running alternator. CAT6 shield-termination strategy still needs the engine-on test in §6 once the car is the power source.
- **Permanent ground integrity** — temporary battery clamps, not a chassis ground bolt with star washer.
- **CAT6 high-level path** — the actual stripped CAT6 from the BE2210 ISO speaker-out pair is not exercised in this variant. That happens during the center-console refresh session.

These four open items are what the in-car install will need to validate, but the "is the chain alive" question is now closed.

---

*Created 2026-04-24 as a weekend-prep artifact. Original §1–§8 (BE2210 + high-level CAT6 procedure) execution targeted 2026-04-26 → deferred. §9 (USB-based variant) executed 2026-05-01.*
