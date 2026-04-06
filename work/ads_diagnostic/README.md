# ADS I System Diagnostic — Full Status Assessment

## Overview

The 1991 Mercedes-Benz 500 SL (R129) — AOK912 (manufactured 09/1991, possibly MY1992 spec) is equipped with ADS I (Adaptive Damping System, first generation). The car drives well and the ride is comfortable ("floating"), confirming the base mechanical springs and nitrogen accumulators are functional.

**STATUS (2026-04-01): ADS SYSTEM ONLINE — OVP FIX CONFIRMED.**

The OVP relay was the root cause. After re-soldering all joints with Sn63/Pb37 (2026-03-31) and reinstalling (2026-04-01), N51 boots cleanly, both cabin ADS switches show red LEDs, and the diagnostic bus is stable. Pin 9 returns **fault code 14** (steering angle sensor N49 not initialized — expected after extended power loss). No other codes. Clear with lock-to-lock steering.

**Current state:**
- N51 online and communicating reliably. OVP 87L joint confirmed as the root cause of all intermittent failures since purchase.
- The tandem pump ADS section is working (confirmed 2026-03-26).
- Phase 1 open-loop flush completed (2026-03-29): 4L ZH-M pumped through, fluid clear, filter cleaned.
- Air in system confirmed (bubbling in reservoir after engine off, 2026-03-29).
- Rear height remains static. Fahrzeugniveau switch stuck (2026-04-02). Y36 solenoid and main control valve not yet inspected.
- Baseline measurements (2026-03-29): Rear L: 67cm, R: 66cm / Front L: 69cm, R: 68.5cm.

**NEXT ACTION: Clear code 14 (lock-to-lock steering), then proceed with closed-loop bleed (Phase 1).**

**IMPORTANT — Manual Discovery (2026-03-23):** We had been referencing the **1990** owner's manual, but the car is a **1991** model. The 1991 manual (now downloaded) reveals major differences: ADS, ASR, ASD, and the snow chain switch were all added for 1991. Critically, **the 1991 manual confirms ADS has a dedicated instrument cluster warning lamp** (page 92: "The indicator lamp comes on with the key in steering lock position 2 and goes out when the engine is running"). Our earlier conclusion that "ADS was never in the standard R129 indicator set" was wrong — it was based on the 1990 manual which predates ADS. **The original "missing lamp" observation may have been the ADS warning lamp.** Needs verification during ignition-ON bulb check.

**CAVEAT — US Manual vs European Car:** The English manuals (1990/1991/1992) are **US-market** editions. AOK912 is European-spec. Key differences: the US cluster shows "BRAKE" text (Euro uses symbol), "CHECK ENGINE" far right (California-only — correctly absent from Euro), and mph speedometer. The German Betriebsanleitung 1991–1993 (`r129-betriebsanleitung-1991-1993-DE.pdf`) covers all three model years in one document (image-only, no extractable text) and its cluster diagram is a **perfect match** to the actual cluster — confirming the European reference.

**Model Year Note:** AOK912 was manufactured 09/1991 and may be MY1992 spec. The 1992 US manual has been downloaded and compared — the ADS section (page 94) is **word-for-word identical** to the 1991 manual (page 92). Same indicator lamp list, same dashboard layout, same ADS cluster lamp description. The German manual covers 1991–1993 in one document. **Conclusion: whether the car is MY1991 or MY1992, the ADS cluster warning lamp should be present.**

