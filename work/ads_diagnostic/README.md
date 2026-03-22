# ADS I System Diagnostic — Full Status Assessment

## Overview

The 1991 Mercedes-Benz 500 SL (R129) — AOK912 is equipped with ADS I (Adaptive Damping System, first generation). The car drives well and the ride is comfortable ("floating"), confirming the base mechanical springs and nitrogen accumulators are functional. However, there is currently **zero sign of life** from the electronic ADS system: the console button is inoperative, the instrument cluster warning lamp appears to have been removed by a previous owner, and the ADS control module does not respond to blink-code diagnostics (weak static glow on X11 Pin 9, no pulse communication).

This project is a structured, step-by-step diagnostic plan to determine the exact state of the ADS I system — from a quick fuse check all the way to component-level testing — before deciding on repair, replacement, or intentional bypass.

## Current Known Status


| Observation                                                          | Source                                     | Date       |
| -------------------------------------------------------------------- | ------------------------------------------ | ---------- |
| ADS switch on center console identified; non-functional              | Pre-purchase inspection                    | 2026-03-13 |
| ADS warning lamp dead — no dead-fronting outline visible in cluster  | Ferry transit observation                  | 2026-03-13 |
| Comfortable "floating" ride at highway speed; accumulators not blown | 700 km shakedown (Vellinge → Kapellskär)   | 2026-03-13 |
| Rear sits lower than front (1–2 finger gap rear vs. 3 finger front)  | "Sag test" on ferry deck                   | 2026-03-14 |
| Rear did NOT rise when engine started — no self-leveling action      | Ferry deck observation                     | 2026-03-14 |
| Bounce test passed — firm but not rock-hard or oscillating           | Manual suspension test                     | 2026-03-14 |
| ADS confirmed in mechanical failsafe / limp mode                     | Aggregate diagnosis                        | 2026-03-14 |
| X11 Pin 9 (ADS): weak static glow, no blink pulses, cannot clear     | Blink-code sweep (ignition ON, engine OFF) | 2026-03-18 |
| Front Right suspension significantly stiffer than Front Left         | Manual suspension test (>24h idle)         | 2026-03-22 |
| Rear suspension compresses more than front, but does not oscillate   | Manual suspension test (>24h idle)         | 2026-03-22 |


**Working hypothesis:**
1.  **The Electronic Fault:** Sometime in the past, an electrical component (e.g., OVP relay, sensor linkage, or shock solenoid) failed. This caused the ADS module to enter "Limp/Sport" mode and triggered the dashboard warning light.
2.  **The Cover-up:** A previous owner physically removed the instrument cluster warning bulb to hide the fault.
3.  **The Mechanical Consequence:** Because the system was permanently stuck in the stiff failsafe mode, the shock absorbers could no longer actively soften impacts. Over time, the constant high-pressure hydraulic hammering caused the Front Right nitrogen accumulator (sphere) diaphragm to rupture.
4.  **Current State:** The ADS control module (N51) is currently offline/not communicating (weak Pin 9 glow). The Front Right sphere is mechanically blown (hydro-locked). The Front Left sphere is intact but defaulting to failsafe-firm. The rear spheres are intact but lack hydraulic pressure due to the system being offline.

## ADS I System Architecture (Reference)

The ADS I system on the early R129 (1990–1995) consists of:

- **ADS Control Module (N51)** — located in the right-side engine bay module box (E-box) near the firewall, under the black plastic cover. Receives inputs from sensors and driver switch; commands the shock absorber solenoids.
- **ADS Console Switch** — center console rocker/button: Sport / Comfort mode selection. Sends a ground signal to N51.
- **ADS Warning Lamp** — instrument cluster. Illuminates on ignition-ON (bulb check), then extinguishes if system is healthy. Stays on or flashes to indicate faults.
- **Speed Sensor Input** — N51 receives vehicle speed from the speedometer or ABS controller.
- **Steering Angle Sensor** — input for dynamic damping adjustment.
- **4× ADS Shock Absorbers** — each contains a proportional solenoid valve that adjusts damping force. Solenoid coil resistance is typically 4–8 Ω.
- **Rear Self-Leveling** — hydraulic pump, accumulator spheres, and rear level control valve maintain rear ride height. Shares fluid circuit with the ADS struts on some configurations.
- **Level Sensors (front & rear)** — plastic linkage rods connected to suspension arms. Brittle with age; breakage is common and causes immediate limp-mode.
- **Diagnostic Output** — X11 Pin 9 blink-code interface (pre-OBD).

## Diagnostic Plan — Simple to Complex

### Phase 1: No-Tools Visual Checks (5 minutes)

