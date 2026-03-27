# nRF5430 Interface Board: Software Requirements & Interface Definition

## 1. Core Operating Modes
The nRF5430 software will operate in two distinct modes driven by the physical state of the vehicle:

1.  **Sleep/Wake Manager (Low Power State):**
    *   **Condition:** Vehicle is turned off (Circuit 15 is 0V, only Circuit 30 is active).
    *   **Function:** The nRF5430 remains in deep sleep, periodically waking to scan for an authorized Bluetooth Low Energy (BLE) MAC address (e.g., the owner's phone).
    *   **Action:** Upon proximity detection and authorization, the nRF5430 flips the high-side load switch (via GPIO) to power up the Raspberry Pi 5. If the BLE device leaves the area and stays gone for a defined timeout (e.g., 5 minutes), the nRF5430 safely shuts down the Pi and returning to deep sleep.
2.  **Instrumentation Frontend (Active State):**
    *   **Condition:** Vehicle is running (Circuit 15 is 12V), and the Pi is actively running the UI.
    *   **Function:** Act as a sensor hub, digitizer, and code reader.
    *   **Action:** Continuously poll the I2C ADC bus, count duty-cycle pulses, and stream this synthesized data over Bluetooth Low Energy (BLE) to the Raspberry Pi 5 for real-time display.

## 2. Sensor Processing & Digitization (Firmware Tasks)

### 2.1 Analog Digitization (ADS1115 via I2C)
*   **Hardware:** ADS1115 (16-bit, 4-Channel).
*   **Firmware Requirement:** Operate the I2C bus at 400kHz (Fast Mode).
*   **Sampling:** Configure the ADS1115 for continuous conversion mode. The nRF5430 should read the converted values at ~100 SPS (Samples Per Second) for the Air-Flow Potentiometer and Battery Voltage.
*   **Multiplexer Control:** If using the CD74HC4051E to expand analog channels, the firmware must cleanly switch the selection GPIOs `(S0, S1, S2)`, wait a tiny settling time (e.g., 1ms), trigger a single-shot ADC conversion, read the result, and move to the next channel.

### 2.2 Blink Code Reader (Galvanic Isolation Path)
*   **Hardware:** TLP521 Optocoupler Output (3.3V GPIO Input).
*   **Firmware Requirement (Read Mode):** When commanded by the RPi5, the nRF5430 monitors the inverted optical input line. It must measure the duration of HIGH pulses (car pulling to ground). A short pulse (~0.5s) is a blink. The software counts the blinks between long pauses (~2.5s) to determine the integer fault code.
*   **Firmware Requirement (Clear Mode):** When commanded by the RPi5 to "Clear Code", the nRF5430 sets the TX GPIO pin HIGH for exactly 8 seconds, activating the optical switch and pulling the car's diagnostic line to Ground, then releases it.

### 2.3 Duty Cycle / PWM Measurement (X11 Pin 3)
*   **Hardware:** TLP521 Optocoupler Output into a Timer/Counter peripheral.
*   **Firmware Requirement:** The KE-Jetronic outputs a 100Hz square wave where the duty cycle (percentage of time spent LOW vs HIGH) represents the mixture correction. The nRF5430 must use a hardware timer with capture/compare features to constantly measure the ON time vs the period time to calculate a live 0-100% duty cycle value, averaged over 500ms intervals.

### 2.4 Outside Temperature (DS18B20 via 1-Wire on RPi5)
*   **Hardware:** DS18B20 digital temperature sensor (~€2), mounted in front airflow path (behind grille or near OEM sensor location).
*   **Interface:** 1-Wire protocol on a single RPi5 GPIO pin (3.3V, GND, data + 4.7kΩ pull-up). Does NOT go through the nRF5430 — read directly by the RPi5.
*   **Rationale:** The OEM outside temperature sensor is a simple NTC thermistor feeding the cluster's VDO LCD display (which is delaminated/failing). Rather than tapping the analog NTC signal through the ADS1115 and characterizing the unknown NTC curve, a modern DS18B20 provides ±0.5°C digital accuracy with trivial software (`w1thermsensor` Python library). This keeps the ADS1115 channels free for signals that only exist as analog (KE duty cycle, oil pressure, battery voltage). The OEM sensor and cluster LCD remain untouched — the RPi5 display supplements rather than replaces.
*   **Future option:** A second DS18B20 can be added on the same 1-Wire bus for cabin temperature.

## 3. Communication Protocol (nRF5430 <-> PC / RPi5)
The interface must establish a unified message format so the exact same test suite can be run from a PC/Mac over UART during initial bring-up, and later transported over Bluetooth Low Energy (BLE GATT) for the final RPi5 UI integration.

### Proposed Unified Payload Structure
All telemetry and commands will be packed into tight structures (e.g., **Header | Length | Type | Data | Checksum**) that can be safely transmitted either as a line-oriented string over a UART terminal, or as a byte array embedded within a BLE Characteristic.

#### Example Payloads:
*   *Type `0x02` (Analog Telemetry):* A packed struct of current Battery V, Airflow V, KE Duty Cycle %, and Outside Temp °C (e.g., streamed at 10Hz). Note: temperature is read locally by RPi5 (DS18B20 1-Wire) and merged into the UI data model, not transmitted over BLE from the nRF5430.
*   *Type `0x03` (Blink Code Read):* Sent when a full code sequence is successfully counted from the ADS module.
*   *Type `0x10` (Target Command - CLEAR CODE):* PC/Pi tells the Nordic to pull the ADS line low for 8 seconds to clear codes.

### Transport Layers
1.  **Transport 1: UART Debug Link (Phases 1-4):**
    *   Sent raw or as Base64/Hex strings over a standard 115200 baud serial connection for direct visibility in a Mac/PC terminal.
2.  **Transport 2: BLE GATT Profile (Phase 5):**
    *   **Service: Vehicle Telemetry (Custom UUID)**
    *   **Characteristic: Analog Data (Notify):** Carries the exact `0x02` binary payload.
    *   **Characteristic: Diagnostic Codes (Notify):** Carries the exact `0x03` binary payload.
    *   **Characteristic: Command Interface (Write):** Accepts the `0x10` clear code command from the RPi5.

*Note: The physical UI inputs (Alps rotary encoder) are wired directly to the RPi5 GPIOs, so they are not part of this communication logic.*

## 4. Development Milestones
1.  **Phase 1 (Wired Logic):** Get simple UART communications working with a PC/Mac to prove the message structuring and basic nRF5430 GPIO actions without vehicle power.
2.  **Phase 2 (Analog Reading):** Integrate the ADS1115 I2C driver and start reading raw voltages from the bench calibration setup, exposing them over the UART log stream.
3.  **Phase 3 (Vehicle Protocol):** Write the specific timing logic for capturing the KE 100Hz duty-cycle and the slow ADS blink codes, logging results to the PC/Mac over UART.
4.  **Phase 4 (BLE Migration):** Once the UART commands are proven perfect in the car, migrate the exact same payload structures to BLE GATT characteristics and link to the final RPi5 UI application.
