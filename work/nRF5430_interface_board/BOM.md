# nRF5430 Interface Board: Bill of Materials (BOM)

This document tracks the components required for the modular nRF5430 interface board prototype. The initial build will be done using a nRF5430 Development Kit (DK) and separate breadboards for each subsystem before migrating to a custom PCB.

## 1. Core Processing
*   **nRF5430 Development Kit (DK):** Selected over the Thingy54 due to the high number of exposed GPIOs required for the various vehicle interfaces and custom UI controls.

## 2. Power Supply Subsystem
*   **Automotive DCDC Buck Converter (5V Logic):** Murata OKI-78SR-5/1.5-W36-C
*   **Low Dropout (LDO) Linear Regulator (3.3V Logic):** STMicroelectronics LD1117V33
*   **TVS Transient Protection:** 1.5KE18A (15.3VWM)
*   **Reverse Polarity Protection:** 1N4007 Diode

## 3. Galvanic Isolation (Vehicle Diagnostics)
*   **Optocoupler Arrays:** Toshiba TLP521-4 (DIP-16)
*   **Current Limiting Resistors:** 1kΩ (RX step-down), 330Ω (TX protection)

## 4. Analog Signal Conditioning & ADC
*   **16-bit 4-Channel ADC:** Texas Instruments ADS1115 (I2C Breakout)
*   **8-Channel Analog Multiplexer:** Texas Instruments CD74HC4051E
*   **Op-Amps (General Purpose):** Texas Instruments LM358P
*   **Current Monitor (EHA Tracking):** Texas Instruments INA169NA/3K
*   **RC Filtering:** 100nF, 10nF ceramic capacitors, various 1/4W resistors

## 5. Logic Interface
*   **Level Shifter (3.3V <-> 5V):** TXB0108 Breakout Board

## 6. Environmental Sensors (RPi5-Direct, not via nRF5430)
*   **Outside Temperature:** DS18B20 1-Wire digital sensor (±0.5°C). Mount in front airflow path. Connects directly to RPi5 GPIO with 4.7kΩ pull-up resistor. **Needed.**
*   **Cabin Temperature (future):** Second DS18B20 on the same 1-Wire bus. **Optional.**

## 7. Prototyping Hardware
*   **Breadboards:** 1x DKS-SOLDERBREAD-02 (PTH), 3x SparkFun 08808, 8x Mixed PTH Boards
*   **Connectors:** 2.54mm Headers (61300411121), 5.08mm Pluggable Screw Terminals
*   **Wiring:** 24AWG Socket-to-Socket jumpers, 22AWG solid core for breadboards
*   **Vehicle Interface:** 4mm Banana Plugs (for X11 socket)
