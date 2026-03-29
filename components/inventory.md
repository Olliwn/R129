# Component Inventory — AOK912 R129 SL

Last updated: 2026-03-21

This document tracks all electronic components on hand for the nRF5430 interface board
and related R129 subsystems. Components are cross-referenced to their purchase orders
and the build stage where they are first used.

Datasheets can be stored alongside this file in `components/datasheets/`.

---

## Power Supply & Protection

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| DC-DC Buck Converter | OKI-78SR-5/1.5-W36-C | SIP-3 | 2 | DigiKey | 98080586 #11 | 4.26 | Stage 1 | 12V→5V, 1.5A, 36V max input |
| DC-DC Buck Converter | OKI-78SR-3.3/1.5-W36-C | SIP-3 | 2 | DigiKey | 98080586 #12 | 4.26 | — | 12V→3.3V direct. Spare / future Pi path |
| LDO Regulator 3.3V | LD1117V33 | TO-220 | 2 | DigiKey | 98080586 #26 | 0.49 | Stage 1 | 5V→3.3V, 800mA |
| LDO Regulator 5V | LM2940T-5.0/NOPB | TO-220 | 2 | DigiKey | 98080586 #25 | 1.70 | — | Automotive-rated 5V LDO, spare/alternate |
| TVS Diode | 1.5KE18A | DO-201 (axial) | 4 | DigiKey | 98080586 #10 | 0.33 | Stage 1 | 15.3V standoff, load dump clamp |
| Rectifier Diode | 1N4007 | DO-204AC | 20 | DigiKey | 98080586 #28 | 0.067 | Stage 1 | 1000V/1A, reverse polarity protection |
| Schottky Diode | 1N5819 | DO-204AC | 3 | DigiKey | 98080586 #29 | 0.23 | — | 40V/1A Schottky, lower Vf. Spare |
| P-Channel MOSFET | IRF5305 | TO-220 | 1 | SP Elektroniikka | 3044737 #111403 | 3.30 | Stage 1 | 55V/31A, Rds_on=60mΩ, Vgs_th=−2 to −4V. Diagnostics enable switch |
| Blade Fuse 2A | 32V 19×20mm | Blade | 2 | SP Elektroniikka | 3044737 #108113 | 1.00 | Stage 1 | Input protection |
| Blade Fuse 5A | 32V 19×20mm | Blade | 2 | SP Elektroniikka | 3044737 #108116 | 1.00 | — | Spare / higher current path |
| Fuse Holder | 19×20mm blade type | Inline w/ crimp | 4 | SP Elektroniikka | 3044737 #100533 | 1.40 | Stage 1 | For automotive blade fuses |
| Step-Down DC-DC | Adjustable 0.8–28V 12A | Module | 1 | SP Elektroniikka | 3044737 MNK-190 | 18.00 | — | For Raspberry Pi 5V/3A path (future) |

## Semiconductors — Discrete

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| NPN Transistor | 2N3904 | TO-92 | 2 | SP Elektroniikka | 3044737 #108580 | 0.50 | Stage 1 | Level shifter (Q_LVL), TX driver (Q_DRV) |
| NPN Transistor | 2N3904 | TO-92 | 25 | DigiKey | 98080586 #24 | — | Stage 2+ | Part of SparkFun semiconductor kit #13682 |
| PNP Transistor | 2N3906 | TO-92 | 25 | DigiKey | 98080586 #24 | — | — | Part of SparkFun semiconductor kit #13682 |
| N-Channel MOSFET | 5LN01SP | SOT-23 | 10 | DigiKey | 98080586 #24 | — | — | SparkFun kit. SOT-23, needs breakout for breadboard |
| P-Channel MOSFET | 5LP01SP | SOT-23 | 10 | DigiKey | 98080586 #24 | — | — | SparkFun kit. SOT-23, Vds=8V only (too low for 12V) |
| Voltage Regulator | LM317LZ | TO-92 | 5 | DigiKey | 98080586 #24 | — | — | SparkFun kit. Adjustable LDO |
| Voltage Reference | TL431A | TO-92 | 5 | DigiKey | 98080586 #24 | — | — | SparkFun kit. 2.5V precision reference |

## Optocouplers & Isolation

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| Quad Optocoupler | TLP521-4 / PC847 | DIP-16 | 6 | SP Elektroniikka | 3044737 #110515 | 2.50 | Stage 2 | 4 channels per IC. Need 5 for full build (3 RX + 2 TX), 1 spare |
| 16-Pin DIP Socket | Machined pin (holkkikanta) | DIP-16 | 6 | SP Elektroniikka | 3044737 SCH29331 | 0.50 | Stage 2 | Sockets for optocouplers — do not solder ICs direct |

