# Cabin Signal Node — Bring-up

## Purpose

Build the always-on cabin node in the `R129` distributed system: a small `nRF54L15` MCU board, wired to the Pi over a serial link (UART for the rear-half always-on board, per the 2026-05-17 link decision; USB-CDC remains the option for the deferred front-half acquisition board where higher bandwidth may matter), with three responsibilities:

1. **Cabin signal acquisition** (when ignition is on) — instrument cluster gauge senders + lamp drives, brake and kickdown switches, hand-brake / reverse / door / hood / trunk ajar, console rocker switches, `KL15` / `KL30` / `KL58` references, plus cabin ambient sensors.
2. **BLE proximity-based central locking** (always on) — replaces the dead IR remote keys; bonded phone in proximity → unlocks via `PSE` central-locking system; phone out of range → locks. See [`docs/known_issues.md`](../../docs/known_issues.md) §"Central Locking (PSE)" for the IR-key abandonment decision.
3. **Pi power-enable / wake control + cabin 12 V power-domain gate** (always on) — the high-side switch that brings the 85 W cigarette-lighter USB charger up on phone approach (and thereby the Pi, the Qi wireless charging pad, and the spare USB outlet that all hang off it) and lets the Pi shut down gracefully after the owner leaves. See §"Pi 5 V high-side switch" below for the upstream-12 V re-spec adopted 2026-05-04.

Roles 2 and 3 were originally on a separate sentry node; they have been folded into this cabin node so that there's exactly one always-on Nordic MCU in the car. Full architectural rationale and the complete signal inventory live in [`docs/cabin_signal_survey.md`](../../docs/cabin_signal_survey.md). This document captures the bring-up tasks, BOM, and stage gates.

### Physical split (as-installed 2026-05-03)

The cabin node ended up **physically split across two locations** during the May 2026 center console refresh — the BLE / Pi-wake half moved to the rear passenger cubby alongside the Pi and the DSP; the cabin-signal-acquisition half is deferred to its own future board near the cluster:

- **Rear cubby (built and powered now):** `nRF54L15` carrier with BLE radio, **UART link to Pi via GPIO header** (re-spec'd from USB-CDC 2026-05-17 — frees a Pi USB-A port; same payload codec, different transport), the high-side power gate for the 85 W charger domain, and the always-on power section (now sourced from a local tap off the post-AGU 8 mm² CCA rail — see §"Always-on power supply" below). This is the always-on portion required for keyless entry + Pi wake. **Mechanical packaging:** mounted on screw-tower standoffs to a 4 mm plastic plate (CTK-damped underside, friction-fit retention, no holes drilled in the car) shared with the DSP, Pi5, nRF93M1, and 85 W charger — see [`work/rear_cubby_rack/README.md`](../rear_cubby_rack/README.md) for plate design, power topology (manual hard-kill switch + ATO fuse in series with the IRF4905), cooling architecture (lid-preserving foam-baffled side-trim vents), bring-up sequence, and cable management. (Mechanical packaging was re-architected on 2026-05-17 from the original aluminum-T-slot extrusion + modular cassette design — captured in `docs/diary/2026-05.md` May 17 entry; the rack README's Work Log preserves both for reference.)
- **Front (deferred):** The cluster-pinout, ambient-sensor, and instrument-tap acquisition front-end (Stages 2–5 below). Will likely live as a second small board near the cluster when the cluster is pulled. The two boards still appear to the Pi as a single logical "cabin node" because they share the same **framed payload format** (transport-agnostic — same `R129_TYPE_*` frames work over USB-CDC, UART, or BLE notify per `R129/FW_nrf/payload/`); whether they end up on one MCU with a long sensor harness or two MCUs federated over a short serial link is a Stage-2 decision.

The BOM, protection rules, frame format, and stage gates below are unchanged by this split — Stages 0–5 still describe the acquisition half, Stages 6–8 still describe the always-on half. Only the geometry and the always-on power source have changed.

## Why a Separate Node (and Not Just More Pi GPIO)

- Pi GPIO is 3.3 V, no analog ADC, vulnerable to noise, and pulled in unhelpful directions during boot. Direct attachment of automotive 12 V signals to the Pi would be unsafe.
- A small dedicated MCU with a protection front-end is the same approach used for the engine-bay node. Reusing the topology keeps protection rules consistent and lets the cabin board reuse the same `TLP521-4` opto + `ADS1115` + clamp parts already in the SP Elektroniikka stock list.
- A wired link to the Pi (no BLE) is low-latency and naturally power-cycles with the cubby supply rail. **Transport choice per board:** the rear-half always-on board uses UART (3 wires, frees a Pi USB-A port — see `work/rear_cubby_rack/README.md` Cable Management § Bundle D2). The deferred front-half acquisition board may use USB-CDC if it wants the higher bandwidth + zero-driver kernel CDC-ACM enumeration; the framed payload codec is the same across both transports.

