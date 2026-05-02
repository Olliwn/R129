# Cabin Signal Survey

## Purpose

Identify which `R129` vehicle signals are accessible *cabin-side* — at the instrument cluster, the brake/accelerator pedals, the steering column stalk, the center console switch pack, and the door/hood/trunk ajar circuits — so that they can be acquired without going through the engine-bay `nRF54L15`/`nRF5340` instrumentation node.

This document is the companion to:

- [`docs/PH2_2_architecture.md`](PH2_2_architecture.md) — the original four-node architecture (cabin hub, engine-bay node, sentry, trunk battery monitor) is now restructured to **four nodes with the always-on cabin signal node absorbing the sentry**: RPi5 cabin hub, engine-bay sensor node, **always-on cabin signal node (handles cabin signal acquisition + BLE keyless lock/unlock + Pi wake)**, and trunk battery monitor.
- [`docs/nRF5430_Interface_Design.md`](nRF5430_Interface_Design.md) — narrows that board's scope to engine-bay-only signals (X11 blink codes, `EHA`, airflow potentiometer, lambda).
- [`work/cabin_signal_node/README.md`](../work/cabin_signal_node/README.md) — bring-up, BOM cross-reference, and build order for the new node.
- [`docs/R129_Driver_UI_System_Design.md`](R129_Driver_UI_System_Design.md) — the Pi UI now has *two* local data sources (BLE engine node + USB cabin node).

## Why a Cabin Node At All

The original four-node split routes everything through the engine-bay node and back to the Pi over BLE. That is the right choice for under-hood signals that physically have to be acquired in the engine bay (`X11` socket, `EHA` insert harness, airflow pot, lambda integrator at `N3`). It is the wrong choice for signals that already exist *inside the cabin* — speed, RPM-for-tach, brake-light feed, kickdown switch, gear-position lamps, cluster gauge senders, instrument-illumination dimmer, door/hood/trunk ajar, hand-brake switch.

Routing those through the firewall to the engine bay and back over BLE costs:

- BLE bandwidth and latency that the UI-critical signals (speed, brake) cannot afford.
- Engine-bay channel count (the planned `ADS1115` + `74HC4051` already has every channel earmarked for engine signals).
- Extra firewall pass-throughs and extra harness mass.
- Heat exposure: the engine-bay node lives in the `F32` box at under-hood temperature; cabin signals do not need to be acquired there.

A small cabin MCU sitting in the same cubby as the Pi, wired by USB-CDC, eliminates all four costs and keeps the engine-bay node focused on the genuinely under-hood signals.

## Tap Locations

Cabin signals are concentrated at five physical locations. Every signal in the table below comes from one of these.

### 1. Behind the instrument cluster (`A1` connectors `X25` / `X3`)

The cluster is the natural collector for everything the driver normally sees on a gauge or warning lamp. To access these, pull the cluster (planned anyway — see `docs/parts_to_order.md` Priority 3 "Instrument Cluster & Diagnostics" — the cluster has to come out for the missing-`ADS`-warning-lamp investigation, the stuck clock, and the delaminated temperature LCD).

What appears at the cluster connectors:

- `VSS` vehicle speed signal (square wave, ~8 pulses per wheel revolution; shared with cruise control, `RST` rollover module, and the trans control)
- `TD` engine-speed pulse (from `EZL` `N1/3`; same signal already on the `nRF5430` engine-bay tap list, but tappable here without crossing the firewall)
- Coolant-temperature gauge sender (analog, separate from the engine-side `B11/2` `ECT` sensor used by `N3`)
- Fuel level sender (analog, ~0–90 Ω lever-arm float)
- Oil pressure / oil level switches (binary on `1991` cars; oil temperature only on later equipped cars)
- Outside-air temperature sensor (`B14`, analog NTC, runs to the cluster)
- Warning-lamp drive lines: `ADS` warning, `ABS`, `ASR`, alternator, brake-pad-wear, brake fluid low, coolant low, washer low, fuel low, seatbelt
- `KL15` (terminal 15, switched ignition) and `KL58` (illumination dimmer PWM)

### 2. Brake pedal switch (driver footwell)

`S9` brake-light switch sits on a bracket above the brake pedal. It feeds `KL54` (stop-lamp circuit) when pressed. A single tap at the switch connector gives a clean `0 V` / `+12 V` digital signal.

### 3. Accelerator pedal kickdown switch (`S16/3`)

