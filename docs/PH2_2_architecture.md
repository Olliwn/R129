# Phase 2.2 Architecture: Vehicle Diagnostics and Sensor Front-End

## Purpose
This document narrows the broader `Hybrid R129` vision down to the specific `Phase 2.2` problem: how to get meaningful vehicle data from the car into the Nordic instrumentation node without damaging the car, the board, or the signal quality.

The focus here is not the Pi GUI itself. The focus is the layer beneath it:

`R129 signal source -> protected front-end -> Nordic node -> BLE -> Raspberry Pi 5 UI`

## Architectural Overview
The system is split into four hardware roles. (An earlier revision had five — a separate "always-on sentry" node — but its responsibilities have been folded into the cabin signal node, which is naturally well-positioned to do them. See node 3 below.)

### 1. Cabin hub: `Raspberry Pi 5`
- fast-boot local UI
- logging, storage, and visualization
- BLE central for the engine-bay sensor node
- USB-CDC host for the always-on cabin signal node
- power-enable controlled by the cabin signal node's high-side switch (Pi boots when the owner's phone is in proximity)
- no direct exposure to raw under-hood automotive signals

### 2. Engine-bay instrumentation node: `Thingy:53` / `nRF5340` / `nRF54L15`
- mounted in the `F32` computer box area
- battery removed before engine-bay deployment
- reads protected analog and digital channels for **under-hood-only signals**: `X11` blink codes, `EHA` current, airflow potentiometer (`B2`), lambda / integrator at `N3`, engine-side `ECT` (`B11/2`)
- timestamps and normalizes the data before sending it over BLE
- *cabin-side signals (cluster gauge senders, brake, kickdown, VSS, TD, etc.) moved to node 3 below — see `docs/cabin_signal_survey.md`*

### 3. Always-on cabin signal node: `nRF54L15`

Same MCU family as the engine-bay node, deliberately, for ecosystem consistency (one Zephyr/`nrfx` toolchain, one `FW_nrf/payload/` wire format, one Nordic SDK across the project).

- mounted in or near the front cubby alongside the RPi5
- powered always-on from `F20_6` (trunk fuse box, 8 A white, terminal 30 permanent 12 V — same fuse that already feeds `PSE`, `IRCL`, antenna, and trunk light) via a low-Iq automotive buck. Target standby ≤200 µA at the input
- connected to the Pi over **USB-CDC** (wired, no BLE for telemetry) — appears as `/dev/ttyACM0`
- reuses the [`FW_nrf/payload/r129_payload.h`](../FW_nrf/payload/r129_payload.h) wire format with a new `R129_TYPE_CABIN = 0x04` payload type

This node has four responsibilities:

#### 3a. Cabin signal acquisition (when ignition is on)
Reads protected cabin-side signals: instrument cluster pulse and gauge-sender lines (`VSS`, `TD`, coolant gauge sender, fuel sender, outside-air temp), warning-lamp drives, brake-light feed (`KL54`), kickdown switch (`S16/3`), reverse light, hand-brake, `KL15`/`KL30`/`KL58`, console rocker switches, door / hood / trunk ajar. Hosts cabin ambient sensors over its own I²C bus: `BME280` (cabin temp/humidity/pressure), IMU (lateral-g for `ADS` correlation), `TSL2591` (ambient light for display auto-dim).

#### 3b. BLE proximity-based central locking
Replaces the factory IRCL infrared remote keys, which are effectively dead on `AOK912`. Both fobs tested with fresh batteries 2026-04-06: one has a hardware-dead IR LED, the other transmits weakly and the car does not respond — likely a rolling-code de-sync that requires MB Star Diagnosis re-pairing (~€200+ dealer visit). Decision: skip the IR repair, drive PSE directly from this always-on node instead.

The cabin node BLE-scans for the bonded owner phone with RSSI hysteresis. Phone in proximity → unlock; phone out of range → lock (after a configurable delay). Drive is a single GPIO routed to a small **trunk-side PSE drive board** (one MOSFET / opto + flyback diode + ferrite, mounted near the IRCL/PSE controllers) over a control wire that reuses one spare CAT6 pair from the existing passenger-side BE2210 tap run. The tap onto the IRCL → PSE signal wire is *additive* (parallel to the factory IRCL output), so any future re-paired IR fob would still work.

#### 3c. Pi `5 V` power-enable / wake control
Drives a high-side P-channel MOSFET on the cabin board itself that switches the Pi `5 V` rail. Logic:
- Phone proximity match → assert PSE unlock + assert Pi enable simultaneously. Pi boots while the car unlocks; UI is up by the time the driver sits down.
- Doors close + `KL15` off + RSSI loss → keep Pi enabled for a configurable shutdown grace period (e.g. 60 s) so logs flush, then deassert.
- `KL15` on (engine running) → keep Pi enabled regardless of BLE state.

