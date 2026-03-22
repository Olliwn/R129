# nRF5430 Interface Board — Breadboard Build Instructions

**Project:** AOK912 R129 SL Diagnostics Interface
**Design source:** SPICE netlists in `spice/netlists/` (simulation-verified 2026-03-21)
**Approach:** Incremental staged build — verify each stage before proceeding

---

## Equipment Required

| Item | Purpose |
|------|---------|
| Bench power supply (0–15V, 1A) | Simulate car 12V battery |
| Multimeter (DMM) | DC voltage verification at each stage |
| Oscilloscope | Timing verification, blink waveforms |
| nRF5340 DK | MCU for GPIO control, ADC reading, **and** blink signal generation |

> **No signal generator needed.** The nRF5340 DK itself generates blink-code test
> signals via a spare GPIO + one NPN transistor. See "Car-Side Blink Simulator" below.

---

## Master Bill of Materials

### Power Supply & Protection

| Ref | Component | Value/Part | Package | Qty | Notes |
|-----|-----------|-----------|---------|-----|-------|
| F1 | Blade fuse + holder | 2A | Inline | 1 | Automotive ATO/ATC fuse |
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
| Q_EN | P-channel MOSFET | IRF9540N | TO-220 (TH) | 1 | Breadboard substitute for Si2301 (SOT-23). Vgs_th ≈ −3.5V, Rds_on ≈ 0.117Ω |
| R_GP | Resistor | 100kΩ | 1/4W TH | 1 | Gate pull-up to V_PROT (FET OFF default) |
| R_GATE | Resistor | 10kΩ | 1/4W TH | 1 | Gate series resistor |
| Q_LVL | NPN transistor | 2N2222 or 2N3904 | TO-92 (TH) | 1 | Level shifter for gate drive |
| R_EN | Resistor | 10kΩ | 1/4W TH | 1 | Base drive from MCU DIAG_EN |
| C_DIAG | Electrolytic cap | 100µF/25V | Radial TH | 1 | V_DIAG bulk capacitor |

> **Note on P-FET substitution:** The Si2301 used in simulation is SOT-23 and won't fit
> a breadboard. The IRF9540N is a TO-220 P-FET with similar function but higher Vgs threshold
> (−3.5V vs −1.2V). This means the NPN level shifter must pull the gate to GND (which it does),
> and the 100kΩ pull-up to V_PROT (~11.3V) keeps it firmly OFF. The higher Rds_on is
> negligible at our current levels (~200mA). Verify Vgs_th on your specific part.

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
| U_RX | Optocoupler | TLP521-1 (single) | DIP-4 | 1 | RX path. Use TLP521-4 (DIP-16) to pack 4 channels per IC |
| R_RX | Resistor | 1kΩ | 1/4W TH | 1 | RX current limiting |
| R_PU | Resistor | 13kΩ | 1/4W TH | 1 | MCU-side pull-up to 3.3V |
| U_TX | Optocoupler | TLP521-1 (single) | DIP-4 | 1 | TX path (emitter-follower) |
| R_TX | Resistor | 330Ω | 1/4W TH | 1 | TX LED current limiting |
| R_OC | Resistor | 1kΩ | 1/4W TH | 1 | TX opto collector pull-up to V_DIAG |
| Q_DRV | NPN transistor | 2N2222 | TO-92 (TH) | 1 | TX car-side driver |
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

```
BENCH SUPPLY +12V ──── F1 (2A fuse) ──── D_RPOL (1N4007, anode←input, cathode→V_PROT)
                                                     │
                                                     ├── D_TVS (1.5KE18A, cathode=V_PROT, anode=GND)
                                                     ├── C_IN (100µF, + to V_PROT, − to GND)
                                                     │
                                            ┌────────┴────────┐
                                     ALWAYS-ON PATH     DIAGNOSTICS BUS
                                            │                 │
                                     OKI-78SR-5              Q_EN (P-FET)
                                     pin1=Vin(V_PROT)        Source = V_PROT
                                     pin2=GND                Gate   = gate_node
                                     pin3=Vout(5V)           Drain  = V_DIAG
                                            │                 │
                                     C_5V (100nF)      C_DIAG (100µF)
                                            │                 │
                                     LD1117V33          ┌─────┘
                                     Vin=5V             │
                                     GND=GND     gate_node ── R_GP (100k) ── V_PROT
                                     Vout=3.3V          │
                                            │      R_GATE (10k)
                                     C_3V3 (100nF)      │
                                                   gate_drv
                                                        │
                                                   Q_LVL (NPN 2N2222)
                                                   C = gate_drv
                                                   E = GND
                                                   B ── R_EN (10k) ── MCU DIAG_EN GPIO
```

**LD1117V33 pinout (TO-220, front view, text facing you):**
- Pin 1 (left): GND
- Pin 2 (center): Vout (3.3V)
- Pin 3 (right): Vin (5V)

**OKI-78SR pinout (SIP-3, text facing you):**
- Pin 1 (left): Vin (V_PROT)
- Pin 2 (center): GND
- Pin 3 (right): Vout (5V)

**IRF9540N pinout (TO-220, front view):**
- Pin 1 (left): Gate
- Pin 2 (center): Drain (V_DIAG output)
- Pin 3 (right): Source (V_PROT input)

**2N2222 / 2N3904 pinout (TO-92, flat side facing you):**
- Pin 1 (left): Emitter
- Pin 2 (center): Base
- Pin 3 (right): Collector

#### 1.2 — Breadboard Layout Tips

