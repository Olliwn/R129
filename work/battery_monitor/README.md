# Battery Voltage & Temperature Monitor — Trunk Module

## Purpose

Continuously measure battery voltage and temperature using an INA226 bus voltage input and a DS18B20 digital temperature sensor, mounted in the trunk next to the battery. This module connects directly to the Raspberry Pi 5 via I2C (voltage) and one-wire (temperature). It is architecturally independent of the engine-bay nRF5340 instrumentation node.

**Design philosophy: fully non-invasive.** No series connection in the battery cable — no shunt, no bolted joints in the high-current path, no added failure points. Battery health and parasitic draw are inferred from voltage behavior over time, compensated by temperature.

## Why Voltage-Only

A current shunt inline with the battery cable provides direct current measurement but introduces mechanical failure points (bolted joints) in the most critical electrical path in the car. A corroded or loose bolt at 200A cranking current is an arc/fire risk. For a 35-year-old daily-driven car where reliability matters more than instrumentation precision, the safer approach is:

- Measure **voltage** at the battery terminals (non-invasive, fused sense wire only)
- Measure **temperature** at the battery case (non-invasive, surface-mounted sensor)
- Derive battery state from voltage behavior using well-established lead-acid models

This covers ~80% of what a full current-sense system would provide, with zero risk. A shunt can always be added later as a bolt-on upgrade if direct current measurement proves necessary.

## System Architecture

```
Battery (+) ── 1A fused sense wire ── INA226 VBUS pin
                                        │
Battery (-) ── existing cable (untouched) ── Chassis ground
                 │
                 └── INA226 GND (via RPi5 ground)

Battery case ── DS18B20 (strapped to side) ── RPi5 GPIO (one-wire)

                    ┌─────────────────────────┐
                    │        INA226           │
                    │  VBUS ← fused from B+   │
                    │  IN+/IN- shorted (unused)│
                    │  SDA ──┐                │
                    │  SCL ─┐│                │
                    │  VCC ┐││                │
                    │  GND┐│││                │
                    └─────┼┼┼┼────────────────┘
                          ││││
                 I2C cable (< 1 m)
                          ││││
                    ┌─────┼┼┼┼────────────────┐
                    │  RPi5                   │
                    │  GPIO 2/3 = I2C         │
                    │  GPIO 4 = DS18B20 1-wire│
                    └─────────────────────────┘
```

## Bill of Materials

| # | Component | Part Number / Ref | Qty | Est. Price | Notes |
|---|-----------|-------------------|-----|------------|-------|
| 1 | Voltage sense IC | **TI INA226** (breakout: CJMCU-226 from Fyndiq, 5-pack €15.39) | 1 (+4 spare) | ~€3/ea | 16-bit bus voltage: 0–36V, 1.25 mV/LSB. I2C. Shunt inputs unused (IN+/IN− shorted). Onboard 0.1Ω SMD shunt left in place — no current flows through it. |
| 2 | Temperature sensor | **DS18B20** (waterproof probe version) | 1 | ~€2–3 | Digital one-wire, ±0.5°C accuracy, −55 to +125°C. Strap to battery case with zip tie or thermal tape. |
| 3 | 4.7 kΩ pull-up resistor | 1/4W through-hole | 1 | ~€0.10 | Required for DS18B20 one-wire data line. |
| 4 | Inline fuse (VBUS sense) | 1A fast-blow glass fuse + holder | 1 | ~€1 | Protects the sense wire from battery positive. |
| 5 | I2C + one-wire cable | 5-conductor shielded, ~80 cm | 1 | ~€2 | SDA, SCL, 3.3V, GND, one-wire data. |
| 6 | Mounting hardware | Zip ties, Velcro, thermal tape | — | ~€1 | Secure PCB and temp sensor near battery. |

**Estimated total: ~€9–12** (INA226 from Fyndiq order, DS18B20 + fuse from local/AliExpress)

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Voltage range | 0–36 V |
| Voltage resolution | 1.25 mV per LSB |
| Temperature range | −55 °C to +125 °C |
| Temperature accuracy | ±0.5 °C |
| Voltage sample rate | Up to 950 Sa/s (configurable averaging) |
| Temperature sample rate | ~1 Sa/s (one-wire conversion time ~750 ms) |
| I2C address (INA226) | 0x40 default (configurable via A0/A1) |
| One-wire address (DS18B20) | Auto-discovered (unique 64-bit ROM code) |
| Supply voltage | 3.3 V from RPi5 GPIO header |

## Physical Installation

### VBUS Sense Wire