- **1.1 — ADS Console Switch Inspection**
  - Locate the ADS rocker switch on the center console (left side of gear lever, with shock absorber icon).
  - Note: The middle button is for snow chains/ASR (Anti-Slip Regulation), and the right button is for the central locking interior switch.
  - Press it: does it click mechanically? Does it feel broken or jammed?
  - Note: The red LED indicator on this switch will be inactive if the ADS module is in limp/failsafe mode.
  - *Pass criteria:* Switch clicks and returns normally.
- **1.2 — Instrument Cluster Warning Lamp Check**
  - Turn ignition to position II (ON, engine off).
  - Observe the instrument cluster during the bulb-check phase (all warning lamps should illuminate for 2–3 seconds).
  - Look for an ADS warning indicator (typically a shock absorber symbol or "ADS" text, located in the lower cluster area).
  - *Expected result:* If the bulb has been removed, there will be no illumination at all — not even during bulb check.
  - *Action if missing:* Pull the cluster and inspect the bulb socket (Phase 3).
- **1.3 — ADS Blink-Code with Engine Running (Crucial 1st Step)**
  - Before pulling any modules or fuses, simply repeat the X11 Pin 9 blink-code read, but this time **with the engine running at idle**.
  - Some early ADS I control modules require the alternator charging voltage (engine running) to fully wake up from sleep/failsafe mode.
  - *Pass criteria:* Blink pulses appear instead of a static glow.
  - *Note on Codes:* If the module wakes up, it will provide distinct blink codes. Yes, **each shock absorber has its own unique fault code** for its internal solenoid valve (e.g., Left Front Solenoid Open Circuit, Right Front Solenoid Short Circuit).
- **1.4 — Under-Hood Visual for ADS Components**
  - With the hood open, visually confirm the ADS shock absorber solenoid connectors on the front strut towers (2-pin connectors on top of each front strut).
  - Check if the connectors are plugged in or deliberately disconnected/zip-tied away.
  - *Pass criteria:* Connectors are physically mated to the shock absorber solenoids.

### Phase 2: Fuse & Power Verification (15 minutes, multimeter required)

- **2.1 — ADS Fuse Check**
  - Locate the ADS fuse(s). On the 1991 R129, check:
    - **Fuse box in the engine bay** (left side): fuse F15 or nearby — consult the fuse chart on the lid.
    - **Fuse box in the trunk** (left side behind the trim panel): secondary fuse allocation for body electronics.
  - Pull the ADS fuse(s) and visually inspect. Test continuity with a multimeter.
  - *Pass criteria:* Fuse intact with continuity. If blown, note the rating and replace — but investigate WHY it blew before powering the system.
- **2.2 — MAS Module / Overvoltage Protection Check (CRITICAL)**
  - On the early 1991 M119 (unlike later cars with an N16 Base Module), the right-most unit in the module box is the **MAS Module** (part number `011 545 82 32` or similar, marked "MAS").
  - The MAS module handles fuel pump relay duties, A/C compressor cut-out, and O2 sensor heating, but **does not have fuses on top of it**.
  - *Update:* Reviewing the engine bay photos again, the silver **OVP Relay** is actually visible mounted right next to the diagnostic connector/module box area. It has a red plastic top with a clear flip-cover containing a 10A blade fuse.
  - A blown OVP fuse or cracked internal solder joints will kill power to the ADS (and ABS), causing a failure to communicate (weak static glow on Pin 9) while the car still runs perfectly.
  - Check the 10A fuse on top of the OVP relay. If intact, pull the relay and inspect for cracked solder joints.
  - *Pass criteria:* Fuses intact, relay clicks with ignition, and provides ~12V output.
- **2.3 — ADS Control Module Power & Ground (at the module connector)**
  - Locate the ADS control module N51 (in the right-side engine bay module box, near the OVP relay).
  - With the module connector plugged in and ignition ON, back-probe or use the connector pins:
    - **Permanent +12V (Terminal 30):** should read battery voltage (~12.4V+) at all times.
    - **Ignition +12V (Terminal 15):** should read battery voltage with ignition ON.
    - **Ground (Terminal 31):** should read <0.1V to chassis ground.
  - *Pass criteria:* Module has clean power and ground. If any supply is missing, trace the wire back to the fuse/relay.
  - *Fail action:* If no power at all — the module has been deliberately disconnected or there's a wiring break. Trace the harness.

### Phase 3: Warning Lamp & Cluster Inspection (30 minutes, trim tools required)

