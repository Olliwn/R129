# Parts to Order — AOK912 (1991 R129 500 SL)

**Vehicle:** WDB 129066 1F 044414 | **Engine:** M119.960 (KE-Jetronic) | **Trans:** 722.3

*Single source of truth for all parts, consumables, and tools. Replaces the former `Karkkainen_Shopping_List.md`. Organized by priority/project. Print this and walk into MB-osat Oulu — they can cross-reference by VIN and confirm fitment for the tricky M119.960 early-model parts that Autodoc gets wrong.*

**Recommended sourcing strategy:**
- **MB-osat (Oulu):** First stop for anything with an "A 1xx..." OEM number. They have the MB parts catalog and can verify fitment by VIN. Best for gaskets, seals, cooling parts, and anything where early/late M119 confusion is a problem.
- **Autodoc.fi:** Good prices on common filters and fluids, but search is unreliable for early M119 parts (often returns W140/late M119 results).
- **eBay DE / specialist forums:** Only source for the aluminum oil bridge clip kit (aftermarket community part, not MB OEM).
- **Motonet / Biltema:** Fluids (ATF, coolant), generic consumables, and tools.

---

## ⚠️ URGENT — ADS Strut Dust Boots (ORDER IMMEDIATELY)

*Discovered 2026-04-02 during katsastus underbody inspection. Lower sections of the dust boots are missing on the ADS shock absorbers, leaving the chrome piston shafts exposed to road debris, grit, and moisture. Pitting on exposed shafts will destroy the internal seals and kill the ADS shocks — which are extremely expensive (~€500–800+ each) and increasingly unavailable. DO NOT drive significant distances until these are installed.*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ADS Shock Absorber Dust Boot (front) | A 129 323 01 92 | 2 | Fits R129/W124/W201. Also: VAICO V30-6033, MEYLE 0140320032, FEBI KIT 13034. ~€5–13 each. |
| ADS Shock Absorber Dust Boot (rear) | A 129 323 01 92 (verify) | 2 | May be same P/N as front — verify with MB-osat by VIN. Rear ADS shocks may use a different boot dimension. |

**Source:** MB-osat Oulu (email order with VIN), or Autodoc/Pelican Parts. These are cheap, common parts — the urgency is installation, not sourcing.

---

## PRIORITY 1 — Next Session (ADS + Cooling + Engine Bay)

### Air Intake Hoses (M119 KE-Jetronic)
*Passenger side is cracked/broken and taped. Driver side likely in similar condition. Both are a known M119 wear item — brittle plastic/rubber that cracks with age. Vacuum leaks here bypass the MAF and allow unfiltered air into the engine.*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Right Intake Hose (passenger side) | A 119 094 01 82 | 1 | **BROKEN — taped as temp fix.** Priority. |
| Left Intake Hose (driver side) | A 119 094 00 82 | 1 | Inspect — likely same age/condition. Order with the right side. |

**MB-osat result (2026-04-02):** NOT AVAILABLE — discontinued / no longer in stock. >100 € each when they were available. **Plan B:** DIY permanent repair — damage is highly localized (banding sections). Splice/replace the cracked banding sections and bond with appropriate adhesive. Research suitable method.

### Cooling System
*Thermostat and radiator cap are cheap insurance items with unknown service history.*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Thermostat (82°C) | A 119 200 04 15 (verify) | 1 | **ORDERED from MB-osat 2026-04-02. ARRIVED 2026-04-16.** |
| Radiator Cap (1.4 bar) | A 124 500 04 06 | 1 | **ORDERED from Autodoc 2026-04-04.** Febi 06568, €6.59. |

**MB-osat (2026-04-02):** Thermostat confirmed and ordered (82°C). Radiator cap ordered from Autodoc (Febi 06568).

### Transmission Fluid (722.3)
*No filter to change on the 722.3 — just fluid. Need enough for 2–3 drain-and-fill cycles (~5L per cycle).*

