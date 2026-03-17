# nRF5430 Interface Board Design

## Scope
This board now has two related but electrically different jobs:

1. act as the always-on BLE wake manager for the Raspberry Pi 5
2. provide a safe experimental front-end for reading selected `R129` diagnostic and sensor signals

Those jobs should share as little raw vehicle wiring as possible. The Pi wake path is a low-power control function. The vehicle diagnostics path is an instrumentation problem and should be treated as a separate protected domain on the board.

## Vehicle-Side Context: The Two R129 Diagnostic Port Families
Across the `R129` platform there are two diagnostic connector families worth designing around:

### 1. Early `X11` / blink-code socket
This is the important one for `AOK912` because the car is a `1991` pre-HFM `M119` car. It is the older Mercedes diagnostic arrangement used before the later `38-pin` centralized connector became common.

What makes it useful:
- provides easy non-invasive access using banana plugs or a breakout lead
- exposes battery and ground references for a test tool
- exposes subsystem-specific diagnostic lines for blink-code reading
- can expose live service signals such as lambda/integrator duty-cycle on KE-Jetronic-era cars
- is ideal for a first-generation passive reader because it lets you observe a lot without opening the engine harness

What it does not do:
- it does not magically provide every analog engine sensor in ready-to-digitize form
- it is not a substitute for tapping the actual airflow potentiometer, EHA circuit, or other harness-level signals when you want continuous high-quality data
- exact socket population varies by year, engine management, and option content, so the final pin map must be checked against the correct wiring manual before connecting anything active

Signal classes typically available on the early socket:
- `+12V` supply reference and chassis/signal ground
- blink-code output lines for individual control units
- KE mixture control duty-cycle / lambda integrator style output
- some engine-speed-related diagnostic pulse signals, depending on engine management version
- subsystem-specific diagnostic selection lines for ABS/ASD/ADS/SRS/climate/alarm depending on equipment

### 2. Later `38-pin X11/4` centralized connector
Later `R129` cars moved to the well-known round `38-pin` diagnostic connector. Even if `AOK912` does not use it, it is worth documenting because it tells us what a more universal Mercedes interface board could support.

Typical lines available on the later `38-pin` connector include:
- ground
- `circuit 30` battery voltage
- `circuit 87` switched supply
- engine fuel system diagnostic line(s)
- ABS / ETS / ASR / ESP diagnostic line
- cruise / idle / EA-CC-ISC line
- `ASD` line
- transmission control line
- `ADS` control line
- speed-sensitive power steering line
- climate control line
- diagnostic module line
- `PSE` / remote central locking related lines
- `SRS` line

Design conclusion:
- for `AOK912`, treat the early `X11` socket as the primary diagnostic entry point
- for long-term reusability, document the board and breakout harness so it could also be adapted to the later `38-pin X11/4` connector

## Signals Worth Studying First
The useful signals divide into two categories: signals already present at a diagnostic connector, and signals that require a dedicated insert harness or sensor tap.

### Signals available from the diagnostic socket

#### Blink-code lines
Use these first. They are low-risk and already part of the car's service interface.

Why they matter:
- allow confirmation of `ADS` faults, engine management faults, and other module faults without invasive disassembly
- perfect for a first passive tool
- can be read with a very simple LED/button reader or with a protected digital input stage

Acquisition method:
- treat as digital diagnostic lines, not analog channels
- use a high-impedance protected input, ideally with a divider and comparator or optocoupler
- if future code-clearing is desired, drive the line only through an open-collector transistor stage with a jumper or software interlock

#### Lambda / integrator duty-cycle
This is one of the most interesting live signals on a KE-Jetronic-era car.

Why it matters:
- gives live mixture correction behavior
- lets you see whether the system is trimming rich/lean or stuck at a limit
- much more useful than fault codes alone when diagnosing driveability

Acquisition method:
- best treated as a digital pulse train and measured by timer capture
- can also be low-pass filtered into a DC value for slow trending, but the digital method preserves more information

#### TD / engine-speed pulse
If available in the chosen diagnostic path, this is valuable for correlating everything else to actual engine speed.

Acquisition method:
- do not feed raw vehicle pulses straight into the `nRF5430`
- use a divider plus clamp and then a Schmitt-trigger/comparator, or use an optocoupler

