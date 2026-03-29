R129 Restomod: Infotainment & Audio Architecture
Project Overview
This document outlines the hardware architecture for modernizing the infotainment system of a 1991 Mercedes-Benz 500SL (R129). The core objective is an "OEM+" integration: providing modern compute (Raspberry Pi 5), navigation, and digital audio without permanently modifying the factory wood trim or compromising the period-correct aesthetic of the dashboard.

System Architecture
The system is divided into three distinct physical zones in the center console:

Audio Hub (DIN Slot): Factory-authentic radio acting as the master audio controller and amplifier.

Compute & Display (Upper Cubby): RPi5 and OLED screen acting as the modern "glass cockpit."

Input Controller (Ashtray): Custom, hidden iDrive-style rotary/joystick controller.

1. Audio Hub: Becker BE2210 ("Mercedes Special")
After evaluating aftermarket retro-styled options (Blaupunkt Bremen SQR 46 DAB) and flagship OEM units (Becker Exquisit BE1490/1690), the Becker BE2210 was selected as the optimal audio hub.

Aesthetic Alignment: Provides the exact 605nm amber illumination, matte black finish, and heavy rubberized tactile feel of the factory R129 interior.

Sourcing: Procured from EU-based specialists (e.g., original-autoradio.de) to ensure it is fully refurbished (dried capacitors replaced, sticky volume potentiometers rebuilt) and includes the necessary anti-theft security code.

