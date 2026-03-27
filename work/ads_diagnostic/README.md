# ADS I System Diagnostic — Full Status Assessment

## Overview

The 1991 Mercedes-Benz 500 SL (R129) — AOK912 (manufactured 09/1991, possibly MY1992 spec) is equipped with ADS I (Adaptive Damping System, first generation). The car drives well and the ride is comfortable ("floating"), confirming the base mechanical springs and nitrogen accumulators are functional. The ADS control module (N51) is **alive and communicating** — returns 1 blink (no stored fault codes) with battery >13V. Both switches work: ADS console switch LED illuminates and turns RED in Sport mode; Fahrzeugniveau (level) switch LED illuminates. ABS warning lamp is confirmed functional. **The tandem pump ADS section IS working** (confirmed 2026-03-26 — reservoir level dropped ~2/3 after engine start). Running the air-starved circuit triggered a fault code and N51 shut down. **2026-03-27: Pin 9 read returned code 14 (steering angle sensor not initialized) — soft fault from the shutdown, not hardware damage. Clear and re-initialize, then proceed with Phase 1 flush.**

**IMPORTANT — Manual Discovery (2026-03-23):** We had been referencing the **1990** owner's manual, but the car is a **1991** model. The 1991 manual (now downloaded) reveals major differences: ADS, ASR, ASD, and the snow chain switch were all added for 1991. Critically, **the 1991 manual confirms ADS has a dedicated instrument cluster warning lamp** (page 92: "The indicator lamp comes on with the key in steering lock position 2 and goes out when the engine is running"). Our earlier conclusion that "ADS was never in the standard R129 indicator set" was wrong — it was based on the 1990 manual which predates ADS. **The original "missing lamp" observation may have been the ADS warning lamp.** Needs verification during ignition-ON bulb check.

**CAVEAT — US Manual vs European Car:** The English manuals (1990/1991/1992) are **US-market** editions. AOK912 is European-spec. Key differences: the US cluster shows "BRAKE" text (Euro uses symbol), "CHECK ENGINE" far right (California-only — correctly absent from Euro), and mph speedometer. The German Betriebsanleitung 1991–1993 (`r129-betriebsanleitung-1991-1993-DE.pdf`) covers all three model years in one document (image-only, no extractable text) and its cluster diagram is a **perfect match** to the actual cluster — confirming the European reference.

**Model Year Note:** AOK912 was manufactured 09/1991 and may be MY1992 spec. The 1992 US manual has been downloaded and compared — the ADS section (page 94) is **word-for-word identical** to the 1991 manual (page 92). Same indicator lamp list, same dashboard layout, same ADS cluster lamp description. The German manual covers 1991–1993 in one document. **Conclusion: whether the car is MY1991 or MY1992, the ADS cluster warning lamp should be present.**

The electronic diagnostic is complete — N51 is healthy, no fault codes, both switches work. The remaining work is mechanical/hydraulic: restore the level control system (Phase 1: flush + filter), replace the blown Front Right accumulator sphere, and investigate the missing cluster warning lamp.

## Current Known Status


| Observation                                                          | Source                                     | Date       |
| -------------------------------------------------------------------- | ------------------------------------------ | ---------- |
| ADS switch on center console identified; ~~non-functional~~ **CORRECTION: switch works — LED illuminates with ignition, turns RED in Sport/up position (tested 2026-03-23 with adequate voltage)** | Pre-purchase inspection / re-test 2026-03-23 | 2026-03-13 |
| ~~ADS warning lamp dead~~ ~~False alarm~~ **RE-OPENED: 1991 manual confirms ADS has a cluster lamp — original observation may be correct** | Ferry transit / 1991 manual discovery 2026-03-23 | 2026-03-13 |
| Comfortable "floating" ride at highway speed; accumulators not blown | 700 km shakedown (Vellinge → Kapellskär)   | 2026-03-13 |
| Rear sits lower than front (1–2 finger gap rear vs. 3 finger front)  | "Sag test" on ferry deck                   | 2026-03-14 |
| Rear did NOT rise when engine started (~~expected — car has no SLS~~ **now understood: car HAS level control, but reservoir nearly empty = system cannot raise**) | Ferry deck observation                     | 2026-03-14 |
| Bounce test passed — firm but not rock-hard or oscillating           | Manual suspension test                     | 2026-03-14 |
| ADS confirmed in mechanical failsafe / limp mode                     | Aggregate diagnosis                        | 2026-03-14 |
| X11 Pin 9 (ADS): weak static glow, no blink pulses, cannot clear     | Blink-code sweep (ignition ON, engine OFF) | 2026-03-18 |
| X11 Pin 9 (ADS): **1 blink (no faults)** — module communicating      | Blink-code re-test (battery >13V)          | 2026-03-23 |
| ~~ADS console switch LED stays off (engine on and off); no mode change~~ **CORRECTED: both night illumination AND red Sport indicator work with adequate voltage. Switch turns RED in Sport/up position.** | Console switch re-test (battery >13V) | 2026-03-23 |
| **Fahrzeugniveau switch (position 2, left panel):** CONFIRMED PRESENT. LED illuminates with ignition. Pressing UP (Raised Level) has **NO EFFECT on ride height** with engine running. | Level switch test 2026-03-23 | 2026-03-23 |
| **ADS hydraulic reservoir below MIN** — level dropped only ~0.5cm since 2026-03-17. MAX/MIN markings deep inside canister (hard to read). No active leak found anywhere. Fluid loss is gradual/historical. Confirms this IS the ADS/Niveauregulierung reservoir (not coolant). | Visual inspection 2026-03-23 | 2026-03-23 |
| Pin 11 or 12 re-tested with >13V — still static glow (not alive)    | Blink-code sanity check                    | 2026-03-23 |
| Front Right suspension significantly stiffer than Front Left         | Manual suspension test (>24h idle)         | 2026-03-22 |
| Rear suspension compresses more than front, but does not oscillate   | Manual suspension test (>24h idle)         | 2026-03-22 |


