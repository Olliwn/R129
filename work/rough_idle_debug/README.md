# Rough Idle Debug Plan — M119.960 KE-Jetronic / EZL

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | **Engine:** M119.960 V8, KE-Jetronic, EZL ignition with dual distributor caps/rotors

**Trigger:** MB-osat inspection on 2026-04-30: engine does not fire all cylinders cleanly at idle. A V8 should idle smoother than this. Distributor-related fault was suspected, and new distributor caps + rotors are already ordered, but the root cause is **not proven**.

---

## Objective

Find the reason for the rough idle without turning the parts cannon on.

The plan is deliberately staged:

1. Establish a repeatable baseline while the old caps/rotors are still installed.
2. Localize the fault: one cylinder, one bank, all cylinders randomly, or load/temperature dependent.
3. Replace caps/rotors as a controlled test.
4. If the problem remains, use the localization data to choose ignition, air/vacuum, fuel, or mechanical checks.

---

## Current Evidence

### 2026-05-01 Oulu MB Klubi Vappu Kulkue Road Test

Trip context: roughly 2 h drive to/from Oulu MB Klubi Vappu parade. Ambient temperature was warmer than previous checks; about 12 deg C outside during the A/C observation, with strong sun load into the cabin.

Findings:

- During about 1 h of very low-speed driving, engine temperature stabilized around **85 deg C**. When traffic cleared and road speed increased, temperature cooled closer to **80 deg C**.
- During the last ~1 km, power windows stopped working. The two top red fuses in the trunk fuse box F20 had blown: **F20-1 (16 A red, window lifter left)** and **F20-2 (16 A red, window lifter right)**. Identification per `r129_data/data/fuse_box.yaml` (factory Betriebsanleitung 1991-1993, p. 120). The trunk fuses had already been replaced earlier with modern non-aluminum torpedo fuses, so this is a real fault event, not aluminum-fuse age fatigue.
- A/C is not producing cold air. Even at only ~12 deg C outside, sun load made it obvious that no cooled air was entering the cabin.

Immediate follow-up:

- Do not treat the 80-85 deg C road-test temperature as overheating evidence by itself; it currently looks load/airflow dependent and within a plausible range.
- Action: replace F20-1 and F20-2 with fresh 16 A fuses and observe on the next drive. Two simultaneous window-circuit failures with modern fuses points to a shared cause; candidates to keep in mind if it repeats: stiff regulators pulling near-stall current under warm/load conditions, moisture ingress at the center console window switch pack, or a chafed point in the shared trunk-to-cabin window harness. If the replacements blow again, do not keep up-rating; investigate the circuits.
- Update 2026-05-01: F20-1 and F20-2 replaced. Both windows now move freely, but the motors are audibly working hard. This is consistent with the stiff-regulator hypothesis (both motors running near their continuous current limit, which on a long warm drive can age both fuses to the point of simultaneous failure). Mechanism inspection and lubrication deferred to the planned door-card removal for speaker installation; that is the right time to clean and re-grease the regulator rails on both sides.
- Treat the A/C as a separate HVAC diagnosis for now: confirm compressor engagement, refrigerant pressure switch state, auxiliary fan behavior, and whether the pushbutton/control unit is commanding cooling.

Known positives:

- Engine internals are cautiously healthy based on oil condition: translucent honey oil after ~1 800 km, no oil consumption, no milkiness, no visible particulate.
- Old spark plug electrodes were clean tan/grey on all 8 cylinders when removed on 2026-04-05.
- New NGK BCP5ES non-resistor plugs installed 2026-04-05 at 22 Nm.
- Crankshaft position sensor fault is resolved: Pin 8 running/post-drive check gave 1 blink on 2026-04-19.

Known concerns:

- 6 of 8 spark plug wells had oil from leaking plug tube seals. Oil can contaminate plug boots and create secondary ignition leakage.
- Old plugs were wrong resistor type, so the ignition system has spent unknown time with excessive secondary resistance.
- Distributor caps/rotors were visually serviceable on 2026-04-05, but MB-osat still considered replacement sensible based on idle quality and cap photos.
- Passenger-side air intake hose is cracked/taped. Vacuum/unmetered-air faults remain plausible on a KE-Jetronic car.
- Engine mounts are aged, but MB-osat's observation means mounts must not be treated as the primary root cause until incomplete combustion is ruled out.

---

## Safety Rules