This is the function the standalone "sentry" node was originally going to provide; it's now on the cabin node's MCU because the cabin node already lives in the right place and is already BLE-aware.

#### 3d. Lock / proximity / Pi-power state reporting
The same USB-CDC frames carry the cabin telemetry plus lock state, BLE proximity, last-unlock-timestamp, and Pi power state. The Pi UI surfaces these on the home view.

Detailed bring-up plan, BOM (including the trunk-side PSE drive board and the always-on supply), and stage gates are in [`work/cabin_signal_node/README.md`](../work/cabin_signal_node/README.md). Detailed signal inventory and PSE wiring approach are in [`docs/cabin_signal_survey.md`](cabin_signal_survey.md) §"Always-On Operation and BLE Keyless Lock/Unlock".

### 4. Trunk battery monitor: `INA226` + `DS18B20`
- mounted in the trunk next to the battery
- connected to the RPi5 via a short I2C cable (< 1 m) and one-wire bus, not via BLE
- **non-invasive design:** no series connection in the battery cable, no added failure points
- measures battery voltage directly at the terminals via a fused sense wire (INA226 bus voltage: 0–36V, 1.25 mV resolution)
- measures battery case temperature (DS18B20: ±0.5°C) for state-of-charge compensation
- parasitic draw estimated from voltage decay rate over time, combined with lead-acid battery model and temperature compensation
- cranking health tracked via voltage sag depth and recovery rate
- replaces the battery voltage divider previously planned for `ADS1115 A1` on the engine-bay node, freeing that channel for a second engine-bay analog sensor
- upgrade path: a bolt-terminal current shunt can be added inline with the battery negative cable later if direct current measurement proves necessary

This four-node split matters because each node has a distinct electrical risk profile and physical location:
- the engine-bay node lives in a hot, electrically noisy environment and must be ruggedized;
- the cabin node lives in the same cubby as the Pi, sees only cabin-tame signals, runs always-on at sub-mA standby off `F20_6` permanent 12 V, and uses USB-CDC for telemetry to the Pi (no firewall to cross, no BLE bandwidth needed) plus its BLE radio for owner-phone proximity unlock;
- the trunk monitor is purely I²C + 1-Wire over a short cable and never touches a vehicle signal pin directly.

The cabin and trunk monitor are the simplest nodes electrically. Routing every cabin signal through the engine-bay node was the previous plan; it was changed when it became clear that signals like `VSS`, `TD`, brake, kickdown, and the cluster gauge senders are all natively cabin-side and forcing them through the firewall costs BLE bandwidth and engine-bay ADC channels for no engineering benefit.

**On the absorbed sentry node**: the previous architecture called for a fifth node, an always-on sentry that owned BLE wake / Pi power-enable / IRCL→PSE keyless drive. With the cabin signal node now necessarily present in the same cubby, and necessarily including BLE for proximity unlock, the cabin node becomes the natural home for those three responsibilities — keeping just one always-on Nordic MCU in the car. See [`work/cabin_signal_node/README.md`](../work/cabin_signal_node/README.md) Stages 6–7 for the bring-up plan.

## The Two R129 Diagnostic Port Families
To study the possibilities properly, it helps to separate platform-wide `R129` knowledge from what is most likely present on `AOK912`.

### Port family A: early `X11` blink-code socket
This is the primary port family for the early `1991` car.

What it is good for:
- passive diagnostics
- reading subsystem blink codes
- accessing certain live service signals without cutting the factory loom
- first-stage prototype work with banana-plug breakouts

What it usually gives access to:
- power and ground references
- engine management blink-code line
- subsystem-specific diagnostic lines for modules such as `ADS`, `ABS/ASD`, `SRS`, alarm, or climate depending on configuration
- KE-Jetronic-era live outputs such as lambda/integrator duty-cycle
- sometimes engine-speed-related diagnostic pulses depending on the exact system

What it is not:
- a complete live-data bus
- a substitute for direct harness access to the air-flow potentiometer or `EHA` wiring when you want detailed analog telemetry

### Port family B: later `38-pin X11/4`
This is the later Mercedes round centralized diagnostic connector used on later `R129` cars and many other 1990s models.

It is useful as a reference because it shows the broader range of module access Mercedes exposed on the platform.

