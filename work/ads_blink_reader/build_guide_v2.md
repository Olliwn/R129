# ADS Blink-Code Reader (V2 - Robust Build)

After the initial prototype wire-harness broke during testing, this guide covers building a **Version 2 (V2)** blink-code reader using a proper circuit board (perfboard/stripboard) or a small project enclosure to ensure mechanical durability for long-term diagnostic use.

## 1. The Circuit Diagram

The X11/4 diagnostic connector uses a very simple ground-switching logic. 
- The car provides **+12V** (Pin 16) and **Ground** (Pin 1).
- The **Signal** pin (e.g., Pin 9 for ADS) is normally floating or pulled high by the car's module. 
- When the module wants to blink the LED, it briefly pulls the Signal pin to Ground.
- When *you* want to trigger the next code or clear a code, you press the button, which manually shorts the Signal pin to Ground.

### Schematic:
```text
[Pin 16] +12V (RED) ──[ 1A FUSE ]──> [ 1kΩ RESISTOR ] ──> (Anode +) [LED] (Cathode -) ──> [Pin X] Signal (YELLOW)
                                                                                            │
[Pin 1]  GND (BLACK) ─────────────────────────────────────────────── [ PUSH BUTTON ] ───────┘
```

## 2. Components Needed

1. **Circuit Board:** Small piece of perfboard/veroboard (approx. 3x3 cm is plenty) OR a small plastic electronics enclosure.
2. **Push Button:** Momentary push button (Normally Open - NO). Panel-mount preferred if using an enclosure, or through-hole tactile switch if just using a bare board.
3. **LED:** 
   - Option A: A pre-wired "12V LED" (has an internal resistor).
   - Option B: A standard 3V/5V LED (e.g., standard 5mm Red/Yellow LED) **PLUS a 680Ω or 1kΩ resistor** in series.
4. **Wiring:** 3 cores of stranded copper wire (~1 meter long). Red, Black, and Yellow are standard.
5. **Fuse:** Inline 1A or 2A fuse (glass or blade type) for the +12V line. Protects the car's diagnostic circuit in case of a short in your tool.
6. **Connectors:** 3x 4mm Banana Plugs (to plug into the car's diagnostic socket).
7. **Strain Relief:** Zip ties or hot glue to secure the wires to the board so they don't snap off at the solder joints.

## 3. Step-by-Step Soldering Guide (Perfboard)

If you are using a standard LED and resistor:

1. **Mount the Components:**
   - Insert the Push Button into the center of the perfboard.
   - Insert the LED.
   - Insert the Resistor.
   - Mount the Fuse Holder (if using a board-mounted fuse, otherwise wire an inline fuse to the Red wire before it reaches the board).

2. **The +12V Path (Red Wire):**
   - Solder the **Red wire** to one side of the Fuse.
   - Solder the other side of the Fuse to one end of the Resistor.
   - Solder the other end of the Resistor to the **LED Anode** (the longer leg).

3. **The Ground Path (Black Wire):**
   - Solder the **Black wire** to one side of the Push Button.

4. **The Signal Path (Yellow Wire) - The Junction:**
   - Solder the **LED Cathode** (the shorter leg) to the *other* side of the Push Button.
   - Solder the **Yellow wire** to this exact same junction (where the LED Cathode and the Button meet).

5. **Strain Relief (CRITICAL):**
   - The reason prototypes break is that wire flexes at the solder joint and snaps. 
   - Drill two small holes at the edge of your perfboard. Run a zip-tie through them and tightly strap all three wires (Red, Black, Yellow) down to the board, about 1cm away from your solder joints. Alternatively, bury the wires in a large blob of hot glue.

6. **Terminate the ends:**
   - Strip the other ends of the 3 wires and screw/solder them into the three 4mm Banana Plugs.

## 4. Testing the Board (Bench Test)
Before plugging it into the car, you can test it with a 12V battery or bench supply:
1. Connect RED plug to +12V.
2. Connect BLACK plug to Ground.
3. The LED should be **OFF**.
4. Touch the YELLOW plug to Ground. The LED should turn **ON**.
5. Disconnect the YELLOW plug from ground. The LED should turn **OFF**.
6. Press the Push Button. The LED should stay **OFF** (because yellow isn't connected to the LED anode, pushing the button just shorts yellow to black. If the LED turns on when you push the button, you have wired the button across the LED incorrectly!).

## 5. Usage in Car

1. Ignition ON (Engine OFF).
2. **RED** plug into **Pin 16**.
3. **BLACK** plug into **Pin 1**.
4. **YELLOW** plug into **Pin 9** (or any other module pin).
5. **To Read:** Press button for 2-4 seconds. Count the flashes.
6. **To Clear:** After reading a code, press button for 6-8 seconds to erase it. Read again to confirm it cleared.