- Do **not** pull plug wires off a running engine. It is a shock hazard and can stress coils/EZL insulation.
- Do **not** spray water mist onto caps/wires as a first-line test. With 35-year-old ignition parts, this can create a fault rather than reveal one.
- Avoid brake-cleaner leak hunting around a hot M119. Prefer smoke test, propane enrichment, or visual/hand inspection first.
- Change one variable at a time. Photograph routing before moving any ignition wire.
- If the engine begins misfiring badly, shut down. Do not idle for long periods with a dead cylinder; unburned fuel can overheat cats.

---

## Tools

Already useful / likely on hand:

- Phone video/audio recording.
- Owon HDS242 / multimeter.
- Basic hand tools.
- Spark plug socket / extensions.
- Infrared thermometer or thermal camera if available.
- Inductive timing light if available.
- Bright flashlight / inspection mirror.
- Vacuum gauge if available.
- Smoke tester if available, or a low-pressure improvised smoke source for intake leak testing.

Worth buying only if the earlier steps point there:

- Inductive timing light: very useful for checking each plug wire without unplugging it.
- Compression tester: only needed if a persistent single-cylinder fault survives spark and fuel checks.
- Leakdown tester: only after compression points to a mechanical issue.
- Fuel pressure gauge with KE-Jetronic-compatible fittings: only if symptoms point to system/control pressure, not as the first move.

---

## Phase 0 — Baseline Before New Caps/Rotors

Do this before Tuesday's distributor parts arrive if possible. Goal: make the symptom measurable.

### 0.1 Warm-idle symptom log

Warm the car fully. Record:


| Condition                  | RPM  | Feel         | Notes                          |
| -------------------------- | ---- | ------------ | ------------------------------ |
| Cold start, first 30 s     | 700  | shaking      | cannot hear/feel a clear rythm |
| Warm idle in P/N           | 700  | shaking      | cannot hear/feel a clear rythm |
| Warm idle in D, brake held | 600  | shaking more | cannot hear/feel a clear rythm |
| Warm idle, A/C off         | 700  | shaking      | cannot hear/feel a clear rythm |
| Warm idle, A/C on          | 700  | shaking      | cannot hear/feel a clear rythm |
| 1 500 rpm no-load hold     | 1500 | almost clean | cannot hear/feel a clear rythm |
| 2 000 rpm no-load hold     | 2000 | clean        | cannot hear/feel a clear rythm |


Interpretation:

- Bad only at hot idle, improves above ~1 500 rpm: vacuum leak, idle air control, injector imbalance, weak spark at low energy reserve.
- Bad cold and hot equally: ignition routing/wire/cap/rotor, dead injector, mechanical compression.
- Worse in D or with A/C load: marginal cylinder or idle-control reserve issue.
- Random shake with no stable rhythm: mixture/idle control or multi-cylinder ignition weakness.
- Regular rhythmic miss: one cylinder or one paired ignition path.

### 0.2 Record evidence

- 20–30 s engine bay video at warm idle.
- 20–30 s exhaust note video near each tailpipe, same distance.
- Tachometer reading.
- Oil pressure at warm idle.
- Any fuel smell, exhaust eye-watering, or raw HC smell.

### 0.3 Diagnostic blink sweep

Repeat the existing X11/4 diagnostic sweep method used earlier in the project. Critical rule: for EZL/crank-sensor-related reads, use engine-running or immediate post-shutdown readings as documented after the crank sensor repair. Do not let KOEO artifact codes steer this diagnosis.

Log any active codes before touching parts.

---

## Phase 1 — Non-Invasive Localization

Goal: determine whether the rough idle is cylinder-specific, bank-specific, or global.

### 1.1 Visual ignition inspection

Engine off, preferably cold:

- Confirm every plug wire is fully seated at the plug end and distributor cap end.
- Inspect plug boots for oil swelling, cracking, carbon tracks, or loose resistor ends.
- Inspect cap towers for hairline cracks, green corrosion, or loose terminals.
- Confirm cap screws are tight and caps sit flush.
- Look for oil still pooled in plug wells after the Apr 5 cleaning.
- Verify wire routing against photos. No crossed wires, no wires stretched tight, no wires lying against sharp/hot edges.

Pass/fail:

- Any oil-wet, cracked, loose, or carbon-tracked boot becomes a suspect even if cap/rotor replacement helps.
- If one bank's wires/boots are visibly worse, keep that bank in mind for Phase 1.3 temperature comparison.

### 1.2 Plug-wire resistance check

Measure wires one at a time, then reinstall before moving to the next wire.


