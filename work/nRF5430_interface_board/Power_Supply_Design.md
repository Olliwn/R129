# Power Supply Subsystem Design (nRF5430 Interface Board)

## Overview
This subsystem provides clean, stable, and protected power for the nRF5430 Development Kit (DK) and the associated logic/analog circuitry, drawing from the R129's dirty 12V automotive environment.

## Requirements
*   **Input:** Automotive 12V (Circuit 30 - Always On, or Circuit 15 - Switched). Note: Automotive "12V" can range from 9V (cranking) to 14.4V (charging) and experience severe voltage spikes (load dumps up to 40V+).
*   **Outputs:**
    *   `5.0V` for logic shifters (TXB0108), analog multiplexers (CD74HC4051E), ADCs (ADS1115), and general Op-Amps (LM358P).
    *   `3.3V` for the nRF5430 DK logic levels, ADC digital interface, and clean analog reference.
*   **Protection:** Must survive reverse polarity (improper jump-starts) and alternator load dumps without passing lethal transients to the 5V and 3.3V rails.

## Power Architecture
The architecture uses a two-stage approach for maximum efficiency and clean analog supply.

### Stage 1: 12V High-Voltage Protection
1.  **Input Fuse:** An inline 2A-5A blade fuse at the physical connection point (e.g., X11 plug or battery tap) to protect the wiring harness against dead shorts.
2.  **Reverse Polarity Protection:** A standard `1N4007` diode in series on the positive rail to block negative voltages. *(Alternatively, a P-Channel MOSFET can be used if the ~0.7V diode drop is unacceptable, but for logic power, the diode is fine).*
3.  **Transient Voltage Suppression (TVS):** A `1.5KE18A` TVS diode placed in parallel immediately after the reverse-polarity diode. This will clamp any voltage spikes exceeding ~15.3V down to a safe level (under 30V), preventing the downstream regulators from being destroyed by 100V+ load dumps.

### Stage 2: Voltage Regulation
1.  **12V to 5V (Primary Bus):**
    *   *Component:* Murata `OKI-78SR-5/1.5-W36-C` (Switching Buck Converter).
    *   *Why:* Highly efficient, no heatsink required, and can handle up to 36V input. It drops the protected 12V down to the primary 5V bus used by the interface ICs.
    *   *Filtering:* Requires bulk capacitance (e.g., 10µF to 100µF electrolytic) on its input and output to handle sudden load changes, plus `100nF` ceramic capacitors physically close to the pins for high-frequency noise rejection.
2.  **5V to 3.3V (Clean Logic/Analog):**
    *   *Component:* STMicroelectronics `LD1117V33` (Linear LDO).
    *   *Why:* LDOs are inefficient when dropping large voltages (like 12V to 3.3V), but extremely clean and quiet when dropping small voltages (5V to 3.3V). By chaining this *after* the Murata switcher, the nRF5430 and ADC get a pristine, low-noise 3.3V supply completely isolated from the main 12V switching noise.
    *   *Alternative:* The `OKI-78SR-3.3/1.5-W36-C` switcher can be used in parallel with the 5V switcher if pure efficiency is prioritized over analog noise floor, but the cascaded LDO is generally better for sensitive ADCs.

## Power States & Wake Logic
*   The nRF5430 (operating as the Bluetooth wake manager) requires always-on power (Circuit 30).
*   To minimize parasitic battery drain (target <5mA while parked), the Murata switcher is preferred over traditional 7805 linear regulators, as its quiescent current is exceptionally low. 
*   Vehicle instrumentation logic (op-amps, level shifters) can either be powered constantly (if total draw is negligible) or sit behind a high-side load switch controlled by the nRF5430, powering up only when the Raspberry Pi 5 UI is awakened.

## Schematic Outline / Netlist Concept
```
[Vehicle 12V (Cct 30/15)] -> [2A Fuse] -> [1N4007 Diode (Anode In, Cathode Out)] -> (Node A)
(Node A) -> [1.5KE18A TVS Diode Cathode] -> (TVS Anode to GND)
(Node A) -> [100µF Cap] -> [OKI-78SR-5 Vin]
[OKI-78SR-5 Vout] -> [10µF Cap] -> (5V_BUS)
(5V_BUS) -> [100nF Cap] -> [LD1117V33 Vin]
[LD1117V33 Vout] -> [10µF Tantalum] -> (3V3_BUS)
```

## Testing Protocol (Breadboard Phase)
1.  **Bench Test (No Load):** Apply 12V bench power. Verify 5.0V ±0.1V on the 5V bus and 3.3V ±0.05V on the 3.3V bus.
2.  **Reverse Polarity Test:** Apply -12V. Verify 0V on the 5V bus and that the 1N4007 does exactly what it is supposed to.
3.  **Load Test:** Connect a ~10 ohm, 5W dummy load to the 5V rail (drawing 500mA). Monitor the OKI-78SR for heat and check for voltage sag.
4.  **Noise Analysis:** Use the Owon HDS242 oscilloscope on the 3.3V rail (AC coupling) to measure peak-to-peak ripple voltage. A clean supply should exhibit <20mV ripple.