The kickdown switch is a momentary `12 V` switch under the accelerator pedal that closes at full throttle. The signal is routed through the firewall to `N16` (engine systems control module — see `docs/ke_jetronic_system.md` §1) for kickdown-valve activation. **The switch itself is in the cabin** — tap at the switch connector under the pedal, before the firewall, and the signal stays cabin-side.

### 4. Steering column / stalk

- Cruise-control stalk (`Tempomat` — `S40/3`): set, accelerate, decelerate, resume, off — five momentary contacts to `N4/1` (cruise-control module). On `AOK912` the cruise system status is **unknown / probably not present** (see `docs/ke_jetronic_system.md` Pin 7 "no `EA/CC` on KE-Jetronic — expected" diary note 2026-04-XX). Document the tap path; do not commit to wiring it until the stalk is confirmed to be functional.
- Turn-signal / high-beam / wiper stalk: routes through the steering-column switch cluster `S4`, and the relevant lamp-active states reach the cluster anyway, so prefer tapping at the cluster.

### 5. Center console switch pack (already exposed during the console refresh)

Listed in `work/center_console_refresh/README.md` "Switches on the Center Console":

- `ADS` Sport/Comfort
- Hazard
- Rear-window defroster
- Soft-top
- Seat heater L / R
- (`ESP/ASR` Off — only if equipped; verify on `AOK912`)

These are all rocker switches with simple on/off states. Each can be tapped at the connector while the console is already open for the audio + RPi5 cable pull.

### 6. Door / hood / trunk ajar (interior light circuit)

The R129 routes door, hood, and trunk ajar through the interior-light circuit (each switch shorts the lamp ground when the panel is opened). The signals also reach the alarm/`PSE`/`IRCL` controller. Easiest tap is at the interior-light timer relay or at the central-locking controller — both cabin-side.

## Signal Inventory

The table below is the candidate list. Each row's *Owner* column proposes who acquires it: `cabin` (new cabin MCU node), `engine` (existing nRF5430 engine-bay node), `pi-i2c` (direct on the Pi I2C bus), or `defer` (catalogue only, do not wire yet).