**Working hypothesis (revised 2026-03-23):**

The **entire ADS electronic system is functional** — module (N51), console switch, and Fahrzeugniveau switch all work with adequate voltage (>13V). The problem is purely mechanical/hydraulic.

**Confirmed issues (updated 2026-03-26):**

1.  **~~Level control inoperative — ADS pump section not circulating fluid.~~** **PUMP IS ALIVE (confirmed 2026-03-26).** Quick pump test: topped reservoir to MAX, started engine — fluid level dropped ~2/3 of the MAX-to-MIN range. The tandem pump ADS section IS drawing and circulating fluid. The system was simply starved/air-locked from years of low fluid. **However:** running the air-contaminated circuit triggered a fault code — N51 shut down the system (both switch LEDs went dark, could not be re-illuminated even in ignition-ON bulb check). **→ NEXT: read Pin 9 blink codes, clear faults, top up reservoir, re-bleed. Full Phase 1 flush still recommended to purge air and old fluid.**
2.  **Front Right accumulator sphere hydro-locked.** Confirmed 2026-03-22 — rock-hard, zero travel. N51 cannot detect this (purely mechanical). **Possible improvement observed 2026-03-26:** left/right suspension stiffness difference felt smaller after engine run (subjective). **→ Phase 2: replace front pair (A 129 320 01 15).**
3.  **ADS cluster warning lamp missing — likely cluster swap (updated 2026-03-26).** Photo of the indicator strip shows **no ADS symbol at all** to the left of ASR — not even a dead-fronted print. All other indicators (ASR, seatbelt, oil, etc.) have clearly visible strip symbols even unlit. A pulled bulb would leave the printed symbol visible; the complete absence of the symbol means the **strip itself is a non-ADS variant**. Combined with the Fahrzeugniveau switch and option 211 confirming the car IS factory ADS-spec, this points to a **cluster swap from a non-ADS R129** — likely done during the 16-year previous ownership (cheapest fix for a failed speedometer/odometer/gauge). This means the oil-level float warning has NEVER worked since the swap — explaining why chronic low fluid went unnoticed. **Odometer accuracy is now in question.** **→ Phase 3: pull cluster, read part number, confirm ADS vs non-ADS variant.**
4.  **ADS fault code identified and understood (2026-03-27).** After pump test drew air-contaminated fluid through the circuit, N51 stored a fault and shut down — both switch LEDs dark, system unresponsive. **Pin 9 read (2026-03-27): code 14 = steering angle sensor (N49) not initialized.** This is a soft calibration fault from the unexpected shutdown, not hardware damage. **→ NEXT: clear code via Pin 9, start engine, turn steering full lock L → R → center to re-initialize. Then proceed with Phase 1 flush.**
5.  **Cluster swap — historical analysis (2026-03-26, updated 2026-03-27 with Swedish records).** The previous owner had the car for 16 years (2008-07-24 → 2024-04-23, confirmed via [biluppgifter.se](https://biluppgifter.se/fordon/AOK912)). Swedish inspection odometer readings from 2013–2026 are smooth and consistent (~200–900 km/year, classic seasonal summer car in Skåne). No jumps or drops in that period. The 1991–2012 readings are not available on biluppgifter.se (platform data limitation — Sweden recorded odometer at inspections since at least 1993, but older records are not surfaced publicly). If the cluster swap happened, it was **before 2013** — most likely before the 2008 owner acquired the car (2002–2008 ownership or earlier). The dealer (2024) invested heavily in cosmetics (new MB OEM soft top, interior trim, polish) and fluid levels, but the ADS cluster lamp was already missing — the non-ADS cluster has no oil-level warning position, so chronic low fluid was invisible. Full Swedish records analysis in Engineering Diary.

## ADS I System Architecture (Reference)

**CRITICAL DISTINCTION — ADS I Has TWO Independent Subsystems:**

The European "Niveauregulierung mit adaptivem Dämpfungs-System (ADS)" on the early R129 (1990–1995) is actually **two largely independent subsystems** sharing the "ADS" name. They have different control methods, different diagnostics, and different failure modes:

### Subsystem A: Adaptive Damping (Electronic — monitored by N51)

Controls shock absorber stiffness via electronic solenoid valves. This subsystem IS monitored by the ADS control module (N51) and DOES report faults via X11 Pin 9 blink codes.

- **ADS Control Module (N51)** — located in the right-side engine bay module box (E-box) near the firewall. Receives inputs from sensors and driver switch; commands the shock absorber solenoids.
- **ADS Console Switch** — center console rocker/button: Sport / Comfort mode selection. Sends a ground signal to N51. **Status: WORKING** — LED illuminates, turns RED in Sport/up position (confirmed 2026-03-23).
- **Speed Sensor Input** — N51 receives vehicle speed from the speedometer or ABS controller.
- **Steering Angle Sensor** — input for dynamic damping adjustment.
- **4× ADS Shock Absorbers** — each contains a proportional solenoid valve that adjusts damping force. Solenoid coil resistance is typically 4–8 Ω. Each shock also contains a nitrogen-charged gas cushion (accumulator sphere). **Front Right sphere is ruptured/hydro-locked** — invisible to N51.
- **ADS Warning Lamp** — cluster warning lamp for damping faults (page 92: *"The indicator lamp comes on with the key in steering lock position 2 and goes out when the engine is running"*). **Status: MISSING from indicator strip** — either dead bulb behind dead-fronting, or cluster variant issue.
- **Diagnostic Output** — X11 Pin 9 blink-code interface (pre-OBD). Requires >13V supply. **Returns 1 blink = no stored damping faults.**

### Subsystem B: Niveauregulierung / Level Control (Mechanical/Hydraulic — NOT monitored by N51)

Controls ride height via a hydraulic system. On ADS I, height sensing is **MECHANICAL** (not electronic) — there are no electronic ride height sensors. This subsystem is **NOT monitored by the ADS module (N51)** and produces **NO fault codes on Pin 9.** The entire level control system can be completely dead and Pin 9 will still report "1 blink = all good" because N51 only monitors damping.

*(Note: ADS II (1996+ R129) upgraded to electronic ride height sensors and integrated level control monitoring into the module. ADS I does not have this.)*

- **Fahrzeugniveau-Einstellung (Vehicle Level Switch)** — position 2 on left instrument panel (next to headlight switch, replaces headlight range adjuster on ADS cars). Controls ride height set point with its own indicator LED. **Status: PRESENT and LED illuminates (confirmed 2026-03-23). No effect on ride height when activated.**
  - **Down = Normales Niveau (Normal Level):** Default. Above ~120 km/h, auto-lowers ~15mm.
  - **Up = Erhöhtes Niveau (Raised Level):** For poor roads. LED illuminates. Below ~50 km/h, raises ~30mm. Auto-reverts to Normal at 120 km/h.
- **Hydraulic Tandem Pump (A 129 460 07 80)** — engine-driven (belt), mounted on the M119. ONE pump with TWO internal sections sharing one drive shaft:
  - Section 1 = Power Steering (draws from metal canister) — **WORKING** (brown/aged fluid, steering assisted)
  - Section 2 = Niveauregulierung (draws from plastic reservoir next to washer fluid) — **NOT WORKING** (clear/un-aged fluid = no circulation for years)
  - Rebuilt pumps: ABCspecialist (NL), ~€850 + old core return
- **ADS/Niveauregulierung Reservoir** — translucent plastic, next to washer fluid bottle. Fluid: MB 343.0 / ZH-M (part number 000 989 91 03). **Level is below MIN. No active leak. Fluid is clear (stagnant).**
- **Rear Level Control Valve (A 129 320 00 58 / A 129 320 08 58)** — hydraulic proportioning valve, mounted mid-rear-axle. Height sensing is MECHANICAL: a **linkage from the rear anti-roll bar** mechanically operates the valve's lever arm. As load changes rotate the ARB, the valve directs fluid to raise or lower the car. **No electronic sensors involved.**
- **Anti-Roll Bar Linkage** — the "sensor" of ADS I level control. A plastic/metal rod connecting the ARB to the proportioning valve lever. Known failure point: shears at lower mounting. If broken, the valve stays in one position and cannot adjust height. **This failure produces NO electronic fault codes.**
- **Hydraulic Lines** — from the pump to the valve block, and from the valve to the rear hydraulic struts.
- **Oil Level Warning** — the reservoir likely has a float sensor wired directly to the cluster warning lamp (the same missing ADS lamp). This warning is independent of N51 — it does not generate a blink code.

### Why Pin 9 = "1 Blink" Despite a Dead Level Control

The ADS module (N51) monitors ONLY Subsystem A (damping solenoids, speed sensor, steering sensor, console switch). The level control (Subsystem B) is a separate mechanical/hydraulic loop with no electronic feedback to N51. A failure in any of these level control components produces **zero fault codes**:
- Empty reservoir → no code
- Air-locked pump section → no code
- Failed pump ADS section → no code
- Broken ARB linkage → no code
- Seized proportioning valve → no code
- Broken hydraulic line → no code

The ONLY electronic indicator for level control problems is the **cluster warning lamp** (oil level float sensor) — which is **missing from this cluster.**

## Diagnostic Plan

### Completed Phases (reference — no further action)

<details>
<summary><b>Phase 1: Visual Checks & Module Communication — COMPLETED 2026-03-23</b></summary>

All steps completed with battery >13V:

- **1.1 — ADS Console Switch** — DONE. Switch clicks, LED illuminates, turns RED in Sport. Works correctly.
- **1.1b — Fahrzeugniveau Switch** — DONE. Present at position 2 (left panel). LED illuminates in UP position. Switch is original ADS-spec.
- **1.2 — Cluster Warning Lamp** — DONE (visual). ADS lamp is MISSING from indicator strip. ABS lamp works. Needs cluster pull to investigate further (see Phase 4 below).
- **1.3 — Blink-Code (Pin 9)** — DONE. Module alive, returns 1 blink = no stored faults. Requires >13V to communicate.
- **1.4 — Under-Hood Visual** — Not yet performed (solenoid connectors on front strut towers). Low priority since module reports no solenoid faults.

</details>

<details>
<summary><b>Phase 2: Fuse & Power — PARTIALLY DONE, remainder deprioritized</b></summary>

Module communicates and reports healthy, so power supply is confirmed adequate. Remaining steps are reference only if a regression occurs.

- **2.1 — ADS Fuse** — Not checked individually. Moot point: module has power (it communicates).
- **2.2 — OVP Relay Fuse** — DONE (2026-03-22). 10A fuse is intact. Full relay test deferred (module is alive, OVP is not the issue).
- **2.3 — Module Power & Ground** — Skipped. Module communicates at >13V = power path is intact.

</details>

<details>
<summary><b>Former Phase 4: Module Communication & Signal Testing — COMPLETED / SUPERSEDED</b></summary>

These steps were written when the module was presumed dead. Now that N51 communicates and both switches work, they are resolved:

- **4.1 — Blink-Code Engine Running** — DONE. 1 blink, no faults.
- **4.2 — Console Switch Signal** — DONE. Switch LED responds to module (turns RED in Sport). N51 is driving the switch correctly.
- **4.3 — Diagnostic Output Pin** — DONE. Pin 9 produces clean blink pulses (not the earlier "weak static glow" which was a voltage issue).
- **4.4 — Speed Sensor** — Not measured directly, but speedometer works and module reports no faults. Low priority.

</details>

---

### Active Phases (in priority order)

### Phase 1: Hydraulic Flush, Filter Replacement & Pump Test (NEXT ACTION)

*Added 2026-03-23. This is the cheapest and most likely fix for the inoperative level control. A clogged suction filter (A 129 327 00 91, ~€7–11) can completely starve the ADS pump section even though the pump physically spins. Combined with a full fluid flush, this test will definitively prove whether the tandem pump's ADS section is alive or dead — before spending €850 on a rebuilt pump.*

**References:**
- MBWorld R129 ADS Fluid Change thread (MB-Dude / Jeff's procedure): https://mbworld.org/forums/sl-class-r129/500408-ads-fluid-change.html
- Rodionenkin.de Ölwechsel Zentralhydraulik (W124/W126/R129): https://www.rodionenkin.de/de/pages/mb-reparaturanleitungen/oelwechsel-zentralhydraulik-asd-niveauregulierung.php
- Classic Jalopy SLS Flush (W126, same system): https://www.classicjalopy.com/2019/09/mercedes-self-leveling-rear-suspension-flush/
- MercedesSource SLS Flush Video ($12.99 or free with kit): https://mercedessource.com/store/replacing-the-fluid-a-self-leveling-rear-suspension-sls-demand-video

**Tools & materials:**
- Brake cleaner (have)
- Transparent PVC hose, 6–8mm inner diameter, ~1m
- Waste oil container (e.g. empty milk jug / bottle)
- Lint-free cloth (have)
- 4L fresh ZH-M / MB 343.0 fluid (have 1L Febi 02615 — **need 3L more**)
- New filter element: **A 129 327 00 91** (or clean old one with denatured alcohol / brake cleaner, outside→inside)
- Old syringe or turkey baster (to extract remaining old fluid from reservoir)

**Phase A — Open-Loop Flush (purge old fluid):**

1. Warm up the engine, activate the Fahrzeugniveau switch up/down a couple of times, then turn off the engine.
2. Clean the reservoir cap and return line fitting with brake cleaner.
3. Remove the reservoir cap.
4. Disconnect the return line at the top of the reservoir. Attach transparent PVC hose to the return line fitting, route into waste container.
5. Remove the sieve/filter element from the reservoir (unscrew counterclockwise). Inspect — if clogged with dark debris, **this may be the root cause.**
6. Using a syringe/turkey baster, withdraw as much old fluid from the reservoir as possible. Wipe the reservoir interior with a lint-free cloth, especially the bottom (sediment).
7. Fill the reservoir with fresh ZH-M (OK to overfill slightly, but not to the brim).
8. Have an assistant start the engine (or do it yourself — the flow rate at idle is slow enough for one person). The pump pushes old fluid out through the return hose into the waste container.
9. **CRITICAL: Keep the reservoir topped up.** Never let it run dry — air ingestion will make things worse. Add fresh fluid continuously as the level drops.
10. With engine idling, activate the Fahrzeugniveau switch UP at least twice — this forces fluid through the level control circuit specifically, not just the power steering loop.
11. Continue until the fluid coming out of the return hose is **clear** (matching fresh ZH-M). Typically takes 3–4L.
12. Turn off the engine.

**Phase B — Close Loop & Pump Test (the critical diagnostic moment):**

1. Clean the filter element with brake cleaner or denatured alcohol (spray/soak from outside to inside, let dry completely) — or install the new filter (A 129 327 00 91).
2. Reinstall the filter in the reservoir.
3. **Reconnect the return line.** The hydraulic loop is now closed.
4. Top up the reservoir to MAX with fresh ZH-M. **Mark the level with a pen/tape on the outside of the reservoir.**
5. Start the engine. Press the Fahrzeugniveau switch to UP (Raised Level).
6. Let the engine idle for 5–10 minutes. **Watch the reservoir level:**
   - **Level DROPS** = fluid is being drawn into the rear circuit = **ADS pump section is working!** The pump had simply lost prime or the filter was clogged. Keep topping up as air purges from the lines. The car should begin to rise at the rear.
   - **Level STAYS STATIC** = the ADS pump section is NOT building pressure. Internal failure (worn vanes/seals). Tandem pump replacement needed (**A 129 460 07 80**, ~€850 rebuilt).
7. Turn off engine. Final fluid level check — top up to MAX with level control in Normal position.
8. If the car rose: drive slowly (<50 km/h) for a few minutes, return, and re-check level. Top up as needed. The system may self-bleed over several drive cycles.

**Expected outcome for AOK912:** The fluid has been stagnant (clear) for years. Most likely scenario:
- **(a) Clogged filter** blocked suction → flush + new filter restores flow → **cheapest fix (~€7)**
- **(b) Air-locked circuit** from running low on fluid → flush + top-up restores prime → **cost of fluid only**
- **(c) Internal pump failure** → level stays static after flush → pump replacement needed → **~€850**

### Phase 2: Mechanical Inspection Under Car (after flush proves pump status)

*Do this with the car on a lift or jack stands, regardless of Phase 1 outcome.*

- **2.1 — Rear Level Control Valve & Linkage**
  - Locate the **rear level control valve** (hydraulic proportioning valve) mounted approximately in the middle of the rear axle area.
  - Trace the **linkage from the rear anti-roll bar** to the proportioning valve lever arm.
  - **CHECK FOR SHEARED LINKAGE:** Known ADS I failure. The plastic linkage part can shear at the lower mounting, causing the system to lose rear ride height completely. A MBClub UK user with a 1992 500SL had this exact failure.
  - Inspect hydraulic lines from the rear shocks to the valve for leaks, kinks, or disconnection.
  - *Pass criteria:* Linkage intact and securely connected at both ends, no hydraulic leaks.
- **2.2 — Accumulator Sphere Condition**
  - Front Right is confirmed hydro-locked (2026-03-22). Assess the other three corners by manual compression test after >24h standing.
  - *Pass criteria:* Shock compresses under body weight and returns without bouncing.
  - *Known result:* Front Left OK, Rear Left/Right compress but sag more than front.
- **2.3 — Shock Absorber External Inspection**
  - Visually inspect all four ADS shocks for oil leaks, dented bodies, or damaged solenoid connectors.
  - Check solenoid connector pins for corrosion.
  - *Pass criteria:* No external oil weep, connectors clean and dry.
- **2.4 — Spring Pad Assessment (only if hydraulic system is restored and rear still sits low)**
  - Measure ride height at all four corners (wheel arch to center of hub).
  - Compare to factory spec (~380–390mm front, ~375–385mm rear).
  - If rear is still low with working level control AND intact linkage, inspect rubber spring pads (nubs 1–4).

### Phase 3: Cluster Pull & ADS Warning Lamp (important — confirms cluster swap theory)

**Updated 2026-03-26:** Photo analysis of the indicator strip shows **no ADS symbol at all** in the position to the left of ASR. All other indicator symbols (ASR, seatbelt, oil, etc.) are clearly visible even when unlit. A pulled bulb would leave the printed symbol visible — the complete absence of the symbol confirms the indicator strip is a **non-ADS variant**. This strongly indicates a **cluster swap from a non-ADS R129** during the car's history. Pulling the cluster will confirm this and reveal odometer implications.

- **3.1 — Pull Cluster & Confirm Cluster Swap**
  - Confirmed by 1991/1992 manuals + German manual: ADS has a dedicated cluster lamp. A MBClub UK 1991 500SL confirms it illuminates during bulb check.
  - Photo evidence (2026-03-26): blank area where ADS symbol should be — not dead bulb, but missing symbol on strip.

  **Cluster Removal Procedure:**
  1. Turn ignition OFF and remove key.
  2. Extend steering wheel fully away and to lowest position. No steering wheel removal needed.
  3. Insert cluster removal hooks (tool **140 589 02 33 00**, or fabricate from a 90° pick with ~3mm toe) into both sides, about 7–8 cm deep.
  4. Twist each hook 90° so toes point inward — they engage toothed plastic molding on the rear housing.
  5. Pull firmly and evenly. If stuck, work a credit card with WD-40 around the 4 rubber bumper locations.
  6. Tilt cluster out between steering wheel and upper dash pad.
  7. Disconnect 4 connectors: 2 round (grab body and pull) + 2 square (pull by harness — normal).

  **Cautions:**
  - Do NOT use shallow hook placement (~1 cm) — this can **crack the lens**.
  - Mechanical drum odometer — disconnecting will NOT affect mileage.

  **Inspection Checklist:**
  1. **Part number** on rear housing label — cross-reference for ADS variant. If part number does NOT match ADS-equipped R129, cluster swap is confirmed.
  2. **Indicator strip** — confirm ADS symbol position is absent (already observed from outside). If strip lacks ADS, it is a non-ADS strip.
  3. **Bottom row bulbs** — count populated/empty sockets. Non-ADS cluster will have fewer sockets.
  4. **Odometer reading** — note the reading. Compare against service records and Swedish public records for mileage plausibility.
  5. **Options:** (a) Source correct ADS cluster (used), (b) swap indicator strip only if mechanically compatible, (c) add a standalone ADS warning LED wired to N51.
  5. **While it's out** — replace ALL indicator bulbs with fresh W1.2W wedge bulbs (34 years in service).

  **Reinstallation:** Reverse of removal. After reconnecting, ADS lamp may stay on until engine started and steering wheel turned full left → full right → center (per 1991 manual page 92).

### Phase 4: Solenoid Testing (only if N51 reports faults after Phases 1–2)

N51 currently reports 0 faults on Pin 9. These tests are needed only if new fault codes appear after restoring the hydraulic system, or if ride quality does not improve.

- **4.1 — Solenoid Coil Resistance (all 4 corners)**
  - Disconnect 2-pin connector from each ADS shock solenoid.
  - Measure resistance: expected 4–8 Ω. Open (∞) or short (~0 Ω) = shock replacement needed.

| Corner      | Resistance (Ω) | Status |
| ----------- | -------------- | ------ |
| Front Left  |                |        |
| Front Right |                |        |
| Rear Left   |                |        |
| Rear Right  |                |        |

- **4.2 — Solenoid Wiring Continuity (harness to module)**
  - Measure continuity from each solenoid connector pin back to N51 module connector.

### Phase 5: Final Assessment & Decision

- **5.1 — Compile Results**
  - After Phases 1–4, the confirmed issues are:

  | Issue | Status | Fix |
  | ----- | ------ | --- |
  | ADS pump section not circulating | Phase 1 will determine: clogged filter / air lock / dead pump | €7 filter → €45 fluid → €850 pump |
  | Front Right sphere hydro-locked | Confirmed 2026-03-22 | Replace front pair: A 129 320 01 15 (~€100–150 each) |
  | ADS cluster warning lamp missing | Confirmed 2026-03-23 | Pull cluster, inspect socket, replace bulb (Phase 3) |
  | Rear level control linkage | Unknown — inspect in Phase 2 | If sheared: cheap plastic/metal rod replacement |

- **5.2 — Decision: Repair or Bypass**
  - **Repair** (recommended — electronics work, only mechanical issues remain):
    - Phase 1 flush + filter may restore level control for ~€50.
    - Front sphere pair replacement restores FR ride quality for ~€200–300.
    - Cluster lamp is cosmetic.
  - **Intentional bypass** (only if pump is dead AND rebuilt pump is uneconomical):
    - Convert to conventional Bilstein B4/B6 shocks and delete ADS. Document the conversion.
  - **Module replacement** — NOT NEEDED. N51 is alive and healthy.

## Parts & Tools Needed

**Phase 1 — Hydraulic Flush (NEXT ACTION):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| ZH-M / MB 343.0 Hydraulic Fluid (4L total) | Flush + top-up. Part no. 000 989 91 03. | **1L Acquired ✓ (Febi 02615) — need 3L more** |
| Hydraulic Suspension Filter (A 129 327 00 91) | Suction filter — prime suspect for blocked pump. ~€7–11. | **Needed** |
| Transparent PVC Hose (6–8mm ID, ~1m) | Open-loop flush — return line to waste container. | **Needed** |
| Brake cleaner | Cleaning reservoir cap and return line fitting. | Acquired ✓ |
| Syringe / turkey baster | Extract old fluid from reservoir. | Acquired ✓ (MTX 500ml) |
| Lint-free cloth | Wipe reservoir interior (sediment). | Acquired ✓ |

**On hand (diagnostic tools):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| Multimeter (Owon HDS242) | Voltage, resistance, continuity | Acquired ✓ |
| Oscilloscope (Owon HDS242) | Signal waveform analysis (Phase 4, if needed) | Acquired ✓ |
| 12V LED blink-code reader | X11 Pin 9 diagnostics | Built ✓ |

**Later phases (not blocking):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| Cluster removal hooks (140 589 02 33 00) or DIY 90° pick | Pull instrument cluster (Phase 3) | Needed (can fabricate) |
| W1.2W / W2W wedge bulbs | ADS cluster lamp + spares (Phase 3) | Needed |
| Front Accumulator Spheres x2 (A 129 320 01 15) | Replace hydro-locked FR + pair FL (Phase 2) | Needed |


## Related Work Items

- ADS Blink-Code Reader (tool & results) → [work/ads_blink_reader/](../ads_blink_reader/README.md)
- Blink-Code Channel Inventory → [work/ads_blink_reader/blinker_report.md](../ads_blink_reader/blinker_report.md)
- Suspension Refresh (mechanical) → [Engineering Diary Task #4](../../docs/AOK912%20Engineering%20Diary.md)
- nRF5430 Interface Board (digital diagnostic tool) → [work/nRF5430_interface_board/](../nRF5430_interface_board/)
- Baseline Service → [work/baseline_service/](../baseline_service/README.md)

## Diagnostic Log

*Record findings from each phase here as work progresses.*

| Date       | Phase | Step                | Finding                               | Action                   |
| ---------- | ----- | ------------------- | ------------------------------------- | ------------------------ |
| 2026-03-13 | —     | Initial inspection  | ADS switch identified, non-functional | —                        |
| 2026-03-13 | —     | Highway observation | Warning lamp missing from cluster     | ~~Suspect ADS bulb removed~~ ~~Revised 03-23: missing lamp is ABS, not ADS~~ **Re-revised: 1991 manual confirms ADS HAS a cluster lamp — original observation may be correct** |
| 2026-03-14 | —     | Sag test            | Rear low, no height change on start   | ~~Confirmed limp mode~~ ~~Revised: car has no SLS — rear low is spring sag / pad wear~~ **Re-revised: German manual confirms Euro ADS I HAS level control (Niveauregulierung). Low rear likely hydraulic level control failure (sheared linkage / low fluid / failed pump).** |
| 2026-03-18 | 4     | Pin 9 blink-code    | Weak static glow, no pulses           | Module not communicating |
| 2026-03-22 | 2     | 2.2 OVP Fuse Check  | 10A fuse inside OVP relay is intact   | Need to test relay power |
| 2026-03-22 | —     | Manual Suspension Test | Front Right is rock hard (almost zero travel under body weight). Front Left compresses. Rear compresses. | Confirms Front Right nitrogen accumulator (sphere) is ruptured/hydro-locked. Front Left sphere is intact and likely defaulting to failsafe firm. |
| 2026-03-23 | 1/4   | 1.3 / 4.1 Pin 9 re-test | **ADS module alive!** Battery >13V (vs. <12V on 03-18). Pin 9 returns **1 blink = no stored faults.** | Module communicating and reports healthy. Previous "static glow" was insufficient supply voltage. Revised hypothesis: electronics OK; ride issue is mechanical (blown sphere). |
| 2026-03-23 | 1     | 1.1 Console switch test | Switch LED stays off with engine on and off. No observable mode change. | Switch LED may be dead, or wiring between N51 and switch is broken. Module reports healthy via blink-code but does not drive the switch indicator. Needs back-probing (Phase 4.2). |
| 2026-03-23 | —     | Pin 11/12 sanity check | Re-tested one of the two (unsure which) with >13V — still static glow, not communicating. | ATA/IRCL module non-communication is NOT a voltage issue (unlike ADS). Genuine module fault or different root cause. Defer to later investigation. |
| 2026-03-23 | —     | Self-leveling analysis | ~~Confirmed via owner's manual + data card: ADS I (code 211) has NO self-leveling.~~ **OVERTURNED by German manual: European ADS I = "Niveauregulierung mit adaptivem Dämpfungs-System" — includes hydraulic level control.** US manual describes damping-only, but is wrong for Euro-spec cars. | ~~Rear low is spring sag / worn spring pads~~ **Hydraulic level control restored to Phase 6. Priority: check reservoir fluid level (engine bay, next to washer fluid), then inspect rear axle linkage.** |
| 2026-03-23 | 3     | Cluster analysis | ABS symbol **confirmed present** and **bulb functional** (illuminates on bulb check, extinguishes with engine). ABS system healthy. | ABS closed — no issue. |
| 2026-03-23 | —     | **1991 manual discovery** | Downloaded 1991 owner's manual (was using 1990 which predates ADS). **Major finding:** 1991 manual confirms ADS has a dedicated cluster warning lamp (page 13 + page 92). Also adds ASR, ASD indicators and snow chain switch not in 1990 manual. Dashboard item 22 changed from antenna switch to ADS switch. | **RE-OPENED warning lamp investigation.** The original "missing lamp" from the ferry may be the ADS indicator. Previous conclusion "ADS not in standard indicator set" was based on wrong-year manual. Check for ADS lamp on next ignition-ON bulb check. |
| 2026-03-23 | —     | Pin 7 identification | **Pin 7 "RB" = Roll Bar (Überrollbügel)**, NOT ABS. Confirmed via WIS documentation, BenzWorld, MBClub UK, Motor-Talk. Codes 2–7 were soft top / roll bar limit switch faults (cleared to 1 blink). | Pin 7 correctly labeled "RB" = Roll Bar. Roll bar system functional (codes cleared). |
| 2026-03-23 | —     | ABS diagnostic research | **ABS has NO blink-code diagnostic on the 16-pin X11 connector.** ABS output only available on 38-pin connector (1993+). Cluster warning lamp is the ONLY ABS diagnostic. ABS lamp confirmed working. | ABS diagnostic closed — lamp works, system healthy. |
| 2026-03-23 | —     | Pin 7 re-test | Pin 7 re-tested with >13V — returns 1 blink (still clear). Roll bar system healthy. | No action needed for roll bar. |
| 2026-03-23 | —     | US vs Euro manual analysis | **Both English manuals (1990/1991) are US-market editions.** AOK912 is European-spec. "CHECK ENGINE" indicator (visible in US manual diagram far right of strip) is California-only (page 93: "On-Board Diagnostic System — California models only"). Correctly absent from user's Euro cluster. "BRAKE" text in US diagram = brake symbol in Euro cluster. German Betriebsanleitung 1991–1993 downloaded but is image-only (no text extraction possible). | **CHECK ENGINE is NOT missing — never fitted to Euro cars.** Indicator strip layout differences are US vs Euro spec. ADS cluster lamp question remains open — needs ignition-ON bulb check. |
| 2026-03-23 | —     | **German manual translation — MAJOR CORRECTION** | Translated German Betriebsanleitung page 97: **"Niveauregulierung mit adaptivem Dämpfungs-System (ADS)"** = Level Control WITH Adaptive Damping System. Page describes: automatic vehicle level adjustment, optimal damper firmness, oil level warning lamp behavior, and oil reservoir. Also found oil level warning: "Ölstand Niveauregulierung zu niedrig" = oil level too low. | **OVERTURNS previous "no self-leveling" conclusion.** European ADS I INCLUDES hydraulic ride height control. System has: pump+reservoir in engine bay (next to washer bottle, fluid MB 343.0/ZH-M), rear proportioning valve with ARB linkage. Low rear likely caused by failed level control linkage (known shear point) or low/empty fluid. **Phase 6 hydraulic steps RESTORED.** |
| 2026-03-23 | —     | **Fahrzeugniveau switch discovery** | German manual page 98: **SEPARATE vehicle level switch** exists at position 2 on the left instrument panel (next to headlight switch). Replaces headlight range adjuster on ADS cars. Two modes: Normal (auto-lowers 15mm >120 km/h) and Raised (+30mm <50 km/h for poor roads). Has its own indicator LED. Speed-dependent: auto-reverts to Normal at 120 km/h. **CONFIRMED PRESENT on AOK912** — owner had mistaken it for an interior lighting switch (US manual ambiguity). | Switch present = car has full ADS/Niveauregulierung as built. Strengthens case that instrument panel is original (weakens cluster-swap theory). |
| 2026-03-23 | 1/6   | **Switch & reservoir re-test (engine running)** | **FINDINGS:** (1) ADS console switch LED **WORKS** — illuminates at night, turns **RED in Sport/up position.** Previous "dead LED" was low voltage. (2) Fahrzeugniveau switch LED **illuminates** with ignition. (3) Level switch UP has **NO effect on ride height** with engine running. (4) Hydraulic reservoir is **below MIN** — level dropped only ~0.5cm since 2026-03-17. **No active leak found.** (5) **CRITICAL CLUE: ADS fluid is CLEAR** while power steering fluid is brown/aged — strongly suggests the ADS pump has NOT been running (fluid not circulated). | Console switch does NOT need replacement. **Level control inoperative likely due to dead/unpowered pump** (not just low fluid). Clear fluid = stagnant = no pumping for years. **NEXT: listen for pump when level switch activated. If silent, check pump fuse/relay/power. Top up to MAX before further testing.** |
| 2026-03-26 | 1     | **Quick pump test (top-up, no flush)** | **PUMP IS ALIVE!** Topped reservoir to MAX, started engine. System started in Sport mode (red LED on, first time seen as default). Fahrzeugniveau switch LED on, toggled UP. **Reservoir level dropped ~2/3 of MAX-to-MIN range** — pump IS circulating fluid. No visible ride height change (circuit full of air). L/R suspension stiffness difference felt smaller (subjective). **FAULT TRIGGERED:** after first run, both switch LEDs went dark and could not be re-illuminated — not even during ignition-ON bulb check. System unresponsive on subsequent starts (~2min wait). N51 likely stored fault from air/pressure anomaly and entered full shutdown. | **Pump confirmed working — €850 rebuilt pump NOT needed.** System was starved/air-locked, not dead. Air in circuit triggered fault → N51 shutdown. **NEXT: (1) Read Pin 9 blink codes. (2) Clear faults. (3) Top up reservoir (level dropped significantly). (4) Proceed with full Phase 1 flush to purge air. (5) Re-test.** |
| 2026-03-27 | 1     | **Pin 9 blink-code read (post-pump-test)** | **14 blinks = Steering angle sensor (N49) not initialized.** Single fault code only. Soft fault — N51 lost steering angle calibration when it shut down during pump test air/pressure anomaly. Sensor hardware intact. | **Clear code via Pin 9 reset, start engine, turn steering full lock L → full lock R → center (re-initialization). If Pin 9 reads 1 blink after, system is clean. Proceed with Phase 1 flush.** |