## Analog & Signal Conditioning

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| Dual Op-Amp | LM358P | DIP-8 | 10 | DigiKey | 98080586 #8 | 0.16 | Stage 4 | Battery + airflow buffers. 9 spares |
| 16-bit ADC Breakout | ADS1115 | I2C module | 1 | DigiKey | 98080586 #7 | 12.80 | — | 4-channel, for precision measurements |
| 8:1 Analog Mux | CD74HC4051E | DIP-16 | 2 | DigiKey | 98080586 #1 | 0.74 | — | Channel expansion for ADC |
| Current Monitor | INA169NA/3K | SOT23-5 | 2 | DigiKey | 98080586 #9 | 1.98 | — | High-side current sense (EHA tracking) |
| Level Shifter | TXB0108 Breakout | Module | 1 | DigiKey | 98080586 #30 | 6.14 | — | 8-ch bidirectional 3.3V↔5V |

## Signal Diodes

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| Signal Diode | 1N4148 | DO-35 | 50 | DigiKey | 98080586 #27 | 0.033 | Stage 4 | Clamping diodes for analog paths |
| Signal Diode | 1N4148 | DO-35 | 20 | DigiKey | 98080586 #24 | — | — | SparkFun semiconductor kit (additional) |
| Power Diode | 1N4004 | DO-204 | 20 | DigiKey | 98080586 #24 | — | — | SparkFun semiconductor kit |

## Passive Components — Resistors

| Component | Values Included | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|----------------|---------|-----|--------|---------|--------|-------------|-------|
| Resistor Kit | 25 values × 20 pcs (500 total) | 1/4W TH | 1 kit | DigiKey | 98080586 #19 | 8.99 | Stage 1+ | SparkFun #10969 |

**Values in kit (25 each):**

| Value | Qty | Used in Build | Role |
|-------|-----|--------------|------|
| 10Ω | 25 | — | — |
| 22Ω | 25 | — | — |
| 47Ω | 25 | — | — |
| 100Ω | 25 | — | — |
| 150Ω | 25 | — | — |
| 220Ω | 25 | — | — |
| 330Ω | 25 | 8 needed | TX LED current limiting (R_TX) |
| 470Ω | 25 | — | — |
| 510Ω | 25 | — | — |
| 680Ω | 25 | 1 needed | Blink simulator pull-up (R_SIM) |
| 1kΩ | 25 | 20 needed | RX limit ×9, TX collector ×8, buffer out ×2, misc |
| 2.2kΩ | 25 | 1 needed | Battery divider lower (R_BAT_LO) |
| 3.3kΩ | 25 | 9 needed | RX pull-up: 10kΩ + 3.3kΩ in series = 13.3kΩ (or use 10kΩ alone) |
| 4.7kΩ | 25 | — | — |
| 5.1kΩ | 25 | — | — |
| 6.8kΩ | 25 | — | — |
| 10kΩ | 25 | 14 needed | TX base pull-down ×8, gate ×1, enable base ×1, dividers ×3, sim base ×1 |
| 22kΩ | 25 | — | — |
| 47kΩ | 25 | — | — |
| 100kΩ | 25 | 1 needed | P-FET gate pull-up (R_GP) |
| 330kΩ | 25 | — | — |
| 1MΩ | 25 | — | — |
| 4.7MΩ | 25 | — | — |
| 10MΩ | 25 | 2 needed | ADC input model (R_ADC), simulation only |

## Passive Components — Capacitors

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| Ceramic Cap | 100nF (0.1µF) 50V X7R | Radial TH | 60 | DigiKey | 98080586 #20/#21 | 0.09 | Stage 1+ | Decoupling everywhere. K104K10X7RF5UH5 |
| Ceramic Cap | 10nF (10000pF) 50V X7R | Radial TH | 10 | DigiKey | 98080586 #22 | 0.15 | — | RC filter option. C315C103K5R5TA |
| Capacitor Kit | Mixed values 10pF–1000µF | TH | 1 kit | DigiKey | 98080586 #23 | 9.85 | Stage 1 | SparkFun #13698. Includes electrolytic 100µF for C_IN, C_DIAG |

## Connectors & Hardware

| Component | Value / Part Number | Package | Qty | Source | Order # | Unit € | Build Stage | Notes |
|-----------|-------------------|---------|-----|--------|---------|--------|-------------|-------|
| Header Vertical 4-pos | 61300411121 | 2.54mm TH | 10 | DigiKey | 98080586 #13 | 0.14 | — | Board-to-board connectors |
| Terminal Block Plug 2-pos | Phoenix 1757019 | 5.08mm | 2 | DigiKey | 98080586 #14 | 2.03 | — | Screw terminal for power |
| Terminal Block Plug 4-pos | Phoenix 1757035 | 5.08mm | 1 | DigiKey | 98080586 #15 | 3.74 | — | Backordered |
| Terminal Block Hdr 2-pos | Phoenix 1786404 | 5.08mm | 2 | DigiKey | 98080586 #16 | 2.33 | — | Mating header for 2-pos plug |
| Terminal Block Hdr 4-pos | Phoenix 1786420 | 5.08mm | 1 | DigiKey | 98080586 #17 | 4.37 | — | Mating header for 4-pos plug |
| Banana Plug Black | BL3 60V/10A | 4mm | 3 | SP Elektroniikka | 3044737 #103678 | 3.30 | Stage 7 | X11 diagnostic connector (GND) |
| Banana Plug Red | BL3 60V/10A | 4mm | 7 | SP Elektroniikka | 3044737 #103677 | 3.30 | Stage 7 | X11 diagnostic connector (signal pins) |
| Pushbutton Blue | PPN1 OFF-ON momentary | Panel mount | 1 | SP Elektroniikka | 3044737 #103138 | 1.20 | — | Manual test button |
| Pushbutton Green | PPN1 OFF-ON momentary | Panel mount | 1 | SP Elektroniikka | 3044737 #103136 | 1.20 | — | Manual test button |

