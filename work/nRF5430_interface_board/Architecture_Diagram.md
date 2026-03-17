# nRF5430 Interface Board Architecture Diagram

The true power of this modular setup is the absolute physical separation between the "Dirty" 12V vehicle side and the "Clean" 3.3V logic side.

```mermaid
flowchart TD
    classDef C_dirty fill:#ffcccc,stroke:#cc0000,stroke-width:2px;
    classDef C_clean fill:#ccffcc,stroke:#009900,stroke-width:2px;
    classDef C_power fill:#ffffcc,stroke:#cccc00,stroke-width:2px;
    classDef C_ext fill:#e6e6e6,stroke:#666666,stroke-width:2px;

    VehicleBatt["Vehicle 12V (Circuit 30/15)"]
    VehicleSensors["Vehicle Sensors (0-14V)"]
    DiagPort["X11 Diagnostic Port (Pin 3/9)"]
    MacPC["PC / Mac (Debug Terminal)"]
    RPi5["Raspberry Pi 5 (UI)"]

    subgraph PowerSystem ["Power Supply Subsystem (Protected 12V to 3.3V)"]
        Fuse["Inline Fuse (2A)"]
        ReversePol["1N4007 Diode (Reverse Polarity)"]
        TVS["1.5KE18A TVS Diode (Load Dump Clamp)"]
        Buck5V["Murata OKI-78SR-5-1.5 (5V Buck)"]
        LDO3V["LD1117V33 (3.3V LDO)"]
    end

    subgraph AnalogCond ["Analog Signal Conditioning Subsystem"]
        Dividers["Resistor Voltage Dividers (Drop 14V to ~2.7V)"]
        Clamps["1N4148 Clamping Diodes (0-3.3V Limit)"]
        OpAmps["LM358P Buffer RC Filter"]
        ADC["ADS1115 (16-bit 4-ch ADC)"]
    end

    subgraph GalvIso ["Galvanic Isolation Subsystem"]
        OptoRX["TLP521 Optocoupler (Read RX Lane)"]
        OptoTX["TLP521 Optocoupler (Write TX Lane)"]
    end

    subgraph NordicCore ["nRF5430 DK (Core Processing & Radio)"]
        MCU["nRF5430 SoC"]
        UART_Int["UART Peripheral"]
        BLE_Int["BLE Peripheral Antenna"]
        I2C_Int["I2C Bus"]
        GPIO_Int["GPIO Pins and Hardware Timers"]
        
        MCU --- UART_Int
        MCU --- BLE_Int
        MCU --- I2C_Int
        MCU --- GPIO_Int
    end

    VehicleBatt --> Fuse
    Fuse --> ReversePol
    ReversePol --> TVS
    TVS -->|Cleaned 12V| Buck5V
    Buck5V -->|5V Bus| LDO3V
    Buck5V -.->|5V Power| ADC
    Buck5V -.->|5V Power| OpAmps
    LDO3V -.->|Ultra-Clean 3.3V| MCU
    LDO3V -.->|Ultra-Clean 3.3V| OptoRX

    VehicleSensors ==>|High Voltage Analog| Dividers
    Dividers --> Clamps
    Clamps --> OpAmps
    OpAmps -->|Conditioned 0-3.3V Analog| ADC
    ADC == "I2C (400kHz)" ==> I2C_Int

    DiagPort ==>|12V Blink Pulses| OptoRX
    OptoRX -->|Inverted 3.3V Logic| GPIO_Int

    GPIO_Int -->|3.3V Logic Trigger| OptoTX
    OptoTX == "Hard Pull to GND" ==> DiagPort

    UART_Int <== "UART Debug Link" ==> MacPC
    BLE_Int <== "BLE GATT Link" ==> RPi5

    class VehicleBatt,VehicleSensors,DiagPort,MacPC,RPi5 C_ext;
    class Buck5V,LDO3V C_power;
    class Dividers,OptoTX C_dirty;
    class Clamps,OpAmps,ADC,OptoRX,MCU,UART_Int,BLE_Int,I2C_Int,GPIO_Int C_clean;
```

### Flow Architecture Narrative
1. **Power Path:** The raw 12V battery power enters through a fuse, passes a reverse-polarity diode, and hits the TVS diode to aggressively clip alternator spikes. The Murata buck converter drops it safely to a 5V logic rail. Finally, the LDO linear regulator drops that 5V down to an ultra-clean 3.3V supply tailored for the nRF5430 and reading optocouplers.
2. **Analog Path:** High voltage signals completely bypass the optocouplers. Instead, they hit resistor dividers, are hard-clamped to never exceed 3.3V, smoothed by LM358 op-amp buffers, and feed into the ADS1115 ADC. The ADC digitizes the signal and crosses the boundary to the nRF5430 via pure I2C data.
3. **Diagnostic (Digital) Path:** 12V diagnostic pulses hit the "Read" Optocoupler LED. This flashes a transistor on the clean side, passing isolated 3.3V logic to the nRF5430 GPIO. Conversely, the nRF5430 can trigger the "Write" Optocoupler, which bridges the vehicle diagnostic line straight to vehicle ground, completely bypassing the 3.3V subsystem.
4. **Data Exfiltration:** Processed data is sent over the UART peripheral directly to the Mac/PC during early phases. Later, this exact data stream routes out via the BLE Antenna directly to the RPi5 in the cabin.
