# X11 Diagnostic Connector - Blink Code Channel Inventory

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) — AOK912
**Connector:** X11 / 16-pin blink-code socket (early pre-HFM type)
**Date of extraction:** 2026-03-18
**Tool used:** LED + push-button blink-code reader (banana plug breakout)

## Pin Allocation

| Pin | Function | Signal Type | Status |
|-----|----------|-------------|--------|
| 1 | Ground (Terminal 31) | Power | Reference ground for all measurements |
| 2 | — | — | Not tested |
| 3 | KE duty-cycle / lambda integrator | Digital pulse (~100Hz) | Expected active (not yet tested with scope) |
| 4 | — | — | Not tested |
| 5 | ASD | Blink-code | **No connector** — module not fitted on this car |
| 6 | SRS (Airbag) | Blink-code | **Active** — returned valid codes |
| 7 | RB | Blink-code | **Active** — returned valid codes |
| 8 | DI/EZL (Ignition) | Blink-code | **Active** — returned valid codes |
| 9 | ADS (Adaptive Damping) | Blink-code | ~~Static glow (weak)~~ → **Active** — returns 1 blink (no faults) when battery >13V |
| 10 | RST | Blink-code | **Active** — returned valid codes (stubborn reset) |
| 11 | ATA (Anti-Theft Alarm) | Blink-code | **Static glow (medium)** — module present but not communicating |
| 12 | IRCL (Infrared Central Lock) | Blink-code | **Static glow (medium)** — module present but not communicating |
| 13 | ETC | Blink-code | **No connector** — module not fitted on this car |
| 14 | ESMC | Blink-code | **Active** — returned valid codes |
| 15 | — | — | Not tested |
| 16 | +12V (Terminal 15, ignition ON) | Power | Supply reference for blink-code reader |

## Extracted Fault Codes

### Pin 6 — SRS (Airbag System)
- **Before reset:** 3 / 8 / 9 pulses (three stored fault codes)
- **After reset:** 1 blink (no faults — successfully cleared)
- **Note:** Was in a 2-blink fault state that needed reset

### Pin 7 — RB (Roll Bar / Überrollbügel)
- **Before reset:** 2 / 3 / 4 / 5 / 6 / 7 pulses (six stored fault codes)
- **After reset:** 1 blink (no faults — successfully cleared)
- **2026-03-23 re-test (>13V):** 1 blink (still clear after garage-only driving)
- **Pin identification confirmed:** Pin 7 on the R129 16-pin X11 = Roll Bar controller (N52). Confirmed via MBClub UK WIS reference, BenzWorld R129 threads, and Motor-Talk. "RB" = Roll Bar (Überrollbügel), not ABS.
- **Approximate fault code mapping** (from WIS CST/RB documentation — W124 Cabriolet reference, R129 codes may differ slightly):

| Blinks | Fault | AOK912 Status |
|--------|-------|---------------|
| 1 | No faults stored | Current (cleared 2026-03-18) |
| 2 | Low voltage / Control module circuit | Was stored; cleared |
| 3 | Normal operating time exceeded | Was stored; cleared |
| 4 | Illogical limit switch signals | Was stored; cleared |
| 5 | Soft top compartment cover locked switch (A25/1s2) | Was stored; cleared |
| 6 | Soft top compartment cover closed switch (A25/1s1) | Was stored; cleared |
| 7 | Soft top storage compartment open switch (S84/5) | Was stored; cleared |

- **Roll bar confirmed operational:** Manual raise/lower via the console button works without problems. The 6 stored codes were stale faults accumulated over time (cleared successfully). A BenzWorld user with a 1992 300SL reported nearly identical codes (2–8) from Pin 7 that would NOT clear — AOK912's clearing to 1 blink confirms the system is healthy.

### Pin 8 — DI/EZL (Ignition System)
- **Before reset:** 17 pulses (single fault code)
- **After reset:** 1 blink (no faults — successfully cleared)

### Pin 9 — ADS (Adaptive Damping System)
- **2026-03-18 (battery <12V):** Weak static glow only — no blink pulses returned
- **2026-03-23 (battery >13V):** **1 blink — no stored fault codes**
- **2026-03-27 (after pump test fault, battery >13V):** **14 blinks — steering angle sensor not initialized**
- **Diagnosis (revised 2026-03-27):** Module is alive and communicating. Code 14 is a soft fault: N51 lost its steering angle sensor (N49) calibration when it shut down after the 2026-03-26 pump test triggered an air/pressure anomaly. The sensor hardware is fine — N51 just needs re-initialization. **Fix:** clear code via Pin 9 reset, start engine, turn steering full lock left → full lock right → center. N51 re-learns sensor endpoints. If Pin 9 then reads 1 blink, system is clean.

