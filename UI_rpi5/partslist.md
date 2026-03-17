# Raspberry Pi 5 (UI & Telematics) Parts List

This document tracks the hardware required for the primary user interface and telematics unit running on the Raspberry Pi 5. The goal is to fit within the standard 1-DIN car audio slot (approx 180mm x 50mm) while maintaining an OEM, premium feel.

## 1. Displays (1-DIN / High Aspect Ratio)
*Requirement: The goal is to fit within the 180mm x 50mm 1-DIN slot. While OLED offers absolute blacks, high-aspect-ratio (bar type) RGB OLEDs do not exist. Therefore, we must use a Full Color IPS LCD and focus intensely on mitigating backlight bleed to blend into the dark dashboard.*

### Option A: The "Holy Grail" (Full Color AMOLED)
*This completely solves the RGB OLED problem. By using a repurposed 5.5" smartphone-style AMOLED panel, we achieve the ultimate automotive UI: high-definition full color AND absolute infinite blacks.*

*   **Waveshare 5.5" HDMI AMOLED (1080x1920):** **[Top Pick]** Once configured to display horizontally (landscape) in the RPi5 software, this becomes a stunning bar display. Because it is true AMOLED, the black UI backgrounds will completely turn off, blending flawlessly into the R129's dark center console without *any* grey backlight bleed.
    *   *Dimensions & Mounting:* The module is roughly 141mm wide x 74.5mm tall. Because it is 24.5mm taller than the standard 50mm 1-DIN slot, you have two choices: Build a custom bezel that mounts the screen slightly *proud* (forward) of the slot, OR use the **"Secret Cubby" Mount** hidden behind the sliding wooden tambor door in the lower console. *(Note: ALWAYS build a physical cardboard mock-up for the cubby to verify hinge mechanism clearance!)*

### Option B: Premium "Bar" Type IPS LCDs (If AMOLED is unavailable)
*These screens connect easily via HDMI or DSI, but because they have backlights, they require software dimming and dark UI design to mitigate grey glow at night.*

*   **Waveshare 7.9" IPS (400x1280):** 205mm wide (Too wide for a flush DIN fit, sits proud).
*   **Waveshare 6.8" IPS (320x1280):** Fits much better within the physical width of the center console.
*   **Waveshare 6.25" IPS (1520x722 DSI):** 159mm x 74mm. Excellent for the "secret cubby" mount.

### Option C: Small Monochrome OLEDs (Retro OEM Look)
*   **3.12" 256x64 OLED (Driver: SSD1322):** Excellent minimalist automotive OLED, ultra-wide aspect ratio, but monochrome only. Interface via SPI.

## 2. Premium Rotary Encoders & Aluminum Knobs (The "iDrive" Feel)
For a true premium feel, skip the standard $1 mechanical EC11 encoders. You want **Optical** or **Magnetic** encoders with engineered haptics.

*   **Grayhill 62S or 62H (High Torque) Series:** **[Top Pick]** Grayhill is legendary for its haptics. These are optical encoders (meaning no physical contacts to wear out). The "62H" series specifically uses specialized detents to provide a heavy, premium, highly tactile "click" reminiscent of high-end luxury car dials.
*   **Bourns EM14 Series:** An excellent optical encoder option.
*   **Bourns PEC11H Series:** The "H" ball/spring mechanical option for heavy detent feel.

### The Knob (Crucial for the "Thunk" feel)
The encoder mechanism is only half the battle. You **must** pair an optical encoder with a heavy, solid machined-aluminum knob. The physical mass of the aluminum acts as a flywheel, significantly enhancing the tactile "thunk" between detents.

*   **Selected Option:** **[Kilo International OEDNI-90-4-7 (DigiKey: OEDNI-90-4-7-ND)](https://www.digikey.fi/en/products/detail/kilo-international/OEDNI-90-4-7/5970359)**
    *   *Why this fits perfectly:* It is **Matte Black** (matching the 90s Mercedes instrument clusters), it fits the exact **6.00mm** shaft of the ALPS RKJXT1F42001, uses a set-screw to lock onto the D-shaft flat, and has a wide, low-profile "hockey puck" shape (23.50mm x 15.88mm) perfect for leveraging the 4-way tilt function of the switch.

### Wiring the Encoder to the RPi5
Wiring a rotary encoder to a Raspberry Pi is brilliantly straightforward. You do not need any special chips between the encoder and the Pi!

1.  **The Inputs (GPIO):** Rotary encoders output "Quadrature" signals (Channel A and Channel B). You simply connect Channel A to one RPi5 GPIO pin (e.g., GPIO 5) and Channel B to another (e.g., GPIO 6). 
2.  **The Common Pin:** Connect the encoder's Common (or Ground) pin to any `GND` pin on the RPi5.
3.  **The Push Button:** Connect one side of the built-in push switch to another GPIO pin (e.g., GPIO 13), and the other side to `GND`.
4.  **Hardware Pull-Ups:** The Raspberry Pi 5 has internal pull-up resistors on all GPIO pins. You just enable them in your Python code, and the Pi will perfectly read the encoder ticks without any extra external resistors needed!

*(Note: If you buy an **Optical** encoder like the Grayhill or Bourns EM14, it will require adding 5V or 3.3V power to run its internal LEDs, in addition to the A, B, and Ground wires).*