- **3.1 — Instrument Cluster Removal & Bulb Socket Inspection**
  - Remove the instrument cluster surround (trim screws and clips).
  - Pull the cluster forward enough to access the rear bulb sockets.
  - Locate the ADS warning lamp socket (consult the cluster bulb assignment diagram — typically a 1.2W or 2W wedge bulb).
  - Determine: is the bulb missing? Burned out? Or has the socket been taped over / filled?
  - *Action:* Install a new bulb (W1.2W or W2W as appropriate). Reassemble and test with ignition ON.
  - *Expected result:* If the ADS module is in fault mode, the warning lamp should now illuminate continuously (good — it means the module is alive and reporting a fault). If it still doesn't light, the module is not driving the lamp circuit.

### Phase 4: Module Communication & Signal Testing (1 hour, multimeter + oscilloscope)

- **4.1 — Re-Test Blink-Code with Engine Running**
  - Previous blink-code test (2026-03-18) was performed with engine OFF (ignition ON only).
  - Some ADS I modules require the engine running (alternator charging) to fully power up.
  - Repeat the Pin 9 blink-code read procedure with the engine running at idle.
  - *Pass criteria:* Blink pulses appear instead of static glow.
- **4.2 — ADS Console Switch Signal Verification**
  - With the module connector accessible, back-probe the switch input pin on the N51 connector.
  - Measure voltage with ignition ON: should toggle between ~0V and ~12V (or vice versa) when the console switch is pressed.
  - If no voltage change: the switch wiring is open or the switch itself is faulty. Test continuity of the switch directly.
  - *Pass criteria:* Measurable voltage change when switch is toggled.
- **4.3 — ADS Module Diagnostic Output Pin (direct probe)**
  - Instead of reading through the X11 connector, probe the diagnostic output pin directly at the N51 module connector.
  - With ignition ON, measure DC voltage on the diagnostic pin:
    - **~0V:** Module is actively pulling low (possible communication, grounding the blink-code line).
    - **~12V:** Module is not driving the line (open-collector output inactive).
    - **Floating / intermediate voltage (~2–6V):** Consistent with the "weak static glow" observation — the output transistor may be partially conducting (internal fault).
  - *Pass criteria:* A definitive 0V or 12V indicates the module is alive and its output stage is functional.
- **4.4 — Speed Sensor Signal to N51**
  - The ADS module needs vehicle speed input to function. If the speed signal is missing, some modules enter permanent safe mode.
  - Back-probe the speed input pin at the N51 connector. With the car on jack stands and a driven wheel spinning (or use the speedometer signal wire), verify a pulsed signal appears.
  - *Alternative:* Simply verify the speedometer works while driving — if it does, the speed signal is likely reaching N51 as well (shared bus).
  - *Pass criteria:* Speed signal present or speedometer confirmed functional.

### Phase 5: Shock Absorber Solenoid Testing (1–2 hours, multimeter + jack stands)

- **5.1 — Solenoid Coil Resistance (all 4 corners)**
  - Disconnect the 2-pin connector from each ADS shock absorber solenoid (2 front on strut towers, 2 rear under the car).
  - Measure resistance across each solenoid coil:
    - **Expected:** 4–8 Ω (varies by manufacturer — Bilstein, Sachs).
    - **Open circuit (∞):** Coil is broken — shock absorber must be replaced.
    - **Short circuit (~0 Ω):** Coil is shorted — shock absorber must be replaced.
  - Record all four readings.
  - *Pass criteria:* All four solenoids within spec and roughly equal.


| Corner      | Resistance (Ω) | Status |
| ----------- | -------------- | ------ |
| Front Left  |                |        |
| Front Right |                |        |
| Rear Left   |                |        |
| Rear Right  |                |        |


- **5.2 — Solenoid Wiring Continuity (harness to module)**
  - With solenoid connectors unplugged and N51 connector unplugged, measure continuity from each solenoid connector pin back to the corresponding pin on the N51 module connector.
  - *Pass criteria:* Continuity on both wires for all four corners, no shorts to ground or to each other.

### Phase 6: Hydraulic System & Self-Leveling (2+ hours, car on lift or jack stands)

- **6.1 — Hydraulic Fluid Level**
  - Locate the ADS/SLS hydraulic reservoir (typically near the power steering reservoir on the M119, or integrated into the rear leveling pump assembly).
  - Check fluid level against min/max marks.
  - Inspect fluid color: should be clear/yellow (ZH-M / MB 343.0 spec). *Note: The earlier R129 ADS/SLS system shares the same ZH-M fluid type as the soft top hydraulics. Newer MB systems use green CHF 11S, but the early R129 uses ZH-M.* Dark brown = severely oxidized; milky = water contamination.
  - *Action:* Top up if low; note for future full flush.
