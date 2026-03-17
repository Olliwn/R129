# Galvanic Isolation Subsystem Design (nRF5430 Interface Board)

## Overview
This subsystem physically separates the delicate 3.3V logic (nRF5430 DK) from the vehicle's 12V diagnostic signaling topology. Because typical Mercedes signals are pulled to 12V and can sink to Ground during diagnostics, they can trivially destroy a 3.3V microcontroller if connected directly.

## Requirements
*   **Safety Boundary:** Electrical noise, transients, and 12V supply must never reach the Nordic's logic side.
*   **Passive Reading:** Listen to 12V square-wave pulses (blink codes) and output an inverted 3.3V logic square-wave to the nRF5430.
*   **Active Pulling (Code Clearing):** Receive a 3.3V signal from the nRF5430 and use it to pull the 12V diagnostic line hard to Ground for up to ~10 seconds without overheating.

## Isolation Architecture
The architecture utilizes the `TLP521-4` (or similar standard optocoupler arrays) to create an optical air-gap. A single bidirectional diagnostic line on the car is split into two one-way optical lanes: an RX path and a TX path.

### Stage 1: The "Read" Path (Car ➔ MCU)
When reading a diagnostic port, the car's pin outputs 12V. When it "blinks," it pulls that 12V momentarily to Ground.

1.  **Vehicle Input:** The car's 12V diagnostic line (e.g., Pin 9 for ADS) connects to an external 1kΩ resistor.
2.  **Optocoupler LED:** This 1kΩ resistor connects to the Anode (Pin 1) of the optocoupler's internal LED. The Cathode (Pin 2) goes to Car Ground (Pin 1 on the X11 socket).
    *   *Sizing Logic:* `(14V peak - 1.2V LED drop) / 1000 ohms = ~12.8mA`. The LED will turn on safely and brightly without burning out.
3.  **Optocoupler Transistor:** The Collector (Pin 4) of the optocoupler connects to the nRF5430's 3.3V input pin. This pin must have an internal Pull-Up resistor enabled in software. The Emitter (Pin 3) connects to the Nordic's clean 3.3V logic Ground.
4.  **Signal Result:** When the car line is resting at 12V, the LED is on, pulling the 3.3V input to Ground (Logic LOW). When the car "blinks" by pulling its line to ground, the LED turns off, and the Nordic's pull-up resistor snaps the input to 3.3V (Logic HIGH). The signal is inverted but safely 3.3V.

### Stage 2: The "Write" Path (MCU ➔ Car)
To clear a code or trigger a module to start reading, the car's diagnostic line must be actively shorted to Car Ground.

1.  **MCU Output:** The nRF5430 sets a GPIO pin HIGH (3.3V).
2.  **Optocoupler LED:** The GPIO goes through a 330Ω resistor into the Anode (Pin 1) of a *second* optocoupler channel. The Cathode (Pin 2) goes to the Nordic's clean logic Ground.
    *   *Sizing Logic:* `(3.3V - 1.2V) / 330 ohms = ~6.3mA`. Safe for a GPIO pin to drive.
3.  **Optocoupler Transistor:** The Collector (Pin 4) connects to the car's 12V diagnostic line. The Emitter (Pin 3) connects to Car Ground.
4.  **Signal Result:** When the GPIO goes HIGH, the optocoupler's transistor switches on, bridging the car's 12V line to ground, effectively pulling it low and executing the "clear" sequence. The 12V never touches the 3.3V side.

## Schematic Outline / Netlist Concept (Single Channel)
```
[Vehicle 12V Diag Line] ---(1kΩ Resistor)---(Opto 1 LED Anode)
(Opto 1 LED Cath) ---(Car_GND)
(Opto 1 Trans Coll) ---(nRF5430 GPIO Input w/ Pull-up)
(Opto 1 Trans Emit) ---(Logic_GND)

[nRF5430 GPIO Output] ---(330Ω Resistor)---(Opto 2 LED Anode)
(Opto 2 LED Cath) ---(Logic_GND)
(Opto 2 Trans Coll) ---(Vehicle 12V Diag Line)
(Opto 2 Trans Emit) ---(Car_GND)
```

## Testing Protocol (Breadboard Phase)
1.  **Isolation Build:** Construct both paths on a breadboard. Ensure there are no accidental paths bridging Car Ground and Logic Ground.
2.  **Bench Test (Read):** Supply a mock 12V to the input. Verify the Nordic pin reads ~0V. Disconnect the 12V input, verify the Nordic pin reads 3.3V.
3.  **Bench Test (Write):** Supply a mock pull-up 12V source to the output pin. Trigger the Nordic GPIO. Measure the mock 12V source point. It should drop to near 0V.
4.  **Oscilloscope Verification (Owon HDS242):** Inject a 20Hz square wave into the mock 12V side. Use the scope to verify the rise/fall times on the 3.3V Nordic side. Confirm the opto-transistor saturates properly without rounding off the signal too severely.