- Use the breadboard **power rails** for GND (both rails) and 3.3V (one rail).
- Place the OKI-78SR and LD1117V33 near the power input end.
- Run a **thick 22AWG wire** for the V_PROT bus — it carries the full board current.
- Keep the TVS diode close to C_IN (short loop for transient absorption).
- The P-FET and its gate driver circuit can go adjacent to the buck converter.
- Leave the right half of the breadboard empty for Stage 2+.

#### 1.3 — Verification Checklist

| Test | Method | Expected | Tolerance |
|------|--------|----------|-----------|
| V_PROT | DMM across C_IN | 11.3V | ±0.5V (12V minus diode drop) |
| 5V rail | DMM across C_5V | 5.00V | ±0.10V |
| 3.3V rail | DMM across C_3V3 | 3.30V | ±0.05V |
| V_DIAG (DIAG_EN = jumper to 3.3V) | DMM across C_DIAG | ~11.3V | ±0.5V |
| V_DIAG (DIAG_EN = jumper to GND) | DMM across C_DIAG | <0.1V | — |
| No smoke, no hot components | Touch test | Lukewarm | — |
| Current draw (DIAG_EN=LOW) | Bench supply reading | ~15mA | <30mA |
| Current draw (DIAG_EN=HIGH, no load) | Bench supply reading | ~20mA | <50mA |

**Troubleshooting:**
- If 5V is 0V: check OKI-78SR pin order (Vin and Vout are NOT the same as LM7805).
- If 3.3V > 5V: LD1117V33 pins are swapped (common mistake, GND is pin 1 not pin 2).
- If V_DIAG doesn't turn off: P-FET drain/source are swapped. For IRF9540N: Source=V_PROT (higher voltage), Drain=V_DIAG (load side).
- If V_DIAG is always ~0.7V below V_PROT even with DIAG_EN=LOW: body diode is conducting — drain and source are definitely swapped.

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
> GPIOs are 3.3V-compatible. ADC inputs must be on pins that support SAADC.

#### 7.3 — Breadboard Layout Strategy

Use **3 breadboards** arranged side by side:

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  BREADBOARD 1   │  │  BREADBOARD 2   │  │  BREADBOARD 3   │
│                 │  │                 │  │                 │
│  Power Supply   │  │  RX Optos       │  │  TX Optos       │
│  + Enable       │  │  (3× TLP521-4)  │  │  (2× TLP521-4)  │
│  + Analog Cond. │  │  + 9× R_RX      │  │  + 8× R_TX      │
│                 │  │  + 9× R_PU      │  │  + 8× R_OC      │
│  LM358 (DIP-8)  │  │                 │  │  + 8× 2N2222    │
│  Dividers       │  │                 │  │  + 8× R_BP      │
│  Clamp diodes   │  │                 │  │                 │
│  RC filters     │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
    ─────┴────────────────────┴────────────────────┴─────
    GND bus (common), 3.3V bus, V_DIAG bus (all interconnected)
```

**Bus wiring between breadboards:**
- Use **22AWG solid core** for GND, 3.3V, and V_DIAG buses between boards.
- Color code: **Black** = GND, **Red** = V_DIAG (12V switched), **Orange** = 3.3V, **Yellow** = 5V.
- Run the diagnostic pin wires (to car connector) from both BB2 (RX) and BB3 (TX) to a common terminal strip.

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

---

## Common Breadboard Pitfalls

1. **Contact resistance on power rails.** Breadboard contacts add ~0.1–0.5Ω per connection. At 200mA total current, this can cause ground bounce. Use thick wire for power buses and multiple parallel contacts for high-current paths.

2. **Stray capacitance.** Adjacent breadboard rows have ~2–5pF coupling. This is negligible for blink-code timing (0.4s pulses) but can cause ringing on the 2N2222 driver edges. Add a 100pF cap across the base-emitter of Q_DRV if you see ringing on the oscilloscope.

3. **Optocoupler CTR variation.** TLP521 CTR ranges from 50% to 600% across production. Our design works with CTR as low as 50% (verified in simulation). If you see weak MCU_RX signals, check the specific optocoupler's CTR by measuring LED current vs collector current.

4. **LM358 output swing.** The LM358 cannot swing to within 0V of GND on its output — it bottoms out at ~20mV. This is fine for our application (battery voltage is never 0V in operation).

5. **IRF9540N vs Si2301.** The breadboard P-FET (IRF9540N) has a higher gate threshold (−3.5V) than the Si2301 (−1.2V). Our NPN pulls the gate to ~0.2V (Vce_sat), so Vgs ≈ −11V — well beyond either threshold. However, the IRF9540N has higher gate capacitance (~2nF vs ~50pF), so turn-on will be slightly slower (~1ms vs ~91µs). This is not an issue for diagnostics enable/disable.

6. **Decouple every IC.** Place 100nF ceramic caps directly at the power pins of every TLP521-4, the LM358, and the LD1117V33. Short leads, close to the pins.

---

## Testing Progression Summary

| Stage | Components Added | Key Verification | Est. Time |
|-------|-----------------|------------------|-----------|
| 1 | Power + enable (14 components) | 5V, 3.3V, V_DIAG on/off | 1 hour |
| 2 | Single RX channel (3 components) | MCU_RX inverts blink pulse | 30 min |
| 3 | Single TX channel (5 components) | Car pin pulled to <0.5V | 30 min |
| 4 | Battery analog path (8 components) | ADC reads 2.04V at 12V input | 30 min |
| 5 | Airflow analog path (6 components) | ADC reads 1.25V at 2.5V input | 20 min |
| 6 | Combined bidir channel | RX+TX on same pin, both work | 20 min |
| 7 | Full 9 channels + car wiring | All channels read blinks | 2–3 hours |

**Total estimated build time: ~5–6 hours** (including testing at each stage)
