# Gate 3 — In-Car Validation Procedure

Read once before the in-car session, tick through live. Builds on the
[Pi → MEC bring-up procedure](../audio_tuning/in_car_pi_bringup_procedure.md)
and the [Gate 2 design](gate2_car_integration_design.md).

**Pass criterion for Gate 3 overall:**

> At least one preset survives a real 15-minute drive without becoming
> tiring, fake, or unsafe — and one tester (driver or passenger)
> reports they would "miss it" if the system were toggled off.

If no preset crosses that bar, the system stays disabled by default.

---

## 1. Pre-flight checklist (do BEFORE engine start)

### 1.1 DSP-side guardrails (5 minutes, laptop with DSP PC-Tool)

The DSP preset is the actual safety net for the tweeters. Verify the
soft-top driver preset (tuned 2026-05-12 per
[`docs/diary/2026-05.md`](../../docs/diary/2026-05.md)) is still in
place:

- [ ] Connect laptop to UP 6DSP, read live preset.
- [ ] **Ch1/Ch2 (L/R tweeter):** HP at 2.5 kHz LR24, gain ≤ −6 dB. The
      synth output is bandlimited to ≤ 500 Hz so it shouldn't touch the
      tweeters even with the HP filter removed — but keep the filter as
      defence in depth.
- [ ] **Ch5/Ch6 (sub DVC):** HP 45 Hz LR24, LP 80 Hz LR24, gain ≤ −6 dB.
      Synth's sub-body layer lands here.
- [ ] Master gain at the same setting as the 2026-05-12 tune. Do not
      touch.
- [ ] No changes saved & stored unless you explicitly intend it.

### 1.2 Pi-side guardrails (SSH from laptop)

- [ ] `ssh pi@r129.local` succeeds.
- [ ] `wpctl status` — confirm music sink + synth sink (loopback) are
      both present.
- [ ] Run `~/bin/audio-safe.sh`. Music sink → 50 % (−6 dB).
- [ ] **Synth bus gain in PipeWire ≤ −9 dBFS** (per Gate 2 §5). The
      synth service should refuse to start if its bus is at unity.
- [ ] Synth service starts with `Engine Sound = Off` and `Intensity = 0 %`.
- [ ] `journalctl -u r129-exhaust-synth -n 20` clean.

### 1.3 Mic placement

For option-1 (reference mic) Gate 3 trial:

- [ ] UMIK-1 mounted in the engine bay, ~30 cm from the exhaust manifold
      or close to an engine mount. Cable runs through an existing
      grommet, no new holes.
- [ ] Mic windshield (foam) fitted.
- [ ] Cable strain relief, away from belts/hot exhaust/moving parts.
- [ ] Mic connected to RPi5 via USB extension; `arecord -l` or
      `pactl list sources` shows the UMIK as available.
- [ ] **Engine OFF** at this point.

### 1.4 Capture-side recording (REW)

You will want to capture the cabin response at the driver-head position
for offline A/B comparison, separately from the engine-bay mic. The
existing UMIK-1 is doing both jobs today, so move it after the engine-
running tests in §3 conclude — for the live tracker tests use only the
engine-bay mic.

A second UMIK-1 would let us run both simultaneously; not in scope for
this Gate 3 entry, but worth noting as a future shopping item.

---

## 2. Driveway bench test — engine OFF first, then idle

The point of §2 is to prove the synth service is functional and safe
without engine confounds.

### 2.1 Engine OFF, synth engaged (synthetic RPM source)

The first thing the system should do is generate audio cleanly with a
known-good RPM source, before being asked to track a real exhaust.

- [ ] In the R129 UI: `Tracker Source = Sim`, `Engine Sound = Luxury`,
      `Intensity = 0 %`.
- [ ] Slowly raise `Intensity` to 50 %. Listen.
  - **Expected:** synth is audible through both fronts + sub. No buzz,
    no oscillation, no feedback howl, no spikes. Soundstage similar
    to the living-room renders.
  - **If anything sounds wrong:** drop intensity to 0 %, set `Engine Sound = Off`,
    diagnose before continuing.
- [ ] Try each preset (`OEM+`, `Luxury`, `AMG-ish`, `Sport`) at 50 %
      intensity. Confirm character matches living-room expectations.
- [ ] Set `Engine Sound = Off`. Verify the synth fades out cleanly.

### 2.2 Engine ON, idle, synth OFF — baseline mic capture