- **6.2 — Rear Leveling Pump Operation**
  - With the engine running, listen near the rear axle area for the leveling pump activating (a faint electric motor whine, typically runs for a few seconds after start-up or after load changes).
  - If the pump is NOT running: check its fuse, relay, and power supply independently.
  - If the pump IS running but the rear doesn't rise: suspect a stuck level control valve, a broken level sensor linkage, or a hydraulic leak.
- **6.3 — Level Sensor Linkage Inspection (front & rear)**
  - Visually inspect the plastic level sensor linkage rods on both axles.
  - These brittle plastic rods connect the suspension arm to a rotary potentiometer on the body. If snapped (extremely common after 35 years), the module sees a fixed "level" and cannot command corrections.
  - *Pass criteria:* Linkage rods intact and moving freely with suspension travel.
- **6.4 — Hydraulic Line Inspection**
  - Trace the high-pressure hydraulic lines from the pump to each rear strut.
  - Look for wet spots, cracked fittings, or disconnected lines.
  - Check the accumulator spheres (pressurized nitrogen balls) — they should be firmly attached and dry at the fittings.

### Phase 7: Module-Level Decision (after all above)

- **7.1 — Assess Results & Determine Root Cause**
  - Compile all findings from Phases 1–6.
  - The most likely failure modes, ranked by probability:
    1. **OVP Relay Failure / Blown Fuse + Bulb Removed** — extremely common. The OVP relay drops power to N51, causing it to go offline (Pin 9 weak glow). Previous owner removed the warning bulb to hide it. (Easy/cheap fix.)
    2. **Ruptured Sphere (Accumulator)** — the computer *cannot* detect this. A blown sphere is a purely mechanical failure. It will cause a rock-hard ride on that corner, but will NOT trigger an ADS warning light on its own. **Note:** If one sphere is blown, it is standard practice to replace them in axle-pairs (i.e., both fronts).
    3. **Broken level sensor linkage** — causes permanent limp mode. Module may still be healthy but stuck in safe mode. (Cheap plastic part.)
    4. **Solenoid coil failure** — one or more burned-out shock absorber solenoids cause the module to fault and enter limp mode. The computer *can* detect this via resistance checking. (Requires ADS-specific shock absorber replacement — expensive.)
    5. **Hydraulic system failure** — low fluid, failed pump, stuck valve. (Repair depends on specific component.)
- **7.2 — Decision: Repair, Replace Module, or Intentional Bypass**
  - Based on findings, decide:
    - **Repair:** If the cause is external to the module (fuse, relay, wiring, sensor linkage), repair and restore ADS function.
    - **Replace module:** If N51 is dead, source a used unit (MB part number depends on exact variant — check the label on the existing module). Program/adapt if required.
    - **Intentional bypass:** If ADS repair is uneconomical (e.g., multiple dead solenoid shocks at ~€500+ each), convert to conventional Bilstein B4/B6 shock absorbers and delete the ADS system cleanly. Document the conversion.

## Parts & Tools Needed


| Item                                 | Purpose                         | Status                 |
| ------------------------------------ | ------------------------------- | ---------------------- |
| Multimeter (Owon HDS242 or Fluke)    | Voltage, resistance, continuity | Acquired ✓             |
| 12V LED blink-code reader            | X11 Pin 9 diagnostics           | Built ✓                |
| Trim removal tools (plastic pry set) | Cluster removal, kick panel     | Needed                 |
| W1.2W / W2W wedge bulb               | ADS warning lamp replacement    | Needed                 |
| Oscilloscope (Owon HDS242)           | Signal waveform analysis        | Acquired ✓             |
| ZH-M Hydraulic Fluid (1L)            | Hydraulic fluid top-up          | Needed (if applicable) |


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
| 2026-03-13 | —     | Highway observation | Warning lamp missing from cluster     | Suspect bulb removed     |
| 2026-03-14 | —     | Sag test            | Rear low, no self-leveling on start   | Confirmed limp mode      |
| 2026-03-18 | 4     | Pin 9 blink-code    | Weak static glow, no pulses           | Module not communicating |
| 2026-03-22 | 2     | 2.2 OVP Fuse Check  | 10A fuse inside OVP relay is intact   | Need to test relay power |
| 2026-03-22 | —     | Manual Suspension Test | Front Right is rock hard (almost zero travel under body weight). Front Left compresses. Rear compresses. | Confirms Front Right nitrogen accumulator (sphere) is ruptured/hydro-locked. Front Left sphere is intact and likely defaulting to failsafe firm. |