| # | Signal | Source / MB ref | Tap location | Class | Conditioning | Owner |
|---|--------|-----------------|--------------|-------|--------------|-------|
| 1 | Vehicle speed `VSS` | `B6` rear-axle Hall sensor → cluster | Cluster `X25` | Pulse, square wave 0/12 V | Divider + clamp + Schmitt or opto, then MCU timer-capture | `cabin` |
| 2 | Engine speed `TD` | `EZL` `N1/3` → cluster tach | Cluster `X25` | Pulse, 0/12 V | Divider + clamp + opto, MCU timer-capture | `cabin` |
| 3 | Brake light feed `KL54` | `S9` brake switch | Switch connector at pedal | Digital 12 V | Divider + opto | `cabin` |
| 4 | Kickdown switch `S16/3` | Accelerator pedal | Switch connector under pedal | Digital 12 V momentary | Divider + opto | `cabin` |
| 5 | Reverse light | Trans selector switch | Reverse-lamp circuit at cluster or kick panel | Digital 12 V | Divider + opto | `cabin` |
| 6 | Hand-brake switch | Console floor switch → cluster lamp | Cluster lamp drive line | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 7 | Coolant temp gauge sender | Cluster sender (separate from `B11/2`) | Cluster `X25` | Analog, ~0–500 Ω NTC to ground | Series R + clamp + RC + ADS1115 | `cabin` |
| 8 | Fuel level sender | Tank float | Cluster `X25` | Analog, ~0–90 Ω lever-arm | Series R + clamp + RC + ADS1115 | `cabin` |
| 9 | Oil pressure switch | Engine sender → cluster | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 10 | Outside air temp `B14` | Front bumper NTC → cluster | Cluster `X25` | Analog, NTC to ground | Series R + clamp + RC + ADS1115 | `cabin` |
| 11 | `KL15` (ignition on) | Any cabin terminal-15 fuse | Cluster pin or `MAIN_5` ignition feed | Digital 12 V | Divider + opto | `cabin` |
| 12 | `KL30` sense (battery presence) | Any cabin terminal-30 fuse | `F19_A` permanent-12V lead at radio harness | Digital 12 V | Divider + opto | `cabin` |
| 13 | `KL58` illumination dimmer | Headlight switch dimmer wheel | Cluster illumination feed | PWM 0–12 V | LDR alternative *or* divider + opto with PWM averaging | `cabin` (open question — see below) |
| 14 | Turn-signal L active | Cluster lamp drive | Cluster `X25` | Digital, blinking 12 V | Divider + opto | `cabin` |
| 15 | Turn-signal R active | Cluster lamp drive | Cluster `X25` | Digital, blinking 12 V | Divider + opto | `cabin` |
| 16 | High-beam indicator | Cluster lamp drive | Cluster `X25` | Digital 12 V | Divider + opto | `cabin` |
| 17 | `ADS` warning lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 18 | `ABS` warning lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 19 | Alternator warning lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 20 | Brake-pad-wear lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 21 | Brake fluid low lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 22 | Coolant low lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 23 | Washer low lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 24 | Fuel low lamp | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 25 | Seatbelt warning | Cluster lamp drive | Cluster `X25` | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 26 | `ADS` Sport/Comfort switch state | Console rocker | Console connector | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 27 | Hazard switch state | Console rocker | Console connector | Digital, blinking 12 V | Divider + opto | `cabin` |
| 28 | Rear-window defroster state | Console rocker | Console connector | Digital 12 V | Divider + opto | `cabin` |
| 29 | Soft-top switch state | Console rocker | Console connector | Digital 12 V | Divider + opto | `cabin` |
| 30 | Seat heater L / R state | Console rocker | Console connector | Digital 12 V | Divider + opto | `defer` (low UI value) |
| 31 | Door L ajar | Door pin switch | Interior-light bus | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 32 | Door R ajar | Door pin switch | Interior-light bus | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 33 | Hood ajar | Hood switch | Alarm/`IRCL` bus | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 34 | Trunk ajar | Trunk switch | Alarm/`IRCL` bus | Digital, switch-to-ground | Pull-up + opto | `cabin` |
| 35 | Cruise-control stalk | `S40/3` | Stalk connector | 5× digital momentary | Pull-up + opto each | `defer` (cruise probably absent on `AOK912`) |
| 36 | Cabin temp + humidity | (new) BME280 | I2C on cabin MCU | Digital I2C | none | `cabin` |
| 37 | Lateral / pitch / yaw `g` | (new) MPU6050 / BMI270 | I2C on cabin MCU | Digital I2C | none | `cabin` |
| 38 | Ambient light | (new) TSL2591 / LDR | I2C or analog | Digital I2C *or* analog | depends | `cabin` |
| 39 | `GPS` position | (new) `u-blox` UART | UART on Pi (already planned) | Digital UART | none | `pi-i2c` (Pi-direct) |
| 40 | PSE lock command **out** | Cabin node → IRCL→PSE wire (or PSE input pin) | Trunk PSE drive board, signal cable from cabin node via passenger-side trim run | Digital output (logic-level GPIO) → 12 V drive at trunk board | Logic GPIO + 1 kΩ series; trunk board has the MOSFET / opto + flyback | `cabin` (BLE keyless) |
| 41 | PSE unlock command **out** | Cabin node → IRCL→PSE wire (or PSE input pin) | Trunk PSE drive board, same cable as row 40 | Digital output (logic-level GPIO) → 12 V drive at trunk board | Logic GPIO + 1 kΩ series; trunk board has the MOSFET / opto + flyback | `cabin` (BLE keyless) |
| 42 | PSE lock-state feedback | PSE controller status output (TBD pin) | Trunk PSE module connector | Digital 12 V *or* switch-to-ground (TBD) | Divider + opto | `cabin` (verify lock command actually executed) |
| 43 | Pi `5 V` enable **out** | Cabin node → high-side switch | High-side switch board (Pi power) | Digital output (logic-level GPIO) → MOSFET high-side | Per `nRF5430_Interface_Design.md` §"Circuit Design: High-Side 12V Switch" Option A or B | `cabin` (Pi wake / shutdown grace) |
| 44 | IRCL → PSE existing signal **in** | IRCL controller output | Trunk, IRCL→PSE harness near IRCL connector | Digital, polarity TBD | Divider + opto | `cabin` (passive monitor — leaves factory IR path intact) |
| — | `X11` blink codes | Engine-bay X11 socket | Engine bay | Bidirectional digital 12 V | Optos per `nRF5430_Interface_Design.md` | `engine` |
| — | `EHA` current `Y1` | Engine-bay insert harness | Engine bay | Analog small DC | Shunt + INA169 | `engine` |
| — | Airflow pot `B2` | Engine-bay airflow meter | Engine bay | Analog 0–5 V | Series R + clamp + RC + ADS1115 | `engine` |
| — | Lambda integrator | `N3` engine-bay | Engine bay | Pulse / duty-cycle 0/12 V | Divider + clamp + opto | `engine` |
| — | Engine `ECT` `B11/2` | At engine | Engine bay | Analog NTC | per `nRF5430` | `engine` |
| — | Battery voltage | Trunk | Trunk | Analog | INA226 | `pi-i2c` (already wired) |
| — | Battery temperature | Trunk | Trunk | Digital 1-wire | DS18B20 | `pi-i2c` (already wired) |