- [ ] Start engine. Let idle stabilise (~30 s warm up if cold).
- [ ] `Tracker Source = Engine Bay Mic` (no synth audio yet).
- [ ] In a debug screen / `journalctl`: confirm tracker reports an RPM
      estimate close to actual (within ±50 rpm) and confidence ≥ 0.7.
  - **If confidence is low:** mic too far / windshield missing / cable
    pickup noise. Fix before continuing.

### 2.3 Engine ON, idle, synth ENGAGED at low level

- [ ] `Engine Sound = Luxury`, `Intensity = 20 %`.
- [ ] Listen at the driver position. Both windows closed; soft top up
      (matches the tuned DSP preset).
  - **Expected:** synth fills the cabin with V8 body that the stock
    exhaust hides at idle. Tracker confidence stays ≥ 0.7.
  - **If you hear feedback howl / runaway**: that's the self-
    contamination loop predicted in Gate 2 §2. Drop intensity, then
    enable synth-output subtraction in the tracker if available, or
    swap to option 2 (accelerometer) path.
- [ ] Raise intensity in 10 % steps to 80 %. At each step check:
  - No distortion / buzz.
  - Tracker confidence stays ≥ 0.7.
  - Cabin pressure feels controlled, not boomy.

### 2.4 Real drive — gentle 15-minute loop

- [ ] Pick a familiar route with both city stop-and-go and a slow rural
      stretch.
- [ ] **Driver:** pay attention to fatigue / annoyance. If at any point
      you find yourself wanting to turn it off, that's the answer.
- [ ] **Passenger:** toggle `Engine Sound` between `Off` and `Luxury` at
      irregular intervals without telling the driver. Note when driver
      asks for it back on vs leaves it off.

---

## 3. REW captures (after the drive, parked engine running)

Once §2 is clean, gather objective data at three steady-RPM holds.

For each of: **idle (~720 rpm), 1500 rpm, 2000 rpm, 2500 rpm**:

1. Engine held at target RPM (foot-on-brake, neutral, gentle throttle).
2. UMIK-1 moved to driver-head position.
3. REW sweep, 20 Hz – 20 kHz, `Engine Sound = Off`. Save as
   `rew_baseline_<rpm>.mdat`.
4. Same RPM, `Engine Sound = Luxury`, `Intensity = 60 %`. Sweep again.
   Save as `rew_engaged_luxury_<rpm>.mdat`.
5. Repeat step 4 for `AMG-ish` at the same intensity.

Save all `.mdat` projects to `work/audio_exhaust_synth/rew_gate3/`.

**Analysis (offline, same evening or next day):**

- Overlay baseline vs engaged. Document where the synth adds energy
  (firing-rate band, harmonics) and where the cabin coloration shifts.
- **Expected result:** strong addition in the 40–250 Hz region at the
  target RPM, falling away above 500 Hz. The plan does *not* expect
  phase alignment to be perfect at all three RPMs from a single tracker
  pass — document the degradation.

---

## 4. Subjective A/B during the drive

Concrete protocol for the passenger A/B test in §2.4:

- Pre-flight: passenger memorises the `Engine Sound` toggle path in
  the UI.
- During drive: at varied moments — straight road, mild acceleration,
  cruise, idle at lights — passenger toggles between `Off` and a
  pre-chosen preset.
- Driver verbally notes one of: `miss it`, `notice it`, `prefer off`.
- Tally per preset over ~10 toggles each.

**A preset is "shippable" only if `miss it` outnumbers `notice it`
and there are zero `prefer off` for that preset.**

---

## 5. Kill switches (in priority order)

1. **Volume widget on the Pi UI** — drops main sink to 0 in one tap.
   Note: this also kills music. Use only as nuclear.
2. **`Intensity = 0 %`** in settings — synth bus to silence but music
   continues.
3. **`Engine Sound = Off`** — synth source disconnected entirely.
4. **`Tracker Source = Sim`** — disconnects the mic from the synth, so
   any mic-induced loop instantly stops.
5. **`systemctl --user stop r129-exhaust-synth`** over SSH — terminates
   the service.
6. **REM line disconnect** — kills the DSP entirely. Music dies too.
   Documented in the bring-up procedure for completeness.

---

## 6. Pass / fail decision

| Outcome | Action |
| :--- | :--- |
| At least one preset gets a clear `miss it`-majority vote and no `prefer off` | Pass — proceed to Final commit |
| Several presets are interesting but tiring after 15 min | Tune intensity defaults, retest |
| Feedback / contamination ruins idle tracking | Switch to accelerometer (option 2 in Gate 2) and retest |
| The synth is audibly fake at speed even with everything tuned | Fail — revisit synth model, or accept the project as "fun but not for daily driving" |

Document the verdict in `docs/diary/2026-MM.md` and update the parent
plan's todo list accordingly.