Audio Routing: The RPi5 handles media playback. Audio is routed from the RPi5 into the BE2210 via the retrofitted internal AUX-IN (3.5mm jack on the rear of the unit, confirmed present on the delivered unit 2026-03-28). OPEN ITEM: The RPi5 has no native analog audio output (unlike the RPi4's 3.5mm jack). A USB audio interface or I2S DAC HAT is required to generate the analog signal. Candidates: HiFiBerry DAC2 Pro, Pimoroni pHAT DAC, or a basic USB sound card. Part selection and order pending.

Space Allocation: The BE2210 occupies the full depth of the DIN slot. Since compute hardware is relocated to the cubby, this depth is no longer a constraint.

Installation Status (2026-03-28): BE2210 received, wired in, and code accepted. Required ISO wiring connector + Wago 221-412 lever connectors for clean, reversible splicing of the factory harness. Old Sony CDX-410 removed and discarded. Still needs ISO-to-DIN (Motorola) antenna adapter — static on speakers until the factory antenna cable is properly connected to the BE2210's DIN antenna input.

Internet Connectivity: nRF93M1 Cat-1bis Module (NEW 2026-03-28)
For always-on internet connectivity (audio streaming, OTA map updates, remote vehicle diagnostics), a Nordic Semiconductor nRF93M1 Cat-1bis cellular module will be integrated with the RPi5. Cat-1bis provides up to 10 Mbit/s downlink — more than sufficient for high-quality audio streaming (Spotify 320 kbps), real-time data, and even firmware OTA. Cat-1bis offers better power efficiency than Cat-4 and wider band coverage than Cat-M1/NB-IoT, making it ideal for automotive IoT. The nRF93M1 connects to the RPi5 via USB or UART. This replaces the earlier "Wi-Fi tethering from phone" plan with a dedicated, always-on cellular link independent of the driver's phone.

Open items for nRF93M1 integration:
- SIM card: Need a data-only M2M/IoT SIM (e.g., Elisa IoT, DNA M2M, or a pan-European IoT SIM for cross-border driving).
- Antenna: External LTE antenna routed to an unobtrusive location (e.g., behind the rear window or inside the trunk lid). The R129's metal body is a Faraday cage — internal placement will not work.
- Power: The nRF93M1 dev kit runs on USB 5V — can share the RPi5's 5V rail.
- Software: AT command interface or native Nordic driver for Linux on the RPi5.

2. Compute & Main Display: RPi5 + 5.5" OLED
The factory storage cubby above the climate control unit is repurposed as the primary digital interface.

Hardware: Raspberry Pi 5.

Display: 5.5-inch OLED touchscreen. Touch capability is prioritized for map navigation (pinch/drag) to avoid clunky rotary UI implementation.

Mounting Strategy: The display will be flush-mounted behind a custom piece of smoked glass or acrylic, featuring rounded edges to mimic a factory option.

Power Delivery: All compute hardware and 5V step-down (buck) converters will be housed entirely within the void of the removed cubby, keeping the wiring harness isolated from the radio DIN slot below.

3. Human Machine Interface (HMI): The "Stealth" Controller
To control custom UI menus and RPi diagnostics without relying strictly on touch or drilling into the irreplaceable Zebrano/Burl Walnut wood console, a custom input device will be built into the factory ashtray.

Core Component: Alps Alpine RKJXT1F42001 (4-way analog joystick + rotary encoder + center push button).

Tactile Upgrade: The raw encoder shaft will be fitted with a premium machined metal knurled knob (e.g., OEDNI-90-4-7 / 226-4203-ND) to match the heavy, damped feel of the Mercedes interior.

Mounting Strategy: A custom ABS/PETG insert will be 3D printed to replace the removable factory ashtray bucket. The controller PCB will mount inside this print.

Clearance: Must be engineered on the Z-axis to ensure the factory sliding wood tambour door can close completely over the knurled knob, hiding the tech entirely when not in use.

Wiring Routing: GPIO lines (approx. 7-9 pins) and 5V power will be routed via multi-core cable (e.g., shielded CAT6) down through the adjacent cigarette lighter channel and up behind the center console to the Pi.

Hardware Pinout: RKJXT1F42001 to RPi5
The RKJXT1F42001 is a mechanical masterpiece, but it is "dumb" (no onboard IC). It relies purely on mechanical contacts. It combines three separate functions into one shaft, requiring 7 GPIO pins and a common ground.

1. The 4-Way Joystick (4 Pins)
These are simple momentary tactile switches for Up, Down, Left, and Right.

Pin A (Up): Route to RPi GPIO

Pin B (Right): Route to RPi GPIO

Pin C (Down): Route to RPi GPIO

Pin D (Left): Route to RPi GPIO

Note: These share a common Ground (COM) pin on the joystick PCB.

2. The Rotary Encoder (2 Pins)
This is a standard quadrature encoder (Phase A and Phase B). As you turn the knob, these two pins pulse, and the Pi calculates the direction (clockwise vs. counter-clockwise) based on which pin pulses first.

Phase A: Route to RPi GPIO

Phase B: Route to RPi GPIO

Note: These also share a common Ground (COM) pin.

3. The Center Push (1 Pin)

Push Switch: Route to RPi GPIO

Note: Shares a Ground (COM) pin.

The Engineering Solution for the Pi
Because the RPi5 GPIO operates at 3.3V logic, you need to manage the "bouncing" (the mechanical chatter of the metal contacts touching).

What you need to build/buy before the radio arrives:

A Custom Breakout Board: The RKJXT1F42001 has tiny, through-hole pins meant for a PCB. Do not try to solder wires directly to the pins; they will snap off when you press the joystick. You need a small piece of perfboard/protoboard to mount the joystick to securely.

Debouncing Strategy (Hardware vs. Software):

Hardware: You can solder small 10nF capacitors across the switch pins to ground on your custom breakout board. This smooths out the mechanical "clicks."

Software: Alternatively, you can just use Python/C++ to add a bouncetime=50 (50 milliseconds) software debounce in your RPi5 code. (Software is usually fine for the joystick, but hardware capacitors are highly recommended for the rotary encoder to prevent your menus from skipping wildly).

Pull-Up Resistors: The RPi5 has internal pull-up resistors you can activate via software. You will wire the joystick's COM pins to a single RPi Ground pin, and route the 7 function pins to 7 RPi GPIO pins. When a switch is pressed, it pulls the GPIO pin to Ground (Logic LOW).

The Umbilical Cord: To get these 8 wires (7 GPIO + 1 Ground) from the ashtray up to the cubby, a standard piece of CAT6 Ethernet cable is absolute perfection. It has exactly 8 wires inside, it is heavily shielded against automotive electrical noise, and it is very easy to route under the wood console.