### Signals that usually require dedicated sensor tapping

#### Air-flow potentiometer
This is a good ADC target because it is fundamentally an analog voltage signal.

Why it matters:
- shows airflow meter flap position
- useful for correlating load, throttle transitions, and mixture behavior
- much easier to sample cleanly than many ignition-related signals

Recommended handling:
- treat it as a dedicated conditioned analog input
- do not switch it through a raw automotive harness and then directly into the ADC
- add series resistance, clamp protection, and an RC filter before the ADC or analog multiplexer

#### EHA current
This is one of the most valuable KE signals, but it is the one that most deserves respect.

Why it matters:
- directly shows how the control system is biasing fuel pressure through the electro-hydraulic actuator
- helps distinguish mechanical fuel-distributor issues from electronic correction behavior

Why it is harder:
- it is a current signal, not a simple sensor voltage
- depending on measurement method it can be bidirectional and electrically noisy
- careless insertion can disturb the fuel-control loop

Recommended handling:
- measure through a dedicated insert harness, not by random piercing or temporary clips
- place a precision shunt resistor only in a designed breakout path
- preferably buffer the shunt with a current-sense amplifier before presenting it to the ADC
- defer this until the passive diagnostic reader and airflow-pot reading are already working

## ADC Choice: `ADS1115`
The `ADS1115` is still a sensible first ADC for this project.

Why it fits:
- `I2C`, easy to integrate with Nordic hardware
- 16-bit resolution is useful for slow automotive analog signals
- four inputs allow a mix of direct and differential channels
- programmable gain is helpful for conditioned low-voltage signals

Where it fits well:
- air-flow potentiometer voltage
- battery voltage after divider
- low-bandwidth temperature / pressure sensors
- conditioned shunt measurements

Where it does not fit well by itself:
- raw `12V` pulse lines
- raw inductive or ignition-related signals
- anything that can swing below ground
- unconditioned EHA current measurement

Important constraint:
`ADS1115` inputs must stay inside the ADC supply rails. That means every vehicle-originated signal must be conditioned before reaching the ADC.

## Analog Switch / Multiplexer Plan
If the intended architecture is `ADS1115 + 74HC4051/CD4051-class analog switch`, that is workable for a prototype, but only if the multiplexer sees already-conditioned low-voltage signals.

Recommended use case for the analog switch:
- expand one `ADS1115` channel into several slow analog measurements
- select between multiple filtered sensor voltages
- avoid dedicating a full ADC channel to every future low-bandwidth sensor

Do not use the analog switch for:
- raw `12V` automotive lines
- ignition-related spikes
- code-clearing pulse injection
- any signal that can go negative

### Wiring Rule for the Analog Switch
Every channel should follow this order:

`vehicle signal -> protection / divider / clamp / RC filter -> analog switch input -> analog switch common -> ADS1115 input`

Not this:

`vehicle signal -> analog switch -> ADS1115`

That single rule is the difference between a useful prototype and a damaged board.

## Recommended Front-End Partitioning

### Domain A: Always-on wake manager
- powered from protected constant `12V` through a small always-on buck converter
- responsible only for BLE scanning, authorization logic, and Pi wake control
- should remain electrically quiet and stable

### Domain B: Vehicle instrumentation front-end
- separate protected input section for all vehicle-facing measurements
- star-ground or carefully managed analog ground return
- connectorized so it can be disconnected independently of the wake function

#### The Core Principle: Galvanic Isolation
Because the car's diagnostic pins (like Pin 9 for ADS) are bidirectional (they both send and receive data on a single wire), the board splits this single wire into two separate, one-way optical lanes: a Read (RX) lane and a Write (TX) lane. By using dedicated chips exclusively for Reading and Writing, the board creates a literal "no man's land". The car's 12V power and dirty ground never physically touch the microcontroller's 3.3V logic and clean ground.

#### The Logic Architecture (Per Channel)
**The "Read" Path (Car ➔ MCU):**
- **Input:** The Car's 12V signal pin connects through a 1kΩ resistor to the optocoupler's LED.
- **Output:** The optocoupler's transistor connects to your MCU's Input pin, which is pulled high to 3.3V.
- **Behavior:** Inverted. When the car line is resting at 12V, your MCU reads LOW. When the car pulses to Ground (flashing a code), your MCU reads HIGH.

