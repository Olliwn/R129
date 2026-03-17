# Analog Signal Conditioning Design (nRF5430 Interface Board)

## Overview
Automotive analog signals are natively incompatible with delicate 3.3V ADCs. They often swing up to 14V (battery voltage), can carry significant high-frequency noise, and may drop below ground due to inductive spikes. This subsystem sits between the raw vehicle sensors and the ADS1115 ADC.

## Requirements
*   **Safety:** The conditioned signal must *never* exceed the ADC's supply voltage (3.3V) or go below Ground.
*   **Precision:** The signal conditioning must not alter the DC value of the measurement beyond an acceptable tolerance.
*   **Filtering:** The subsystem must remove alternator whine and high-frequency ignition noise.

## 1. Air-Flow Potentiometer & Battery Voltage (High-Voltage Analog)
These signals represent large voltage swings (0-5V or 0-14V).

### Architecture: Divider -> Clamp -> Buffer (Optional) -> Low-Pass Filter -> ADC
1.  **Voltage Divider:**
    *   *Battery Voltage (14.4V max):* Route through a `10kΩ` and `2.2kΩ` divider. This drops 15V down to ~2.7V, sitting comfortably within the 3.3V ADC range.
    *   *Air-Flow Pot (5V max):* Route through a `10kΩ` and `10kΩ` divider. Drops 5V to 2.5V.
2.  **Clamping Diodes:**
    *   Place a pair of fast-switching diodes (e.g., `1N4148`) after the divider.
    *   *Diode 1:* Anode to signal, Cathode to 3.3V rail. Clips any spike above 3.3V + 0.6V.
    *   *Diode 2:* Anode to Ground, Cathode to signal. Clips any spike below Ground - 0.6V.
3.  **Buffer (LM358P):**
    *   *Why:* Voltage dividers have high output impedance. If the ADC or Multiplexer draws any current, the measured voltage drops.
    *   *Implementation:* Pass the clamped, divided signal into a unity-gain buffer using the LM358 op-amp. This provides a very strong, low-impedance signal to the ADC.
4.  **RC Low-Pass Filter:**
    *   After the buffer, place a `1kΩ` resistor in series and a `1nF` or `10nF` capacitor to ground. This acts as a final anti-aliasing filter to remove RF noise before the ADC samples.

## 2. Electro-Hydraulic Actuator (EHA) Current Monitoring
The EHA is controlled by varying the current (typically between -60mA to +60mA, depending on the operational status and temperature). This is a *current*, not a voltage, requiring a shunt resistor.

### Architecture: Insert Harness -> Current Sense Amplifier -> ADC
1.  **Insert Harness:**
    *   NEVER pierce the EHA wires. Build a custom pass-through harness featuring a precision shunt resistor (e.g., `0.1Ω` or `1Ω`, 1% tolerance) placed in series with one of the EHA lines.
2.  **Current Monitor (INA169NA/3K):**
    *   The `INA169` is a dedicated High-Side Current Monitor. It measures the tiny voltage drop *across* the shunt resistor, amplifies it, and outputs a ground-referenced voltage proportional to the current.
    *   *Current to Voltage:* The output voltage is set by selecting a load resistor (RL).
    *   *Example:* If shunt is `0.1Ω` and RL is `10kΩ`, an EHA current of 50mA produces a `0.5V` output.
3.  **Bidirectional Challenge:**
    *   The KE-Jetronic system sometimes reverses the current flow. The INA169 is *unidirectional*. To measure bidirectional current, you either need a dedicated bidirectional chip (like an INA219) or two INA169s wired in anti-parallel. For the prototype, we will analyze the positive flow first to establish baseline operation.

## Schematic Outline / Netlist Concept (Battery Div)
```
[Vehicle KL15 12V] ---(10kΩ Resistor)---(Node B)
(Node B) ---(2.2kΩ Resistor)---(Logic_GND)
(Node B) ---(1N4148 Anode) | (1N4148 Cathode)---(3V3_BUS)
(Node B) ---(1N4148 Cathode) | (1N4148 Anode)---(Logic_GND)
(Node B) ---(LM358 Non-Inverting Input +)
(LM358 Inverting Input -) ---(LM358 Output)
(LM358 Output) ---(1kΩ Resistor)---(Node C)
(Node C) ---(10nF Capacitor)---(Logic_GND)
(Node C) ---(ADS1115 A0 Input)
```

## Testing Protocol (Breadboard Phase)
1.  **Bench Calibration (Divider):** Apply a known 12.00V from the bench supply. Measure the output of the LM358 buffer. Calculate the exact divider ratio to use in software.
2.  **Transient Injection:** Momentarily touch a 20V source to the 12V input side. Verify the output of the buffer does not exceed ~3.9V (clamping action working).
3.  **Noise Rejection:** Inject a noisy 12V signal (if available) and use the Owon oscilloscope to confirm the RC filter smooths the signal into a clean DC line prior to the ADC input.
