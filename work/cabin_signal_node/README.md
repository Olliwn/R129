# Cabin Signal Node — Bring-up

## Purpose

Build the always-on cabin node in the `R129` distributed system: a small `nRF54L15` MCU board mounted in or near the front cubby (alongside the RPi5), wired to the Pi over USB-CDC, with three responsibilities:

1. **Cabin signal acquisition** (when ignition is on) — instrument cluster gauge senders + lamp drives, brake and kickdown switches, hand-brake / reverse / door / hood / trunk ajar, console rocker switches, `KL15` / `KL30` / `KL58` references, plus cabin ambient sensors.
2. **BLE proximity-based central locking** (always on) — replaces the dead IR remote keys; bonded phone in proximity → unlocks via `PSE` central-locking system; phone out of range → locks. See [`docs/known_issues.md`](../../docs/known_issues.md) §"Central Locking (PSE)" for the IR-key abandonment decision.
3. **Pi `5 V` power-enable / wake control** (always on) — the high-side switch that brings the Pi up on phone approach and lets it shut down gracefully after the owner leaves.

Roles 2 and 3 were originally on a separate sentry node; they have been folded into this cabin node so that there's exactly one always-on Nordic MCU in the car. Full architectural rationale and the complete signal inventory live in [`docs/cabin_signal_survey.md`](../../docs/cabin_signal_survey.md). This document captures the bring-up tasks, BOM, and stage gates.

## Why a Separate Node (and Not Just More Pi GPIO)

- Pi GPIO is 3.3 V, no analog ADC, vulnerable to noise, and pulled in unhelpful directions during boot. Direct attachment of automotive 12 V signals to the Pi would be unsafe.
- A small dedicated MCU with a protection front-end is the same approach used for the engine-bay node. Reusing the topology keeps protection rules consistent and lets the cabin board reuse the same `TLP521-4` opto + `ADS1115` + clamp parts already in the SP Elektroniikka stock list.
- USB-CDC to the Pi is wired (no BLE), zero-driver (kernel CDC-ACM), low-latency, and naturally power-cycles with the cubby supply rail.

## Architectural Position

```
F20_6 +12V ─► fuse ─► low-Iq buck ─► +3.3 V always-on
                                            │
                ┌─────────────────── cabin signal node (this work) ───────────────────┐
cluster X25/X3 ─►                                                                     │
brake / kickdown ─► protection front-end ──┬─► nRF54L15 ──USB-CDC──►──► RPi5         │
console / doors  ─►                        │       │                  vehicle_state.py
ambient sensors  ─►                        ADS1115 │                                  │
                                                   │                                  │
                                                   ├── BLE radio (always-on, scanning)
                                                   │     phone proximity, RSSI hysteresis
                                                   │
                                                   ├── GPIO out → trunk-side PSE drive board
                                                   │              → IRCL→PSE wire (lock/unlock)
                                                   │
                                                   └── GPIO out → high-side MOSFET → Pi 5 V
                                                                  (wake on approach,
                                                                   shutdown grace after leave)
                └─────────────────────────────────────────────────────────────────────┘

                ┌────────── engine-bay node (existing) ──────────────┐
X11 / EHA / B2 ─► protection ─► nRF54L15/nRF5340 ──BLE─────────────►┤
                └────────────────────────────────────────────────────┘
                                                                    │
                ┌────────── trunk monitor (existing) ────────────────┤
INA226 + DS18B20 ─────────────────────────I²C / 1-Wire──────────────►
                └────────────────────────────────────────────────────┘

(Standalone sentry node deleted — its BLE-keyless and Pi-wake roles are
now provided by the always-on cabin signal node above.)
```

## MCU Choice

**`nRF54L15`** — same MCU family as the engine-bay node. Standardizing on this part across the project keeps everything on one Zephyr/`nrfx` toolchain, one `FW_nrf/payload/` wire format, and a single Nordic SDK version.

For bench bring-up: `nRF54L15-DK`. For the in-car install: a small `nRF54L15` module on a custom carrier with the protection front-end and the always-on / PSE / Pi-wake outputs on the same board. Same Veroboard-prototype-then-PCB path as the engine-bay board.