**The "Write" Path (MCU ➔ Car):**
- **Input:** Your MCU's Output pin connects through a 330Ω resistor to the optocoupler's LED.
- **Output:** The optocoupler's transistor connects directly to the Car's signal pin and Car Ground.
- **Behavior:** Standard. When your MCU pin goes HIGH, the optocoupler bridges the car's diagnostic line to Car Ground, initiating the 3-second code read or 8-second code clear command.

#### Critical Build Reminder
When assembling on Veroboard, follow the **Strip Cut Rule**: physically sever the copper tracks directly underneath the center of every single IC socket. Failing to do this will bridge the 12V car side to the 3.3V MCU side, instantly destroying the microcontroller.

## Circuit Design: High-Side 12V Switch
Since the Nordic node operates at `3.3V` logic, it cannot directly drive a `12V` P-channel MOSFET gate over the full range. The gate should be pulled by a small transistor or N-channel stage, or the switching function can be delegated to a relay or automotive high-side switch.

### Option A: Solid-State MOSFET Path
- `Q1` small logic-level N-channel MOSFET or NPN transistor driven by the `nRF5430` GPIO through a `1k` resistor
- `Q2` automotive-suitable P-channel MOSFET or high-side switch controlling the Pi power feed
- `10k` pull-up from gate to vehicle `12V` so the Pi stays off by default
- TVS and input fuse ahead of the whole power section

### Option B: Relay Path
- `3.3V` compatible relay module or automotive relay driver
- simpler to prototype
- gives stronger separation between Nordic logic and high-current load path
- noisier and less elegant than a proper solid-state high-side design

## Example Measurement Wiring

### 1. Air-flow potentiometer into the `ADS1115`
Suggested path:

`air-flow pot signal -> 4.7k to 10k series resistor -> clamp to ADC rail -> RC filter -> ADS1115 A0`

Notes:
- keep this on a dedicated ADC channel at first
- do not put it behind the analog switch until the direct path is validated
- sample slowly but repeatedly and correlate against RPM and duty-cycle

### 2. Battery voltage monitor
Suggested path:

`KL30 or KL15 -> resistor divider -> RC filter -> ADS1115 A1`

Notes:
- useful for confirming supply droop during crank or wake events
- good sanity channel for every logging session

### 3. EHA current via insert harness
Suggested path:

`EHA insert harness -> precision shunt -> differential amplifier or differential ADC input -> ADS1115 A2/A3`

Notes:
- do this only after building a proper insert harness
- never disturb the original loop casually

### 4. Expanded low-speed sensors through the analog switch
Suggested path:

`conditioned sensor 1/2/3/... -> 4051 inputs -> 4051 common -> ADS1115 A2`

Control:
- `S0/S1/S2` from `nRF5430` GPIO
- optional `EN` pin for known-safe startup state
- short settle delay before every conversion after a channel change

Good candidates for the switched group:
- filtered hydraulic pressure sensor output
- under-hood temperature sensor
- spare conditioned analog tap
- averaged duty-cycle monitor for trending only

## Development Order
1. Build a passive breakout for the early `X11` socket and confirm power/ground safely.
2. Implement blink-code reading first.
3. Add digital capture for duty-cycle and any usable RPM/TD pulse.
4. Add one clean direct ADC channel for the air-flow potentiometer.
5. Add the analog switch only for already-conditioned low-speed channels.
6. Leave `EHA` current measurement until a proper insert harness exists.

## SP Elektroniikka Shopping List (Updated)

1. **Power and protection**
   - [x] 1x automotive-rated `12V -> 5V` buck converter for always-on Nordic power (12V DCDC 50W grade)
   - [x] **Automotive DCDC Buck Converter (DigiKey Sourced - for nRF5430 & signal logic):**
     - *Murata OKI-78SR-5/1.5-W36-C* (5V / 8W output for 5V logic/analog).
     - *Murata OKI-78SR-3.3/1.5-W36-C* (3.3V / 5W output for Nordic logic).
   - [x] **Low Dropout (LDO) Linear Regulators (DigiKey Sourced - Clean logic/ADC power alternates):**
     - *5.0V LDO:* **LM2940T-5.0/NOPB** (Automotive 12V input rated, TO-220).
     - *3.3V LDO:* **LD1117V33** (Clean 3.3V derived power, TO-220).
   - [x] PFET / High-Side switching devices
   - [x] 1x inline fuse holder and appropriate blade fuses
   - [ ] 1x protected `12V -> 5V` high-current converter or UPS HAT path for the Pi
   - [x] **Automotive TVS Diode & Protection (DigiKey Sourced)**:
     - *1.5KE18A* (Through-hole axial lead 15.3VWM TVS diode for load-dump transient clamping).