| Part | Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ATF (MB 236.1 spec) | e.g., Fuchs TITAN ATF 3353 or Febi 08971 | 10 L | 722.3 capacity ~7L total; 2–3 drain cycles needed for near-complete exchange. |

**Source:** Buy locally from Motonet or Biltema when ready — Dexron II / MB 236.1 is common shelf stock. No need to ship. Confirm MB 236.1 (NOT 236.10 or 236.14 — those are for later transmissions).

### ADS Hydraulic System

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ADS Suction Filter | A 129 327 00 91 | 1 | **ORDERED from MB-osat 2026-04-02. ARRIVED 2026-04-16.** Old one cleaned on 2026-03-29 as interim fix. |
| ZH-M Hydraulic Fluid (MB 343.0) | 000 989 91 03 (Febi 02615) | 1–2 L | Top-up for closed-loop bleed. 4L used in open-loop flush on 03-29. Check remaining level. |

### Engine Oil Service Consumables

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Oil Drain Plug Washer (copper, M14) | A 007 603 014 106 (Febi 07215) | 5 | **ORDERED from Autodoc 2026-04-04.** €0.59 each. Buy a pack — one used per oil change. |

### Crankshaft Position Sensor (EZL Code 17 — Active Fault)

*Diagnosed 2026-04-04 during full X11/4 sweep. Pin 8 code 17 = crankshaft position sensor (L5) defective. Code reappears after every drive. Sensor is marginal/intermittent — car starts and runs but EZL falls back to base timing map. A full failure will cause a no-start.*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Crankshaft Position Sensor | A 003 153 01 28 (Topran 408 205) | 1 | **ORDERED from Autodoc 2026-04-04.** €50.99. Located at back of engine near bellhousing (~11 o'clock). 6mm Allen bolt + Phillips screwdriver. 5 min job if sensor isn't seized. OEM Bosch 0261210055 was out of stock / €161 — Topran is a reputable German aftermarket, correct OE cross-reference confirmed. |

### Predictive Electronics Maintenance (Task #14)

| Part | Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Thermal Compound | Arctic MX-6 or Noctua NT-H1 | 1 tube (4g) | EZL ignition module thermal paste refresh — original has dried to chalk after 35 years. Non-conductive type required. Also useful for any heat-sinked power modules. |

---

## PRIORITY 2 — Upper Timing & Valve Cover Service (M119)

*Preventive inspection of timing chain guides and upgrade of oil bridge clips. The single most important M119 preventive maintenance task. All parts needed before the valve covers come off.*

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Valve Cover Gasket Set (Right bank) | 119 010 03 30 | 1 | **ORDERED from MB-osat 2026-04-02. ARRIVED 2026-04-16.** Incl. spark plug tube seals. **Confirmed needed 2026-04-05** — 6/8 plug wells have oil. |
| Valve Cover Gasket Set (Left bank) | 119 010 04 30 | 1 | **ORDERED from MB-osat 2026-04-02. ARRIVED 2026-04-16.** Incl. spark plug tube seals. **Confirmed needed 2026-04-05** — both banks affected. |
| Upper Timing Chain Guide (Slide rail) | 119 050 02 16 | 2 | **ORDERED from MB-osat 2026-04-02. ARRIVED 2026-04-16.** >100 € per side. |
| Upper Timing Chain Guide (U-shape) | 119 052 09 16 | 1–2 | Depending on M119 sub-version — confirm with MB-osat. |
| Camshaft Oiler Tubes | 119 187 00 87 (factory aluminum, early M119) | — | **INSPECT FIRST — likely already present.** Factory M119 oilers were aluminum through ~1992; the problematic plastic design (119 180 02 66) only appeared from ~1993. AOK912 engine 119960 12 024990 was built 1991-09, so the factory aluminum tubes are most likely still installed. **Pre-inspect via the oil filler hole with a flashlight** (work plan Phase 2.3) — if aluminum and intact, no order needed. If damaged, prefer used-OEM 119 187 00 87 from a German/NL R129 breaker. Superseded earlier URO aftermarket recommendation (2026-04-18 correction; European forum feedback negative on URO casting/O-ring quality). |
| Breather Hose (Crankcase vent) | 119 094 03 82 | 1 | **NOT ORDERED** — will inspect condition first. |

**MB-osat (2026-04-02):** Timing guides confirmed and ordered (arrived 2026-04-16). Breather hose deferred to inspect-first. Future orders to be sent by email.

**Oiler tube plan corrected (2026-04-18):** Earlier plan to order URO aftermarket aluminum tubes from RockAuto before opening valve covers has been **dropped.** AOK912's 1991-09 build is pre-plastic-transition, so factory aluminum tubes (P/N 119 187 00 87) are most likely already in place. New plan: oil-filler-hole visual inspection first (no tools, no ordering). The valve cover / gasket / timing guide job is therefore **not blocked** on the tube decision — it can proceed once the rest of the baseline is in shape, subject to what the inspection shows.

---

## PRIORITY 3 — Instrument Cluster & Diagnostics

*Cluster pull needed to investigate the missing ADS warning lamp (confirmed non-ADS cluster swap) and address the stuck clock + delaminated temperature LCD.*

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Cluster Removal Hooks | 140 589 02 33 00 (MB special tool) | 1 pair | Or fabricate from a 90° pick with ~3mm toe. Ask MB-osat if they have this tool or can lend it. |
| Instrument Cluster Bulbs (W1.2W wedge) | — | 10+ | Spares for all 34-year-old indicator lamps. Replace the entire bottom row while the cluster is out. |
| Instrument Cluster Bulbs (W2W wedge) | — | 4–6 | For brighter indicator positions if applicable. |

---

## PRIORITY 4 — Baseline Service (Inspect First, Then Order)

*These parts should be inspected before ordering. Do NOT blind-order — check condition during the baseline service.*

| Part | OEM Number / Ref | Qty | Condition | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Distributor Caps | A 119 158 01 02 | 2 | **Inspect first** | Replace only if carbon tracking, deep pitting, or cracking. Bosch or Bremi. |
| Distributor Rotors | (verify w/ MB-osat) | 2 | **Inspect first** | Replace only if pitted or burned contact. |
| Spark Plug Wires (full set) | (verify w/ MB-osat) | 1 set (8) | **Inspect first** | Measure resistance: <10 kΩ per wire. Replace if out of spec or brittle. |
| V-Belt Set (M119) | (verify w/ MB-osat) | 1 set | **Inspect first** | M119 uses multiple V-belts, not single serpentine. Replace if cracked/glazed or age unknown. |
| Belt Tensioners / Idler Pulleys | (verify w/ MB-osat) | as needed | **Inspect first** | Check for bearing play/noise. |
| Brake Flex Hoses (all 4 corners) | (verify w/ MB-osat) | 4 | **Inspect first** | 35-year-old rubber. Replace if any doubt. |
| Flare Nut Wrench Set (7–19mm) | **Bahco** | 1 set | **Needed** | 6-point chrome-vanadium. For brake bleed nipples (7/8mm) and ADS hydraulic fittings. Frequent use expected. Check Kärkkäinen stock. |
| ~~One-Person Pressure Bleeder~~ | ~~Gunson Eezibleed or similar~~ | ~~1~~ | **REPLACED** | ~~Connects to brake reservoir cap, pressurizes to ~1 bar.~~ **Replaced by MTX pneumatic vacuum bleeder (see below).** |
| MTX Automotive pneumatic brake bleeder 1L | Motonet 75-1000 | 1 | **Ordering from Motonet 2026-04-03** | Pneumatic vacuum bleeder, 6-12 bar, 1L tank, connects to compressor. One-person brake flush tool. Also usable for ADS bleed points (with separate clean hose — never cross-contaminate DOT4/ZH-M). **Buy 1/4" air pistoke fitting separately.** 29.90€. |
| Brake Fluid (extra) | ATE TYP200 DOT4 | 1 L | **Ordering from Motonet 2026-04-03** | Second bottle for a full 4-corner flush (1L already on hand, need 2L total). |
| PTFE / Teflon Tape | — | 1 roll | **Needed** | Wrap around brake bleed nipple threads to prevent false air ingestion during vacuum bleeding. Also useful for general hydraulic thread sealing. |

---

## PRIORITY 5 — Suspension (Post-OVP Fix + Closed-Loop Bleed)

*Order AFTER OVP re-solder → N51 online → closed-loop bleed confirms rear height behavior. Pump is confirmed working (2026-03-26).*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ~~Front Accumulator Spheres~~ | ~~A 129 320 01 15~~ | ~~2~~ | **CANCELLED (2026-04-02).** All four spheres confirmed healthy — exceptional ride quality on first drive, inspector commented. Earlier FR stiffness was air-lock from depleted system. |
| Rear Level Control Linkage | (inspect under car first) | 1 | Known ADS I failure: plastic link shears at lower mount. Inspect BEFORE ordering. |
| ADS Tandem Pump (CONDITIONAL) | A 129 460 07 80 | 1 | ~€850 rebuilt from ABCspecialist NL + core deposit. **Pump confirmed ALIVE (2026-03-26) — DO NOT ORDER.** Only if future testing reveals internal failure. |

---

## PRIORITY 6 — Telematics / RPi5 Display System

| Part | Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| CarPlay USB Dongle | Carlinkit CPC200-CCPA | 1 | **ORDERED from MyTrendyPhone.fi 2026-04-03. ARRIVED 2026-04-16.** ~€48. Connected, enumerated, and integrated into the PyQt5 UI same day (see `RPi5_Bring-up_Plan.md` Step 7). USB dongle with MFi authentication for wireless Apple CarPlay. Dongle connects to Pi via USB (hidden behind dash), iPhone connects to dongle via WiFi Direct (automatic, no cable). Outputs H.264 video + PCM audio over USB, accepts touch input back. No user-facing USB port needed in the cabin. Used with [LIVI](https://github.com/f-io/LIVI) open-source CarPlay host on the Pi (explicitly supports CPC200-CCPA on RPi5). |
| Flat FPC HDMI Cable | Micro-HDMI (Type D) → HDMI (Type A) | 1 | Thin flexible ribbon cable for flush panel mounting. Replaces the round HDMI cable. ~10–20cm length depending on mounting. AliExpress/Amazon. |
| Flat Micro-USB Cable | Micro-USB → USB-A | 1 | Thin flexible cable for touch/power connection. For flush panel mounting alongside the FPC HDMI cable. |

**Note:** Waveshare 5.5" AMOLED display, 180° adapter connectors, and standard cables already on hand (2026-04-03).

### Battery Voltage & Temperature Monitor (Trunk Module)

*Non-invasive battery monitor mounted in the trunk next to the battery. INA226 measures voltage directly at the terminals (0–36V, 1.25 mV resolution) via a fused sense wire. DS18B20 measures battery case temperature for SoC compensation. No series connection in battery cable — zero added failure points. Parasitic draw estimated from voltage decay over time. See `work/battery_monitor/README.md` for full design. Current shunt can be added later as a bolt-on upgrade if needed.*

| Part | Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| INA226 Breakout Board (×5) | CJMCU-226 (Fyndiq, €15.39/5-pack) | 5 | **ORDERED from Fyndiq 2026-04-05. ARRIVED 2026-04-16** (on the early end of the ETA window). €3.08/ea. Generic INA226 breakout. Shunt inputs unused (IN+/IN− shorted) — bus voltage measurement only. |
| DS18B20 Temperature Sensor | Waterproof probe (AliExpress/Motonet) | 1 | ~€2–3. One-wire digital, ±0.5°C. Strap to battery case for electrolyte temperature tracking. |
| 4.7 kΩ Resistor | 1/4W through-hole | 1 | ~€0.10. Pull-up for DS18B20 one-wire data line. |
| Inline Fuse + Holder (1A) | Glass fuse, fast-blow | 1 | ~€1. Protects VBUS sense wire from battery positive terminal. |
| 5-Wire Shielded Cable (~80 cm) | I2C + one-wire: SDA, SCL, 3.3V, GND, DATA | 1 | ~€2. Short run from INA226 + DS18B20 to RPi5 GPIO header. |

**Source:** INA226 breakout from Fyndiq (€15.39 for 5-pack). DS18B20 from AliExpress or Motonet. Fuse holder from Motonet/Biltema. Estimated total: ~€21 (includes 4 spare INA226 boards).

---

## PRIORITY 6B — Audio System (Fully Active 2.1)

*Complete audio upgrade: fully active 2-way front + 10" DVC2 subwoofer, driven by 6-channel DSP amplifier. RPi5 feeds digital audio via USB. Factory door wiring reused for woofers — no new wires through door boots, no professional labor needed. See `work/audio_upgrade_blueprint.md` for full architecture and installation plan.*

| Part | Ref / Model | Qty | Notes |
| :--- | :--- | :--- | :--- |
| DSP Amplifier | **Match UP 6DSP** | 1 | 6-ch DSP amp (4×65W + 2×160W). **€649 from Kärkkäinen. ORDERED 2026-04-04. ARRIVED 2026-04-16.** Mounts in rear cubby. Chosen over UP 8DSP (€749) — 2-way setup needs exactly 6 channels. |
| USB Audio Module | **MEC HD-USB (M142045)** | 1 | USB Audio Class input for UP 6DSP. Driverless on Linux. **€149 from Kärkkäinen. ORDERED 2026-04-04. ARRIVED 2026-04-16.** Compatible with UP 6DSP / UP 8DSP / UP 8BMW. |
| Front 2-Way Speakers | **Hertz MPK 1650.3** (Mille Pro) | 1 set | MP 165P.3 woofer (63mm depth, 3Ω) + **MP 28.3 tweeter (Tetolon, 900 Hz Fs)**. Passive crossovers included but unused (fully active). **€331.26 from masori.de. ORDERED 2026-04-04.** Free shipping to FI, 3-yr warranty. 93 dB sensitivity. Chosen for premium tweeter enabling low 2.5 kHz crossover in 2-way active setup. |
| Subwoofer | **Helix IK S10-DVC2** | 1 | 10" sub, DVC 2×2Ω, 300W RMS, 84.5mm depth. **€199 from Kärkkäinen. ORDERED 2026-04-04. ARRIVED 2026-04-16.** Each coil → separate DSP channel (Ch 5 + Ch 6). Same manufacturer (Audiotec Fischer) as Match DSP. |
| Door Speaker Brackets | **MR129.com Bracket Kit** (STL) | 1 set | 3D adapter brackets (4 pieces, 2/door — woofer only). ~$39 for STL download. Self-printed: PLA test-fit → PETG/ABS final. Verify Hertz MP 165P.3 141mm mounting hole + 63mm depth against STL dimensions before final print. |
| Speaker Wire | OFC 2×1.5mm² + 2×2.5mm² | ~15m total | Tweeter runs in cabin (1.5mm²) + sub run (2.5mm²). Partially in inventory. |
| Sub Enclosure Materials | 16mm MDF + polyfill | — | Sealed 14L box for rear cubby. ~€30. |

**All major components ordered 2026-04-04. Audio system total: ~€1,434.**
Savings vs. original 3-way plan (UP 8DSP + MPK 163.3 + professional door wiring): ~€336.

---

## PRIORITY 7 — Electrical Consumables & Small Items

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Torpedo Fuses (8A white) | — | 5+ | For trunk F20 fuse box. Need enough to replace all positions + spares. Check current ratings: 16A, 16A, 25A, 8A, 16A, 8A. |
| Torpedo Fuses (16A red) | — | 5+ | Most common in F20 box (3 positions). Copper/ceramic preferred over aluminum. |
| Torpedo Fuses (25A blue) | — | 2+ | One position in F20 box. |
| Headlight Switch Knob | (verify P/N w/ MB-osat by VIN) | 1 | Current knob is worn/soft. Check if the knob is replaceable separately or if the entire switch assembly is needed. |

---

## PRIORITY 8 — Body & Trim (Whenever Convenient)

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Antenna Grommet (Upper) | A 129 827 02 98 | 1 | Cracked seal leaks water onto the PSE pump in the trunk. |
| Antenna Grommet (Lower) | A 129 827 03 98 | 1 | Order with upper. |
| Silicone Spray (aerosol) | Biltema / Würth / CRC | 1 can | For antenna mast tube long-term lubrication (WD-40 freed segments 2026-04-03, not a lasting lubricant). Also useful for rubber seals. Motonet/Biltema/Kärkkäinen. |
| Scotch Fix Extreme Exterior 19mm × 5m | 3M (double-sided, 13kg max) | 1 roll | For re-securing door seat control panels (P/N 129 820 71 10) where front lower plastic clip broke. Biltema basic tape failed. 3M acrylic foam (VHB-class). -40°C to +90°C. Clean surfaces with brake cleaner before applying. **Ordered from Motonet 2026-04-03.** |
| Touch-up Paint Pen | Color code **744 Brilliant Silver Metallic** | 1 | Base coat + clear coat. For the hood scratch and behind-wheel bare steel. |
| Plastic Scrapers | — | 1 set | For the hood pad adhesive removal. No metal on aluminum. |
| Seat Adjustment Panel Clips (door) | (verify P/N — inspect mounting first) | as needed | Both door panels loose at bottom. Likely broken/missing clips. |

---

## MB-osat Visit Checklist

**Bring:**
- This printed list
- VIN: **WDB 129066 1F 044414**
- Phone with photos of the broken passenger intake hose (taped section)

**Key questions for MB-osat:**
1. **Intake hoses:** Confirm A 119 094 01 82 / 00 82 fitment for the early M119.960 (KE-Jetronic).
2. **Timing guides:** Pull the EPC for M119.960 (VIN ...044414) — confirm upper guide part numbers (119 050 02 16 / 119 052 09 16) and quantities.
3. **Thermostat:** Confirm correct part number and 80°C spec for M119.960.
4. **722.3 ATF:** Confirm MB 236.1 is the right spec (not 236.10/236.14).
5. **Cluster removal hooks:** Do they stock tool 140 589 02 33 00, or can they suggest a substitute?
6. ~~**Aluminum oil bridge clips:**~~ Resolved — MB-osat OEM plastic tubes priced similarly to URO aluminum. Ordering aluminum from RockAuto.
7. **Paint code confirmed:** 744 Brilliant Silver Metallic (from mbdecoder.com VIN decode, 2026-04-01). Ask MB-osat to confirm and source correct touch-up pen.
8. **ADS confirmed factory (option 216):** Lastvin.com shows option 216 (self-leveling + ADS). All ADS hardware is original. The mbdecoder.com decode was incomplete.
9. **Availability & lead times:** Which parts are in stock vs. special order from MB Germany?

---

---

## ACQUIRED — Tools, Consumables & Fluids (Reference)

*Items already purchased and on hand. Formerly tracked in `Karkkainen_Shopping_List.md` (now retired).*

<details>
<summary><b>Tools (all acquired)</b></summary>

- Socket/Wrench: Bahco S910, SBSL25, combination wrenches
- Torx: Bondhus set
- Pliers: 3× Knipex (87, 70, 26)
- Floor Jack: >2.5t low-profile
- Jack Stands: Bahco BH33000 3T ×4 + 100mm rubber pads ×4
- Breaker Bar: MTX 1/2" 600mm
- Wheel Chocks: 2× plastic 155mm
- Torque Wrench: 20–110Nm + 40–210Nm
- Oil Filter Wrench: Bahco BE6307614F 74mm/14-flute
- Fluid Syringe: MTX 500ml
- Pry Bar Set: Bahco 2484T/S4
- Transmission Funnel: KABI set
- Magnetic Pick-up Tool, Magnetic Parts Tray
- Oil Drain Pan
- Multimeter: MS8233B (car kit) + Owon HDS242 (scope/DMM combo)
- Soldering Iron & Solder
- Wire Strippers, Crimping Tool, Automotive Test Light
- Trim Removal Tools: MTX Automotive set
- Work Light: Berg COB+XPE LED
- Heat Shrink Tubing assortment
- Wet/Dry Shop Vacuum: Kärcher WD3

</details>

<details>
<summary><b>Consumables (all acquired)</b></summary>

- Brake Cleaner (6× cans)
- Penetrating Oil (WD-40)
- Dielectric Grease, Lithium Grease (CRC), Silicone Grease (CRC)
- Threadlocker (Loctite 243 Blue)
- Microfiber Cloths (8 pcs), Shop Towels
- Nitrile Gloves (NEO TOOLS Orange Diamond 50pcs)
- APC / Plastic Cleaner / Engine Bay Cleaner
- Plastic Dressing: Chemical Guys VRP 473ml
- Iron Remover: Korrek Pro Irox 700ml
- Adhesive Remover: AT Stripper 400ml
- Leather Conditioner: Leather Master Leather Vital 250ml
- Polishing Compound: King Carthur Reshine Finish 3/3
- Car Wax: Soft99 FUSSO Coat White 200g
- Detailing Brushes: Soft99 exterior/interior
- Drop cloths (old linen/blankets)

</details>

<details>
<summary><b>Fluids & Filters (all acquired)</b></summary>

- Engine Oil: 8L Mobil 1 FS 0W-40 (MB 229.5)
- Oil Filter: MANN H 829/1 x
- Engine Air Filters: MANN C 3388 ×2 (installed 03-30)
- Cabin Air Filter: MANN CU 5041 (installed 03-30)
- Fuel Filter: MANN WK 830/3
- Power Steering Filter: MANN H 85
- ~~Spark Plugs: NGK BP5ES ×8~~ **WRONG HEX (20.8mm).** Replaced with NGK BCP5ES 7496 ×8 (16mm hex, Puuilo €4.49/ea). **INSTALLED 2026-04-05.**
- Brake Fluid: ATE TYP200 DOT4 1L
- Power Steering Fluid: 2L Febi 08972 MB 236.3
- ADS Hydraulic Fluid: 4L Febi 02615 MB 343.0/ZH-M (used in flush 03-29)
- Coolant: Motox Classic G11 Blue 10L + 10L distilled water
- Windshield Washer Fluid
- Fuses: Ceramic/Copper torpedo set (installed 03-30) + Dunlop blade assortment
- PVC Hose: ToppBright 6mm + 8mm clear, 2m each

</details>

<details>
<summary><b>Engine & Drivetrain Mounts (acquired, awaiting install)</b></summary>

- Engine Mounts ×2: Corteco 80001913
- Transmission Mount: Corteco 21652116

</details>

<details>
<summary><b>Body Parts (acquired, awaiting install)</b></summary>

- Hood Insulation Pad + Clips: IPG-87742-Set (AMS Auto)

</details>

---

*Last updated: 2026-04-16 (delivery day — Kärkkäinen audio order, MB-osat MB parts order, Carlinkit dongle, Fyndiq INA226 boards all arrived).*