| Cylinder | Resistance | Pass/Fail | Notes |
| -------- | ---------- | --------- | ----- |
| 1        |            |           |       |
| 2        |            |           |       |
| 3        |            |           |       |
| 4        |            |           |       |
| 5        |            |           |       |
| 6        |            |           |       |
| 7        |            |           |       |
| 8        |            |           |       |


Interpretation:

- Use the repo's current service criterion: **less than 10 kOhm per wire** and no open circuit.
- More important than exact value: outliers. One wire much higher than the other seven is suspicious.
- Infinite/open, unstable reading while flexing, or very high resistance means the wire is bad.

### 1.3 Cylinder heat comparison

Use an IR thermometer or thermal camera after a cold start or after 1–2 minutes of warm idle. Measure each exhaust runner as close to the head as accessible, consistently from the same distance/angle.


| Cylinder | Temp | Relative result |
| -------- | ---- | --------------- |
| 1        |      |                 |
| 2        |      |                 |
| 3        |      |                 |
| 4        |      |                 |
| 5        |      |                 |
| 6        |      |                 |
| 7        |      |                 |
| 8        |      |                 |


Interpretation:

- One cold runner: that cylinder is weak/dead. Go to ignition flash check, then injector/mechanical checks for that cylinder.
- One bank cooler: bank-level ignition/cap/rotor/coil issue, intake leak on that side, or fuel distributor imbalance.
- All roughly equal: roughness may be idle control, mounts, mixture, or a subtle multi-cylinder issue.

### 1.4 Inductive timing-light check

If an inductive timing light is available, clamp it around each plug wire at warm idle. Do not unplug anything.

Expected: steady flashing on every cylinder.

Interpretation:

- Irregular/no flash on the same cylinder that is cold: ignition delivery problem upstream of that plug.
- Irregular flash on four cylinders fed by one cap/rotor/coil path: bank/path problem.
- Steady flash on a cold cylinder: spark trigger exists, so check plug boot arcing under load, injector delivery, or compression.

### 1.5 Injector sound check

Use a mechanic's stethoscope or long screwdriver against each injector body.

Expected: similar ticking pattern on all 8.

Interpretation:

- One silent or very different injector: fuel delivery fault on that cylinder.
- All similar: does not prove spray quality, but lowers the chance of a dead injector.

---

## Phase 2 — Controlled Distributor Cap/Rotor Replacement

Do this when the new caps/rotors arrive. Treat it as a test.

### 2.1 Before removal

- Photograph both caps, wire routing, cap orientation, and rotor orientation.
- Mark left/right parts if not obvious.
- Label wires if there is any risk of mixing.
- Record baseline warm-idle video immediately before the work if Phase 0 was not already done.

### 2.2 Inspect old parts as evidence

For each cap:

- Carbon tracking lines.
- Cracks around towers.
- Center carbon brush wear/sticking.
- Brass contact erosion/pitting.
- Moisture/oil/dust inside cap.
- Uneven wear pattern indicating rotor/cap alignment issue.

For each rotor:

- Burned or deeply eroded tip.
- Cracked plastic.
- Loose fit on the drive.
- Evidence it was not fully seated.

### 2.3 Install

- Replace one side at a time.
- Seat rotor fully.
- Seat cap squarely; do not trap wires.
- Reinstall wires exactly as photographed.
- Confirm cap screws snug, not overtightened.

### 2.4 Post-replacement test

Repeat Phase 0.1 and compare:


| Result                       | Meaning                                                     | Next                                                                  |
| ---------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------- |
| Idle becomes V8-smooth       | Caps/rotors were the root cause or a major contributor      | Log resolved, still inspect plug wells/boots during valve-cover job   |
| Improvement but still uneven | Caps/rotors were contributing, but another weakness remains | Continue Phase 3, starting with wires/boots and cylinder localization |
| No change                    | Caps/rotors likely not the root cause                       | Continue Phase 3 using the Phase 1 localization data                  |
| Worse                        | Installation/routing error until proven otherwise           | Stop, verify firing order/routing/cap seating/rotor seating           |


---

## Phase 3 — If Rough Idle Remains

Use the Phase 1 pattern to choose the branch. Do not run all branches blindly.

### Branch A — One cylinder weak

Order of checks:

1. Recheck that cylinder's plug wire seating and resistance.
2. Inspect plug boot for oil tracking, cracks, or loose resistor end.
3. Use inductive timing light on that wire.
4. Pull and inspect that spark plug if the wire/boot is suspect or the runner is cold.
5. Listen to that injector.
6. If spark is steady and injector clicks, do compression test on all 8, not just the suspect cylinder.
7. If compression is low, follow with leakdown to separate rings, intake valve, exhaust valve, or head gasket.