**2026-03-30 UPDATE — OVP RELAY ROOT CAUSE IDENTIFIED:** The OVP relay was disassembled and found to have **3–4 ring-shaped cracked solder joints**, worst on the **87L pin** (suspected N51 power feed). This explains all intermittent ADS behavior since purchase. Repair: re-solder with Sn63/Pb37 leaded solder. Once N51 has reliable power, the remaining work is mechanical/hydraulic: closed-loop bleed, ride height assessment, and cluster investigation.

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
| Phase 1 open-loop flush completed (4L ZH-M). Fluid clear quickly. System shut down mid-flush. | Flush execution | 2026-03-29 |
| Air in system confirmed — visible bubbling in reservoir after engine off | Pre-flush baseline test | 2026-03-29 |
| **OVP relay: 3–4 cracked solder joints found (thermal fatigue).** Worst on 87L (N51 power feed). Interior clean/dry. | OVP disassembly & inspection | 2026-03-30 |
| Electronics bay inspected — general surface oxidation but no water pooling. No moisture inside OVP. | Visual inspection | 2026-03-30 |
| ADS system currently OFFLINE — Pin 9 shows "dim glow," no blink response | Blink-code reader test | 2026-03-30 |
| **OVP reinstalled — ADS ONLINE.** N51 stable, both switches active, Pin 9 returns code 14 only. | OVP reinstall + test | 2026-04-01 |
| **First drive (post-OVP fix): Sport/Comfort damping CONFIRMED WORKING.** Inspector independently commented on smooth ride. | Road test + katsastus | 2026-04-02 |
| **All four accumulator spheres HEALTHY.** Ride quality exceptional — earlier FR stiffness was air-lock, not blown sphere. | Road test observation | 2026-04-02 |
| **Fahrzeugniveau switch STUCK** — red LED permanently on, toggle has no effect on LED or ride height. Different from pre-flush behavior. | First drive observation | 2026-04-02 |
| **⚠️ ADS strut dust boots — lower sections MISSING.** Chrome piston shafts exposed to road debris. Urgent: pitting will destroy internal seals on irreplaceable ADS shocks. | Underbody inspection (katsastus) | 2026-04-02 |
| Underbody generally clean (summer-only car). No transmission leaks. Exhaust center silencer outer shell starting to rust. Rear diff surface rust. | Underbody inspection | 2026-04-02 |


**Working hypothesis (revised 2026-04-02):**

**Subsystem A (Adaptive Damping) is FULLY WORKING.** OVP root cause resolved (2026-04-01). Sport/Comfort modes confirmed on first drive (2026-04-02) — damping difference perceptible, inspector independently commented on smooth ride. All four accumulator spheres are healthy (earlier FR stiffness was air-lock from depleted system). Code 14 (steering angle sensor) needs clearing.

**Subsystem B (Level Control / Niveauregulierung) is NOT WORKING.** Fahrzeugniveau switch is stuck with red LED permanently on — toggling does not change state or affect ride height. This is a **new symptom** (different from pre-flush behavior when the switch toggled normally). Rear height remains static. Pump is proven alive, flush is done, fluid is fresh. The remaining unknowns are: switch/relay logic, rear level control valve function, and whether the hydraulic circuit to the rear struts flows.

**⚠️ URGENT — ADS strut dust boots are missing lower sections.** Chrome piston shafts are exposed to road debris. Pitting on the shafts will destroy internal seals and kill the ADS shocks, which are extremely expensive and increasingly unavailable. **Order and install dust boots before any further driving.**

**Issue tracker (updated 2026-04-02):**