Typical signal families available there include:
- ground
- `circuit 30` battery
- `circuit 87` switched voltage
- engine fuel system
- `ABS/ETS/ASR/ESP`
- cruise / idle (`EA/CC/ISC`)
- `ASD`
- transmission control
- `ADS`
- speed-sensitive power steering
- climate control
- diagnostic module
- `PSE` / remote central locking
- `SRS`

Design implication:
- the current car should be instrumented around the early `X11` socket first
- documentation and breakout philosophy should remain portable to the later `38-pin` connector family

## Signal Categories and What They Tell You

Each signal in this section is annotated with its owner node (engine-bay or cabin) — see [`docs/cabin_signal_survey.md`](cabin_signal_survey.md) for the full per-signal table.

### 1. Blink-code lines (engine-bay node)
These are the safest and most valuable first targets.

Why they matter:
- verify whether `ADS` really has stored faults instead of relying on symptoms alone
- confirm engine-management and other subsystem fault presence
- require minimal invasiveness

Recommended acquisition:
- protected digital input only
- divider plus clamp and comparator, or optocoupler isolation
- optional future open-collector code-clear output, but only with a deliberate interlock

### 2. Lambda / integrator duty-cycle (engine-bay node)
This is one of the best live KE-Jetronic signals for actual diagnosis.

Why it matters:
- shows whether closed-loop control is active
- shows whether the ECU is driving rich or lean correction
- useful for validating vacuum leaks, fuel delivery issues, and mixture adjustment state

Recommended acquisition:
- primary path: digital pulse measurement
- secondary path: RC-averaged analog trend if needed

### 3. TD / RPM pulse (cabin node — moved 2026-04-26)
Useful as a common timing reference for all other measurements.

Why it matters:
- correlates load and fueling changes to engine speed
- makes air-flow and duty-cycle traces far more interpretable

Recommended acquisition:
- **tap at the instrument cluster** (cluster receives `TD` from `EZL` `N1/3` to drive the tach gauge — no need to cross the firewall)
- protected digital front-end with divider/clamp and opto, MCU timer-capture pin
- not a direct ADC target

### 4. Air-flow potentiometer (engine-bay node)
This is one of the best first analog signals to bring into the ADC path.

Why it matters:
- approximates engine load in a way that matches KE airflow mechanics
- provides a stable, intuitive analog signal for graphing and calibration

Recommended acquisition:
- direct dedicated conditioned ADC channel first
- series resistor, clamp, and RC filter before the ADC

### 5. `EHA` current (engine-bay node)
This is a high-value signal and a second-stage task.

Why it matters:
- shows active electronic mixture correction effort directly at the hydraulic actuator
- helps separate mechanical problems from control behavior

Why it is risky:
- current must be measured in-circuit
- the measurement path can disturb the system if done badly
- noise and offset matter much more than with a simple sensor voltage

Recommended acquisition:
- dedicated insert harness only
- precision shunt with proper amplifier or carefully designed differential measurement
- do not attempt this through a casual probe arrangement

### 6. Cabin-side signals (cabin node — added 2026-04-26)
A large family of signals that physically appear inside the cabin and have nothing to gain from a firewall round-trip:

- **Vehicle speed `VSS`** — pulse at the cluster, used by cruise, trans, and the rollover module. Tap at cluster `X25`.
- **Brake-light feed `KL54`** — at the brake pedal switch (`S9`). Digital 12 V.
- **Kickdown switch `S16/3`** — under the accelerator pedal, before the firewall. Digital 12 V momentary.
- **Reverse light** — from the trans selector switch, reaches the cluster reverse-lamp circuit. Digital 12 V.
- **Hand-brake switch** — switch-to-ground, lights the dash lamp.
- **Cluster analog senders** — coolant gauge sender, fuel level sender, oil pressure / oil level switch, outside-air temperature (`B14`). Conditioned to an `ADS1115` on the cabin node.
- **Cluster warning lamps** — `ADS`, `ABS`, `ASR`, alternator, brake-pad-wear, brake fluid, coolant low, washer low, fuel low, seatbelt. Read passively at the lamp drive lines.
- **`KL15` / `KL30` / `KL58`** — ignition-on, battery-presence, illumination-dimmer references for the Pi UI auto-dim and wake logic.
- **Console rocker switch states** — `ADS` Sport/Comfort, hazard, defroster, soft-top.
- **Door / hood / trunk ajar** — interior-light circuit taps.
- **Cabin ambient (new sensors)** — `BME280`, IMU, `TSL2591` over the cabin node's I²C bus.

Full inventory and per-signal tap point / conditioning / ownership table: [`docs/cabin_signal_survey.md`](cabin_signal_survey.md).

## Front-End Electronics Strategy

### Rule 1: Separate digital and analog acquisition mentally and electrically
The same board may carry both, but the design should treat them as different subsystems:

