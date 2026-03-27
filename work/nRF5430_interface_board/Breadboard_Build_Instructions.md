# nRF5430 Interface Board — Breadboard Build Instructions

**Project:** AOK912 R129 SL Diagnostics Interface
**Design source:** SPICE netlists in `spice/netlists/` (simulation-verified 2026-03-21)
**Approach:** Incremental staged build — verify each stage before proceeding

## Parts Availability

All components for the full build are on hand from two orders:

| Source | Order Date | Key Parts |
|--------|-----------|-----------|
| **DigiKey** #98080586 | 17-MAR-2026 | OKI-78SR-5V, LD1117V33, 1.5KE18A TVS, 1N4007, 1N4148, LM358P, resistor/cap/semiconductor kits, breadboards, ADS1115, TXB0108 |
| **SP Elektroniikka** #3044737 | 16-MAR-2026 | IRF5305 P-FET, 6× TLP521-4 optocouplers, 6× 16-pin DIP sockets, 2N3904, 2A fuses + holders, banana plugs, wire, pushbuttons |

**No additional parts need to be ordered. All 7 stages can be built with parts on hand.**

---

## Equipment Required

| Item | Purpose |
|------|---------|
| Bench power supply (0–15V, 1A) | Simulate car 12V battery |
| Multimeter (DMM) | DC voltage verification at each stage |
| Oscilloscope | Timing verification, blink waveforms |
| nRF5340 DK | MCU for GPIO control, ADC reading, **and** blink signal generation |
| USB cable (micro-USB) | Programming/debugging DK on bench (temporary, not needed in car) |

> **No signal generator needed.** The nRF5340 DK itself generates blink-code test
> signals via a spare GPIO + one NPN transistor. See "Car-Side Blink Simulator" below.

> **DK power:** The nRF5340 DK is powered from the interface board's **5V rail**
> (OKI-78SR output), not from USB. In the car there is no USB host — the interface
> board is the sole power source. For bench programming, temporarily connect USB
> alongside the 5V feed (the DK handles dual sources safely via its onboard power
> management). Set DK switch **SW6 = nRF ONLY** to disable the interface MCU and
> save ~5mA when USB is not connected.

---

## Master Bill of Materials

### Power Supply & Protection

| Ref | Component | Value/Part | Package | Qty | Notes |
|-----|-----------|-----------|---------|-----|-------|
| F1 | Blade fuse + holder | 2A, 32V | 19×20mm | 1 | SP Elektroniikka #108113 (fuse) + #100533 (holder) |
| D_RPOL | Rectifier diode | 1N4007 | DO-41 (TH) | 1 | Reverse polarity protection |
| D_TVS | TVS diode | 1.5KE18A | DO-201 (TH) | 1 | Load dump clamp, 15.3V standoff |
| C_IN | Electrolytic cap | 100µF/25V | Radial TH | 1 | Bulk input after protection |
| U_BUCK | DC-DC buck converter | OKI-78SR-5/1.5-W36-C | SIP-3 (TH) | 1 | 12V→5V, plugs into breadboard |
| C_5V | Ceramic cap | 100nF | TH or MLCC | 1 | 5V decoupling |
| U_LDO | LDO regulator | LD1117V33 | TO-220 (TH) | 1 | 5V→3.3V |
| C_3V3 | Ceramic cap | 100nF | TH or MLCC | 1 | 3.3V decoupling |

### Diagnostics Enable Switch

| Ref | Component | Value/Part | Package | Qty | Notes |
|-----|-----------|-----------|---------|-----|-------|
| Q_EN | P-channel MOSFET | IRF5305 | TO-220 (TH) | 1 | SP Elektroniikka #111403. Vds=−55V, Vgs_th ≈ −3V, Rds_on = 0.06Ω |
| R_GP | Resistor | 100kΩ | 1/4W TH | 1 | Gate pull-up to V_PROT (FET OFF default) |
| R_GATE | Resistor | 10kΩ | 1/4W TH | 1 | Gate series resistor |
| Q_LVL | NPN transistor | 2N3904 | TO-92 (TH) | 1 | SP Elektroniikka #108580. Level shifter for gate drive |
| R_EN | Resistor | 10kΩ | 1/4W TH | 1 | Base drive from MCU DIAG_EN |
| C_DIAG | Electrolytic cap | 100µF/25V | Radial TH | 1 | V_DIAG bulk capacitor |