Likely root causes:

- Oil-contaminated plug boot from leaking tube seals.
- High-resistance/open plug wire.
- Bad plug despite being new.
- Dirty/stuck injector.
- Mechanical compression issue, lower probability given current engine-health evidence.

### Branch B — One bank weak

Order of checks:

1. Recheck cap/rotor installation on that bank.
2. Compare plug-wire resistance on the weak bank vs the other bank.
3. Inspect that bank's cap towers and coil lead.
4. Check for bank-local vacuum leak: intake boot, manifold area, breather hose, injector seals.
5. If ignition and air checks pass, consider KE fuel distributor / injector delivery imbalance.

Likely root causes:

- Cap/rotor/coil path issue.
- Multiple aged wires/boots on one bank.
- Intake/vacuum leak affecting one side more than the other.
- Fuel distribution imbalance.

### Branch C — Random multi-cylinder roughness

Order of checks:

1. Verify charging voltage at idle. Low voltage can weaken idle control and ignition reserve.
2. Inspect main engine grounds and coil grounds.
3. Check idle air control behavior and hoses.
4. Smoke-test intake tract: taped intake hose, breather hoses, injector seals, brake booster line, vacuum fittings.
5. Perform KE-Jetronic duty-cycle / lambda correction check. Do not adjust mixture until vacuum leaks and ignition faults are ruled out.
6. Check fuel system pressure only if duty-cycle behavior or drivability points there.

Likely root causes:

- Vacuum leak / unmetered air.
- Idle air control fault.
- KE mixture correction at limit.
- System/control pressure issue.
- General secondary ignition weakness.

### Branch D — Smooth above idle, rough only at loaded idle

Order of checks:

1. Verify idle speed target hot in P/N and D.
2. Check idle air control valve and hoses.
3. Smoke-test intake.
4. Check engine/trans mounts only after incomplete combustion is ruled out. Mounts can amplify a rough idle, but should not create a missing-cylinder signature.

Likely root causes:

- Idle-control reserve issue.
- Vacuum leak.
- Marginal ignition that only shows under low-speed/high-load conditions.
- Mounts as amplifier, not primary cause.

---

## Decision Matrix


| Evidence                                         | Most likely area             | Next action                                      |
| ------------------------------------------------ | ---------------------------- | ------------------------------------------------ |
| One cold runner + irregular timing-light flash   | Ignition to that cylinder    | Wire/boot/plug/cap tower                         |
| One cold runner + steady flash + injector silent | Fuel injector                | Injector electrical/mechanical check             |
| One cold runner + steady flash + injector clicks | Fuel spray or compression    | Plug check, compression/leakdown                 |
| Four cylinders on one cap path affected          | Cap/rotor/coil/path          | Recheck distributor install, coil lead, cap      |
| All runners similar, idle still rough            | Idle/mix/mount amplification | Vacuum/ICV/KE duty cycle, then mounts            |
| Idle fixed by caps/rotors                        | Distributor parts confirmed  | Log resolved; continue planned tube-seal service |
| Idle improved but not fixed                      | Multiple contributors        | Continue with wires/boots and vacuum leaks       |


---

## What Not To Do Yet

- Do not adjust KE mixture screw before ignition and vacuum leaks are ruled out.
- Do not replace injectors as a set without first identifying fuel-side evidence.
- Do not replace coils/EZL based only on rough idle.
- Do not treat engine mounts as the cause if a cold-runner, missing-flash, or fuel smell signature exists.
- Do not run a compression test first unless Phase 1 clearly points to one cylinder and spark/fuel checks do not explain it.

---

## Logging Template

Create a dated diary entry for each session:

```text
Date:
Ambient temp:
Engine state: cold / warm / fully hot
Fuel level:
Symptoms:
Codes:
Cylinder heat results:
Wire resistance results:
Timing-light results:
Parts changed:
Before/after idle verdict:
Next branch:
```

---

## Current Next Step

Before new caps/rotors arrive:

1. Run Phase 0 baseline.
2. Run Phase 1.1 visual inspection.
3. If tools are available, run Phase 1.2 wire resistance and Phase 1.3 heat comparison.

When caps/rotors arrive:

1. Execute Phase 2 as a controlled replacement.
2. Decide next branch from the before/after result.