2. **Wake switch hardware**
   - [x] 2x logic-level small N-channel MOSFETs (2N7000)
   - [ ] 1x relay option for quick prototype

3. **Core ICs & Galvanic Isolation (Diagnostics)**
   - [x] 6x **Optocoupler Arrays**: TLP521-4 (DIP-16 package).
   - [x] Resistors: 5% assortment (including 1kΩ, 330Ω, 10kΩ).
   - [x] **DigiKey Resistor & Capacitor Assortments (For signal conditioning):**
     - *SparkFun Resistor Kit (1/4W, 500 Total) - 10969*
     - *SparkFun Capacitor Kit - 13698*
     - *100nF (0.1µF) 50V X7R Ceramic Capacitors* (x60 total, K104K10X7RF5UH5)
     - *10nF (10000pF) 50V X7R Ceramic Capacitors* (x10 total, C315C103K5R5TA)
   - [x] LEDs (Standard for diagnostics)
   - [x] **Standard Protection Diodes (DigiKey Sourced)**
     - *1N4148* (x50, DO-35 Small logic signal switching/clamping).
     - *1N4007* (x20, DO-204AC 1A rectifier, reverse-polarity protection).
     - *1N5819* (x3, DO-204AC Schottky, lower forward voltage drop).
   - [x] **Logic Level Shifters (DigiKey Sourced)**
     - *TXB0108 Breakout Board - AK-LVLSHF-TXB-BB* (Bidirectional 8-channel shifter for 3.3V to 5V conversions).
   - [x] Switches (Push buttons, toggles)
   - [ ] 6x **IC Sockets**: 16-pin "Holkkikanta" (machined/turned pin sockets).
   - [x] **Op-Amps & Current Monitors (DigiKey Sourced)**:
     - *LM358P* (x10, General purpose op-amp, DIP-8).
     - *INA169NA/3K* (x2, High-side current monitor for EHA tracking, SOT23-5).
   - [x] `ADS1115` 16-bit 4-channel ADC breakout (DigiKey Sourced)
   - [x] `CD74HC4051E` 8-channel analog multiplexer (DigiKey Sourced)
   - [x] Small capacitors for RC filtering (Covered by Ceramic orders)

4. **Harness and prototyping**
   - [x] Wire: Signal (small) and Power wires.
   - [x] Alligator clips (Hauenleuat)
   - [x] 4 mm banana plug set for the early `X11` socket.
   - [x] Heat shrink tubing (Kutistesukka)
   - [x] **Discrete Semiconductors Kit** (SparkFun 13682 - DigiKey Sourced)
   - [x] **Breadboards (DigiKey Sourced)**
     - *DKS-SOLDERBREAD-02* (x1, Plated Through Hole).
     - *08808* (x3, SparkFun General Purpose).
     - *ST1* & *5588* & *PTS-00079-201* (x8 total, mixed PTH sizes).
   - [x] **Header Pins (DigiKey Sourced)**
     - *61300411121* (x10, 4-pos Vertical 2.54mm pitch).
   - [x] **Female Jumper Pigtails (DigiKey Sourced)**
     - *ASPHSPH24K102* (x10, Socket-to-Socket 24AWG, 4-inch).
   - [x] **Pluggable Screw Terminals (DigiKey Sourced - 5.08mm Pitch)**
     - *1757019* (x2, 2-pos Plug) & *1786404* (x2, 2-pos Header)
     - *1757035* (x1, 4-pos Plug) & *1786420* (x1, 4-pos Header)

5. **Test Equipment Needs (Purchased)**
   - [x] **Owon HDS242 Handheld Oscilloscope + Multimeter Combo**