Run a single thin wire (22–24 AWG) from the INA226 VBUS pin to the battery positive terminal through the inline 1A fuse. This lets the INA226 measure battery voltage directly at the terminal. The wire carries only microamps of bias current — the fuse is purely for protection if the wire chafes.

### INA226 PCB Mounting

Mount the CJMCU-226 breakout near the battery on the trunk wall using Velcro or a small bracket. The shunt inputs (IN+/IN−) are unused — either short them together on the board or leave the onboard 0.1Ω SMD shunt in place (no current flows through it in this configuration).

### DS18B20 Temperature Sensor

Strap the waterproof DS18B20 probe to the battery case side wall using a zip tie or thermal-adhesive tape. Position it mid-height on the battery, away from the terminals. The sensor reads the battery's surface temperature, which closely tracks electrolyte temperature with a few minutes of thermal lag.

### Cable to RPi5

A single 5-conductor cable carries everything:

| Wire | INA226 / DS18B20 | RPi5 GPIO Pin | Function |
|------|-------------------|---------------|----------|
| 1 | INA226 VCC | Pin 1 (3.3V) | Power |
| 2 | INA226 GND + DS18B20 GND | Pin 6 (GND) | Ground |
| 3 | INA226 SDA | Pin 3 (GPIO 2 / SDA1) | I2C data |
| 4 | INA226 SCL | Pin 5 (GPIO 3 / SCL1) | I2C clock |
| 5 | DS18B20 DATA | Pin 7 (GPIO 4) | One-wire data (4.7 kΩ pull-up to 3.3V) |

Cable length ≤1 m. I2C at 100 kHz and one-wire both work fine at this distance.

## INA226 Configuration (Voltage-Only Mode)

With no shunt connected, only the bus voltage register is used. Configure for high-accuracy voltage measurement:

| Register | Field | Value | Effect |
|----------|-------|-------|--------|
| Config (0x00) | AVG | 64 samples | Good noise reduction |
| Config (0x00) | VBUS CT | 1.1 ms | Bus voltage conversion time |
| Config (0x00) | VSH CT | 140 µs | Minimum (shunt unused) |
| Config (0x00) | Mode | Bus voltage only, continuous | Save power, skip shunt conversion |

Effective update rate: ~14 Hz with 64× averaging.

## Software Integration (RPi5)

### Python Driver

```python
import smbus2
import glob
import time

INA226_ADDR = 0x40
REG_CONFIG  = 0x00
REG_BUS_V   = 0x02

bus = smbus2.SMBus(1)

def write_reg(reg, value):
    msb = (value >> 8) & 0xFF
    lsb = value & 0xFF
    bus.write_i2c_block_data(INA226_ADDR, reg, [msb, lsb])

def read_reg(reg):
    data = bus.read_i2c_block_data(INA226_ADDR, reg, 2)
    return (data[0] << 8) | data[1]

def init_ina226():
    # 64x averaging, 1.1ms VBUS CT, 140µs VSH CT, bus-only continuous
    config = 0x4205
    write_reg(REG_CONFIG, config)

def read_voltage_V():
    raw = read_reg(REG_BUS_V)
    return raw * 1.25 / 1000

# DS18B20 one-wire (requires dtoverlay=w1-gpio in /boot/config.txt)
def read_temp_C():
    devices = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
    if not devices:
        return None
    with open(devices[0], 'r') as f:
        lines = f.readlines()
    if lines[0].strip().endswith('YES'):
        idx = lines[1].find('t=')
        if idx != -1:
            return int(lines[1][idx+2:]) / 1000.0
    return None

init_ina226()
while True:
    v = read_voltage_V()
    t = read_temp_C()
    print(f"V = {v:6.3f} V  |  T = {t:5.1f} °C" if t else f"V = {v:6.3f} V  |  T = n/a")
    time.sleep(1.0)
```

### RPi5 Configuration

Enable one-wire interface for the DS18B20 by adding to `/boot/config.txt`:
```
dtoverlay=w1-gpio,gpiopin=4
```

### Data Logging

Log to the same data store used by the nRF5340 BLE telemetry stream. Each record:

```
timestamp, battery_voltage_V, battery_temp_C
```

## Derived Metrics — What Voltage Tells You

### 1. State of Charge (resting voltage)

A 12V lead-acid battery at rest (≥30 min, no load, no charge) has a predictable voltage-to-SoC relationship. Temperature compensation at ~−18 mV/°C improves accuracy significantly.

| Resting Voltage (25°C) | State of Charge |
|-------------------------|-----------------|
| 12.70 V | 100% |
| 12.50 V | ~85% |
| 12.40 V | ~75% |
| 12.20 V | ~50% |
| 12.00 V | ~25% |
| 11.80 V | Effectively dead |

