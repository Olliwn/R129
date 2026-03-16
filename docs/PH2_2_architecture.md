# Phase 2.2 Architecture: Vehicle Diagnostics and Sensor Front-End

## Purpose
This document narrows the broader `Hybrid R129` vision down to the specific `Phase 2.2` problem: how to get meaningful vehicle data from the car into the Nordic instrumentation node without damaging the car, the board, or the signal quality.

The focus here is not the Pi GUI itself. The focus is the layer beneath it:

`R129 signal source -> protected front-end -> Nordic node -> BLE -> Raspberry Pi 5 UI`

## Architectural Overview
The system is split into three hardware roles:

### 1. Cabin hub: `Raspberry Pi 5`
- fast-boot local UI
- logging, storage, and visualization
- BLE central for the sensor node
- no direct exposure to raw under-hood automotive signals

### 2. Engine-bay instrumentation node: `Thingy:53` / `nRF5340`
- mounted in the `F32` computer box area
- battery removed before engine-bay deployment
- reads protected analog and digital channels
- timestamps and normalizes the data before sending it over BLE

### 3. Always-on sentry node: low-power Nordic device
- separate from the engine-bay measurement path
- handles BLE wake-on-approach
- controls the Pi power-enable path

This split matters because the always-on node and the engine-bay measurement node have different electrical risk profiles.

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

### 1. Blink-code lines
These are the safest and most valuable first targets.

Why they matter:
- verify whether `ADS` really has stored faults instead of relying on symptoms alone
- confirm engine-management and other subsystem fault presence
- require minimal invasiveness

Recommended acquisition:
- protected digital input only
- divider plus clamp and comparator, or optocoupler isolation
- optional future open-collector code-clear output, but only with a deliberate interlock

### 2. Lambda / integrator duty-cycle
This is one of the best live KE-Jetronic signals for actual diagnosis.

Why it matters:
- shows whether closed-loop control is active
- shows whether the ECU is driving rich or lean correction
- useful for validating vacuum leaks, fuel delivery issues, and mixture adjustment state

Recommended acquisition:
- primary path: digital pulse measurement
- secondary path: RC-averaged analog trend if needed

### 3. TD / RPM pulse
Useful as a common timing reference for all other measurements.

Why it matters:
- correlates load and fueling changes to engine speed
- makes air-flow and duty-cycle traces far more interpretable

Recommended acquisition:
- protected digital front-end with divider/clamp and edge cleanup
- not a direct ADC target

### 4. Air-flow potentiometer
This is one of the best first analog signals to bring into the ADC path.

Why it matters:
- approximates engine load in a way that matches KE airflow mechanics
- provides a stable, intuitive analog signal for graphing and calibration

Recommended acquisition:
- direct dedicated conditioned ADC channel first
- series resistor, clamp, and RC filter before the ADC

### 5. `EHA` current
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
- conditioned battery monitor
- future pressure sensors
- low-bandwidth shunt-derived measurements

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
- `ADS1115 A1`: battery or switched-supply monitor
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
- Blink-code, duty-cycle, and RPM are the best first data sources.
- Air-flow potentiometer is the best first analog channel.
- `EHA` current is a high-value second-stage measurement that deserves its own insert harness and careful analog design.