## Ownership Rules of Thumb

- **If the signal physically appears in the cabin, the cabin node owns it.** Even if it could also be tapped at the engine-bay end, the cabin tap avoids the firewall and keeps the engine-bay node lean.
- **If the signal is high-resolution analog and the source is in the engine bay** (airflow pot, `EHA` shunt, engine `ECT`), the engine-bay node owns it. There is no point routing that as a long analog wire into the cabin.
- **If the signal is `I²C` / `1-Wire` / `UART`** and the device is physically next to the Pi or the cabin MCU, prefer the closer node for cable simplicity.
- **The `BLE` link is only used for the engine-bay node.** The cabin node uses USB-CDC because it lives in the same cubby; no wireless link is needed and the wired path is faster, lower-jitter, and lower-power.

## Cabin MCU Hardware

### Decision: `nRF54L15`

The cabin node uses an **`nRF54L15`** — the same MCU family as the engine-bay node — both for ecosystem consistency and because the cabin node also takes over the always-on BLE keyless and Pi-wake functions previously assigned to a separate sentry node (see §"Always-On Operation and BLE Keyless Lock/Unlock" below). Standardizing on `nRF54L15` keeps the project on a single Zephyr/`nrfx` toolchain, a single `FW_nrf/payload/` wire format, and a single Nordic part family across all three Nordic nodes (engine-bay, cabin, and the residual sensor node if/when added).

Rationale:

- Reuses the project's Zephyr toolchain. `FW_nrf/` already builds Zephyr apps and has shared `host_test/` + `payload/` infrastructure. `FW_nrf/payload/r129_payload.h` defines a portable wire format that compiles unchanged on Zephyr and host.
- Native USB-CDC support (the device shows up to the Pi as `/dev/ttyACM0` with no extra drivers).
- Plenty of GPIO for the ~25-signal target plus the PSE drive output and Pi high-side enable output.
- Excellent timer-capture peripherals (GRTC/GPIOTE) for `VSS` and `TD` pulse measurement.
- **Always-on capable** — System OFF / RAM-retention sleep with BLE wake at single-µA standby is ideal for the proximity-unlock use case. The car's `F20_6` permanent-12V circuit can supply a small always-on buck converter without measurable parasitic draw.
- Newest Nordic platform — better roadmap longevity than `nRF52840`.

Candidate boards:

- **Nordic `nRF54L15-DK`** — bench dev with the standard Nordic tooling.
- **Custom `nRF54L15` carrier** — for the in-car install, a small carrier with the protection front-end on the same PCB. Same Veroboard-prototype-then-PCB path as the engine-bay board.

### Why not `RP2040` / `nRF52840`

- `RP2040` (Pi Pico) is cheaper and has excellent `PIO` pulse counting, but it forks the firmware ecosystem away from Nordic / Zephyr and has no BLE — so it cannot do proximity unlock without a separate radio. Rejected for this role.
- `nRF52840` is a perfectly capable alternative and was the original recommendation. Standardizing on `nRF54L15` instead avoids running two different Nordic part families across the three Nordic nodes.

## Always-On Operation and BLE Keyless Lock/Unlock

### Why the cabin node is always-on

`AOK912`'s factory IR remote keys are effectively dead (see [`docs/known_issues.md`](known_issues.md) §"Central Locking (PSE)"): one fob has a hardware-dead IR LED, the other transmits weakly and the car does not respond — likely a rolling-code de-sync that requires MB Star Diagnosis re-pairing (~€200+ dealer visit). Per the 2026-04-06 decision the IR repair has been abandoned in favour of phone-BLE proximity unlock. That work was originally assigned to a separate "always-on sentry" Nordic device (see [`docs/PH2_2_architecture.md`](PH2_2_architecture.md) §3 in the previous architecture revision); since the cabin node now exists and is well-positioned to do exactly this, the sentry's two responsibilities (BLE keyless + Pi wake / high-side switch) **fold into the cabin node**.

