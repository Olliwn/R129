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
| 9 | ADS (Adaptive Damping) | Blink-code | **Static glow (weak)** — module present but not communicating |
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

### Pin 7 — RB
- **Before reset:** 2 / 3 / 4 / 5 / 6 / 7 pulses (six stored fault codes)
- **After reset:** 1 blink (no faults — successfully cleared)

### Pin 8 — DI/EZL (Ignition System)
- **Before reset:** 17 pulses (single fault code)
- **After reset:** 1 blink (no faults — successfully cleared)

### Pin 9 — ADS (Adaptive Damping System)
- **Before reset:** Weak static glow only — no blink pulses returned
- **After reset:** N/A (cannot clear without valid communication)
- **Diagnosis:** ADS control module is not communicating properly. Consistent with earlier failsafe/limp-mode diagnosis. Module may be powered but its internal diagnostic output stage is either faulted or held in an intermediate state.

### Pin 10 — RST
- **Before reset:** 11 / 20 / 28 / 29 pulses (four stored fault codes)
- **After reset:** Did not clear after single reset. Required two reset attempts with ignition power cycle between them.
- **Note:** This module is stubborn — power cycle the car between reset attempts.

### Pin 11 — ATA (Anti-Theft Alarm)
- **Before reset:** Static glow (medium intensity) — no blink pulses
- **After reset:** N/A
- **Diagnosis:** Module present but not generating diagnostic output. May be disabled or in a permanent fault state.

### Pin 12 — IRCL (Infrared Central Lock)
- **Before reset:** Static glow (medium intensity) — no blink pulses
- **After reset:** N/A
- **Diagnosis:** Same as ATA — module present but not communicating. Possibly related to the inoperative PSE central locking system.

### Pin 14 — ESMC
- **Before reset:** 11 / 12 pulses (two stored fault codes)
- **After reset:** 1 blink (no faults — successfully cleared)
- **Note:** Was in a 2-blink fault state that needed reset

## Channel Summary for Interface Board Design

| Category | Pins | Count | Interface Requirement |
|----------|------|-------|-----------------------|
| Active blink-code (RX+TX) | 6, 7, 8, 10, 14 | 5 | TLP521 RX opto + TX opto (emitter-follower) + 2N2222 driver |
| Static glow (RX+TX) | 9, 11, 12 | 3 | Same hardware as above; firmware detects static vs. pulsing |
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