## Breadboards & Prototyping

| Component | Description | Qty | Source | Order # | Unit € | Assignment | Notes |
|-----------|------------|-----|--------|---------|--------|-----------|-------|
| Proto-Half | PTSolns PTS-00079-201 | 2 | DigiKey | 98080586 #6 | 2.15 | **#1:** Power + Analog, **#2:** Optos + Drivers | 116.8×58.4mm, 450 tie-points, 2.54mm pitch, screw terminal, configurable power rails, M3 mount holes |
| Stripboard | BusBoard ST1 (PTH) | 3 | DigiKey | 98080586 #4 | 3.00 | Breakout / overflow | 50×80mm, 31×19 holes, FR4 stripboard, 2.54mm pitch |
| Solderable BB | DKS-SOLDERBREAD-02 (PTH) | 1 | DigiKey | 98080586 #2 | 2.99 | Spare / expansion | 81.3×50.8mm, double-sided, 5-hole pad groups, 2.54mm pitch |
| Proto-board | SparkFun 08808 | 3 | DigiKey | 98080586 #3 | 2.53 | Breakout jigs | 25.4×25.4mm (1" square), 3-hole traces, 2.54mm pitch. Too small for circuits — useful for SOT-23 breakouts |
| Proto-board | Adafruit 5588 | 3 | DigiKey | 98080586 #5 | 1.67 | **NOT USABLE** | **2mm pitch — incompatible with standard 2.54mm components.** Intended for XBee-style modules only |

## Wire & Consumables

| Component | Description | Qty | Source | Order # | Unit € | Notes |
|-----------|------------|-----|--------|---------|--------|-------|
| Jumper Wire | SKT-SKT 24AWG 4" Black | 10 | DigiKey | 98080586 #18 | 0.26 | JST ASPHSPH24K102 |
| Hook-up Wire Yellow | 0.25mm² 10m | 1 | SP Elektroniikka | 3044737 | 3.00 | Signal wiring |
| Hook-up Wire Black | 0.25mm² 10m | 1 | SP Elektroniikka | 3044737 | 3.00 | GND bus |
| Hook-up Wire Red | 0.25mm² 10m | 1 | SP Elektroniikka | 3044737 | 3.00 | Power bus |
| LED Kit | 3mm + 5mm, 5 colors, 300 pcs | 1 | SP Elektroniikka | 3044737 691-LEDKIT3 | 6.00 | Status indicators |
| Heat Shrink Kit | 100 pcs black | 1 | SP Elektroniikka | 3044737 #206936 | 3.50 | Wire insulation |
| Alligator Clips | 48cm leads, 10 pcs | 1 | SP Elektroniikka | 3044737 #109953 | 6.80 | Temporary connections |
| Solder | 1.0mm lead-free, 16g | 1 | SP Elektroniikka | 3044737 #23052 | 6.50 | |
| Solder Wick | 3.0mm × 1.5m | 1 | SP Elektroniikka | 3044737 998-HWY-30x | 4.00 | Desoldering |
| Tweezers | Anti-magnetic curved 125mm | 1 | SP Elektroniikka | 3044737 SPN23287 | 4.50 | SMD handling |
| Speaker Cable | OFC 2×1.5mm² 10m | 1 | SP Elektroniikka | 3044737 #15096 | 22.50 | For car audio / power wiring |

## UI & Input (Future)

| Component | Description | Qty | Source | Order # | Unit € | Notes |
|-----------|------------|-----|--------|---------|--------|-------|
| Joystick | ALPS RKJXT1F42001 analog | 1 | DigiKey | 98080586 #31 | 7.44 | Radio/UI navigation |
| Knob | KILO OEDNI-90-4-7 knurled metal | 1 | DigiKey | 98080586 #32 | 10.68 | For joystick/encoder |
| AMOLED Display | Waveshare 5.5" 1080×1920 HDMI | 1 | Waveshare | 260318-150638-E0 | $124.99 | RPi5 cabin display |
| DSI Cable 500mm | RPi5 22-to-15 pin FPC | 1 | Waveshare | 260318-150638-E0 | $3.49 | |
| DSI Cable 200mm | RPi5 22-to-15 pin FPC | 1 | Waveshare | 260318-150638-E0 | $1.19 | |

## Test Equipment

| Item | Model | Source | Order # | Price € | Notes |
|------|-------|--------|---------|---------|-------|
| Handheld Oscilloscope | Owon HDS242 40MHz 2CH | Elgood Oy | 400656 | 178.00 | Purchased 16.3.2026 |
