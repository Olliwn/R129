# ADS Blink-Code Reader

## Overview
A simple diagnostic tool consisting of a momentary push button and a 12V LED. This is used to read and clear blink codes from the Adaptive Damping System (ADS) on the 1991 Mercedes-Benz R129 500 SL.

## Components
- 1x 12V LED (or standard LED with appropriate series resistor, e.g., 680Ω to 1kΩ)
- 1x Momentary push button (Normally Open)
- 3x 4mm Banana Plugs (for X11 / 16-pin diagnostic port)
- Wiring (e.g., Tesa cloth taped for a clean look)
- (Optional) Small project enclosure

## Wiring / Schematic
The 16-pin diagnostic connector (X11/4) in the engine bay requires the following connections for ADS diagnosis:
- **Pin 1:** Ground (Terminal 31)
- **Pin 9:** ADS Diagnostic output signal
- **Pin 16:** +12V Power (Terminal 15, Ignition ON)

### Circuit / Wiring Steps
**1. Prepare the wires with Banana Plugs:**
   - **RED Wire:** Attach to a 4mm Banana Plug. This will go to **Pin 16 (+12V)**.
   - **BLACK Wire:** Attach to a 4mm Banana Plug. This will go to **Pin 1 (Ground)**.
   - **YELLOW Wire:** Attach to a 4mm Banana Plug. This will go to **Pin 9 (Signal)**.

**2. Wire the LED:**
   - Connect the **Anode (+)** (longer leg) of the LED to the **RED Wire (+12V)**.
   - Connect the **Cathode (-)** (shorter leg) of the LED to the **YELLOW Wire (Signal)**.

**3. Wire the Push Button:**
   - Connect one terminal of the **Push Button** to the **YELLOW Wire (Signal)**.
   - Connect the other terminal of the **Push Button** to the **BLACK Wire (Ground)**.

*Note: The control module will ground Pin 9 to light the LED and flash the codes. Shorting Pin 9 to Ground via the push button signals the module to output the next code or clear the current code.*

## Usage Procedure
1. Turn the ignition to the **ON** position (engine off).
2. Connect the tool's banana plugs to pins 1, 9, and 16.
3. **Read Codes:** 
   - Press the button for **2 to 4 seconds**.
   - Count the number of flashes on the LED. The number of flashes represents the fault code.
   - Repeat the process until the first code repeats (indicates all codes have been read).
   - *Note: Code 1 means "No faults stored."*
4. **Clear Codes:** 
   - You must read a code first. 
   - Once it finishes flashing, press and hold the button for **6 to 8 seconds**.
   - Release the button. 
   - Fault codes must be erased one by one. Read the next code and repeat the erase procedure.

## Log / Notes
*TODO: Document fault codes extracted from vehicle and the results of the reset here.*

5/ ASD - no connector
6/ SRS -  3/8/9 pulses - after reset 1 blink (2 blink state that needed to be reset)
7/ RB - 2/3/4/5/6/7 pulses - after reset i blink
8 /DI/EZL - 17 pulses -after reset 1 blink
9 / ADS - weak static glow
10/ RST - 11/20/28/29 pulses - bo blinks after single reset, happened twice
11/ ATA - static glow (medium)
12 / IRCL - static glow (medium)
13 / ETC - no connector
14/ ESMC - 11/12 pulses - after reset 1 blink (2 blink state that needed to be reset)