**Known ADS I (N51) Blink Codes (partial — from WIS and r129-forum.de):**

| Blinks | Fault | WIS Test Step |
|--------|-------|---------------|
| 1 | No faults stored | — |
| 2 | ADS control module (N51) internal | Replace N51 |
| 3 | Body acceleration sensor (B24) | 23 7.0 |
| 4 | Wheel acceleration sensor (B24/1) | 23 6.0 |
| 5 | Steering angle sensor (N49) | 23 9.0 |
| 6 | Left/right front axle solenoid valve 1 (Y51y1, Y52y1) | 23 14.0, 16.0 |
| 7 | Left/right front axle solenoid valve 2 (Y51y2, Y52y2) | 23 15.0, 17.0 |
| 8 | Left/right rear axle solenoid valve 1 (Y53y1, Y54y1) | 23 12.0 |
| 9 | Left/right rear axle solenoid valve 2 (Y53y2, Y54y2) | 23 13.0 |
| 10–11 | Not for U.S.A. vehicles (Euro-only parameters) | — |
| 12 | Vehicle speed signal (VSS) from ABS/ASR (R129: left front) | 23 4.0 |
| 13 | Oil level switch (S44) — R129 only | 23 18.0 |
| 14 | **Steering angle sensor (N49) not initialized** | 23 10.0 |
| 15 | Comfort/sport switch (S45/1), short circuit | 23 11.0 |
| 17 | Vehicle load sensor (N51/1) | 23 8.0 |
| 18 | ADS MIL (A1e27) | 23 5.0 |
| 19 | Voltage supply too low | 23 1.0 |
| 20 | Steering angle sensor (N49) — continuous fault | 23 9.0 |
| 21 | Voltage supply too high | 23 1.0 |

*Source: WIS DTC reference (W140 M119 1992–95, applicable to R129 N51), confirmed code 13/14/20 via r129-forum.de thread #18606.*

### Pin 10 — RST
- **Before reset:** 11 / 20 / 28 / 29 pulses (four stored fault codes)
- **After reset:** Did not clear after single reset. Required two reset attempts with ignition power cycle between them.
- **Note:** This module is stubborn — power cycle the car between reset attempts.

### Pin 11 — ATA (Anti-Theft Alarm)
- **Before reset:** Static glow (medium intensity) — no blink pulses
- **After reset:** N/A
- **2026-03-23 re-test (>13V):** One of Pin 11 or 12 was re-tested as a sanity check with battery >13V — still static glow, not communicating. Unlike ADS (Pin 9), the ATA/IRCL non-communication is NOT a voltage issue.
- **Diagnosis:** Module present but not generating diagnostic output. May be disabled or in a permanent fault state. Confirmed not a supply voltage issue (unlike ADS which woke up at >13V).

### Pin 12 — IRCL (Infrared Central Lock)
- **Before reset:** Static glow (medium intensity) — no blink pulses
- **After reset:** N/A
- **2026-03-23 note:** See Pin 11 note — one of these two was re-tested at >13V and still showed static glow. The other remains untested at higher voltage.
- **Diagnosis:** Same as ATA — module present but not communicating. Possibly related to the inoperative PSE central locking system. Not a voltage-related issue.

### Pin 14 — ESMC
- **Before reset:** 11 / 12 pulses (two stored fault codes)
- **After reset:** 1 blink (no faults — successfully cleared)
- **Note:** Was in a 2-blink fault state that needed reset

## ABS Diagnostic Availability — NONE on 16-pin X11

**CRITICAL FINDING (2026-03-23):** The early R129 (1991) with M119.960 KE-Jetronic and the 16-pin X11 connector does **NOT** have ABS diagnostic blink codes on any pin. Pin 7 (initially suspected as ABS) is confirmed to be the Roll Bar. ABS diagnostic output was only introduced on the 38-pin X11/14 connector (1993+ models).

The **only** ABS status indicator on this car is the **ABS warning lamp in the instrument cluster.** ABS lamp is **functional** — symbol present, bulb illuminates on ignition-ON bulb check, extinguishes with engine running (= ABS healthy). No action needed.