Temperature-compensated voltage: `V_corrected = V_measured + 0.018 × (T_battery − 25)`

### 2. Parasitic Draw Estimation

With the car off and locked, log voltage every 60 seconds. The rate of voltage decay indicates parasitic draw:

- **Healthy (<50 mA):** Voltage drops ~10–20 mV over 8 hours.
- **Elevated (100–400 mA):** Voltage drops 50–200 mV over 8 hours.
- **Critical (>500 mA):** Voltage drops visibly within 1–2 hours.

The decay rate combined with known battery capacity (typically 70–80 Ah for R129) and temperature gives an approximate current estimate. This requires the car to be undisturbed for several hours, but the RPi5 sentry node can log overnight autonomously.

### 3. Cranking Health

During engine start, the voltage sags sharply. Log at maximum rate (~14 Hz) during crank events:

- **Healthy battery:** Sag to 10.0–10.5V, recovers to >12V within 1 second.
- **Weak battery:** Sag below 9.5V, slow recovery.
- **Failing battery:** Sag below 9V, may not recover enough to crank.

Trending the cranking sag depth over months shows battery aging before it fails.

### 4. Alternator Output

With engine running, voltage should be 13.8–14.4V. Below 13.5V suggests alternator trouble or belt slip. Above 14.8V suggests regulator failure.

### 5. Temperature-Correlated Trends

Battery capacity drops in cold weather (~50% at −20°C vs 25°C). By logging voltage vs temperature over a full winter/summer cycle, the system builds a model of the specific battery's behavior, enabling better SoC estimation and early failure prediction.

## UI Gauges

Add to the RPi5 gauge view:
- Battery voltage (numeric + bar, 10.0–15.0 V range)
- Battery temperature (numeric, −30 to +60 °C)
- Voltage trend (line chart, last 24 hours — reveals parasitic draw patterns)
- Cranking voltage log (triggered capture of start events)

## Relationship to Other Nodes

| Node | Location | Connection | Role |
|------|----------|------------|------|
| RPi5 | Trunk/cabin | — | Central hub, display, logging |
| nRF5340 + ADS1115 | Engine bay (F32 box) | BLE → RPi5 | Engine diagnostics: RPM, duty-cycle, airflow, blink codes |
| Battery monitor (this) | Trunk, near battery | I2C + one-wire → RPi5 | Battery voltage, temperature, SoC estimation, parasitic draw inference |
| Sentry node | TBD | BLE → RPi5 | Wake-on-approach, Pi power control |

The nRF5340's ADS1115 channel A1 was previously reserved for a battery voltage divider. With this dedicated trunk module providing higher-accuracy voltage measurements directly at the battery terminals, ADS1115 A1 is freed for a second engine-bay analog sensor (oil pressure, secondary temperature, or spare).

## Future Upgrade Path: Current Shunt

If direct current measurement is needed in the future, the design supports a straightforward upgrade:

1. Add a bolt-terminal shunt resistor (e.g. Milliohm HoFL2-75A or Vishay WSBS8518, 1 mΩ) inline with the battery negative cable.
2. Connect the shunt's Kelvin sense posts to the CJMCU-226 board's IN+/IN− pads (remove the short or desolder the onboard SMD shunt).
3. Program the INA226 calibration register (CAL = 0x0800 for 1 mΩ).
4. Update the software to read shunt voltage and current registers in addition to bus voltage.

This is a 30-minute hardware upgrade and a software config change. The INA226 and wiring are already in place.

## Build Sequence

1. **Order parts:** CJMCU-226 already ordered from Fyndiq (ETA April 16–22). Order DS18B20 + 4.7 kΩ resistor + fuse holder.
2. **Bench test:** Power INA226 from RPi5, connect VBUS to a bench supply, verify voltage readings. Test DS18B20 one-wire communication.
3. **Install VBUS wire:** Fused sense wire from battery positive to INA226.
4. **Mount PCB:** Near battery on trunk wall.
5. **Mount DS18B20:** Strap to battery case.
6. **Run cable:** To RPi5 GPIO header.
7. **Software:** Enable one-wire overlay, deploy driver, add to logging pipeline, add UI gauges.

## Safety Notes

- The VBUS sense wire to battery positive **must** be fused (1A). An unfused wire from the positive terminal is a fire risk if it chafes through insulation.
- The INA226, DS18B20, and cable carry only 3.3V logic signals — no automotive voltage exposure on the RPi5 side.
- No modifications to battery cables. The battery negative cable remains untouched.
- The DS18B20 is electrically isolated from the battery (reads temperature through the case wall).