## Architectural Position

```
trunk battery +12V ─► 40 A AGU ─► 8 mm² CCA to rear cubby ─► DSP +12V terminal
                                                          │
                                                          ├── local Wago tap
                                                          │      │
                                                          │      ├─► 1 A ATO fuse ─► low-Iq buck ─► +3.3 V always-on
                                                          │      │                                       │
                                                          │      │     ┌────── cabin node (rear half, always-on) ─────┐
                                                          │      │     │                                              │
                                                          │      │     │  nRF54L15 ─────UART────►──► RPi5            │
                                                          │      │     │       │                  vehicle_state.py    │
                                                          │      │     │       │                                      │
                                                          │      │     │       ├── BLE radio (scanning)               │
                                                          │      │     │       │     phone proximity, RSSI hysteresis │
                                                          │      │     │       │                                      │
                                                          │      │     │       ├── GPIO out → trunk-side PSE drive    │
                                                          │      │     │       │              board → IRCL→PSE wire   │
                                                          │      │     │       │                                      │
                                                          │      │     │       └── GPIO out → 12 V high-side MOSFET ──┼─► 85 W charger ─► Pi 5 V
                                                          │      │     │                       (gates the entire      │                  ─► Qi pad
                                                          │      │     │                        85 W charger domain)  │                  ─► spare USB
                                                          │      │     └──────────────────────────────────────────────┘
                                                          │      │
                                                          │      └─► (high-side MOSFET drain — see above)
                                                          │
                                                          └─► (DSP — independent, always-on per audio architecture)


                ┌──── cabin signal node, FRONT HALF (deferred — Stage 0/2–5) ────────┐
cluster X25/X3 ─►                                                                    │
brake / kickdown ─► protection front-end ──┬─► nRF54L15 ──USB-CDC──►──► RPi5        │
console / doors  ─►                        │                       vehicle_state.py  │
ambient sensors  ─►                        ADS1115                                   │
                └────────────────────────────────────────────────────────────────────┘

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

**Source change 2026-05-04:** The originally planned `F20_6` long pull from the cabin fuse box is **dropped**. With the cabin node's always-on half relocated to the rear cubby alongside the DSP, it now taps the post-AGU 8 mm² CCA rail locally (Wago lever-nut on the DSP +12 V terminal). This eliminates the long permanent-12 V cable run that would otherwise have been redundant with the CCA rail running to the same physical location, and consolidates everything downstream of one fuse (the 40 A AGU at the trunk battery). The local in-line fuse is still required to protect the cabin-node branch from the 40 A upstream limit.

| # | Component | Part / Ref | Qty | Source | Notes |
|---|-----------|------------|-----|--------|-------|
| A1 | Low-Iq buck `12 V → 3.3 V` | `Recom R-78E3.3-0.5` (~10 µA Iq) *or* `TI TPS62840` SMD if available | 1 | new (~€8) | Powers the cabin node from the post-AGU CCA rail; target ≤200 µA standby for the cabin board itself |
| A2 | In-line fuse holder | ATO blade in-line | 1 | new (~€3) | On the local Wago tap branch — protects against an unfused short on the cabin-node branch (40 A AGU upstream is too coarse to protect 22 AWG branch wiring) |
| A3 | ATO 1 A fuse | — | 2 | new (~€1) | Holder + spare. Sized to cabin-node + buck draw (~50 mA worst-case); high-side MOSFET drain takes its own dedicated tap branch — see §"Pi 5 V high-side switch" |
| A4 | Local-tap branch wire | 1.5 mm² red, ~0.5 m | qty | in stock | Wago lever-nut on DSP +12 V terminal → fuse → buck (rear cubby internal run) |
| A5 | Reverse-polarity / TVS protection | `SS24` Schottky + `SMBJ18A` TVS at the input | 1 | in stock | Standard automotive front-end (kept even though the post-AGU rail is reverse-polarity-clean by virtue of the AGU + battery clamp) |
| A6 | Wago lever-nut, 3-conductor, 4 mm² | `221-413` | 1 | in stock | Tap point on DSP +12 V terminal — sized to land 8 mm² CCA + 1.5 mm² branch + 1.5 mm² high-side MOSFET drain branch on a single nut |

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

### Cabin 12 V power-domain high-side switch (re-spec 2026-05-04 — gates the entire 85 W charger downstream)

**Re-spec context:** Originally this circuit was a small Pi-only `5 V` high-side switch (a few amps). With the architecture decision in [`work/center_console_refresh/README.md`](../center_console_refresh/README.md) §5.6b, this switch is **promoted to the upstream 12 V gate for the entire 85 W cigarette-lighter USB charger**, which in turn feeds the Pi (≤3 A @ 5 V), the Qi wireless charging pad (~2 A @ 5 V), and a spare USB outlet. By gating on the 12 V side *upstream of the charger*, the charger's own quiescent draw also collapses to zero when the Pi is off — a few hundred µA of switch / sense leakage is the only thing left on the always-on rail downstream of this MOSFET.

**Manual hard-kill in series (added 2026-05-17 — permanent, not interim):** A 50 A rocker switch + 7.5 A slow-blow ATO fuse sit upstream of this IRF4905 in the +12 V series chain (full topology in [`work/rear_cubby_rack/README.md`](../rear_cubby_rack/README.md) §"Power Topology"). The two controls are **complementary**, not redundant: the IRF4905 is the firmware-driven path (BLE proximity, KL15 override, graceful-shutdown handshake); the manual switch is the firmware-independent path (transport mode, service disable, firmware-bug recovery, long-storage zero-parasitic-drain). Either off → charger off → Pi off. This matches industry practice for production embedded vehicle ECUs and survives every plausible firmware failure mode. Originally conceived as an interim during firmware development; promoted to permanent infrastructure on 2026-05-17.

Steady-state load: ~6–8 A at 12 V (85 W charger ≈ 90 % efficient at 70 % load). Worst-case start-up inrush into the charger's input bulk caps + Qi pad start-up: design for **15 A peak for ≤10 ms**, **10 A continuous** with thermal margin. Same circuit topology family as [`docs/nRF5430_Interface_Design.md`](../../docs/nRF5430_Interface_Design.md) §"Circuit Design: High-Side 12V Switch" Option B, scaled up.

| # | Component | Part / Ref | Qty | Source | Notes |
|---|-----------|------------|-----|--------|-------|
| H1 | P-channel logic-level MOSFET | `IRF4905` (TO-220, ≥40 A, R<sub>DS(on)</sub> ~20 mΩ @ V<sub>GS</sub>=−10 V) **OR** `IPP80P03P4L` (D²PAK, 80 A, R<sub>DS(on)</sub> ~3 mΩ) | 1 | new (~€3–5) | **Re-specced from `IRF9540N` / `AO3401`** — those are sub-5 A parts and would dissipate too much at 8 A continuous. Mount with small heat-spreader tab on the Veroboard copper. Verify R<sub>DS(on)</sub> × I² ≤ 0.5 W at 8 A continuous. |
| H2 | Gate-drive transistor | `2N3904` | 1 | in stock | Logic-level GPIO pulls gate low to enable |
| H3 | Gate Zener | 12 V Zener | 1 | in stock | V<sub>GS</sub> clamp |
| H4 | Gate pull-up | 10 kΩ | 1 | in stock | Default-off on power loss / MCU reset |
| H5 | Source/drain bulk capacitor | 470 µF / 25 V low-ESR | 1 | new (~€1) | **Bumped from 100 µF** — supports the larger inrush into the charger's input caps. Place at the MOSFET drain. |
| H6 | Inrush limiter | 10 Ω NTC inrush-current-limiter (`SCK-103`) **OR** soft-start RC on gate | 1 | new (~€2) | Optional but recommended — keeps inrush ≤15 A even into a fully-discharged charger input cap. Soft-start gate RC (10 kΩ × 100 nF) is the cheaper alternative if NTC self-heating is a concern. |
| H7 | Reverse-polarity protection | `SS54` Schottky | 1 | in stock | Already covered upstream by AGU+battery, but local protection on the MOSFET source is cheap insurance |
| H8 | High-side current sense (optional) | `INA226` | 1 | in stock | Reuses the spare INA226 from the trunk battery monitor 5-pack. Lets the cabin node tell the Pi "you are drawing X A right now" — useful for parasitic-draw diagnostics and for catching a stuck-on Qi pad. |
| H9 | Local tap branch wire | 4 mm² red, ~0.3 m | qty | in stock | Wago tap on DSP +12 V terminal → MOSFET source. Sized for 10 A continuous + voltage drop. |

**Default state on MCU reset / power loss:** OFF (gate pulled high by H4). On every clean boot, the cabin node holds the gate off until the proximity state machine has converged (≥3 scan windows). Combined with the rear-half cabin node also losing its own 3.3 V rail if the AGU blows, **a single fault upstream brings the entire cabin 12 V power domain down safely** — there is no path for the charger to stay on if the cabin node is dead.

**Parasitic budget when off:** cabin node deep-sleep + BLE scan duty-cycle ≤200 µA, MOSFET gate-leak ≤1 µA, INA226 always-on ~330 µA, leakage through the 470 µF cap ≤10 µA → **target total ≤600 µA on the always-on rail downstream of the AGU.** At 12.5 V resting battery, that's ~7.5 mW or ~180 mWh/day — a 100 Ah battery loses 0.0014 % per day to this domain, well below normal self-discharge.

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

- [ ] Build the always-on power section on the cabin Veroboard: post-AGU CCA-rail Wago tap → 1 A in-line fuse → reverse-polarity protection → low-Iq buck → 3.3 V always-on rail. Smoke-test on the bench with a 12 V supply and confirm steady-state input current ≤200 µA with the MCU asleep.
- [ ] Wire the local tap on the DSP +12 V terminal in the rear cubby (Wago `221-413`, 4 mm² lever-nut). Branch 1: cabin-node always-on (this stage). Branch 2: high-side MOSFET source for the 85 W charger domain (Stage 6b below).
- [ ] Implement Zephyr System OFF / RAM-retention sleep with periodic BLE scan wake (e.g. 1 s scan every 5 s while idle).
- [ ] Implement phone bonding flow: long-press the on-board "bond" button, accept pairing on the phone, store LTK in flash. Test re-bonding after `nrf` reflash. (One-time setup.)
- [ ] Implement RSSI-based proximity state machine with hysteresis: `unlock` requires RSSI > −60 dBm sustained ≥3 scans; `lock` requires RSSI < −85 dBm or no advert seen for ≥30 s. Tune in the diary as part of in-car testing.
- [ ] **Stage 6b (re-spec 2026-05-04):** Build the cabin **12 V power-domain high-side switch** on the cabin board (re-spec — see §"Cabin 12 V power-domain high-side switch" above). Drives the upstream 12 V input of the 85 W cigarette-lighter USB charger; the charger's downstream USB outputs feed the Pi (5 V), the Qi pad, and one spare USB outlet — the entire cabin domain comes up and down as one. Wire its enable input to a cabin-node GPIO. Bench-verify with a 12 V supply + a resistive load representing the ~70 W steady-state draw before connecting to the real charger. Stage 6 success is measured *without* the PSE drive yet — just confirm phone-approach turns the charger (and therefore the Pi) on and phone-leave turns it off after the grace period.
- [ ] Verify ignition on (`KL15`) overrides the proximity logic: while the engine is running, the cabin charger domain stays on regardless of phone state. (KL15 sense lives on the deferred front-half acquisition board — until that board exists, use a temporary jumper from the BE2210 ACC-sense line in the rear cubby as a stand-in `KL15` input. Document the jumper in the diary so it's removed once the front-half board lands.)

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
| 2026-05-05 | Re-architecture (post-center-console-install) | Three coupled changes captured in this README following the May 2–5 center console install: (1) **Physical split** — always-on / BLE / Pi-wake half relocated to the rear passenger cubby alongside the Pi + DSP; cabin-signal acquisition half deferred to a future board near the cluster. Both still federate as one logical "cabin node" over the same USB-CDC frame format. (2) **Always-on power source change** — the planned `F20_6` long pull is **dropped**. The rear-half cabin board now taps the post-AGU 8 mm² CCA rail locally on the DSP +12 V terminal (Wago `221-413`, 1 A in-line fuse, low-Iq buck). Eliminates one long permanent-12 V cable run and consolidates everything downstream of the 40 A AGU at the trunk battery. (3) **Pi 5 V high-side switch promoted to cabin 12 V power-domain gate** — re-specced from a sub-5 A FET to `IRF4905` / `IPP80P03P4L` (≥10 A continuous, ≥15 A peak), now gating the upstream 12 V input of the 85 W cigarette-lighter USB charger that feeds the Pi + Qi pad + spare USB. Architectural rationale and the upstream-vs-downstream-gating trade-off is captured in detail in [`work/center_console_refresh/README.md`](../center_console_refresh/README.md) §5.6b. Net parasitic budget on the always-on rail downstream of the AGU drops to ≤600 µA (~7.5 mW). Stage 6b text updated; KL15 overrides documented as a temporary jumper until the front-half acquisition board is built. |