**1991 Manual Discovery (2026-03-23):** The 1991 owner's manual (correct model year — we were previously referencing the 1990 manual which predates ADS) confirms that **ADS also has a dedicated cluster warning lamp** (page 13 + page 92). This means the original "missing lamp" observation may have been the ADS indicator, not ABS. The ADS cluster lamp should illuminate at ignition position 2 and extinguish with the engine running (page 92). **Needs verification on next ignition-ON bulb check.**

**German Manual Translation — MAJOR SYSTEM CORRECTION (2026-03-23):** The German Betriebsanleitung 1991–1993 describes European ADS as **"Niveauregulierung mit adaptivem Dämpfungs-System (ADS)"** — Level Control WITH Adaptive Damping. Unlike the US manual (damping-only), the European system includes hydraulic ride height control with: tandem pump (A 129 460 07 80, engine-driven, shared with power steering), reservoir (engine bay, next to washer fluid; MB 343.0 / ZH-M fluid), rear proportioning valve with anti-roll bar linkage, and hydraulic lines to shocks.

**CRITICAL: Pin 9 ONLY Monitors Damping, NOT Level Control (2026-03-23):** On ADS I, the system is actually TWO independent subsystems: (A) Adaptive Damping (electronic, monitored by N51 → Pin 9 blink codes) and (B) Niveauregulierung / Level Control (mechanical/hydraulic, NOT monitored by N51). Height sensing on ADS I is MECHANICAL (anti-roll bar linkage to proportioning valve — no electronic sensors). The ADS module has NO visibility into the level control system. **Pin 9 returning 1 blink = damping electronics are healthy. It tells us NOTHING about level control.** The entire hydraulic level control loop can be completely dead (empty reservoir, failed pump section, broken linkage, seized valve) and Pin 9 will still report "1 blink = all good." The only electronic warning for level control is the cluster oil-level float sensor → ADS warning lamp — which is MISSING from this cluster. *(ADS II, 1996+, upgraded to electronic ride height sensors integrated with the module.)*

Confirmed R129 16-pin X11 pin map (1991 M119.960 KE-Jetronic):

| Pin | System | Source |
|-----|--------|--------|
| 1 | Ground (Terminal 31) | Standard |
| 3 | KE (Fuel Injection) | WIS via MBClub UK |
| 6 | SRS (Airbag) | Tested + confirmed |
| 7 | RB (Roll Bar) | WIS + BenzWorld + Motor-Talk confirmed |
| 8 | EZL/AKR (Ignition) | WIS via MBClub UK |
| 9 | ADS (Adaptive **Damping** only — does NOT cover Niveauregulierung/level control) | Tested + confirmed (option 211) |
| 10 | RST (Soft Top) | BenzWorld R129 thread |
| 11 | ATA (Anti-Theft Alarm) | Tested |
| 12 | IRCL (Infrared Central Lock) | Tested |
| 14 | ESMC | Tested + confirmed |
| 16 | +12V (Terminal 15) | Standard |
| — | **ABS: NOT AVAILABLE** | WIS + multiple forum sources |

## Channel Summary for Interface Board Design

| Category | Pins | Count | Interface Requirement |
|----------|------|-------|-----------------------|
| Active blink-code (RX+TX) | 6, 7, 8, 9, 10, 14 | 6 | TLP521 RX opto + TX opto (emitter-follower) + 2N2222 driver |
| Static glow (RX+TX) | 11, 12 | 2 | Same hardware as above; firmware detects static vs. pulsing |
| KE duty-cycle (RX only) | 3 | 1 | TLP521 RX opto only, timer capture for duty-cycle measurement |
| Not fitted | 5, 13 | 2 | No hardware needed |
| Power/Ground | 1, 16 | 2 | Direct connection (fused) |
| **Total optocoupler channels** | | **9 RX + 8 TX = 17** | **Requires 5x TLP521-4 (4-channel arrays)** |

## SPICE Simulation Verification

All channel types have been verified with ngspice 45.2 time-domain simulations:
- **TB1:** Blink read path — 3 pulses correctly received, 31us rise time
- **TB2:** Code clear path — pin pulled to 0.062V, 134us response
- **TB8:** Static glow — optocoupler threshold at 1.21V; all static glow pins read as definite LOW

See `work/nRF5430_interface_board/spice/results/simulation_report.txt` for full results.