> **P-FET note:** The Si2301 used in simulation is SOT-23 (not breadboard-friendly).
> The IRF5305 from SP Elektroniikka is the breadboard substitute: TO-220 package,
> Vds=−55V (plenty of margin for 11.3V), Rds_on=60mΩ (even lower than Si2301's 110mΩ),
> Vgs_th=−2V to −4V. Our NPN level shifter pulls the gate to ~0.2V giving Vgs ≈ −11V,
> well beyond threshold. The 100kΩ pull-up to V_PROT keeps it firmly OFF when DIAG_EN is LOW.

### Car-Side Blink Simulator (bench testing only)

| Ref | Component | Value/Part | Package | Qty | Notes |
|-----|-----------|-----------|---------|-----|-------|
| Q_SIM | NPN transistor | 2N2222 | TO-92 (TH) | 1 | Simulates ECU open-collector output |
| R_SIM | Resistor | 680Ω | 1/4W TH | 1 | Simulates car ECU pull-up |
| R_SIM_B | Resistor | 10kΩ | 1/4W TH | 1 | Base drive from MCU SIM_BLINK GPIO |

> These parts replace the need for a signal generator. The nRF5340 DK generates
> blink patterns in firmware via SIM_BLINK GPIO → Q_SIM → 12V open-collector output.
> Q_SIM and R_SIM_B can be scavenged from the TX channel spares when no longer needed.

### Diagnostic Channels (per channel)

| Ref | Component | Value/Part | Package | Qty/ch | Notes |
|-----|-----------|-----------|---------|--------|-------|
| U_RX | Optocoupler | TLP521-4 / PC847 | DIP-16 | 1/4 ch | SP Elektroniikka #110515 (6 pcs). Use DIP sockets #SCH29331 |
| R_RX | Resistor | 1kΩ | 1/4W TH | 1 | RX current limiting |
| R_PU | Resistor | 13kΩ | 1/4W TH | 1 | MCU-side pull-up to 3.3V |
| U_TX | Optocoupler | TLP521-4 / PC847 | DIP-16 | 1/4 ch | Same IC as RX (separate channel within the quad package) |
| R_TX | Resistor | 330Ω | 1/4W TH | 1 | TX LED current limiting |
| R_OC | Resistor | 1kΩ | 1/4W TH | 1 | TX opto collector pull-up to V_DIAG |
| Q_DRV | NPN transistor | 2N3904 | TO-92 (TH) | 1 | TX car-side driver (200mA rating, 18mA needed — fine) |
| R_BP | Resistor | 10kΩ | 1/4W TH | 1 | TX base pull-down |

**Channel count:** 8 bidirectional (pins 6–12, 14) + 1 RX-only (pin 3 KE) = 9 total.
Using TLP521-4 quad optocouplers: need 3× for RX (9 channels), 2× for TX (8 channels) = **5× TLP521-4**.

### Analog Conditioning (2 paths)

| Ref | Component | Value/Part | Package | Qty | Notes |
|-----|-----------|-----------|---------|-----|-------|
| U_OPAMP | Dual op-amp | LM358P | DIP-8 (TH) | 1 | Both buffers in one package |
| R_DIV_HI | Resistor | 10kΩ | 1/4W TH | 2 | Upper divider (both paths) |
| R_BAT_LO | Resistor | 2.2kΩ | 1/4W TH | 1 | Battery divider lower |
| R_AIR_LO | Resistor | 10kΩ | 1/4W TH | 1 | Airflow divider lower |
| D_CLAMP | Signal diode | 1N4148 | DO-35 (TH) | 4 | 2 per path (hi + lo clamp) |
| R_BUF | Resistor | 1kΩ | 1/4W TH | 2 | Buffer output series |
| C_FILT | Ceramic cap | 100nF | TH | 2 | RC filter |

### Resistor Totals (for full 9-channel build)

| Value | Qty | Used in |
|-------|-----|---------|
| 330Ω | 8 | TX LED current limit (8 bidir channels) |
| 1kΩ | 20 | RX limit ×9, TX collector ×8, buffer output ×2, misc |
| 2.2kΩ | 1 | Battery divider lower |
| 10kΩ | 14 | TX base pull-down ×8, gate resistor, enable base, dividers ×3, misc |
| 13kΩ | 9 | MCU pull-up (all 9 RX channels) |
| 100kΩ | 1 | P-FET gate pull-up |

---

## Build Stages

### STAGE 1: Power Supply + Enable Switch

**Goal:** Produce stable 5V, 3.3V, and switchable V_DIAG from a 12V bench supply.

#### 1.1 — Wiring

The circuit has three sub-sections. Build them in order, testing each before continuing.

**NET NAMES** used below (label these on the board with a marker):

| Net | Description | Voltage |
|-----|-------------|---------|
| **V_IN** | Raw bench supply input | 12V |
| **V_PROT** | Protected 12V bus (after fuse + diode + TVS) | ~11.3V |
| **5V** | Regulated 5V rail | 5.0V |
| **3V3** | Regulated 3.3V rail | 3.30V |
| **V_DIAG** | Switched 12V diagnostics bus (controlled by Q_EN) | 0V or ~11.3V |
| **gate_node** | P-FET gate, between R_GP and R_GATE | varies |
| **gate_drv** | Junction between R_GATE and Q_LVL collector | varies |
| **GND** | Ground / 0V reference | 0V |

---

**SUB-CIRCUIT A — Input Protection (4 components)**

```
    V_IN                           V_PROT
     │                               │
     │    ┌──────┐    ┌─────────┐    │
     ├────┤ F1   ├────┤ D_RPOL  ├────┤
     │    │ 2A   │    │ 1N4007  │    │
     │    └──────┘    │ A→ │ →K │    ├──── D_TVS (1.5KE18A)
     │                └─────────┘    │    cathode = V_PROT
     │                               │    anode   = GND
     │                               │
     │                          C_IN ┤ + (V_PROT)
     │                       100µF/25V│
     │                               ┤ − (GND)
     │                               │
    GND ──────────────────────────── GND
```

> **Test A:** Apply 12V from bench supply. Measure V_PROT with DMM → expect ~11.3V (one diode drop below 12V).

---

**SUB-CIRCUIT B — Always-On Regulators + DK Power (4 components + DK connection)**

```
    V_PROT                          5V                           3V3
      │                              │                            │
      │   ┌──────────────┐           │   ┌──────────────┐        │
      ├───┤ OKI-78SR-5   ├───────────┤───┤ LD1117V33    ├────────┤
      │   │ pin1=Vin     │           │   │ pin3=Vin(5V) │        │
      │   │ pin2=GND ────┤── GND     │   │ pin1=GND ────┤── GND  │
      │   │ pin3=Vout(5V)│          C_5V │ pin2=Vout    │       C_3V3
      │   └──────────────┘         100nF │ (3.3V)       │      100nF
      │                              │   └──────────────┘        │
      │                              │                           GND
      │                              │
      │                     ┌────────┴────────┐
      │                     │  TO nRF5340 DK  │
      │                     │                 │
      │                     │  5V ──→ P1 "5V" │
      │                     │  GND ─→ P1 "GND"│
      │                     └─────────────────┘
      │                              │
     GND ─────────────────────────  GND (common with DK)
```

**5V rail current budget:**

| Consumer | Current | Notes |
|----------|---------|-------|
| LD1117V33 → 3.3V rail | ~20mA | Opto pull-ups, LM358, gate driver |
| LM358 op-amp (5V direct) | ~1mA | Quiescent |
| nRF5340 DK (SW6 = nRF ONLY) | 30–80mA | Active with BLE; peaks ~100mA during TX |
| **Total from OKI-78SR** | **~50–100mA** | OKI-78SR rated 1.5A — plenty of headroom |

> **Test B:** Measure 5V rail → 5.00V (±0.1V). Measure 3V3 rail → 3.30V (±0.05V).
> **Do NOT connect the DK yet** — verify rails are stable first, then proceed to DK power-up in Test D.

---

**SUB-CIRCUIT C — Diagnostics Enable Switch (6 components)**

```
    V_PROT ──────────────────────────────────── R_GP (100kΩ) ── gate_node
      │                                                             │
      │   IRF5305 (Q_EN)                                       R_GATE (10kΩ)
      │   ┌───────────────┐                                         │
      ├───┤ pin3 = Source  │                                     gate_drv
      │   │               │                                         │
      │   │ pin1 = Gate ──┤────────────────────────────────── gate_node
      │   │               │                                         │
      │   │ pin2 = Drain ─┤──── V_DIAG                     Q_LVL (2N3904)
      │   └───────────────┘       │                         ┌───────────────┐
      │                      C_DIAG ┤ + (V_DIAG)            │ pin3 = C ─────┤── gate_drv
      │                    100µF/25V │                       │ pin1 = E ─────┤── GND
      │                             ┤ − (GND)               │ pin2 = B ─────┤── R_EN (10kΩ)
      │                             │                        └───────────────┘       │
     GND ───────────────────────── GND                                          MCU DIAG_EN
                                                                                (3.3V GPIO)
```

**How it works:**

| MCU DIAG_EN | Q_LVL | gate_node | Q_EN (P-FET) | V_DIAG |
|-------------|-------|-----------|--------------|--------|
| LOW (0V) | OFF | Pulled to V_PROT by R_GP → Vgs ≈ 0V | **OFF** | ~0V |
| HIGH (3.3V) | ON, pulls gate_drv to ~0.2V | ~0.2V → Vgs ≈ −11V | **ON** | ~11.3V |

**Connection checklist for Sub-Circuit C:**

| From | To | Wire / Component |
|------|----|-----------------|
| V_PROT rail | Q_EN pin 3 (Source) | Short wire |
| V_PROT rail | R_GP (100kΩ) one end | Short wire |
| R_GP other end | gate_node row | Resistor spans these two rows |
| gate_node row | Q_EN pin 1 (Gate) | Short wire |
| gate_node row | R_GATE (10kΩ) one end | Short wire |
| R_GATE other end | gate_drv row | Resistor spans these two rows |
| gate_drv row | Q_LVL pin 3 (Collector) | Short wire |
| Q_LVL pin 1 (Emitter) | GND rail | Short wire |
| Q_LVL pin 2 (Base) | R_EN (10kΩ) one end | Short wire |
| R_EN other end | MCU DIAG_EN GPIO | Jumper wire to DK |
| Q_EN pin 2 (Drain) | V_DIAG row | Short wire |
| C_DIAG + leg | V_DIAG row | Observe polarity |
| C_DIAG − leg | GND rail | Observe polarity |

> **Test C:** Jumper DIAG_EN to 3.3V → V_DIAG ≈ 11.3V. Jumper DIAG_EN to GND → V_DIAG < 0.1V.

---

**SUB-CIRCUIT D — nRF5340 DK Power Connection (2 wires)**

```
    Interface Board                              nRF5340 DK
    Proto-Half #1                                (PCA10095)
                                                 ┌─────────────────────┐
    5V rail ─── red wire ──────────────────────→ │ P1 header: "5V" pin │
                                                 │                     │
    GND rail ── black wire ────────────────────→ │ P1 header: "GND" pin│
                                                 │                     │
                                                 │ SW6 = nRF ONLY      │
                                                 │ (push toward "nRF") │
                                                 └─────────────────────┘
```

**nRF5340 DK P1 power header pinout:**

The P1 header is in the Arduino-compatible position (bottom-left of the DK
when the USB connectors face up). Pin assignments:

| P1 Pin | Signal | Connection |
|--------|--------|-----------|
| 1 | NC / IOREF | — |
| 2 | RESET | — |
| 3 | 3V3 | DK output (do NOT connect to board 3.3V) |
| 4 | **5V** | **← Connect interface board 5V rail here** |
| 5 | GND | **← Connect interface board GND here** |
| 6 | GND | Alternative GND (use both for lower resistance) |
| 7 | VIN | — (unused) |
| 8 | — | — |

> **IMPORTANT:** Do NOT connect the interface board's 3.3V rail to P1 pin 3.
> The DK generates its own VDD (3.0V) from the 5V input via its onboard
> buck regulator. Connecting an external 3.3V would fight the DK's regulator.

**DK switch settings for car deployment:**

| Switch | Position | Effect |
|--------|----------|--------|
| **SW6** (nRF ONLY) | **nRF** (toward edge) | Disables interface MCU (J-Link). Saves ~5mA. Required when no USB. |
| SW9 (Power source) | VDD (default) | DK uses onboard VDD regulators fed from 5V domain |

**Connection checklist for Sub-Circuit D:**

| From | To | Wire | Notes |
|------|----|------|-------|
| 5V rail on Proto-Half | DK P1 pin 4 (5V) | Red, 22AWG | Solder to board, DuPont/jumper to DK header |
| GND rail on Proto-Half | DK P1 pin 5 (GND) | Black, 22AWG | Use both pin 5 and pin 6 for lower resistance |

> **Test D (after Tests A, B, C pass):**
>
> 1. Set DK switch SW6 = nRF ONLY
> 2. Disconnect any USB cables from the DK
> 3. Connect 5V and GND wires from the interface board to DK P1
> 4. Apply 12V from bench supply
> 5. Verify: DK power LED (LD5, green) lights up
> 6. Verify: DK current draw adds ~30–50mA to bench supply reading
> 7. Verify: DK VDD (measure on P1 pin 3) ≈ 3.0V (±0.1V)
> 8. If DK doesn't power up: check SW6 position, check SW9 = VDD, check 5V is present

---

**LD1117V33 pinout (TO-220, front view, text facing you):**
- Pin 1 (left): GND
- Pin 2 (center): Vout (3.3V)
- Pin 3 (right): Vin (5V)

**OKI-78SR pinout (SIP-3, text facing you):**
- Pin 1 (left): Vin (V_PROT)
- Pin 2 (center): GND
- Pin 3 (right): Vout (5V)

**IRF5305 pinout (TO-220, front view, text facing you):**
- Pin 1 (left): Gate
- Pin 2 (center): Drain (V_DIAG output)
- Pin 3 (right): Source (V_PROT input)

**2N2222 / 2N3904 pinout (TO-92, flat side facing you):**
- Pin 1 (left): Emitter
- Pin 2 (center): Base
- Pin 3 (right): Collector

#### 1.2 — Board Selection & Layout

**Board:** PTSolns Proto-Half (PTS-00079-201) — solderable perf breadboard.

| Spec | Value |
|------|-------|
| Dimensions | 116.8 × 58.4 mm |
| Tie-points | 450 (2.54mm / 0.1" pitch) |
| Power input | On-board screw terminal **or** 2.1mm barrel jack |
| Power rails | 2× positive, 2× negative, 1× central — all independently configurable |
| Mounting | 4× M3 holes (101.6 × 43.2mm spacing), can be grounded individually |
| Copper | Thick traces, lead-free HASL-RoHS |

> **Why solderable?** The power supply stage carries 100–200mA continuous.
> Soldered joints eliminate the 0.1–0.5Ω contact resistance of solderless
> breadboard spring contacts, preventing ground bounce and voltage drops
> under load. Once verified, the board becomes a permanent, reliable module.

**Layout guidelines:**

- **Power input:** Use the on-board screw terminal for bench supply +12V / GND.
- **Left side** — protection stage: F1, D_RPOL, D_TVS, C_IN. Keep the TVS close to C_IN (short loop for transient absorption).
- **Center** — regulators: OKI-78SR and LD1117V33 with their decoupling caps. Both are SIP-3 / TO-220 and fit standard 2.54mm rows.
- **Right side** — P-FET enable circuit: IRF5305, R_GP, R_GATE, Q_LVL, R_EN, C_DIAG.
- **Power rails:** Assign one positive rail to 5V, one to 3.3V. Use jumper caps (if Deluxe package) or solder bridges to connect/isolate rails as needed.
- **Central rail:** Leave unconnected for now — can be tied to GND later if useful.
- **V_PROT bus:** Run a short, thick solder bridge or wire between the protection output and the OKI-78SR input. This carries full board current.
- **Datasheets:** [Proto-Half Datasheet](https://docs.ptsolns.com/Products/PTS-00079_Proto-Half/Datasheets/Datasheet_PTS-00079_Proto-Half.pdf) — has full pad layout, rail topology, and jumper positions.

#### 1.3 — Verification Checklist

**Phase 1 — Board only (DK not connected):**

| # | Test | Method | Expected | Tolerance |
|---|------|--------|----------|-----------|
| 1 | V_PROT | DMM across C_IN | 11.3V | ±0.5V |
| 2 | 5V rail | DMM across C_5V | 5.00V | ±0.10V |
| 3 | 3.3V rail | DMM across C_3V3 | 3.30V | ±0.05V |
| 4 | V_DIAG ON | Jumper DIAG_EN to 3.3V, DMM across C_DIAG | ~11.3V | ±0.5V |
| 5 | V_DIAG OFF | Jumper DIAG_EN to GND, DMM across C_DIAG | <0.1V | — |
| 6 | Thermal | Touch test all components | Lukewarm | — |
| 7 | Idle current (DIAG_EN=LOW) | Bench supply reading | ~15mA | <30mA |
| 8 | Active current (DIAG_EN=HIGH, no load) | Bench supply reading | ~20mA | <50mA |

**Phase 2 — Connect DK (only after Phase 1 passes):**

| # | Test | Method | Expected | Tolerance |
|---|------|--------|----------|-----------|
| 9 | DK power LED | Set SW6=nRF ONLY, connect 5V+GND to P1, apply 12V | LD5 (green) lights up | — |
| 10 | DK VDD | DMM on P1 pin 3 (3V3 output) | ~3.0V | ±0.1V |
| 11 | Total current (DIAG_EN=LOW) | Bench supply reading | ~45–65mA | <100mA |
| 12 | Total current (DIAG_EN=HIGH) | Bench supply reading | ~50–70mA | <120mA |
| 13 | DK firmware | Flash a simple LED blink via USB, disconnect USB, power from board | LED blinks | — |

**Troubleshooting:**
- If 5V is 0V: check OKI-78SR pin order (Vin and Vout are NOT the same as LM7805).
- If 3.3V > 5V: LD1117V33 pins are swapped (common mistake, GND is pin 1 not pin 2).
- If V_DIAG doesn't turn off: P-FET drain/source are swapped. For IRF5305: Source=V_PROT (higher voltage, pin 3), Drain=V_DIAG (load side, pin 2).
- If V_DIAG is always ~0.7V below V_PROT even with DIAG_EN=LOW: body diode is conducting — drain and source are definitely swapped.
- If DK doesn't power up: verify SW6 = nRF ONLY, SW9 = VDD. Measure 5V at DK P1 pin 4. Check GND continuity between board GND and DK P1 pin 5.
- If DK VDD reads 0V but 5V at P1 is correct: SW9 may be in wrong position (should be VDD, not USB or Li-Po).

---

### Car-Side Blink Simulator (used in Stages 2, 5, 6)

Since there is no signal generator available, the nRF5340 DK generates the blink
test signals itself. One spare GPIO drives a 2N2222 NPN transistor that pulls a
12V diagnostic pin LOW — exactly mimicking the car's ECU open-collector output.

**Circuit:**

```
V_DIAG (+12V switched) ── R_SIM (680Ω) ──┬── DIAG_PIN_SIM
                                           │
                                      Q_SIM (2N2222)
                                      C = DIAG_PIN_SIM
                                      E = GND
                                      B ── R_SIM_B (10kΩ) ── MCU SIM_BLINK GPIO (3.3V output)
```

**Parts needed:** 1× 2N2222 (TO-92), 1× 680Ω, 1× 10kΩ — all already in the master BOM.

**Operation:**
- `SIM_BLINK` GPIO LOW → Q_SIM OFF → DIAG_PIN_SIM at ~12V (idle)
- `SIM_BLINK` GPIO HIGH → Q_SIM ON → DIAG_PIN_SIM pulled to <0.3V (blink)

**Firmware test pattern (pseudocode):**

```c
#define SIM_BLINK_PIN  <spare GPIO>
#define BLINK_ON_MS    400    // 0.4s ON (ECU pulls pin LOW)
#define BLINK_OFF_MS   400    // 0.4s OFF (pin returns to 12V)
#define NUM_BLINKS     3      // typical fault code: 3 blinks

void simulate_blink_code(int num_blinks) {
    for (int i = 0; i < num_blinks; i++) {
        gpio_pin_set(SIM_BLINK_PIN, 1);   // pull LOW (blink)
        k_msleep(BLINK_ON_MS);
        gpio_pin_set(SIM_BLINK_PIN, 0);   // release (idle)
        k_msleep(BLINK_OFF_MS);
    }
}
```

This lets you programmatically test any blink pattern (1–12 pulses, variable timing,
static glow simulation by holding GPIO HIGH continuously, etc.) without external
equipment. The same DK simultaneously reads back the signal on the RX GPIO,
giving a full loopback test.

> **Tip:** Wire the SIM_BLINK output to the same DIAG_PIN_SIM node as the RX
> optocoupler input. This creates a **loopback**: the DK generates a blink on Q_SIM,
> and simultaneously reads it back through the RX opto on MCU_RX. If the received
> pattern matches the transmitted pattern (with inversion), the full RX chain works.

**For Stage 3 (TX test):** No simulator circuit is needed — the MCU directly drives
the TX opto via MCU_TX GPIO. The 680Ω pull-up to 12V acts as the car-side load.

---

### STAGE 2: Single RX Channel (Blink Read)

**Goal:** Read a simulated blink-code signal through one optocoupler to the MCU.

#### 2.1 — Build the Car-Side Blink Simulator

Build the simulator circuit described above. Connect Q_SIM collector + R_SIM (680Ω)
to create the DIAG_PIN_SIM node.

#### 2.2 — RX Optocoupler Wiring

```
DIAG_PIN_SIM ── R_RX (1kΩ) ── TLP521 pin 1 (Anode)
                               TLP521 pin 2 (Cathode) ── GND (car-side)

                               TLP521 pin 4 (Collector) ──┬── R_PU (13kΩ) ── 3.3V
                                                          │
                                                          └── MCU_RX (GPIO input)
                               TLP521 pin 3 (Emitter)  ── GND (MCU-side)
```

**TLP521-1 pinout (DIP-4, dot = pin 1):**
- Pin 1: LED Anode (→ from car via R_RX)
- Pin 2: LED Cathode (→ GND)
- Pin 3: Phototransistor Emitter (→ GND)
- Pin 4: Phototransistor Collector (→ MCU_RX + R_PU)

#### 2.3 — Verification Checklist

| Test | Method | Expected | Tolerance |
|------|--------|----------|-----------|
| MCU_RX when idle (SIM_BLINK LOW) | DMM or scope on MCU_RX | <0.1V (LOW) | <0.5V |
| MCU_RX during blink (SIM_BLINK HIGH) | DMM or scope on MCU_RX | ~3.3V (HIGH) | >2.5V |
| DIAG_PIN_SIM when idle | Scope ch1 | ~12V | >11V |
| DIAG_PIN_SIM during blink | Scope ch1 | <0.3V | <0.5V |
| Loopback test | Firmware: send 3 blinks, count RX edges | 3 rising + 3 falling | exact |
| Waveform timing | Scope: ch1=DIAG_PIN, ch2=MCU_RX | Rise <100µs | — |

**Note on inversion:** The RX path is inverting. Car pin HIGH (12V idle) → opto LED ON → NPN ON → MCU_RX pulled LOW. Car pin LOW (blink) → opto LED OFF → NPN OFF → MCU_RX pulled HIGH by 13kΩ. Firmware must invert the logic.

**Loopback test procedure:** Run `simulate_blink_code(3)` while simultaneously
sampling MCU_RX with a GPIO interrupt or timer capture. Log timestamps. Verify
3 pulses received, timing within 5% of the 400ms/400ms pattern.

---

### STAGE 3: Single TX Channel (Code Clear)

**Goal:** MCU drives a car diagnostic pin LOW through the emitter-follower opto + 2N2222 driver.

#### 3.1 — Car-Side Load

Reuse the 680Ω pull-up from the blink simulator (disconnect Q_SIM for this test,
or just leave SIM_BLINK GPIO LOW so Q_SIM is OFF):

```
V_DIAG (+12V) ── R_LOAD (680Ω) ──┬── DIAG_PIN_SIM
                                   │
                                 (scope probe here)
```

The 680Ω simulates the car's ECU pull-up. When the TX driver activates, it should pull DIAG_PIN_SIM to <0.5V.

#### 3.2 — Wiring

```
MCU_TX GPIO (3.3V) ── R_TX (330Ω) ── TLP521 pin 1 (Anode)
                                      TLP521 pin 2 (Cathode) ── GND (MCU-side)

V_DIAG ── R_OC (1kΩ) ── TLP521 pin 4 (Collector)
                         TLP521 pin 3 (Emitter) ──┬── R_BP (10kΩ) ── GND
                                                   │
                                                   └── Q_DRV Base (2N2222)

DIAG_PIN_SIM ── Q_DRV Collector
                Q_DRV Emitter ── GND
```

**Emitter-follower topology explained:**
- TX opto collector is pulled to V_DIAG (~11.3V) via R_OC
- When opto LED is ON (MCU_TX HIGH), phototransistor conducts
- Emitter follows collector voltage minus Vce_sat → emitter rises to ~2–3V
- This drives Q_DRV (2N2222) base → Q_DRV saturates → pulls car pin to GND
- R_BP (10kΩ) ensures Q_DRV is OFF when opto is OFF

#### 3.3 — Verification Checklist

| Test | Method | Expected | Tolerance |
|------|--------|----------|-----------|
| DIAG_PIN (MCU_TX = LOW) | DMM | ~12V (idle) | >11V |
| DIAG_PIN (MCU_TX = HIGH) | DMM | <0.1V (pulled low) | <0.5V |
| Q_DRV base voltage (MCU_TX HIGH) | DMM | ~2–3V | >1.5V |
| Q_DRV base voltage (MCU_TX LOW) | DMM | <0.1V | <0.5V |
| TX LED current | Calculate: (3.3−1.15)/330 ≈ 6.5mA | ~6.5mA | ±2mA |

**Troubleshooting:**
- If car pin doesn't go low: check Q_DRV is a 2N2222 (not 2N2907 which is PNP). Check E-B-C pinout.
- If car pin goes to ~6V instead of <0.5V: Q_DRV is not saturating. Check R_OC is connected to V_DIAG (not floating), and R_BP is to GND.
- If V_DIAG drops significantly when TX activates: check C_DIAG is installed and P-FET is ON.

---

### STAGE 4: Analog Conditioning (Battery Path)

**Goal:** Scale 12V battery voltage to 0–2.6V for ADC input, with clamping and filtering.

#### 4.1 — Wiring

```
V_DIAG ── R_DIV_HI (10kΩ) ──┬── R_DIV_LO (2.2kΩ) ── GND
                              │
                    bat_div ──┤
                              ├── D_HI (1N4148, anode=bat_div, cathode=3.3V)
                              ├── D_LO (1N4148, anode=GND, cathode=bat_div)
                              │
                              └── LM358 pin 3 (non-inverting input, marked +)

LM358 pin 2 (inverting input, marked −) ── LM358 pin 1 (output)  [feedback wire]
LM358 pin 8 = VCC (3.3V or 5V)
LM358 pin 4 = GND

LM358 pin 1 (output) ── R_BUF (1kΩ) ──┬── C_FILT (100nF) ── GND
                                        │
                                        └── ADC_BAT input (to nRF5340 ADC or ADS1115)
```

**LM358P pinout (DIP-8, dot = pin 1):**
- Pin 1: Output A ← use for battery buffer
- Pin 2: Inverting input A (−)
- Pin 3: Non-inverting input A (+)
- Pin 4: V− (GND)
- Pin 5: Non-inverting input B (+) ← use for airflow buffer
- Pin 6: Inverting input B (−)
- Pin 7: Output B
- Pin 8: V+ (3.3V or 5V supply)

> **Op-amp supply choice:** LM358 works with single supply from 3V to 32V. Use **5V** for supply
> (pin 8 = 5V bus) to get full rail-to-rail at the 0–2.6V output range. With 3.3V supply, the
> output would clip near 2.6V.

#### 4.2 — Verification Checklist

| Test | Method | Expected | Tolerance |
|------|--------|----------|-----------|
| bat_div @ V_DIAG=11.3V (nom 12V input) | DMM at divider midpoint | 2.04V | ±0.1V |
| ADC_BAT @ V_DIAG=11.3V | DMM after RC filter | 2.04V | ±0.1V |
| bat_div @ bench supply = 14.4V | DMM | 2.45V | ±0.1V |
| bat_div @ bench supply = 9V | DMM | 1.50V | ±0.1V |
| D_HI clamp test: set bench to 20V | DMM at bat_div | ~3.3V (clamped) | <3.6V |
| D_LO clamp test: momentarily short input to -1V | DMM at bat_div | ~−0.6V | >−0.7V |

---

### STAGE 5: Analog Conditioning (Airflow Path)

**Goal:** Scale 0–5V potentiometer signal to 0–2.5V for ADC.

#### 5.1 — Wiring

Same as Stage 4 but with different divider:

```
V_AIR (potentiometer wiper, 0–5V) ── R_DIV_HI (10kΩ) ──┬── R_DIV_LO (10kΩ) ── GND
                                                          │
                                                   air_div
                                                          ├── D_HI (1N4148 → 3.3V)
                                                          ├── D_LO (1N4148, GND →)
                                                          │
                                                          └── LM358 pin 5 (+)

LM358 pin 6 (−) ── LM358 pin 7 (output)  [feedback]

LM358 pin 7 ── R_BUF (1kΩ) ──┬── C_FILT (100nF) ── GND
                               │
                               └── ADC_AIR input
```

#### 5.2 — Verification

| Test | Method | Expected |
|------|--------|----------|
| ADC_AIR @ 0V input | DMM | 0.00V |
| ADC_AIR @ 2.5V input | DMM | 1.25V |
| ADC_AIR @ 5.0V input | DMM | 2.50V |

---

### STAGE 6: Full Bidirectional Channel

**Goal:** Combine RX + TX on one diagnostic pin and verify both directions work.

#### 6.1 — Wiring

Connect Stages 2 + 3 to the **same DIAG_PIN_SIM node**:

```
                             ┌── R_RX (1kΩ) → RX opto → MCU_RX
                             │
Bench 12V ── 680Ω ──┬── DIAG_PIN ──┤
                     │              │
              (blink button)        └── Q_DRV collector (from TX path)
                     │
                    GND
```

#### 6.2 — Test Sequence

1. **RX test:** Leave MCU_TX LOW. Press blink button. Verify MCU_RX pulses HIGH.
2. **TX test:** Stop pressing button. Set MCU_TX HIGH for 8 seconds. Verify DIAG_PIN drops to <0.5V.
3. **Isolation test:** During TX (pin pulled low), verify MCU_RX goes HIGH (as expected — pin is low, so opto LED is off, MCU_RX pulled to 3.3V).
4. **Release test:** Set MCU_TX LOW. Verify DIAG_PIN returns to ~12V within 10ms.

---

### STAGE 7: Scale to Full 9 Channels

#### 7.1 — TLP521-4 Quad Optocoupler Mapping

Each TLP521-4 contains 4 independent optocouplers in a DIP-16 package.

**TLP521-4 pinout (DIP-16, dot = pin 1):**

```
        ┌──── U ────┐
  1A  ──┤ 1      16 ├── 4C
  1K  ──┤ 2      15 ├── 4E
  2A  ──┤ 3      14 ├── 3C
  2K  ──┤ 4      13 ├── 3E
  3A  ──┤ 5      12 ├── 2C
  3K  ──┤ 6      11 ├── 2E
  4A  ──┤ 7      10 ├── 1C
  4K  ──┤ 8       9 ├── 1E
        └───────────┘
  A=Anode, K=Cathode, C=Collector, E=Emitter
```

**RX optocoupler allocation (3× TLP521-4):**

| IC | Ch1 | Ch2 | Ch3 | Ch4 |
|----|-----|-----|-----|-----|
| RX_U1 | Pin 6 (SRS) | Pin 7 (RB) | Pin 8 (DI/EZL) | Pin 9 (ADS) |
| RX_U2 | Pin 10 (RST) | Pin 11 (ATA) | Pin 12 (IRCL) | Pin 14 (ESMC) |
| RX_U3 | Pin 3 (KE) | — | — | — |

**TX optocoupler allocation (2× TLP521-4):**

| IC | Ch1 | Ch2 | Ch3 | Ch4 |
|----|-----|-----|-----|-----|
| TX_U1 | Pin 6 (SRS) | Pin 7 (RB) | Pin 8 (DI/EZL) | Pin 9 (ADS) |
| TX_U2 | Pin 10 (RST) | Pin 11 (ATA) | Pin 12 (IRCL) | Pin 14 (ESMC) |

> Pin 3 (KE) is RX-only — no TX optocoupler needed.

#### 7.2 — MCU GPIO Allocation

| Function | GPIO | Direction | Notes |
|----------|------|-----------|-------|
| DIAG_EN | P0.xx | Output | Enable V_DIAG bus |
| SIM_BLINK | P0.xx | Output | Car-side blink simulator (test only) |
| MCU_RX_CH6 | P0.xx | Input | SRS blink read |
| MCU_RX_CH7 | P0.xx | Input | RB blink read |
| MCU_RX_CH8 | P0.xx | Input | DI/EZL blink read |
| MCU_RX_CH9 | P0.xx | Input | ADS static glow |
| MCU_RX_CH10 | P0.xx | Input | RST blink read |
| MCU_RX_CH11 | P0.xx | Input | ATA static glow |
| MCU_RX_CH12 | P0.xx | Input | IRCL static glow |
| MCU_RX_CH14 | P0.xx | Input | ESMC blink read |
| MCU_RX_CH3 | P0.xx | Input | KE duty-cycle |
| MCU_TX_CH6 | P0.xx | Output | SRS code clear |
| MCU_TX_CH7 | P0.xx | Output | RB code clear |
| MCU_TX_CH8 | P0.xx | Output | DI/EZL code clear |
| MCU_TX_CH9 | P0.xx | Output | ADS code clear |
| MCU_TX_CH10 | P0.xx | Output | RST code clear |
| MCU_TX_CH11 | P0.xx | Output | ATA code clear |
| MCU_TX_CH12 | P0.xx | Output | IRCL code clear |
| MCU_TX_CH14 | P0.xx | Output | ESMC code clear |
| ADC_BAT | ADC input | Analog | Battery voltage |
| ADC_AIR | ADC input | Analog | Airflow pot |

**Total GPIOs: 1 (enable) + 1 (sim) + 9 (RX) + 8 (TX) + 2 (ADC) = 21 pins**

> The SIM_BLINK GPIO is only needed during bench testing. When connected to the
> actual car, it can be reassigned or left unconnected.

> Assign specific pin numbers when the nRF5340 DK pin mapping is finalized. All digital
> GPIOs are 3.3V-compatible (DK VDD = 3.0V, pull-ups are 3.3V from LD1117V33 —
> within the 3.6V absolute max for VDD-domain pins). ADC inputs must be on pins
> that support SAADC (P0.04–P0.07, P0.25, P0.26 on nRF5340).
>
> **DK is powered from the interface board's 5V rail** — no USB required in deployment.
> All signal wires + 5V + GND run between Proto-Half #1 and the DK via a wiring harness.

#### 7.3 — Board Layout Strategy

**Board inventory for full build:**

| Board | Type | Assignment |
|-------|------|-----------|
| PTS-00079-201 #1 | Solderable Proto-Half (450 pts) | Power Supply + Enable + Analog Conditioning |
| PTS-00079-201 #2 | Solderable Proto-Half (450 pts) | RX Optos (3× TLP521-4) + TX Optos (2× TLP521-4) |
| BusBoard ST1 ×1–3 | Solderable Stripboard (50×80mm) | Overflow / breakout boards for connectors, test points |

> **Adafruit 5588 is NOT usable** — its 2mm pitch is incompatible with standard 2.54mm through-hole parts.
> **SparkFun 08808** (1" square) — useful as small breakout boards for SOT-23 parts or test jigs.

**Physical arrangement (2 Proto-Half boards + ST1 breakouts):**

```
┌──────────────────────────┐  ┌──────────────────────────┐
│  PROTO-HALF #1           │  │  PROTO-HALF #2           │
│  (116.8 × 58.4 mm)      │  │  (116.8 × 58.4 mm)      │
│                          │  │                          │
│  Power Supply + Enable   │  │  RX Optos (3× TLP521-4) │
│  (Stage 1)               │  │  + 9× R_RX, 9× R_PU    │
│                          │  │                          │
│  Analog Conditioning     │  │  TX Optos (2× TLP521-4) │
│  (Stages 4–5)            │  │  + 8× R_TX, R_OC, R_BP  │
│  LM358, dividers,        │  │  + 8× 2N3904 drivers    │
│  clamp diodes, RC filter │  │                          │
└──────────────────────────┘  └──────────────────────────┘
         │                              │
    ─────┴──────────────────────────────┴─────
    GND bus, 3.3V bus, V_DIAG bus (soldered inter-board wires)
```

**Bus wiring between boards:**
- Solder **22AWG solid core** jumper wires for GND, 3.3V, 5V, and V_DIAG buses between the two Proto-Half boards.
- Color code: **Black** = GND, **Red** = V_DIAG (12V switched), **Orange** = 3.3V, **Yellow** = 5V.
- Run the diagnostic pin wires (to car connector) from Proto-Half #2 to a common terminal strip or banana plug breakout.
- Use M3 standoffs on the mounting holes to stack or mount the boards to a base plate.

---

## Wiring to the Car (X11 16-Pin Diagnostic Connector)

When breadboard testing is complete and you're ready to connect to the R129:

| X11 Pin | ECU | Board Connection | Wire Color (suggested) |
|---------|-----|-----------------|----------------------|
| 1 | Ground | Board GND (car-side) | Black |
| 3 | KE (duty-cycle) | R_RX_CH3 input | White |
| 6 | SRS | DIAG_PIN_CH6 (RX + TX) | Blue |
| 7 | RB | DIAG_PIN_CH7 (RX + TX) | Green |
| 8 | DI/EZL | DIAG_PIN_CH8 (RX + TX) | Yellow |
| 9 | ADS | DIAG_PIN_CH9 (RX + TX) | Orange |
| 10 | RST | DIAG_PIN_CH10 (RX + TX) | Brown |
| 11 | ATA | DIAG_PIN_CH11 (RX + TX) | Red |
| 12 | IRCL | DIAG_PIN_CH12 (RX + TX) | Purple |
| 14 | ESMC | DIAG_PIN_CH14 (RX + TX) | Gray |
| 16 | +12V (from car) | Board V_BAT input via fuse | Red (thick) |

> **SAFETY:** When connecting to the car, **always use the fuse** (F1, 2A) on pin 16.
> The TVS diode protects against transients. Never connect the board to the car
> without the full protection stage (Stage 1) verified and working.
> Test with the bench supply first, then the car with engine OFF, then engine ON.
>
> **Power architecture note:** The Raspberry Pi 5 (cabin display) is powered
> separately from 12V via its own supply (MNK-190 buck module or cigarette
> lighter USB adapter). It does NOT share the interface board's V_PROT bus.
> D_RPOL (1N4007, 1A) only carries interface board + nRF5340 DK current
> (~88mA worst case). Communication between the Pi and the nRF5340 is
> wireless (BLE) — no power or signal wires between cabin and engine bay.

---

## Common Breadboard Pitfalls

1. **Contact resistance on power rails.** Breadboard contacts add ~0.1–0.5Ω per connection. At 200mA total current, this can cause ground bounce. Use thick wire for power buses and multiple parallel contacts for high-current paths.

2. **Stray capacitance.** Adjacent breadboard rows have ~2–5pF coupling. This is negligible for blink-code timing (0.4s pulses) but can cause ringing on the 2N2222 driver edges. Add a 100pF cap across the base-emitter of Q_DRV if you see ringing on the oscilloscope.

3. **Optocoupler CTR variation.** TLP521 CTR ranges from 50% to 600% across production. Our design works with CTR as low as 50% (verified in simulation). If you see weak MCU_RX signals, check the specific optocoupler's CTR by measuring LED current vs collector current.

4. **LM358 output swing.** The LM358 cannot swing to within 0V of GND on its output — it bottoms out at ~20mV. This is fine for our application (battery voltage is never 0V in operation).

5. **IRF5305 vs Si2301.** The breadboard P-FET (IRF5305) has a higher gate threshold (−2V to −4V) than the Si2301 (−1.2V). Our NPN pulls the gate to ~0.2V (Vce_sat), so Vgs ≈ −11V — well beyond either threshold. The IRF5305 has higher gate capacitance (~3.6nF vs ~50pF), so turn-on will be slightly slower (~1–2ms vs ~91µs). This is not an issue for diagnostics enable/disable. The IRF5305 actually has lower Rds_on (60mΩ vs 110mΩ) — a bonus.

6. **Decouple every IC.** Place 100nF ceramic caps directly at the power pins of every TLP521-4, the LM358, and the LD1117V33. Short leads, close to the pins.

7. **DK power from 5V rail.** The nRF5340 DK is powered from the interface board's OKI-78SR 5V output via P1 header. Set SW6 = nRF ONLY when no USB is connected. Do NOT connect the board's 3.3V rail to the DK's 3V3 pin — the DK generates its own 3.0V internally. The DK's GPIO VDD is 3.0V; the board's 3.3V pull-ups are safe (below the 3.6V absolute max).

---

## Testing Progression Summary

| Stage | Components Added | Key Verification | Est. Time |
|-------|-----------------|------------------|-----------|
| 1a | Power + enable (14 components) | 5V, 3.3V, V_DIAG on/off (board only) | 1 hour |
| 1b | DK power connection (2 wires) | DK boots from board 5V, LED blinks | 30 min |
| 2 | Single RX channel (3 components) | MCU_RX inverts blink pulse | 30 min |
| 3 | Single TX channel (5 components) | Car pin pulled to <0.5V | 30 min |
| 4 | Battery analog path (8 components) | ADC reads 2.04V at 12V input | 30 min |
| 5 | Airflow analog path (6 components) | ADC reads 1.25V at 2.5V input | 20 min |
| 6 | Combined bidir channel | RX+TX on same pin, both work | 20 min |
| 7 | Full 9 channels + car wiring | All channels read blinks | 2–3 hours |

**Total estimated build time: ~6–7 hours** (including testing at each stage)