Why not `nRF52840` (the original recommendation): only reason was tooling convenience. With `nRF54L15` already chosen for the engine-bay node, picking it for the cabin node too eliminates running two Nordic part families in parallel.

Why not `RP2040` / `Pi Pico`: no BLE radio — would need a separate radio for proximity unlock — and forks the firmware ecosystem off Zephyr. Rejected.

Full rationale and alternatives in `docs/cabin_signal_survey.md` §"Cabin MCU Hardware".

## Bill of Materials

Most parts are already in stock per the engine-bay node's `docs/nRF5430_Interface_Design.md` SP Elektroniikka shopping list. Only the items marked *new* are net-additional.

### Core cabin-signal-acquisition parts

| # | Component | Part / Ref | Qty | Source | Notes |
|---|-----------|------------|-----|--------|-------|
| 1 | Cabin MCU dev kit | Nordic `nRF54L15-DK` | 1 | new (~€60) | Bench bring-up; same DK family as engine bay |
| 1b | Cabin MCU production module | `nRF54L15` carrier (TBD — Fanstel module or custom) | 1 | new (~€20–35) | In-car install on Veroboard / PCB |
| 2 | Optocoupler array | `TLP521-4` DIP-16 | 2 | in stock | 2 of the 6 already procured (4 channels each → 8 channels total) |
| 3 | Analog ADC | `ADS1115` 16-bit 4-channel | 1 | new (~€5) | Engine bay already uses 1× from stock; order one more |
| 4 | Analog mux | `74HC4051` (`CD74HC4051E`) | 1 | in stock | Optional — only if more than 4 conditioned analog channels needed |
| 5 | Cabin temp/humidity/pressure | `BME280` breakout | 1 | new (~€5) | I²C, on cabin MCU bus |
| 6 | IMU | `MPU6050` *or* `BMI270` breakout | 1 | new (~€5) | I²C, lateral g + pitch/yaw |
| 7 | Ambient light | `TSL2591` breakout *or* analog LDR | 1 | new (~€5) | For Pi display auto-dim |
| 8 | Resistors | 1 kΩ, 4.7 kΩ, 10 kΩ from SparkFun assortment | qty | in stock | Series + pull-up |
| 9 | Diodes | `1N4148` clamp, 5 V Zener | qty | in stock | Per-input clamp |
| 10 | TVS | `1.5KE18A` | 2 | in stock | Vehicle-side surge protection |
| 11 | IC sockets | 16-pin machined "Holkkikanta" | 2 | in stock | One per `TLP521-4` |
| 12 | Veroboard / proto PCB | SparkFun general-purpose, etc. | 1 | in stock | From DigiKey order |
| 13 | Pluggable screw terminals | `1757019` / `1786404` (2-pos) and `1757035` / `1786420` (4-pos), 5.08 mm pitch | qty | in stock | Vehicle-side connector pluggables |
| 14 | Header pins | 4-pos vertical 2.54 mm | qty | in stock | MCU breakout |
| 15 | Cable to vehicle harness | 24 AWG signal wire | ~5 m | in stock | One conductor per signal + grounds |
| 16 | USB-C to USB-A cable, 30 cm | — | 1 | new (~€3) | MCU → Pi USB-A port |

### Always-on power supply (new — was on the deleted sentry node)

| # | Component | Part / Ref | Qty | Source | Notes |
|---|-----------|------------|-----|--------|-------|
| A1 | Low-Iq buck `12 V → 3.3 V` | `Recom R-78E3.3-0.5` (~10 µA Iq) *or* `TI TPS62840` SMD if available | 1 | new (~€8) | Powers the cabin node from `F20_6` permanent 12 V; target ≤200 µA standby |
| A2 | In-line fuse holder | ATO blade in-line | 1 | new (~€3) | On the new `F20_6` tap before the buck |
| A3 | ATO 5 A fuse | — | 2 | new (~€1) | Holder + spare |
| A4 | Permanent-12V wire | 1.5 mm² red, ~3 m | qty | in stock | `F20_6` to front cubby along the passenger-side trim run |
| A5 | Reverse-polarity / TVS protection | `SS24` Schottky + `SMBJ18A` TVS at the input | 1 | in stock | Standard automotive front-end |