The cabin node therefore has three roles:

1. **Always-on (sub-mA standby) BLE proximity scanner** — bonded to the owner's phone, watches RSSI with hysteresis to avoid false triggers from passing-by neighbours.
2. **PSE central-locking driver** — replaces the IRCL → PSE wire with a GPIO + small MOSFET output. Phone proximity → unlock; phone-out-of-range → lock (after a configurable delay).
3. **Pi power-enable / wake controller** — drives the same high-side switch the sentry was going to drive, so the Pi boots on phone approach simultaneously with the car unlocking.

Plus the cabin signal acquisition role described in the rest of this document, which only runs when ignition is on.

### Power: where the always-on supply comes from

- **Source**: `F20_6` (trunk fuse box, 8 A white, position 6, terminal 30 permanent 12 V) — same fuse that already powers `PSE`, `IRCL`, automatic antenna, and trunk light. This is the canonical cabin/trunk permanent-12-V rail.
  - Confirmed `8 A` white torpedo, `permanent_12v: true` per [`r129_data/data/fuse_box.yaml`](../r129_data/data/fuse_box.yaml) `F20_6`.
  - Replaced and verified holding 2026-04-03 after the original aluminium fuse was found blown.
- **Buck**: small automotive `12V → 3.3V` (or `12V → 5V` if a separate `5V` rail is also wanted for the protection front-end's optocoupler LED side) low-Iq buck. Target standby ≤200 µA at the input. Murata `OKI-78SR-3.3` is overkill (its no-load current is ~14 mA); for the always-on path use a low-Iq part such as `TI TPS62840` (60 nA Iq, hard to find) or a `Recom R-78E3.3-0.5` class part with input shutdown via the cabin MCU's wake logic. Decide at bring-up.
- **Routing**: the cabin node lives in the front cubby (alongside the Pi). The permanent-12-V feed has to come *to* the cubby. The cleanest path is along the **same passenger-side trans-tunnel run that already carries the BE2210 tap, USB, and DSP power** — see [`work/center_console_refresh/README.md`](../work/center_console_refresh/README.md) Phase 5. Add one fused 1.5 mm² red wire from `F20_6` (or its tap point at the trunk) to the cubby. **Do not** tap from `F19_A` (radio memory keep-alive) — that fuse is already loaded and adding a node to it complicates parasitic-draw debugging.

### PSE drive: the IRCL → PSE signal wire

Standard R129 PSE controller (`Steuergerät Zentralverriegelung`) accepts lock/unlock commands from three sources: the door key cylinders (mechanical + microswitch), the trunk lock, and the IRCL controller (`Steuergerät Infrarot-Fernbedienung`). The IRCL → PSE link is what we replace.

- **Both modules are physically located in the trunk** (right-side trim, near `F20_6`). The IRCL receiver is the dome on the rear-view-mirror cover that the keys point at; the actual IRCL *controller* is in the trunk.
- **The IRCL → PSE signal wire** runs between those two modules in the right-side trunk trim. Identifying it is the prerequisite to any cabin-node PSE drive — pin number, signal style (sustained 12 V vs momentary pulse vs open-collector), and pulse polarity / duration are all unverified on `AOK912` and must be measured before any drive output is wired up.
- **Tap method (recommended)**: small "PSE drive board" — a single MOSFET / opto + flyback diode + connector — physically located in the right-side trunk trim near IRCL/PSE, taking a low-current GPIO control line from the cabin node back along the existing passenger-side trim run. The cabin node sources only a logic-level signal; the actual current to PSE is sourced locally at the trunk board. This avoids running a long signal wire that's susceptible to noise.
  - Reuse one spare pair of the existing **CAT6 BE2210 tap cable** (`work/center_console_refresh/README.md` §"Wire & connector choice for the tap" reserves the **Brown / White-Brown pair** as `SPARE-DC-1/2`). One conductor = ground, one conductor = PSE drive control from cabin node to trunk board.
- **Alternative tap (deferred)**: drive the PSE controller's input pin directly, bypassing IRCL. Cleaner electrically (no IRCL in the loop) but requires identifying the PSE controller's lock/unlock input pinout, which is a deeper investigation. The IRCL → PSE wire tap above is intentionally the lower-risk first iteration — it leaves the factory IRCL untouched (so the existing key fobs would still work if ever re-paired), and just *adds* a parallel input.

### BLE proximity-unlock logic

- **Bonding**: phone bonds to the cabin node once during initial pairing (long-press a hidden button on the cabin board, follow Nordic's standard bonding flow). LTK stored in flash.
- **Scanning**: cabin node BLE-scans on a duty cycle (e.g. 1 s scan every 5 s) for the phone's resolvable private address. Match → start RSSI tracking.
- **Hysteresis**: unlock when RSSI > −60 dBm for ≥3 consecutive scans; lock when RSSI < −85 dBm or no advert seen for ≥30 s. Tune empirically.
- **Driver-side key linkage**: as separately noted in `known_issues.md`, the driver-side door lock cylinder linkage is currently disconnected. This is independent of the BLE work — when the BLE unlock asserts, the entire car unlocks via the PSE pump, regardless of which cylinder is mechanically connected. The driver-side cylinder repair stays a separate task.
- **Failure mode**: cabin node MCU dies → no BLE unlock → fall back to the working passenger-side mechanical key. (And, eventually, to driver-side key once the linkage is repaired.) Mechanical key always wins.

### Pi wake / high-side switch (sentry function)

The cabin node adds a second GPIO output that drives the high-side MOSFET / relay enabling the Pi's `5 V` rail — same circuit topology as `docs/nRF5430_Interface_Design.md` §"Circuit Design: High-Side 12V Switch" Option A or B. Logic:

- BLE proximity match → assert PSE unlock pulse + assert Pi enable simultaneously. Pi boots while the car unlocks. UI is up by the time the driver is in the seat.
- Door close + KL15 off + RSSI loss → keep Pi enabled for a configurable shutdown grace period (e.g. 60 s) so logs flush, then deassert.
- KL15 on (ignition crank-and-run) → keep Pi enabled regardless of BLE state.

This is the same behaviour the sentry node was originally going to provide; it's just now on the cabin node's MCU.

## Front-End Protection Rules

These mirror `docs/nRF5430_Interface_Design.md` §"The Core Principle: Galvanic Isolation" and §"Front-End Electronics Strategy". No raw 12 V touches the cabin MCU.

### Digital 12 V signals

```
vehicle 12 V signal -> 1 kΩ series R -> opto LED -> opto transistor -> MCU GPIO (with internal pull-up)
                              |
                              v
                          1N4148 clamp + 12 V TVS to GND
```

Optocoupler: `TLP521-4` (DIP-16 four-channel). Already in stock per the `nRF5430` BOM (6× units in inventory) — no new shopping.

### Switch-to-ground signals (most cluster lamp-drive lines)

```
3.3 V via 10 kΩ pull-up -> opto LED anode
                                 |
                                 v
opto LED cathode -> vehicle signal (ground when active)
                                 |
                                 v
opto transistor -> MCU GPIO
```

Same `TLP521-4`, just driven from the 3.3 V side.

### Analog cluster senders

```
sender 0–12 V or 0–5 V -> 4.7 kΩ series R -> 5 V Zener clamp -> 100 nF RC -> ADS1115 input
```

`ADS1115` over I²C to the cabin MCU. `1×` `ADS1115` covers four conditioned analog channels (coolant gauge sender, fuel sender, outside-air temp, one spare). A `74HC4051` mux can extend one ADC channel to 8 slow analog signals if more analog is needed later — same topology as the engine-bay node.

### Pulse signals (`VSS`, `TD`)

```
12 V pulse -> 4.7 kΩ series R -> 5 V Zener clamp -> opto -> MCU timer-capture pin
```

Opto isolation rather than divider-only because both signals are sensitive to ground noise from the alternator and ignition.

### Strip-cut rule

Same Veroboard discipline as the engine-bay board: physically sever the copper tracks underneath the centre of every IC socket so the 12 V car side and the 3.3 V MCU side can never bridge through a stray solder bead.

## Bill of Materials (cross-reference)

Every part needed for the cabin front-end is already on the engine-bay shopping list (`docs/nRF5430_Interface_Design.md` §"SP Elektroniikka Shopping List"). The cabin board reuses the same parts pool:

- 2× `TLP521-4` optos (out of the 6× already in stock — leaves 4× for the engine bay)
- 1× `ADS1115` 16-bit ADC breakout (1× already in stock; order a second for the cabin board)
- 1× `74HC4051` mux (already in stock)
- Resistors / capacitors / 1N4148 / Zener clamps from the existing SparkFun assortments
- **1× `nRF54L15-DK` for bench bring-up + 1× `nRF54L15` module (e.g. `Fanstel BC54L15` once Nordic's first-party module ships) for the in-car install** — same MCU as the engine-bay node, single Zephyr/`nrfx` toolchain
- Pluggable screw terminals from the existing DigiKey order (`1757019` / `1757035` etc.)
- (optional) 1× BME280, 1× MPU6050, 1× TSL2591 — small order, ~€20 total

Always-on / PSE / Pi-wake additions (folded in from the former sentry node):

- 1× low-Iq automotive `12 V → 3.3 V` buck for the cabin node's permanent-12-V supply (target ≤200 µA standby). Candidate: `Recom R-78E3.3-0.5` (~10 µA Iq) or `TI TPS62840` if available.
- 1× **PSE drive board** to live in the trunk near the IRCL/PSE modules: small Veroboard with 1× MOSFET (e.g. `IRLZ44N` or logic-level `2N7000` for low-current loads) or `TLP785` opto with `2N7000` follower, 1× `1N4007` flyback diode, 1× pluggable terminal block, 1× ferrite bead on the control input. Drives whatever signal style the IRCL→PSE wire turns out to be (verify pulse polarity and duration during the door-panel access for the driver-cylinder linkage repair).
- 1× **Pi `5 V` high-side switch** — same circuit as the original sentry plan in [`docs/nRF5430_Interface_Design.md`](nRF5430_Interface_Design.md) §"Circuit Design: High-Side 12V Switch". P-channel logic-level MOSFET (e.g. `IRF9540N` or `AO3401`) + gate-drive transistor + Zener clamp, on the cabin board itself rather than on a separate sentry board.
- 1× automotive in-line fuse holder + 5 A fuse on the new `F20_6` tap.
- 2× 1.5 mm² red wire (~3 m run from `F20_6` tap area to the front cubby) — one for `+12 V`, one for the cabin-node-to-trunk control link (or reuse the spare CAT6 pair as described in §"PSE drive: the IRCL → PSE signal wire").

Net new shopping for the cabin node: ~€60–80 (DK + module + second `ADS1115` + low-Iq buck + PSE drive board parts + ambient sensors). Slightly more than the original `nRF52840`-only estimate because of the always-on supply + PSE drive board, but offset by deleting the standalone sentry-node BOM entirely.

## Signal Path Summary

```
                 ┌──────── cabin signal node (always-on) ─────────────┐
                 │                                                    │
cluster X25 ──────► protection front-end ──┬─► nRF54L15 ──USB-CDC──► RPi5 UI
brake / kickdown ─►                        │       │                 (vehicle_state.py)
console / doors  ─►                        │       │
                 │     ADS1115 (cluster    │       │
                 │     analog senders) ────┘       ├──── BLE radio (always-on, scanning)
                 │                                 │       └──► owner phone (proximity unlock)
                 │     I²C: BME280 / IMU / TSL2591 │
                 │                                 ├──── GPIO out → trunk PSE drive board → IRCL→PSE wire
F20_6 +12 V ─────► low-Iq buck → 3.3 V always-on ──┘                                       (lock / unlock)
                 │                                 ├──── GPIO out → high-side MOSFET → Pi 5 V (wake)
                 └────────────────────────────────────────────────────┘

                 ┌──────── engine-bay node (existing) ─┐
X11 socket ──────►                                     │
EHA insert ──────► protection front-end ──► nRF54L15  ──BLE──► RPi5 UI
airflow B2 ──────►                                     │
lambda / N3 ─────►                                     │
                 └─────────────────────────────────────┘

                 ┌──────── trunk monitor (existing) ───┐
battery + ───────► INA226  ──I²C────────► RPi5 UI
battery temp ────► DS18B20 ──1-Wire────►
                 └─────────────────────────────────────┘

(Standalone sentry node deleted — its BLE-keyless and Pi-wake roles are
now provided by the always-on cabin signal node above.)
```

## Open Questions

- **Cluster connector pinout for `AOK912`**. The car has a confirmed non-`ADS` cluster swap (see `docs/diary/2026-04.md` "April XX entries on the cluster swap"). The pinout needs to be verified against the actually-installed cluster, not the WIS reference for an `ADS`-equipped car. Pull the cluster, photograph the connector backshells, and trace each pin before finalizing the cabin-board harness.
- **`KL58` dimmer strategy**. The illumination feed is PWM at the headlight switch dimmer wheel. Two options: (a) digitize the PWM via opto + MCU timer (gives the driver-set dim level directly); (b) ignore `KL58` and use a `TSL2591` ambient-light sensor instead (gives actual cabin illumination, which is closer to what the Pi display auto-dim wants). Decide at bring-up.
- **`I²C` topology for the ambient sensors**. `BME280` / `MPU6050` / `TSL2591` could hang off either the Pi's I²C-1 bus (simpler) or the cabin MCU's I²C bus (consolidated). Either works. Pi-direct gets the data to the UI faster (no MCU intermediary); MCU-bus consolidates the cabin wiring at one place. Default to MCU-bus unless the bring-up shows a reason to split.
- **USB power-cycle resilience**. The cabin MCU should tolerate Pi reboots cleanly — re-enumerate, reset cleanly, no firmware corruption. This is normal USB-CDC behaviour but needs a smoke test before in-car install.
- **Wire format**. Decide whether the cabin node uses the same `r129_payload.h` framing as the engine-bay node (recommended, for code reuse) or a separate scheme. The framing is transport-agnostic — `SYNC + LEN + TYPE + DATA + CRC16` works equally over USB-CDC and BLE. Recommendation: reuse `r129_payload.h` and add a new `R129_TYPE_CABIN = 0x04` payload type.
- **Cruise-control tap viability**. Cruise is presumed absent on `AOK912` (Pin 7 "no `EA/CC` on KE-Jetronic — expected" diary note). Verify by inspecting the steering column for the cruise stalk, and check `S40/3` connector presence at the column. If absent, drop rows 35 from the cabin-board harness; if present, restore.
- **IRCL → PSE wire signal characteristics**. Polarity (active-high 12 V vs active-low / open-collector pull to ground), pulse duration for lock-vs-unlock, and whether lock and unlock share one wire (with different pulse encodings) or are two separate wires. Measure with the scope at the IRCL connector during a passenger-side mechanical-key actuation (which currently does drive PSE) and during a working-key IR transmission (if any single fob press still elicits a response). This determines the exact gate-drive logic on the trunk-side PSE drive board.
- **Always-on standby budget**. Target is ≤200 µA total at the `F20_6` tap with the cabin node sleeping and BLE-scanning at duty cycle. Verify on the bench before in-car install. The existing `F20_6` baseline (PSE + IRCL + antenna + trunk light) already has its own steady-state load — adding the cabin node should remain in the noise.
- **Proximity hysteresis tuning**. RSSI thresholds for unlock / lock, scan duty cycle, and lock-after-leave delay all need empirical tuning. Risk: false unlock when the owner walks past the parked car on a public street. Default conservative values (RSSI > −55 dBm + ≥3 consecutive scans for unlock) and tune in the diary.
- **Whether to keep the IR keys functional in parallel**. Recommended yes — the IRCL → PSE wire tap is purely additive (the cabin node injects pulses on the same wire), so if the keys are ever re-paired they continue to work. Verify that simultaneous IRCL output + cabin node output cannot produce a conflicting drive (likely fine since both are momentary lock/unlock pulses, but worth scoping).

## Build Order

See [`work/cabin_signal_node/README.md`](../work/cabin_signal_node/README.md) for the staged bring-up plan. In summary:

1. Paper survey + WIS pin-out verification at the cluster + IRCL→PSE wire identification at the trunk module.
2. Bench bring-up of the `nRF54L15` board with USB-CDC heartbeat to the Pi, reusing `FW_nrf/payload/r129_payload.h`.
3. Stage 1 — passive digital cabin signals (brake, reverse, hand-brake, `KL15`, door / hood / trunk ajar).
4. Stage 2 — pulse signals (`VSS`, `TD`) with cross-validation against the engine-bay node's `TD`.
5. Stage 3 — cluster analog senders via `ADS1115`.
6. Stage 4 — cabin ambient (`BME280` / IMU / `TSL2591`).
7. Stage 5 — **Always-on power supply + BLE proximity scanner + Pi `5 V` high-side switch.** Cabin node now stays alive on `F20_6`, scans for the bonded phone, drives the Pi-power MOSFET on approach. (Absorbs the former sentry-node bring-up.)
8. Stage 6 — **PSE central-locking drive.** Trunk-side PSE drive board, control link routed via the existing passenger-side trim run, unlock-on-approach and lock-on-leave wired to the proximity scanner from Stage 5. Replaces the IR remote.
9. Stage 7 — Pi UI integration (extend `UI_rpi5/src/vehicle_state.py` to consume USB-CDC frames in addition to BLE; surface lock state, BLE proximity, and last-unlock-timestamp on the UI).