1.  **~~Level control inoperative — pump not circulating.~~** **PUMP ALIVE (2026-03-26). Flush DONE (2026-03-29).** Rear height still static. Fahrzeugniveau switch now stuck (red LED permanently on, new symptom post-OVP-fix). **→ Next: (a) Clear code 14. (b) Read Pin 9 for any new codes. (c) Manual valve test — disconnect ARB linkage from rear level control valve, manually move lever with system pressurized on jack stands. (d) If valve responds to manual input, problem is upstream (switch/relay/wiring). If not, valve or hydraulic supply is blocked.**
2.  **~~Front accumulator spheres suspect.~~** **CLEARED (2026-04-02).** Ride quality exceptional on first drive — inspector commented on smooth adaptive ride. All four spheres healthy. Earlier FR stiffness (2026-03-22) was air-lock from depleted hydraulic system, not a ruptured diaphragm. **No replacement needed.**
3.  **ADS cluster warning lamp missing — confirmed cluster swap (option 216 factory ADS, confirmed via lastvin.com 2026-04-01).** Non-ADS cluster. **→ Pull cluster when tools available (Phase 3).**
4.  **Fault code 14 (steering angle sensor).** Returned after OVP reinstall (expected — N51 was unpowered for days). **→ Clear with lock-to-lock steering.**
5.  **Cluster swap — historical analysis (2026-03-27).** Swedish records show smooth odometer 2013–2024. Swap likely pre-2008.
6.  **~~OVP RELAY CRACKED SOLDER JOINTS.~~** **CONFIRMED & RESOLVED (2026-04-01).** Done.
7.  **⚠️ ADS STRUT DUST BOOTS — LOWER SECTIONS MISSING (2026-04-02).** Chrome piston shafts exposed. Pitting will destroy seals on irreplaceable ADS shocks. **→ ORDER IMMEDIATELY. Install before further driving.**
8.  **Fahrzeugniveau switch stuck (2026-04-02).** Red LED permanently on, toggle has no effect. New behavior — switch worked normally before flush (Mar 23–28). Possible causes: stuck relay, N51 latched state, switch failure, wiring issue from electronics bay work, or Y36 solenoid seized in energized position. **→ Investigate: (a) Check 12V at Y36 connector (right front wheel well) — if voltage present continuously, switch/relay circuit is latched. (b) Y36 click test. (c) If Y36 is clicking but no height change, suspect clogged sintered bronze filter inside Y36 (documented #1 failure on European ADS I). See [level_control_system.md](level_control_system.md) for detailed failure mode analysis.**
9.  **Level control not raising car — full Y36/valve diagnostic needed (2026-04-06).** With pump alive, flush done, and fluid fresh, the remaining suspects for no height change are: (a) Y36 sintered filter clogged (most likely — car has sat for years). (b) Height control rod pistons seized from inactivity. (c) Rear ARB linkage sheared. (d) Main valve regulating piston (50c) orientation incorrect or stuck. (e) Main valve ball check valves stuck. **→ Systematic diagnosis in Phase 2 steps 2.1–2.4.**

## ADS I System Architecture (Reference)

**CRITICAL DISTINCTION — ADS I Has TWO Independent Subsystems:**

The European "Niveauregulierung mit adaptivem Dämpfungs-System (ADS)" on the early R129 (1990–1995) is actually **two largely independent subsystems** sharing the "ADS" name. They have different control methods, different diagnostics, and different failure modes:

### Subsystem A: Adaptive Damping (Electronic — monitored by N51)

Controls shock absorber stiffness via electronic solenoid valves. This subsystem IS monitored by the ADS control module (N51) and DOES report faults via X11 Pin 9 blink codes.

- **ADS Control Module (N51)** — located in the firewall-mounted electronics bay (passenger side), second from the right. Smaller plastic module. Receives power via OVP relay (87L pin). Receives inputs from sensors and driver switch; commands the shock absorber solenoids. (See Electronics Bay Module Layout appendix in Engineering Diary.)
- **ADS Console Switch** — center console rocker/button: Sport / Comfort mode selection. Sends a ground signal to N51. **Status: WORKING** — LED illuminates, turns RED in Sport/up position (confirmed 2026-03-23).
- **Speed Sensor Input** — N51 receives vehicle speed from the speedometer or ABS controller.
- **Steering Angle Sensor** — input for dynamic damping adjustment.
- **4× ADS Shock Absorbers** — each contains a proportional solenoid valve that adjusts damping force. Solenoid coil resistance is typically 4–8 Ω. Each shock also contains a nitrogen-charged gas cushion (accumulator sphere). **All four spheres confirmed healthy (2026-04-02)** — exceptional ride quality on first drive, inspector commented. Earlier FR stiffness was air-lock. **⚠️ Dust boots missing lower sections — shafts exposed. Urgent replacement needed to protect these irreplaceable shocks.**
- **ADS Warning Lamp** — cluster warning lamp for damping faults (page 92: *"The indicator lamp comes on with the key in steering lock position 2 and goes out when the engine is running"*). **Status: MISSING from indicator strip** — either dead bulb behind dead-fronting, or cluster variant issue.
- **Diagnostic Output** — X11 Pin 9 blink-code interface (pre-OBD). Requires >13V supply. **Returns 1 blink = no stored damping faults.**

### Subsystem B: Niveauregulierung / Level Control (Mechanical/Hydraulic — NOT monitored by N51)

Controls ride height via a hydraulic system. On ADS I, height sensing is **MECHANICAL** (not electronic) — there are no electronic ride height sensors. This subsystem is **NOT monitored by the ADS module (N51)** and produces **NO fault codes on Pin 9.** The entire level control system can be completely dead and Pin 9 will still report "1 blink = all good" because N51 only monitors damping.

*(Note: ADS II (1996+ R129) upgraded to electronic ride height sensors and integrated level control monitoring into the module. ADS I does not have this.)*

**For detailed system operation, valve internals, control loops, failure modes, and electronic replacement concept, see [level_control_system.md](level_control_system.md).**

The level control has **three independent control functions** (not two as initially assumed):

1. **Automatic rear self-leveling** — purely mechanical closed loop via rear ARB linkage → proportional valve
2. **Manual height adjustment** — Fahrzeugniveau switch → Y36 solenoid → height control rods at **both front and rear** (not front only)
3. **Automatic speed-dependent lowering** — Y37 solenoid → lowers ~15mm above ~120 km/h

Key components summary (details in the reference doc):

- **Fahrzeugniveau-Einstellung (Vehicle Level Switch)** — position 2 on left instrument panel (next to headlight switch, replaces headlight range adjuster on ADS cars). Controls ride height set point with its own indicator LED. **Status: PRESENT and LED illuminates (confirmed 2026-03-23). STUCK with LED permanently on (2026-04-02).**
  - **Down = Normales Niveau (Normal Level):** Default. Above ~120 km/h, auto-lowers ~15mm via Y37.
  - **Up = Erhöhtes Niveau (Raised Level):** For poor roads. LED illuminates. Below ~50 km/h, raises ~30mm via Y36. Auto-reverts to Normal at 120 km/h.
  - **Absent on US-market ADS I cars** (likely bumper height regulations). This is why US forum threads rarely discuss height control.
- **Main Control Valve (A 129 320 00 58)** — central valve block, mounted in **right front wheel well area**. Contains sliding valve, 3× ball check valves, regulating piston, overpressure valve (160 bar max), and distributor valve (50a). All level control hydraulics pass through it.
- **Y36 Height Control Solenoid** — mounted on/adjacent to the main control valve. Energized by Fahrzeugniveau switch. Opens pressure path to height control rods. Contains a **sintered bronze filter** that is the #1 documented failure cause (clogs after 25–35 years). **Status: NOT YET TESTED.**
- **Y37 Speed-Dependent Lowering Solenoid** — second solenoid on valve block. Driven by speed relay. **Status: NOT YET TESTED.**
- **Height Control Rods** — hydraulic cylinders at **both front and rear** axles. Pistons extend/retract to change ride height. Can seize if system has been inactive for years. OEM replacements >€500 each.
- **Hydraulic Tandem Pump (A 129 460 07 80)** — engine-driven (belt), mounted on the M119. ONE pump with TWO internal sections sharing one drive shaft:
  - Section 1 = Power Steering (draws from metal canister) — **WORKING** (brown/aged fluid, steering assisted)
  - Section 2 = Niveauregulierung (draws from plastic reservoir next to washer fluid) — **PUMP ALIVE (confirmed 2026-03-26)**, flush done, but level control still not working
  - Min pressure: 133 bar. Min flow at idle: 0.2 L/min. Rebuilt pumps: ABCspecialist (NL), ~€850 + old core return
- **ADS/Niveauregulierung Reservoir** — translucent plastic, next to washer fluid bottle. Fluid: MB 343.0 / ZH-M (part number 000 989 91 03). **Flushed with 4L fresh ZH-M (2026-03-29). Level at MAX (engine off). Filter cleaned — new filter (A 129 327 00 91) to be ordered.**
- **Rear Level Control Valve** — hydraulic proportioning valve, mounted mid-rear-axle. Height sensing is MECHANICAL: a **linkage from the rear anti-roll bar** mechanically operates the valve's lever arm. As load changes rotate the ARB, the valve directs fluid to raise or lower the car. **No electronic sensors involved.**
- **Anti-Roll Bar Linkage** — the "sensor" of ADS I level control. A plastic/metal rod connecting the ARB to the proportioning valve lever. Known failure point: shears at lower mounting. If broken, the valve stays in one position and cannot adjust height. **This failure produces NO electronic fault codes.**
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
<summary><b>Phase 2: Fuse & Power — OVP RELAY ROOT CAUSE FOUND (2026-03-30)</b></summary>

- **2.1 — ADS Fuse** — Not checked individually. N51 communicates when OVP provides clean power.
- **2.2 — OVP Relay Fuse** — DONE (2026-03-22). 10A internal fuse is intact.
- **2.3 — OVP Relay PCB Inspection** — DONE (2026-03-30). **ROOT CAUSE FOUND.** 3–4 ring-shaped thermal fatigue fractures on PCB, worst on 87L (N51 power feed). OVP interior clean/dry — pure thermal fatigue. **→ Re-solder is now Phase 0 (Active).**

</details>

<details>
<summary><b>Phase 1 Hydraulic: Open-Loop Flush — COMPLETED 2026-03-29</b></summary>

4L ZH-M pumped through via open-loop flush. Key results:
- Fluid ran clear very quickly (<1L of new fluid).
- No air bubbles seen from return line (air trapped in dead-end circuits, not main loop).
- Filter cleaned (~99%) — small amount of sediment. New filter (A 129 327 00 91) to be ordered.
- System shut down mid-flush due to OVP solder joint failure (identified 2026-03-30).
- Closed-loop bleed was NOT performed (blocked by OVP failure). → Now Phase 1 (Active).

References used:
- MBWorld R129 ADS Fluid Change thread (MB-Dude / Jeff's procedure)
- Rodionenkin.de Ölwechsel Zentralhydraulik
- Classic Jalopy SLS Flush (W126, same system)

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

### Phase 0: OVP Relay Re-Solder — COMPLETED ✓ (2026-04-01)

*Root cause confirmed. OVP relay cracked solder joints on 87L (N51 power feed) caused all intermittent ADS failures since purchase.*

- **Found (2026-03-30):** 3–4 ring-shaped thermal fatigue fractures on OVP PCB, worst on 87L.
- **Re-soldered (2026-03-31):** All joints reworked with Sn63/Pb37. Optical inspection passed.
- **Reinstalled & verified (2026-04-01):** N51 boots cleanly. Both cabin switches show red LEDs. Diagnostic bus stable. Pin 9 returns code 14 (N49 steering angle sensor — expected, clear with lock-to-lock). **No other fault codes.**

### Phase 1: Closed-Loop Bleed & Ride Height Assessment (NEXT ACTION)

*Phase 0 prerequisite MET — N51 is online and stable. Open-loop flush was completed on 2026-03-29 (4L ZH-M, fluid clear, filter cleaned). Air entrapment confirmed (bubbling). The closed-loop bleed was never performed because OVP failed mid-flush.*

**Before starting:** Clear code 14 — start engine, turn steering full lock left → full lock right → center. Read Pin 9 to confirm 1 blink (no faults).

**Procedure:**
1. Top up reservoir to MAX with fresh ZH-M.
2. Start engine. Verify ADS switches are active (console + Fahrzeugniveau).
3. Jack rear to full droop — forces the rear level control valve to "fill" position, pushing fluid into rear struts and forcing trapped air back to reservoir.
4. Lower rear back to ground. Repeat 2–3 times.
5. "Trunk bounce" — load/unload weight in the trunk to cycle the rear valve through its range.
6. Activate Fahrzeugniveau UP/DOWN several times during the process.
7. Check reservoir for bubbling after engine off. Repeat until no bubbles.
8. **Measure fender-to-ground** at all four corners. Compare to baseline (Rear L: 67cm, R: 66cm / Front L: 69cm, R: 68.5cm).
9. Top up reservoir to MAX.

**Success criteria:** Rear height increases from baseline. Bubbling eliminated. Reservoir level stable.

**If rear still static after bleed:** proceed to Phase 2 (mechanical inspection — rear level control valve, ARB linkage).

### Phase 2: Mechanical & Hydraulic Inspection Under Car (after bleed proves system status)

*Do this with the car on a lift or jack stands, regardless of Phase 1 outcome. See [level_control_system.md](level_control_system.md) for detailed component descriptions.*

- **2.1 — Y36 Solenoid Click Test (can do before jacking)**
  - Engine running, have someone press Fahrzeugniveau switch to Raised position.
  - Listen near the **right front wheel well** for an audible **click** from Y36.
  - If click: solenoid energizing. Problem is downstream (clogged sintered filter, seized height control rods, blocked hydraulic path).
  - If no click: measure 12V at Y36 connector. Voltage present + no click → seized solenoid. No voltage → wiring/switch/relay fault.
  - **Note:** Fahrzeugniveau switch is currently STUCK with LED permanently on (since 2026-04-02). Y36 may be receiving continuous power — check with multimeter at Y36 connector even without pressing the switch.

- **2.2 — Main Control Valve & Y36 Visual Inspection**
  - Locate the **main control valve** (A 129 320 00 58) in the right front wheel well area. Multiple hydraulic steel lines attach to it, plus electrical connectors for Y36 and Y37.
  - Check for external leaks at all fittings and solenoid connections.
  - Identify Y36 electrical connector — 2-pin, 12V when Fahrzeugniveau is active.
  - Identify Y37 electrical connector — second solenoid on the valve body.

- **2.3 — Rear Level Control Valve & Linkage**
  - Locate the **rear level control valve** (hydraulic proportioning valve) mounted approximately in the middle of the rear axle area.
  - Trace the **linkage from the rear anti-roll bar** to the proportioning valve lever arm.
  - **CHECK FOR SHEARED LINKAGE:** Known ADS I failure. The plastic linkage part can shear at the lower mounting, causing the system to lose rear ride height completely. A MBClub UK user with a 1992 500SL had this exact failure.
  - Inspect hydraulic lines from the rear shocks to the valve for leaks, kinks, or disconnection.
  - **Manual valve test:** Disconnect ARB linkage from the valve lever. Manually move lever back and forth with engine running. If car rises/lowers → hydraulics are good, problem is upstream (linkage, switch, Y36). If no response → valve or hydraulic supply is blocked.
  - *Pass criteria:* Linkage intact and securely connected at both ends, no hydraulic leaks, manual lever test responds.

- **2.4 — Height Control Rods**
  - Inspect front and rear height control rods. Pressure line marked with **red paint blob**.
  - Check rod pistons for freedom of movement (if accessible). Pistons seize after years of inactivity.
  - *Pass criteria:* Rods not visibly seized, no external leaks at rod seals.

- **2.5 — Accumulator Sphere Condition**
  - ~~Front Right is confirmed hydro-locked (2026-03-22).~~ **CLEARED (2026-04-02)** — all four spheres healthy, earlier FR stiffness was air-lock.
  - *Pass criteria:* Shock compresses under body weight and returns without bouncing.

- **2.6 — Shock Absorber External Inspection**
  - Visually inspect all four ADS shocks for oil leaks, dented bodies, or damaged solenoid connectors.
  - Check solenoid connector pins for corrosion.
  - *Pass criteria:* No external oil weep, connectors clean and dry.

- **2.7 — Spring Pad Assessment (only if hydraulic system is restored and rear still sits low)**
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

- **5.1 — Compile Results (updated 2026-03-30)**

  | Issue | Status | Fix | Cost |
  | ----- | ------ | --- | ---- |
  | OVP relay cracked solder joints | **ROOT CAUSE FOUND (2026-03-30)** | Re-solder with Sn63/Pb37 | ~€0 (solder from lab) |
  | ADS pump section not circulating | **RESOLVED** — pump alive, flush completed | Flush done, closed-loop bleed pending | €40 (fluid used) |
  | Air in hydraulic system | **CONFIRMED** — bubbling observed | Closed-loop bleed (Phase 1 active) | €0 (labor only) |
  | Front Right sphere suspect | Pending "straw test" after system online | If blown: replace front pair A 129 320 01 15 | ~€200–300 |
  | Rear height static | Pending — cannot evaluate until N51 online + bleed done | May resolve with bleed; if not, inspect valve/linkage | TBD |
  | ADS cluster warning lamp missing | Confirmed non-ADS cluster swap | Pull cluster, read P/N, source correct strip or cluster | TBD |
  | Hydraulic filter aging | Old filter cleaned, needs replacement | Order A 129 327 00 91 | ~€7–11 |

- **5.2 — Decision: Repair or Bypass**
  - **Repair** (strongly recommended — the most expensive feared failure (pump: €850) is ruled out; OVP fix is essentially free; electronics are healthy):
    - OVP re-solder restores N51 power for ~€0.
    - Closed-loop bleed should clear remaining air.
    - Front spheres may not even be blown (air-lock possible) — test first.
    - Cluster lamp is cosmetic but important for oil-level warning visibility.
  - **Intentional bypass** (only if unexpected further failures emerge):
    - Convert to conventional Bilstein B4/B6 shocks and delete ADS. Document the conversion.
  - **Module replacement** — NOT NEEDED. N51 is healthy when powered.

## Parts & Tools Needed

**Phase 0 — OVP Re-Solder (NEXT ACTION):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| Sn63/Pb37 leaded solder | Re-solder all OVP relay joints | **Source from office/lab** |
| Desoldering wick | Remove old solder cleanly | **Source from office/lab** |
| Soldering iron (fine tip) | Re-flow joints | Available ✓ |
| Isopropyl alcohol + cotton swabs | Clean pads after desoldering | Available ✓ |
| Magnifying glass / loupe | Post-solder inspection | Available ✓ |

**Phase 1 — Closed-Loop Bleed (after OVP fix):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| ZH-M / MB 343.0 Hydraulic Fluid | Top-up during bleed (~0.5–1L) | 4L acquired, most used in flush — check remaining level |
| Hydraulic Suspension Filter (A 129 327 00 91) | Replace cleaned filter for long-term reliability. ~€7–11. | **ORDER NEEDED** |
| Jack + jack stands | Jack rear to full droop for bleed | Available ✓ |
| Wheel chocks | Safety during jack work | Acquired ✓ (Motonet) |

**Hydraulic flush supplies (COMPLETED 2026-03-29):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| ZH-M / MB 343.0 Hydraulic Fluid (4L) | Open-loop flush | Used ✓ |
| Transparent PVC Hose (6mm + 8mm, 2m each) | Return line to waste container | Acquired ✓ (Motonet) |
| Brake cleaner | Cleaning fittings | Used ✓ |
| Syringe / turkey baster (MTX 500ml) | Extract old fluid from reservoir | Used ✓ |

**On hand (diagnostic tools):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| Multimeter (Owon HDS242) | Voltage, resistance, continuity | Acquired ✓ |
| Oscilloscope (Owon HDS242) | Signal waveform analysis (if needed) | Acquired ✓ |
| 12V LED blink-code reader (V2) | X11 Pin 9 diagnostics | Built ✓ |

**Later phases (not blocking):**

| Item | Purpose | Status |
| ---- | ------- | ------ |
| Cluster removal hooks (140 589 02 33 00) or DIY 90° pick | Pull instrument cluster (Phase 3) | Needed (can fabricate) |
| W1.2W / W2W wedge bulbs | ADS cluster lamp + spares (Phase 3) | Needed |
| Front Accumulator Spheres x2 (A 129 320 01 15) | Pending "straw test" — may not be needed if air-lock was the cause | Pending assessment |


## Related Work Items

- **Level Control System Reference** → [level_control_system.md](level_control_system.md) — detailed operation of the Niveauregulierung: valve internals, Y36/Y37 solenoids, height control rods, control loops, known failure modes, and electronic replacement concept
- ADS Blink-Code Reader (tool & results) → [work/ads_blink_reader/](../ads_blink_reader/README.md)
- Blink-Code Channel Inventory → [work/ads_blink_reader/blinker_report.md](../ads_blink_reader/blinker_report.md)
- Suspension Refresh (mechanical) → [Active Tasks #4](../../docs/tasks.md)
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
| 2026-03-28 | 1     | **Lock-to-lock + extended observation** | **CODE 14 CLEARED — SYSTEM FULLY ONLINE.** Lock-to-lock steering re-initialized N49. System stable across multiple engine starts throughout the day (car not driven — not registered). **Key observations:** (1) Both switch LEDs illuminate correctly and remain active. (2) Console Sport/Comfort works consistently (red on/off). (3) **Reservoir level returned to near-MAX with engine off** — fluid enters circuit when running, returns when depressurized. No net loss (>100ml), confirms no external leaks. (4) **Possible front height change** — visual impression only, needs fender-to-ground measurement. (5) **Rear height static** — no change with Fahrzeugniveau UP. (6) **Fahrzeugniveau switch slow to deactivate** — LED stays on for some time after toggling off. | **System stable and ready for Phase 1 flush.** Rear-specific issue confirmed — front may respond to level commands while rear does not. Post-flush focus: rear level control valve, rear ARB linkage, air in rear lines. **ACTION: measure fender-to-ground at all four corners before and after flush.** |
| 2026-03-29 | 1     | **Phase 1 Flush Execution** | **Flush completed using 4L ZH-M.** Findings: (1) Fluid ran clear very quickly (<1L). (2) **No air bubbles** seen from return line during the open-loop flush. (3) Reservoir kept above MIN successfully. (4) **System shut down mid-test:** Fahrzeugniveau switch LED went dark and stopped responding. (5) **Diagnostic ports unresponsive:** Pin 9 shows "static dim glow" on the LED tester, no blinks — even with engine running at 14V. | See 2026-03-30 OVP findings below — the mid-flush shutdown was likely caused by OVP solder joint failure under sustained heat/vibration. |
| 2026-03-30 | —     | **OVP RELAY CRACKED SOLDER JOINTS FOUND** | Removed and disassembled OVP relay. 3–4 ring-shaped thermal fatigue fractures on PCB, worst on 87L (N51 power feed). Interior clean/dry — pure thermal fatigue. | Root cause of all intermittent ADS symptoms identified. Re-solder with Sn63/Pb37. |
| 2026-03-31 | 0     | **OVP re-soldered** | All joints reworked with Sn63/Pb37 leaded solder. Optical inspection: good wetting, no ring cracks, no cold joints, no bridges. | Awaiting reinstall + test. |
| 2026-04-01 | 0     | **OVP REINSTALLED — ADS ONLINE ✓** | OVP reinstalled. N51 boots cleanly. Both cabin switches show red LEDs. Diagnostic bus stable. **Pin 9 returns code 14 only** (steering angle sensor N49 — expected after extended power loss). No other fault codes. | **ROOT CAUSE CONFIRMED.** OVP 87L cracked solder joint was the sole cause of all intermittent ADS failures since purchase. Next: clear code 14 (lock-to-lock), then closed-loop bleed (Phase 1). |

