# Integration & Test Plan (nRF5430 Interface Board)

## 1. Prototype Build Phasing
To prevent cascading failures and isolate bugs, the interface board will be built and tested in strictly separated stages using breadboards before any final soldering or PCB design.

### Phase 1: Engine Independence (The "Clean" Side)
*   **Goal:** Establish the 3.3V power, baseline logic core, and UART debug link.
*   **Action:**
    1.  Power the nRF5430 DK via USB (no car power).
    2.  Develop the UART serial link to the PC/Mac.
    3.  Implement a simple text or binary protocol to simulate and dump diagnostic payloads over the serial terminal.
*   **Success Criteria:** The PC/Mac terminal successfully connects to the nRF5430, can send commands, and receives dummy telemetry without any vehicle power present.

### Phase 2: Power Supply Independence
*   **Goal:** Prove the power subsystem can survive the car without frying the DK.
*   **Action:**
    1.  Build the entire **Power Supply Subsystem** (TVS, Diodes, 5V Switcher, 3.3V LDO) on a standalone breadboard.
    2.  DO NOT connect the nRF5430.
    3.  Connect to bench power (14V). Load test the 5V and 3.3V outputs using dummy resistors.
    4.  Simulate severe electrical noise (flicking the bench power switch on/off rapidly) and watch the 3.3V rail on the Owon oscilloscope.
*   **Success Criteria:** A rock-solid, noise-free 3.3V output that never spikes above 3.6V under any switching condition.

### Phase 3: The "Dirty" Side Integration (Analog & Isolation)
*   **Goal:** Bring the vehicle signals into the prototype safely.
*   **Action:**
    1.  Build the **Galvanic Isolation** optocoupler circuits. Test with a 12V bench signal while monitoring the 3.3V output for clean square waves.
    2.  Build the **Analog Signal Conditioning** (Dividers, clamps, LM358 buffers).
    3.  Connect the ADS1115 to the conditioned analog lines.
    4.  Power this entire board from the proven Phase 2 Power Supply. Connect the nRF5430 DK via I2C to the ADS1115 and GPIO to the Optocouplers.
    5.  Observe the telemetry via the UART serial link to the PC/Mac.
*   **Success Criteria:** The nRF5430 can read analog voltages and simulated blink codes from a safe bench supply mimicking the car, logging results correctly to the PC terminal.

### Phase 4: Vehicle In-Loop Validation (AOK912)
*   **Goal:** Connect the full prototype to the R129's X11 socket.
*   **Action:**
    1.  Tap Pin 1 (GND) and Pin 3 (TD/Duty Cycle) or Pin 6 (Batt+) on the X11 diagnostic socket using banana plugs.
    2.  Monitor the Optocoupler output and the Analog buffered output with the Owon Oscilloscope *before* connecting them to the Nordic pins.
    3.  Once signals are verified safe (logic levels are 0-3.3V), connect the nRF5430 inputs.
    4.  Run the engine and observe live telemetry streaming to the PC/Mac terminal inside the vehicle cabin over UART.
*   **Success Criteria:** Live engine data (e.g., Battery Voltage, Duty Cycle) is displayed on the PC terminal without glitching or crashing the system during engine revs or startup.

### Phase 5: Wireless Migration (BLE to RPi5 UI)
*   **Goal:** Transition from the wired PC/Mac debug link to the final BLE GATT link with the Raspberry Pi 5.
*   **Action:**
    1.  Develop the BLE Peripheral code on the nRF5430 to advertise the telemetry services.
    2.  Migrate the proven UART messaging structures directly into BLE characteristic payloads.
    3.  Connect the RPi5 UI application to the nRF5430 over Bluetooth.
*   **Success Criteria:** The RPi5 UI application receives the exact same, stable telemetry format over BLE that the PC previously received over UART, completely wire-free.

## 2. Risk Management & Fallbacks

### Risk: nRF5430 DK is too bulky for permanent vehicle installation.
*   *Mitigation:* The DK is strictly for firmware development. Once the software architecture (I2C, BLE GATT) is proven, the design will migrate to a smaller production module (e.g., a pre-certified nRF5430 or nRF52840 module like a Seeed XIAO BLE or custom PCB).

### Risk: Analog ground loops induce noise in the ADS1115 measurements.
*   *Mitigation:* The power supply design enforces a single-point "Star Ground" meeting at the main Power Supply breadboard. If noise persists, the analog front-end will be updated to use differential measurement (`AIN0 - AIN1`) on the ADS1115 instead of referencing the vehicle chassis ground directly.

### Risk: 12V Load Dump destroys the switching regulators.
*   *Mitigation:* The `1.5KE18A` TVS diode is specifically designed to absorb massive energy spikes. If the Owon scope reveals it is insufficient during Phase 4, a Series Inductor (Pi-Filter layout) will be added before the Murata switcher to slow the dV/dt of the transient spike.
