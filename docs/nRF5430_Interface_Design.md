# nRF5430 Interface Board Design

## Concept
The nRF5430 will act as a low-power, always-on Bluetooth LE scanner. When it detects the owner's smartphone, it will pull a GPIO pin HIGH. This GPIO will trigger a power-switching circuit to supply 12V/5V power to the Raspberry Pi 5 (and its UPS HAT), booting it up before the driver even opens the door.

## Automotive Power Considerations
- **Car Battery (Terminal 30):** Constant 12V (fluctuates between 11.5V and 14.4V).
- **Nordic Node Power:** Needs constant 5V (USB) or 3.3V. Current draw is negligible (~mA).
- **RPi 5 Power:** Requires up to 5V 5A (25W). It is much safer to switch the 12V high-side power going into a dedicated RPi 5 buck-converter/UPS HAT than to try and switch 5A at 5V directly through a MOSFET.

## Circuit Design: High-Side 12V Switch
Since the Nordic node operates at 3.3V logic, it cannot directly drive a 12V P-Channel MOSFET (it won't fully turn it off). We need an N-Channel MOSFET or standard NPN transistor to pull the gate of a P-Channel MOSFET low, or simply use an automotive-grade Relay module designed for 3.3V logic.

### Option A: Solid State (MOSFETs)
- **Q1 (Logic Level N-Channel MOSFET):** e.g., 2N7000 or IRLZ44N. Gate connects to nRF5430 GPIO (via 1kΩ resistor).
- **Q2 (Power P-Channel MOSFET):** e.g., IRF4905. Source connects to Car 12V. Drain connects to RPi Buck Converter. Gate connects to Q1 Drain.
- Pull-up resistor (10kΩ) between Car 12V and P-Channel Gate to keep it off by default.

### Option B: Pre-built Relay Module (Recommended for simplicity)
- A 3.3V compatible 1-channel relay module with optocoupler isolation. This safely isolates the delicate nRF5430 from the noisy 12V car electrical system.

## SP Elektroniikka Shopping List (Oulu)

1. **Power Conversion:**
   - [ ] 1x **12V to 5V USB Buck Converter** (For powering the nRF5430 constantly).
   - [ ] 1x **High Power 12V to 5V 5A Buck Converter** (For the Raspberry Pi 5, if not using a dedicated Car UPS HAT).

2. **Switching Components (Buy both options to test):**
   - [ ] 1x **3.3V Logic Relay Module** (with opto-isolator, rated for 10A+ at 12V/14V DC).
   - [ ] 2x **IRLZ44N** N-Channel MOSFETs (Logic level).
   - [ ] 2x **IRF4905** P-Channel MOSFETs (High current).

3. **Passive Components & Protection:**
   - [ ] 1x Resistor Assortment (Need 1kΩ, 10kΩ).
   - [ ] 2x **1N4007** Diodes (Flyback protection, especially if building relays manually).
   - [ ] 1x **Inline Automotive Blade Fuse Holder** (Splash-proof).
   - [ ] 1x Pack of **5A & 10A ATO/ATC Fuses**.

4. **Prototyping & Connectors:**
   - [ ] 1x **Solderable Perfboard (Reikälevy)** for mounting the MOSFETs/Relay permanently.
   - [ ] 1x Set of **Screw Terminal Blocks (Piirikorttiliitin)** (2-pin and 3-pin for easy 12V in/out wiring).
   - [ ] High-temp automotive wire (AWG 14 or 1.5mm² for power routes, AWG 22 for logic).
   - [ ] Heat shrink tubing & Zip ties.