- blink-code and RPM/duty digital capture
- slow conditioned analog measurement

### Rule 2: The diagnostic port is for passive access first
The early project stages should prioritize:
- reading
- logging
- correlating

Not:
- actuating
- clearing faults automatically
- injecting control signals

### Rule 3: Condition every vehicle signal before it reaches the Nordic side
No raw automotive line should touch:
- `nRF5430` / `nRF5340` GPIO
- `ADS1115`
- analog multiplexer inputs

## Planned ADC and Analog Switch Topology

### ADC: `ADS1115`
The planned `ADS1115` remains a good choice for `Phase 2.2` because it suits slow, conditioned analog channels well.

Best uses:
- air-flow potentiometer
- future pressure sensors
- low-bandwidth shunt-derived measurements (e.g. EHA current)
- oil temperature or oil pressure sender

Poor uses:
- raw ignition-like pulses
- raw diagnostic lines
- anything outside the ADC rails

### Analog switch / multiplexer
If the planned expansion part is a `74HC4051` / `CD4051`-class analog switch, it should only be used after per-channel conditioning.

Best uses:
- selecting among several slow analog sensor voltages
- saving ADC channels for future expansion
- switching between already filtered low-voltage nodes

Poor uses:
- raw `12V` lines
- lines with negative excursions
- fast noisy automotive pulse signals

### Practical topology
A sensible first layout is:

- `ADS1115 A0`: direct air-flow potentiometer channel
- `ADS1115 A1`: spare conditioned channel (battery voltage monitoring moved to the dedicated trunk INA226 module)
- `ADS1115 A2/A3`: differential or spare conditioned channel
- `4051 common`: routed to one spare ADC input for future slow sensors

That preserves one direct known-good path while still leaving room for experimentation.

## Wiring Recommendation

### Early `X11` breakout harness
Build a removable harness that brings the selected socket positions to the interface board through:
- banana plugs or a non-destructive adapter
- labeled wires
- a small fuse on the board-side supply feed if power is taken from the socket

The breakout harness should support:
- power and ground reference
- one or more blink-code lines
- duty-cycle line if present
- any usable speed pulse if present

### Dedicated analog insert harnesses
For signals that are not really diagnostic-port outputs, use dedicated harnesses:
- air-flow potentiometer breakout lead
- `EHA` insert harness

This keeps the diagnostic-port harness simple and avoids pretending the service socket is a universal sensor bus.

### Protection order
Each analog path should look like:

`vehicle signal -> series resistor -> clamp / divider -> RC filter -> optional analog switch -> ADS1115`

Each digital path should look like:

`vehicle signal -> divider / current limiting -> clamp or optocoupler -> clean logic edge -> Nordic GPIO`

## Recommended Phase 2.2 Build Sequence

### Stage 1: Passive diagnostic reader
- confirm socket power and ground
- read blink codes from the relevant modules
- validate `ADS` fault access

### Stage 2: Live digital signals
- capture duty-cycle
- capture RPM / TD if accessible
- correlate them in logs

### Stage 3: First analog channel
- wire the air-flow potentiometer through a dedicated conditioned path to the `ADS1115`
- validate noise, offset, and repeatability

### Stage 4: Multiplexed analog expansion
- add the analog switch for future slow channels only
- keep at least one direct ADC path for comparison

### Stage 5: `EHA` current
- build the insert harness
- add the shunt/amplifier path
- verify that the measurement arrangement does not alter engine behavior

## Thermal and Mechanical Constraints
The `Thingy:53` deployment assumptions still stand:

- battery removed before engine-bay use
- mounted inside the `F32` computer box where the factory blower helps airflow
- analog front-end placed close enough to keep unconditioned wiring short
- BLE link validated through the firewall before finalizing enclosure strategy

## Design Conclusions
- The early `X11` socket is the right first foothold for `AOK912`.
- The later `38-pin` port is still worth documenting as the broader `R129` reference design target.
- `ADS1115` is appropriate for conditioned slow analog signals, not raw vehicle lines.
- The analog switch should sit after protection/filtering, never before it.
- Blink-code and duty-cycle are the best first engine-bay data sources.
- Air-flow potentiometer is the best first engine-bay analog channel.
- `EHA` current is a high-value second-stage measurement that deserves its own insert harness and careful analog design.
- **`VSS`, `TD`, brake, kickdown, cluster gauge senders, and warning lamps are owned by the new cabin signal node, not the engine-bay node** — see [`docs/cabin_signal_survey.md`](cabin_signal_survey.md). The engine-bay node's `ADS1115` channels and GPIO budget are reserved for genuinely under-hood signals.