### PSE central-locking drive board (new — trunk-side, replaces IR remote function)

Lives in the trunk near the IRCL/PSE controllers. Driven from the cabin node by a single logic-level control wire run along the existing passenger-side cable bundle (one spare CAT6 pair from the BE2210 tap, see [`work/center_console_refresh/README.md`](../center_console_refresh/README.md)).

| # | Component | Part / Ref | Qty | Source | Notes |
|---|-----------|------------|-----|--------|-------|
| P1 | Control opto + low-side switch | `TLP785` opto + `2N7000` SOT-23 logic-level MOSFET | 1 each | in stock + new | Galvanic isolation from cabin to trunk + low-current 12 V drive of IRCL→PSE wire |
| P2 | Flyback diode | `1N4007` | 1 | in stock | Across the load (PSE controller's input is likely capacitive but include for safety) |
| P3 | Pull-up / pull-down resistors | 10 kΩ, 1 kΩ | qty | in stock | Default-deassert on power loss |
| P4 | Ferrite bead on control input | BLM18 series | 1 | in stock | Common-mode noise suppression on the long control wire |
| P5 | Pluggable screw terminals | 2-pos and 3-pos, 5.08 mm pitch | 2 | in stock | Cabin-side control + vehicle-side IRCL→PSE tap-in |
| P6 | Veroboard for the trunk drive board | small offcut | 1 | in stock | ~30 × 25 mm enough |
| P7 | Heat-shrink + small ABS enclosure | — | 1 | in stock | Mount in the right-rear trim near the IRCL controller |

### Pi `5 V` high-side switch (new — was on the deleted sentry node)

Mounted on the cabin board itself. Same circuit topology as [`docs/nRF5430_Interface_Design.md`](../../docs/nRF5430_Interface_Design.md) §"Circuit Design: High-Side 12V Switch" Option A or B.

| # | Component | Part / Ref | Qty | Source | Notes |
|---|-----------|------------|-----|--------|-------|
| H1 | P-channel logic-level MOSFET | `IRF9540N` *or* `AO3401` (SMD) | 1 | new (~€2) | High-side switch for Pi `5 V` rail |
| H2 | Gate-drive transistor | `2N3904` | 1 | in stock | Logic-level GPIO pulls gate low to enable |
| H3 | Gate Zener | 12 V Zener | 1 | in stock | Vgs clamp |
| H4 | Source/drain bulk capacitor | 100 µF / 25 V | 1 | in stock | Inrush smoothing |
| H5 | Reverse-polarity protection | `SS24` Schottky | 1 | in stock | Already in `H1` package alternative |

**Net-new cost (rough): ~€100** (DK + module + low-Iq buck + PSE drive board parts + high-side switch + ambient sensors + USB cable). Slightly more than the original `nRF52840`-only estimate, but **offset by deleting the entire standalone sentry-node BOM** that would otherwise have been spent. Net delta vs. the original four-node plan is small.

## Front-End Protection (Summary)

Full protection rules are in `docs/cabin_signal_survey.md` §"Front-End Protection Rules". The cabin board mirrors the engine-bay board topology exactly:

```
12 V digital  →  1 kΩ series  →  TLP521-4 LED  →  TLP521-4 Tx  →  MCU GPIO (with 3.3 V pull-up)
                                                                     ↑
                                                          1N4148 + Zener clamp to 3.3 V

switch-to-GND →  3.3 V via 10 kΩ pull-up  →  TLP521-4 LED anode
                                                cathode → vehicle signal (ground when active)
                                                Tx → MCU GPIO

analog sender →  4.7 kΩ series  →  5 V Zener clamp  →  100 nF RC  →  ADS1115 input

12 V pulse   →  4.7 kΩ series  →  5 V Zener clamp  →  TLP521-4  →  MCU timer-capture pin
```

**Strip-cut rule (Veroboard build):** physically sever the copper tracks underneath the centre of every IC socket so the 12 V vehicle side and the 3.3 V MCU side cannot bridge through a stray solder bead. Same rule as the engine-bay board.

## Wire Format

Reuses [`FW_nrf/payload/r129_payload.h`](../../FW_nrf/payload/r129_payload.h) framing:

```
SYNC (0xAE) | LEN | TYPE | DATA[LEN] | CRC16-CCITT-FALSE
```

Add a new payload type:

```c
#define R129_TYPE_CABIN  0x04   /* cabin signal node frame */
```

Cabin frame `DATA` payload (proposal, to refine during bring-up):

```c
typedef struct {
    uint32_t uptime_ms;       /* le, MCU uptime since reset */
    uint32_t digital_bits;    /* le, bit per digital signal (see signal_id_t enum) */
    uint16_t vss_pulse_hz;    /* le, last 100 ms pulse rate */
    uint16_t td_pulse_hz;     /* le, last 100 ms pulse rate */
    int16_t  ads_a0;          /* le, raw ADS1115 ch0 (coolant gauge sender) */
    int16_t  ads_a1;          /* le, raw ADS1115 ch1 (fuel sender) */
    int16_t  ads_a2;          /* le, raw ADS1115 ch2 (outside-air temp) */
    int16_t  ads_a3;          /* le, raw ADS1115 ch3 (spare) */
    int16_t  cabin_temp_c100; /* le, BME280 temp in 0.01 °C */
    uint16_t cabin_rh_pct100; /* le, BME280 humidity in 0.01 % */
    int16_t  imu_ax_mg;       /* le, lateral g in milli-g */
    int16_t  imu_ay_mg;       /* le, longitudinal g in milli-g */
    int16_t  imu_az_mg;       /* le, vertical g in milli-g */
    uint16_t lux;             /* le, ambient light in lux */
    /* always-on / BLE keyless / Pi-wake fields (Stages 7–8) */
    uint8_t  lock_state;      /* 0 = unknown, 1 = unlocked, 2 = locked, 3 = transition */
    uint8_t  proximity_state; /* 0 = no phone seen, 1 = far, 2 = near, 3 = bonded-and-active */
    int8_t   phone_rssi_dbm;  /* last seen RSSI (-128 = no phone) */
    uint8_t  pi_power_state;  /* 0 = off, 1 = grace-period, 2 = on */
    uint32_t last_unlock_ms;  /* le, MCU uptime at last unlock command (0 = never) */
    uint32_t last_lock_ms;    /* le, MCU uptime at last lock command (0 = never) */
} r129_cabin_t;
```

Frame rate target: 10 Hz. Nominal frame size: ~50 bytes per frame, ~500 B/s — trivial for USB-CDC.

## Build Stages

### Stage 0 — Paper survey + cluster pin-out verification

- [ ] Read `docs/cabin_signal_survey.md` end-to-end and confirm the signal table matches what is actually wanted.
- [ ] Pull the instrument cluster (already on the Priority 3 task list per `docs/parts_to_order.md`). Photograph the connector backshells front and back.
- [ ] Cross-reference cluster pin-out against WIS for the actually-installed cluster (the car has a confirmed non-`ADS` cluster swap — do not blindly trust `ADS`-equipped diagrams).
- [ ] Annotate the photo with each pin's signal name, expected resting voltage, expected active voltage, and the cabin-board input class (digital 12 V / switch-to-ground / analog / pulse).
- [ ] Trace the brake-light switch (`S9`) connector and the kickdown switch (`S16/3`) connector — easy enough to do under-dash without removing anything else.
- [ ] Resolve the cruise-control open question (`S40/3` connector present or not).
- [ ] **IRCL → PSE wire identification (trunk).** With the right-rear trim already opened (or during the next access for any other trunk task), photograph the IRCL controller connector and the `PSE` controller connector. Identify the IRCL→PSE signal wire(s). Probe with the scope while actuating the working passenger-side mechanical key — that key reliably triggers PSE today, so the IRCL output line should pulse simultaneously. Record polarity (active-high 12 V vs active-low / open-collector), pulse duration for lock vs unlock, and whether one wire encodes both directions (different pulse durations) or two separate wires exist.
- [ ] **Driver-cylinder linkage repair window (opportunistic).** The driver-side door key cylinder linkage is currently disconnected ([`docs/known_issues.md`](../../docs/known_issues.md) §"Central Locking (PSE)"). If the door panel is removed for any reason during this stage, take the opportunity to inspect and reconnect the linkage. Independent of the BLE work but covered by the same trim-removal task.

**Exit criteria:** Every signal in `docs/cabin_signal_survey.md` table that's owned by the cabin node has a confirmed tap-point pin number. The IRCL → PSE wire is positively identified, with measured polarity and pulse-duration values recorded in the diary.

### Stage 1 — Bench MCU bring-up + USB-CDC heartbeat

- [ ] Procure the `nRF54L15-DK` for bench bring-up. Identify a target production module / carrier (Fanstel module, Nordic reference, or custom PCB) for the in-car install.
- [ ] Stand up a Zephyr project (mirror `FW_nrf/app/` structure). Vendor `FW_nrf/payload/r129_payload.h` and `r129_payload.c` unchanged.
- [ ] Implement a 1 Hz USB-CDC heartbeat: `R129_TYPE_HEARTBEAT` frames containing uptime + counter, identical to the BLE engine-node heartbeat.
- [ ] On the Pi, write a small Python USB-CDC reader that decodes frames and prints them. Reuse the wire-format spec; consider extracting a shared Python decoder.
- [ ] Confirm the cabin node enumerates as `/dev/ttyACM*`, the Pi can read it, and Pi reboots cleanly disconnect/reconnect without hanging the MCU.

**Exit criteria:** Heartbeat frames flow Pi-side at 1 Hz with no dropped or corrupted frames over a one-hour soak.

### Stage 2 — Passive digital cabin signals

The lowest-risk first batch — all simple optocoupled `0`/`12 V` inputs.

- [ ] Build the protection front-end on Veroboard (strip-cut rule applied). 8 channels in the first pass.
- [ ] Wire to: brake (`KL54`), reverse light, hand-brake, `KL15`, door L, door R, hood, trunk.
- [ ] Map each input to an MCU GPIO.
- [ ] Extend the cabin frame's `digital_bits` field with one bit per signal.
- [ ] Verify on the bench with a `12 V` bench supply: each channel asserts and de-asserts cleanly with the expected polarity.
- [ ] In-car test: confirm brake-light toggle when pedal pressed, door-ajar bits track door open/close, etc.

**Exit criteria:** All 8 digital signals readable in real-time on the Pi side. Cross-check against the diary entries that document each switch's known state (e.g. brake switch verified working during the BE2210 install).

### Stage 3 — Pulse signals (`VSS`, `TD`)

- [ ] Add two more opto channels routed to MCU timer-capture pins.
- [ ] Implement Zephyr counter / GPIOTE-based pulse-rate measurement at 100 ms windows.
- [ ] Cross-validate `TD` against the engine-bay node's `TD` reading (both nodes should report the same RPM within a few percent).
- [ ] Cross-validate `VSS` against the cluster odometer — drive a known distance and confirm the integrated pulse count matches.

**Exit criteria:** `vss_pulse_hz` and `td_pulse_hz` track real driving conditions on a short test drive.

### Stage 4 — Cluster analog senders

- [ ] Add `ADS1115` to the cabin board's I²C bus.
- [ ] Wire 4 conditioned analog inputs: coolant gauge sender, fuel level sender, outside-air temp, one spare.
- [ ] Calibrate against the cluster gauge readings (the cluster gauge itself is the easiest reference for "this is the right sender voltage range").
- [ ] (Optional) Add `74HC4051` mux for additional slow analog channels if the spare gets used up.

**Exit criteria:** Cabin frame's `ads_a0..a3` track real sender voltages and can be calibrated to engineering units (°C, % fuel, °C OAT).

### Stage 5 — Cabin ambient sensors

- [ ] Add `BME280` (cabin temp/humidity/pressure), `MPU6050` or `BMI270` (IMU), `TSL2591` (ambient light) to the cabin MCU's I²C bus.
- [ ] Decide whether ambient sensors stay on the MCU bus (consolidated wiring) or move to the Pi I²C-1 bus (one less hop). Default: MCU bus.
- [ ] Verify temperature, humidity, pressure, lateral-g, ambient-lux all populate the cabin frame at 10 Hz.

**Exit criteria:** All ambient fields plausible at rest and during a short test drive.

### Stage 6 — Always-on power supply + BLE proximity scanner + Pi `5 V` high-side switch

This stage absorbs what was originally going to be the standalone sentry-node bring-up.

- [ ] Build the always-on power section on the cabin Veroboard: `F20_6` tap → in-line fuse → reverse-polarity protection → low-Iq buck → 3.3 V always-on rail. Smoke-test on the bench with a 12 V supply and confirm steady-state input current ≤200 µA with the MCU asleep.
- [ ] Run the new permanent-12-V wire from `F20_6` to the front cubby along the existing passenger-side trim run (same path used by the BE2210 tap and DSP power — see `work/center_console_refresh/README.md`).
- [ ] Implement Zephyr System OFF / RAM-retention sleep with periodic BLE scan wake (e.g. 1 s scan every 5 s while idle).
- [ ] Implement phone bonding flow: long-press the on-board "bond" button, accept pairing on the phone, store LTK in flash. Test re-bonding after `nrf` reflash. (One-time setup.)
- [ ] Implement RSSI-based proximity state machine with hysteresis: `unlock` requires RSSI > −60 dBm sustained ≥3 scans; `lock` requires RSSI < −85 dBm or no advert seen for ≥30 s. Tune in the diary as part of in-car testing.
- [ ] Build the Pi `5 V` high-side switch on the cabin board. Wire its enable input to a cabin-node GPIO. Stage 6 success is measured *without* the PSE drive yet — just confirm phone-approach turns the Pi on and phone-leave turns it off after the grace period.
- [ ] Verify ignition on (`KL15`) overrides the proximity logic: while the engine is running, the Pi stays on regardless of phone state. (KL15 sense already wired in Stage 2.)

**Exit criteria:**

1. Cabin node runs ≥48 h on the bench off a 12 V supply with measured average input current ≤200 µA and BLE scanning continuously.
2. Phone approach reliably triggers the Pi `5 V` rail within ≤5 s.
3. Phone leave reliably drops the Pi `5 V` rail after the configured grace period.
4. No false unlocks / wakes from neighbouring BLE devices in a one-week monitoring period parked outdoors.

### Stage 7 — PSE central-locking drive

- [ ] Build the trunk-side PSE drive board (BOM section §"PSE central-locking drive board"). Bench-test by toggling its control input with a 3.3 V signal generator — confirm the output drives the load (use a 12 V LED + 1 kΩ resistor as a proxy for the IRCL→PSE wire) cleanly without ringing.
- [ ] Identify the spare CAT6 pair to use for the cabin → trunk control link. Default: the `SPARE-DC-1/2` pair from `work/center_console_refresh/README.md` §"Wire & connector choice for the tap" (Brown / White-Brown). Document the pair selection.
- [ ] Install the trunk drive board in the right-rear trim near the IRCL controller. Tap onto the IRCL → PSE wire identified in Stage 0 in *parallel* with the existing IRCL output (so factory IR keys, if ever revived, continue to work).
- [ ] Wire one cabin GPIO → trunk drive board control input via the chosen CAT6 pair.
- [ ] Implement Zephyr-side lock/unlock pulse generator. Use the polarity / pulse-duration values measured in Stage 0. Default behaviour: on proximity-unlock state machine entering `unlocked`, fire one unlock pulse and update `last_unlock_ms`; on entering `locked`, fire one lock pulse and update `last_lock_ms`.
- [ ] In-car test: walk away from the parked car with the phone → lock fires (audible PSE pump). Walk back → unlock fires.
- [ ] Add cabin-side input monitoring on the IRCL → PSE wire (signal #44 in the survey table) to confirm the cabin node's own pulses are received correctly + to coexist with any future re-paired IR key without conflict.

**Exit criteria:** Phone-proximity lock and unlock both work reliably for ≥1 week of daily driving without missed events or false triggers. Mechanical passenger-side key still works as a fallback.

### Stage 8 — Pi UI integration

- [ ] Extend `UI_rpi5/src/vehicle_state.py` to subscribe to the USB-CDC stream alongside the BLE engine stream.
- [ ] Add a `CabinDataProvider` mirroring whatever provider already exists for the BLE engine node (or the simulator). Frames decode through the same `r129_payload` decoder.
- [ ] Wire a few cabin signals into the existing UI views: brake state into the gauge view, lateral-g into the home wireframe view as a body-roll cue, ambient lux into the display brightness controller.
- [ ] Surface the new always-on / lock / proximity fields on the UI: lock state indicator, BLE proximity bars, "last unlocked at HH:MM" / "last locked at HH:MM" lines on the home view.
- [ ] Confirm the UI degrades gracefully if the cabin node disappears (USB unplugged) — UI continues, "no cabin data" indicator surfaces but nothing else breaks. **Note**: the cabin node will normally still be alive even when the Pi reboots, since they're on independent power rails. USB re-enumeration on Pi reboot must be smoke-tested.

**Exit criteria:** Pi UI shows live cabin data — including lock state, proximity, and last-unlock timestamp — alongside live engine-bay BLE data. UI startup is unaffected by cabin-node connect/disconnect.

## Open Questions / Decisions

These are duplicated from `docs/cabin_signal_survey.md` §"Open Questions" so this README can be used standalone at the bench:

- Cluster pin-out for the actually-installed (non-`ADS`) cluster on `AOK912`.
- `KL58` dimmer: PWM digitization vs. `TSL2591` ambient-light proxy.
- I²C topology for ambient sensors (MCU bus vs. Pi-direct).
- Cruise-stalk presence on `AOK912`.
- USB-CDC re-enumeration smoke test through Pi power cycles.
- IRCL → PSE wire signal characteristics (polarity, pulse-duration, one-wire-vs-two).
- Always-on standby budget at the `F20_6` tap (≤200 µA target).
- Proximity hysteresis tuning (RSSI thresholds, scan duty cycle, lock-after-leave delay).
- Whether to keep the IR keys functional in parallel (recommended yes — additive tap, no conflict expected).

## Cross-References

- [`docs/cabin_signal_survey.md`](../../docs/cabin_signal_survey.md) — full signal inventory, tap locations, ownership rules, MCU choice rationale, protection rules, BLE keyless / PSE drive design.
- [`docs/PH2_2_architecture.md`](../../docs/PH2_2_architecture.md) — distributed-node architecture overview (now: cabin hub + always-on cabin node + engine-bay node + trunk monitor).
- [`docs/nRF5430_Interface_Design.md`](../../docs/nRF5430_Interface_Design.md) — sister engine-bay node; shares the protection topology, the high-side-switch topology, and the BOM.
- [`docs/R129_Driver_UI_System_Design.md`](../../docs/R129_Driver_UI_System_Design.md) — how the cabin frames flow into the Pi UI.
- [`docs/known_issues.md`](../../docs/known_issues.md) §"Central Locking (PSE)" — the IR-key abandonment decision that motivates Stages 6–7.
- [`work/pse_central_locking/README.md`](../pse_central_locking/README.md) — original PSE investigation notes.
- [`work/center_console_refresh/README.md`](../center_console_refresh/README.md) — passenger-side trim cable run that the PSE control link reuses.
- [`FW_nrf/payload/r129_payload.h`](../../FW_nrf/payload/r129_payload.h) — wire format reused on the cabin USB-CDC link.
- [`r129_data/data/fuse_box.yaml`](../../r129_data/data/fuse_box.yaml) `F20_6` — the permanent-12-V tap source.

## Work Log

| Date | Status | Notes |
| :--- | :--- | :--- |
| 2026-04-26 | Created | Cabin signal node added as a new node in the architecture. Plan, BOM, and stage gates captured. Hardware procurement and Stage 0 cluster-pinout work scheduled to follow the cluster-pull task already on `docs/parts_to_order.md` Priority 3. |
| 2026-04-26 | Scope expanded | MCU choice updated to `nRF54L15` (matches engine-bay node, single Nordic part family). Always-on operation, BLE proximity-based central locking (replacing the dead IR remote keys per `docs/known_issues.md` §"Central Locking (PSE)"), and the Pi `5 V` high-side switch all folded in from the previously planned standalone sentry node. Stage 0 expanded with IRCL → PSE wire identification; new Stages 6 (always-on + Pi wake), 7 (PSE drive), 8 (Pi UI) added. |
