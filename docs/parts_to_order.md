# Parts to Order — AOK912 (1991 R129 500 SL)

**Vehicle:** WDB 129066 1F 044414 | **Engine:** M119.960 (KE-Jetronic) | **Trans:** 722.3

*Single source of truth for all parts, consumables, and tools. Replaces the former `Karkkainen_Shopping_List.md`. Organized by priority/project. Print this and walk into MB-osat Oulu — they can cross-reference by VIN and confirm fitment for the tricky M119.960 early-model parts that Autodoc gets wrong.*

**Recommended sourcing strategy:**
- **MB-osat (Oulu):** First stop for anything with an "A 1xx..." OEM number. They have the MB parts catalog and can verify fitment by VIN. Best for gaskets, seals, cooling parts, and anything where early/late M119 confusion is a problem.
- **Autodoc.fi:** Good prices on common filters and fluids, but search is unreliable for early M119 parts (often returns W140/late M119 results).
- **eBay DE / specialist forums:** Only source for the aluminum oil bridge clip kit (aftermarket community part, not MB OEM).
- **Motonet / Biltema:** Fluids (ATF, coolant), generic consumables, and tools.

---

## ⚠️ URGENT — ADS Strut Dust Boots (FRONT-ONLY, PENDING PHOTO CONFIRMATION)

*Discovered 2026-04-02 during katsastus underbody inspection ("lower sections missing"). Initial assumption was ×4 all corners. **Rear strut photograph 2026-04-18** shows rear boots present, seated, no exposed chrome — Apr 2 note was front-biased. Quantity reduced to ×2 pending tomorrow's front-strut photo confirmation (Apr 19 on jack stands). Pitting on exposed front shafts will still destroy internal seals on the irreplaceable front ADS shocks — do the front install promptly once parts arrive.*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ADS Shock Absorber Dust Boot (front) | A 129 323 01 92 (≡ `1293230192`) | 2 | **ORDERED from Autodoc 2026-04-20** — MEYLE 014 032 0032 (ORIGINAL Quality, "Etuakseli"), €8.29 each = €16.58 total. Front-axle separation at lower compression seal confirmed via photograph 2026-04-20 (see diary) — matches Apr 2 katsastus "lower sections missing" observation. Passenger-side front not yet photographed but ordering 2× on the assumption of symmetric degradation (matched ADS corners typically age together). |
| ~~ADS Shock Absorber Dust Boot (rear)~~ | ~~A 129 323 01 92 (verify)~~ | ~~2~~ | **DROPPED 2026-04-18.** Rear struts photographed, bellows intact. No part needed. |

**Source preference:**
1. **MB-osat Oulu** — genuine MB, MB klubi −15 %, no shipping. Send email with VIN `WDB 129066 1F 044414` and part number, ask them to confirm no separate rear-specific PN exists (defensive — we don't think there is one, but we only have three corners worth of data and MB-osat has the EPC).
2. **Fallback: ClassicFactoryShop (PL)** at €12.80/ea, 3–5 d to FI.
3. **Last resort: Autodoc.fi** aftermarket (MEYLE) at ~€5–10/ea, Stettin dispatch 3–5 d.

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

*Timing is relaxed after 2026-04-18 dipstick finding (light honey amber at 1800 km on owner-driven oil). Next change paired with UOA + filter element inspection + magnetic sump plug install — see `docs/engine_condition_baseline.md`.*

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Oil Drain Plug Washer (copper, M14) | A 007 603 014 106 (Febi 07215) | 5 | **ORDERED from Autodoc 2026-04-04.** €0.59 each. Buy a pack — one used per oil change. |
| Magnetic Sump Plug (M14×1.5) | Dimple Magnetic or equivalent rare-earth | 1 | **New for the next change.** Replaces the factory non-magnetic plug. Passive early-warning for ferrous wear particles. ~€15 on Amazon.de / eBay. Inspect captured material at each subsequent change. |
| Oil Filter Housing O-Ring Kit | (varies by mfr — Mann or Mahle usually bundle with the element) | 1 set | 3 rings: large lid, center stud, small sealing. One-shot — replace every time the housing is opened. Bundled with most OEM filter kits. |
| Used-Oil Analysis (UOA) — service not part | Oelcheck Trucker/Car kit, DE | 1 | ~€30–40, mail-in postal kit. Sample drawn from the drain stream at the next change. Returns Fe/Al/Cu/Pb/Si wear metals, fuel %, coolant %, viscosity, TBN. One UOA on a 34-year-old engine of unknown history is worth more than a year of guessing. |

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

## PRIORITY 1B — Belt Set (Glazed, Slipping, Spray-Exhausted)

*Promoted from Priority 4 "inspect first" on 2026-04-19. Glazed-belt hypothesis (Apr 3 friction-spray test) confirmed when squeal re-emerged during Apr 19 test drive — spray treatment exhausted. Order the two belts now from MB-osat; inspect the tensioner + pulleys at the same bench session when the belts arrive so we don't risk a repeat glaze from weak preload or a failed bearing.*

*Part numbers verified 2026-04-20 for M119.960 serial 024990 (1991-09 build) with catalytic converter + air conditioning. Cross-referenced against SL Shop, Pelican, mbpartsgiant, and benzworld / 500Eboard technical archives. **Terminology correction:** the 1990–92 M119.960 tensioner is a **rubber-bushed** design, not hydraulic — the hydraulic/spring-loaded redesign came in ~1993 on later M119 variants. The "shock" you see in some diagrams is actually a threaded adjustment rod (A 119 200 00 36), not a hydraulic damper.*

| Part | OEM Number | Qty | Posture | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Main Poly-V Serpentine Belt** (alternator / PS / water pump) | **A 010 997 99 92** | 1 | **ORDERED Autodoc 2026-04-20** | **ContiTech 6PK2523** (51% off RRP, €32.49). Spec 6PK2523 (6 ribs × 2523 mm). Cross-listed as A 011 997 68 92 / A 119 997 01 92. Correct specifically for M119.960 *with catalytic converter* (AOK912 match). Do NOT substitute the 6PK2510 (late M119.982 w/ A/C), 6PK2425 (M119.982 w/o A/C), 6PK2535 / 6PK2540 (M119.972) — all are different M119 variants with different accessory drive layouts. |
| **A/C Compressor V-Belt** (separate classic V-belt) | **A 004 997 05 92** | 1 | **ORDERED Autodoc 2026-04-20** | **ContiTech AVX13X950** (43% off RRP, €10.49). Modern raw-edge cogged replacement for the factory 12 × 960 wrapped V-belt — same application, same OEM cross-reference, functional upgrade. Early M119.960 uses a dedicated V-belt for the A/C compressor in addition to the main poly-V. |
| **Belt Tensioner Rod / Adjustment Bar** | **A 119 200 00 36** | 1 | **CHECK STOCK** | The threaded adjusting rod that sets belt preload (#12 in WIS diagram, pivots the tensioner arm). Often listed discontinued at US dealers — **this is the hardest-to-find item of the set**; ask MB-osat to check stock when placing the belt order. ~€25–35 when available. Aftermarket Febi/Meyle is an acceptable fallback if MB is out. |
| **Belt Tensioner Assembly** (rubber-bushed, 1990–92 early design) | A 119 200 02 70 | 1 | **INSPECT FIRST** | Criteria for replacement: any visible cracking in the rubber bushing, pivot free play, or audible slop when belt removed. Rubber bushings are a documented M119 wear point (benzworld reports 2–3 year failures in hot climates); at 35 years this is absolutely past design life, but Finnish climate is much kinder to it than Texas. Febi 1192000270 ~€100, genuine ~€200+. |
| **Tensioner Pulley** (bearing on the tensioner arm) | A 119 200 14 70 | 1 | **INSPECT FIRST** | Spin by hand with belt off — should turn silky smooth, no grit, no lateral play. Replace if in doubt. |
| **Deflection / Guide Pulley** | A 119 200 04 70 | 1 | **INSPECT FIRST** | Same hand-spin check. |
| **Auxiliary / Idler Pulley** (M119.960-specific) | A 601 200 09 70 | 1 | **INSPECT FIRST** | The M119.960 uses the 601-prefix aux pulley, NOT the later A 601 200 10 70 used on other R129 variants — confirm by VIN at the parts counter. Same hand-spin check. |
| V-Belt Friction Spray (interim) | any auto-parts brand | 1 can | On hand | Acceptable to nurse the belt with occasional re-application until the new set is installed. Do NOT rely on spray long-term — slipping belts overheat, crack, and eventually snap. |

**MB-osat email / counter talking points** (VIN `WDB 129066 1F 044414`):
1. Confirm A 010 997 99 92 and A 004 997 05 92 by VIN → order both.
2. Check stock on A 119 200 00 36 (tensioner rod) → order now if available, fallback to aftermarket if not.
3. Price-check but do NOT order the tensioner assembly (A 119 200 02 70), the two pulleys (A 119 200 14 70, A 119 200 04 70), and the aux pulley (A 601 200 09 70). Decide at the bench session after hand-spin inspection.

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
| ~~V-Belt Set (M119) — moved to Priority 1B, glazed and slipping confirmed 2026-04-19~~ | — | — | **PROMOTED** | See new Priority 1B entry below. No longer "inspect first". |
| ~~Belt Tensioners / Idler Pulleys — moved to Priority 1B, inspect during belt swap~~ | — | — | **PROMOTED** | See new Priority 1B entry below. |
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
| Speaker Wire | OFC 2×1.5mm² + 2×2.5mm² | ~15m total | Tweeter runs in cabin (1.5mm²) + sub run (2.5mm²). Partially in inventory; the CCA 2×2.5 mm² speaker cable from the retained Biltema 84-574 kit (below) also covers rear-cubby short runs. |
| Sub Enclosure Materials | 16 mm MDF (40 × 120 cm) + polyfill (~135 g) + neutral-cure silicone + **Casco SuperFix+ (SMP)** + 4×40 mm wood screws + **terminal cup (included with Helix shipment)** | — | Sealed ~16.9 L external / ~12.5 L effective box for the driver-side rear cubby (geometry locked 2026-04-25 evening; **Strategy C silicone-fillet joinery, no cleats** — adopted 2026-04-25 after MDF panel size constrained the cleat-stock margin). **Acquired Saturday 2026-04-25:** ✅ MDF panel (40 × 120 cm — tight but feasible without cleats; nesting layout required at the panel saw), ✅ Casco SuperFix+ (SMP construction adhesive, **substituted for PVA D3** — better gap-fill, 20 min open time, elastic cure resists hairline cracks; bead-applied, 1–3 mm bond line, white-spirit cleanup), ✅ 4×40 mm wood screws, ✅ terminal cup (included with Helix IK S10-DVC2 shipment, **saves the Autoviihde trip** — verify 4-post DVC2 isolation + gasket before install). **Still to acquire Sunday 2026-04-26 AM:** caulking gun for SF+ cartridge, white spirit (mineraalitärpätti), neutral-cure silicone (verify inventory), polyfill ~135 g (pillow-stuffing from Sinelli/Tokmanni/Biltema — Autoviihde no longer on the critical path). Build spec: `work/subwoofer_enclosure/README.md` (§3.6 panel-size analysis, §5 SF+ application, §5.4 Strategy C joinery, §11 decisions log). |
| DSP Power & Ground Kit | **Biltema 84-574** Car stereo install kit (CCA 8 mm²) | 1 | **RETAINED 2026-04-24** (reversed the 2026-04-19 "return to Biltema" decision — see diary). Kit contents: 6 m × 8 mm² CCA power (red) + 1 m × 8 mm² CCA ground (black) + 2 × 2.5 mm² speaker cable 5 m + 5 m RCA (unused) + 5 m remote wire (optional with UP 6DSP auto-sense) + AGU fuse holder + 40 A fuse + lugs + cable ties. **CCA is acceptable for this application** because: (a) actual run length is shorter than the worst case assumed in the Apr 19 analysis (~4 m battery → rear cubby), (b) UP 6DSP steady current draw is ~25 A at full output with ~30 A bass-transient peaks — well within 8 mm² CCA's ≥40 A SAE ampacity, so the 40 A AGU is correctly sized, (c) weight savings welcome on a shared-loom run. **Mitigation — crimp-creep is the real risk, independent of current:** (1) hex-crimp all lugs with a ratcheting tool, not pliers; (2) dielectric grease in every crimp cup + ring-terminal mating face; (3) tinned-copper lugs on the CCA conductor (standard automotive harness pairing); (4) **re-torque check at 3 months (≈2026-07-26) and 12 months (≈2027-04-26)** logged in diary; any wire movement or lug discoloration at the 3-month check → rebuild with OFC. |
| DSP Mount & Ground Hardware | M6 ring terminal (8 mm² conductor, tinned copper) + M6 external-tooth star washer + M6 flat washer + M6 nyloc / stop nut + M5 × 16 mm self-tappers ×2 + cup washers ×2 (trim panel positive retention, optional) + M4 × 16 mm wood screws ×4 (amp → base plate) + 12 mm plywood/MDF base plate offcut (~250 × 140 mm) | 1 set | **Acquire Motonet/Biltema/Puuilo on next trip.** Confirmed by passenger-cubby recon 2026-04-26: factory M6 welded stud on cubby floor will serve as the dedicated DSP audio ground (paint-scraped to bare metal under the ring terminal, star washer essential for breaking through paint/oxide, dielectric grease already in inventory for corrosion protection). Becker module bolts rejected for grounding — 129 820 00 97 confirmed as Verdeck (soft-top) control unit, motor return current pulses unsuitable for audio reference. Factory plastic trim panel sits friction-fit on cubby floor; M5 self-tappers + cup washers are optional positive retention if friction proves inadequate. Base plate cut from sub-box MDF offcut (40 × 120 cm panel had ~22% slack with corrected wall heights — should yield a usable rectangle). Re-torque ground stud at 3-month / 12-month checkpoints alongside the power-side crimps. **Estimate: ~€5–8 for the small fastener bag, base plate is offcut.** |

**All major components ordered 2026-04-04. Audio system total: ~€1,434.**
Savings vs. original 3-way plan (UP 8DSP + MPK 163.3 + professional door wiring): ~€336.

---

## PRIORITY 6C — Center Console-Out (Cable Harness & Refresh Consumables)

*Single shopping list to finish the combined console-out task: BE2210 → UP 6DSP high-level tap, DSP-direction cable pull (USB + tweeters), Pi-direction cable pull (CAT6 + AUX + 5 V), and the wood/switch refresh. See `work/center_console_refresh/README.md` for the full plan. This is the enabling task for PRIORITY 6 (Pi infotainment) and PRIORITY 6B (Audio) — everything downstream needs these cables in place first.*

### 6C.1 — BE2210 → UP 6DSP High-Level Tap

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Shielded CAT6 cable (F/UTP or S/FTP) | 4 twisted pairs, 23 AWG solid-core preferred, overall foil shield + drain wire | ~3.5 m | **ORDER NEXT** — any reputable brand. Verkkokauppa.com (Deltaco / LogiLink / Digitus shielded patch cable, ~€8–15 for 5 m) or Biltema bulk solid-core install cable (~€1.50/m). Pair assignment: Blue = LF+/LF−, Orange = RF+/RF−, Green + Brown = future spares (line-level input + DC control). Keep pair twist intact within ≤13 mm of termination. Overall shield grounded at DSP end only. **Decision rationale (2026-04-20):** substituted for originally-planned Sommer/Cordial audio multi-core because (a) CAT6 is the right technical fit — twisted pairs + overall shield; 100 Ω impedance is irrelevant at audio frequencies; 23 AWG gauge is fine for high-Z DSP input (≥10 kΩ, μA-level signal current, not a speaker-drive application); (b) pro-audio precedent (Rane, Radial, Whirlwind, BSS Soundweb all use CAT5/6 for balanced analog runs); (c) trivially sourceable in Finland vs. multi-week EU order for Sommer / Cordial. **Buy one bulk spool and share with §6C.3 Alps CAT6 run.** |
| ~~Motonet 7 × 1.5 mm² unshielded cable (art. 0000606156)~~ | ~~7-conductor automotive cable, 7 m~~ | — | **RE-PARKED to inventory 2026-04-20.** Initially purchased 2026-04-20 to substitute for a proper shielded cable, with a manual twist-pairs + pseudo-shield install plan. Superseded same day by the shielded-CAT6 decision above (cleaner, no jacket-strip-and-retwist labour, no long-term Tesa-glue dependency for re-sheathing). **Probable future use:** Hertz door-woofer multi-conductor harness during the Priority 6B speaker upgrade — 2× woofer pairs + tweeter pair + spare = 7 conductors, speaker-level signals so unshielded is fine. Parked in electrical stock until that task opens. |
| Wago 221-413 (3-way lever nut) | 0.2–4 mm² clamp range | 4 pcs | **ACQUIRED from Motonet 2026-04-20** (art. 0000728703, "Wago 3-napainen vipuliitin 0,2[–4 mm²]", €9.99/pack). Parallel tap at the BE2210 ISO speaker pigtail — one per signal (LF+, LF−, RF+, RF−). Spares retained. |
| Bootlace ferrules | 0.75 mm², insulated, red | ~10 pcs | DSP-end terminal entry (4 signals) + spares. Assortment kit from Motonet/SP Elektroniikka is fine. ~€5 for the kit. |
| Ring terminal | M6, insulated, 0.5–1.5 mm² | 1 pc | Shield drain → DSP chassis ground bolt. **Motonet assortment.** |
| Heat-shrink labels | 6 mm black + 3 mm black | — | Already in inventory (Stage 1 heat-shrink kit). Use a fine-tip marker + clear shrink-over for durable labels. |

### 6C.2 — DSP-Direction Cable Pull (front cubby → rear cubby)

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| USB 2.0 cable, shielded | Type-A → Type-B (**verify MEC HD-USB connector before buying** — some revisions are Type-A) | 3 m | RPi5 → MEC HD-USB (inside UP 6DSP). Shielded, ferrite chokes a plus. **Verkkokauppa, Clas Ohlson, Puuilo.** ~€8–12. |
| Tweeter / speaker wire | OFC 2 × 1.5 mm² | +5 m | **10 m already in inventory** (Components inventory, SP Elektroniikka #15096). Need ~6 m total (two pairs, rear cubby → dash via A-pillar). The 10 m roll covers it — **no new purchase required** unless extra slack wanted for future changes. |

### 6C.3 — Pi-Direction Cable Pull (ashtray / BE2210 → front cubby)

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| CAT6 Ethernet cable | Shielded (F/UTP or S/FTP) | 1.5 m | Alps RKJXT1F42001 (ashtray) → front cubby. 8 conductors = 7 GPIO + 1 GND. **Shared purchase with §6C.1 BE2210 tap (2026-04-20 decision):** buy one 5 m spool of shielded CAT6 and cut two lengths — 3.5 m for §6C.1, 1.5 m for §6C.3. **Verkkokauppa, Clas Ohlson, Puuilo, or Biltema bulk solid-core.** ~€8–15 for the shared 5 m. |
| Stereo AUX cable, shielded | 3.5 mm TRS male ↔ 3.5 mm TRS male | 0.5–1 m | BE2210 rear AUX jack → front cubby (RPi5 Waveshare / USB DAC output). Short, shielded, slim (not the chunky speaker-use kind). **Clas Ohlson, Verkkokauppa.** ~€5–8. |
| Hook-up wire | 2 × 1.5 mm² red/black automotive | 2 m | 5 V feed into the cubby from the nRF5430 wake-switch output. Can also be made from existing 1.5 mm² speaker cable in inventory — no new purchase strictly required if slack remains after 6C.2. |
| Fuse holder + 3 A blade fuse | ATO blade, inline | 1 | On the 5 V-bound 12 V feed before it enters the cubby DC-DC buck. **Motonet/Biltema assortment** — already likely in inventory (check Priority 7 torpedo box — but 3 A ATO is different from torpedo). ~€2. |

### 6C.4 — Loom Finishing & Pass-Through

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Tesa cloth tape | 51608 (or 51026), 19 mm × 25 m, black | 1 roll | Period-correct loom wrap. Automotive-grade cloth PET, heat-resistant, non-sticky residue. **Motonet, Biltema, Puuilo, or any auto-parts shop.** €8–12. |
| Split loom / convoluted tubing | 6 mm ID, black polypropylene | 2 m | Protection where cables cross sharp metal edges (sill plate region, tweeter run). **Motonet, Biltema.** ~€5 for a small roll. |
| Rubber grommets, assorted | 6–10 mm hole sizes | 1 assortment pack | **ACQUIRED from Motonet 2026-04-20** (art. 0000648787, "MTX Basic läpivientikumilajite", €6.99). Any new pass-throughs drilled in plastic dividers. |
| Cable ties, black | 100 mm × 2.5 mm | 1 bag (~100 pcs) | Securing the loom to factory harness clips. **Motonet/Puuilo.** ~€3. Probably already on hand. |

### 6C.5 — Wood Polish

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Beeswax wood polish | Howard Feed-N-Wax (or equivalent beeswax + orange oil for lacquered wood) | 1 bottle | Bench cleaning + protection of the Zebrano/Burl Walnut panels. **K-Rauta, Bauhaus, Amazon.fi, or furniture-restoration shops.** ~€12–15 / 473 ml bottle — lifetime supply. Alternative: Liberon Natural Finish Beeswax (more readily available in EU). |
| Microfiber cloths | Lint-free, 30 × 30 cm | 2 fresh | Already in inventory (general detailing) — just use clean/unused ones for the wood. |

### 6C.6 — Switch Refresh

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Contact cleaner, plastic-safe | CRC QD Electronic Cleaner 2-26, or WD-40 Specialist Contact Cleaner | 1 can | Non-residue, plastic-safe. Do **not** use generic brake cleaner on the rocker switch plastics. **Motonet, Biltema, Puuilo.** ~€10. |
| Isopropyl alcohol 99% | Any lab-grade IPA | 100 ml+ | For plastic housings and illumination lenses. **Apteekki (pharmacy) or Motonet.** Probably already on hand. |
| Cotton swabs | Regular | 1 pack | For rocker pivot points. Grocery-store aisle. |
| PTFE dry lube or dielectric grease | CRC 2-50 PTFE or CRC Dielectric Grease (already in inventory) | 1 can / existing tube | Dielectric grease is **already in inventory** (Priority 4 consumables). A tiny dab per switch pivot. **No purchase needed if dielectric grease is used.** PTFE dry lube is an alternative if dust-attraction is a worry. |

### 6C.7 — Optional / Nice-to-Have

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Replacement trim clips (universal) | R129-compatible dash-clip assortment | 1 pack | In case original clips break during wood-panel removal. **Biltema universal trim clip kit (~€10) or MB-specific from MB-osat if a specific clip breaks.** Buy pre-emptively — they *will* break on 35-year-old panels. |
| Microphone hardware | **DECISION PENDING** (see `docs/tasks.md` "Microphone integration") | 1 | ⚠ **Must be decided before the console closes.** USB / analog shielded / I2S — spec depends on choice. Do not skip this line item — pulling a mic cable later means re-pulling the trim. |

### 6C.8 — Wireless iPhone Charger (drawer cubby behind the ashtray)

*Embedded Qi pad mounted under the drawer floor, hidden from view. Phone sits flat in the drawer and charges with the lid closed — no surface modification to the original drawer. Powered from the cigarette-lighter hot wire: **MAIN_12 8A white, Klemme 15 (ignition-switched), `permanent_12v: false` field-verified 2026-04-07** — zero parasitic draw with key out. All wiring is local to the center console (no long run). Add to the §5.6b step in `work/center_console_refresh/README.md`.*

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| **Embedded Qi wireless charger module** | **USB-C input, 7.5–15 W output, designed for under-surface mount** (Ugreen 15 W concealed / Choetech CH002 / Nillkin MagicCube class) | 1 | **DECISION PENDING — pick a specific model.** 7.5 W is the iPhone Qi ceiling so anything ≥7.5 W is sufficient; 15 W modules are usually the same price and future-proof for an Android. Mounts UNDER the drawer floor with 3M VHB or a 3D-printed bracket. Spec sheet should state field works through ≥10 mm of non-metal (most "concealed/under-desk" modules state 25–30 mm). **Source:** Verkkokauppa.com (Ugreen typically ~€20–30) or Amazon.de. Avoid round "puck" chargers that need a flat top surface — we want a flat embedded PCB-in-plastic disc. **Reject:** Aircharge Slimline (~€80, overkill — proper flush-mount needs a cutout we don't want), Apple MagSafe puck (~€45, sits visibly inside the drawer and eats vertical clearance). |
| Automotive 12 V → 5 V buck converter | 5 V / 3 A output, 12 V automotive input rated, with input transient protection | 1 | Generic enclosed buck module (Motonet/AliExpress, ~€5–10). Mounts inside the lighter cavity / behind-ashtray void — keeps heat away from the drawer plastic. Or repurpose a gutted USB car-adapter (already on hand) if the bench-tested 5 V/3 A spec checks out. **Verify the module is rated for automotive 12 V (with load-dump tolerance), not just 12 V DC bench input** — the lighter circuit sees alternator transients. |
| Inline 3 A blade fuse + holder | ATO blade, inline | 1 | On the buck's 5 V output. Module itself usually has internal fusing but the run to it is short and an extra 3 A is cheap insurance. **Motonet/Biltema assortment** — likely already on hand from §6C.3. |
| Wago 221-413 (3-port lever nut) | 0.2–4 mm² clamp range | 1 pc | Tap onto the cigarette-lighter hot wire at the connector backshell. Same approach as the BE2210 audio tap. **Already in inventory** (4-pack acquired Motonet 2026-04-20, art. 0000728703 — only 4 used for the BE2210 tap, so spares cover this). |
| Hook-up wire | 2 × 0.75 mm² red/black automotive | ~30 cm | Lighter Wago tap → buck input. Trivial run inside the console void. **Probably already in inventory**; if not, included with any small Motonet hook-up wire roll. |
| 3D-printed mounting bracket (optional) | PETG or ABS, ~5 mm tall flange | 1 | Cleaner than VHB for holding the Qi module flat against the underside of the drawer floor. Print after the Qi module arrives so the bracket can be modeled to its exact dimensions. PLA is fine for first fit but PETG/ABS for the final to survive summer cabin temps. **Self-printed — no purchase.** |

**Net cost: ~€25–35 (charger module) + ~€8–10 (buck + fuse + wire) = ~€35–45 all-in.** All sourceable in a single Verkkokauppa or Motonet trip.

**Decision needed before ordering:** pick the specific Qi module. Recommendation is a Ugreen / Choetech / Nillkin USB-C-input embedded pad in the €20–30 range — confirm by spec sheet that it (a) accepts USB-C 5 V/2 A input (some need 9 V QC — we'd need a different buck), (b) supports through-surface install ≥10 mm, (c) has thermal cutoff and foreign-object detection (FOD).

---

### Summary — What to buy for Console-Out

Net new purchases, excluding items already in inventory:

| Category | Item | Est. cost |
| :--- | :--- | :--- |
| Audio signal | Shielded CAT6 (F/UTP or S/FTP), 5 m (shared with §6C.3 Alps run) | €8–15 |
| | ~~Wago 221-413 × 4~~ — ACQUIRED Motonet 2026-04-20 | ~~€3~~ |
| | Ferrules assortment | €5 |
| | Ring terminal M6 | €0.50 |
| Data | USB 2.0 A-B shielded 3 m | €10 |
| | ~~CAT6 1.5 m~~ — included in the 5 m shared spool above | — |
| | 3.5 mm TRS stereo 0.5 m | €6 |
| Power | 3 A inline fuse holder + fuse | €2 |
| Loom | Tesa cloth tape 19 mm × 25 m | €10 |
| | Split loom 6 mm × 2 m | €5 |
| | Grommet assortment | €5 |
| Wood | Howard Feed-N-Wax or Liberon beeswax | €13 |
| Switches | CRC QD Electronic Cleaner | €10 |
| Safety net | Universal trim clip kit | €10 |
| Wireless charger | Embedded Qi pad (USB-C, 7.5–15 W) | €25–30 |
| | 12 V → 5 V / 3 A automotive buck | €8 |
| | Inline 3 A fuse + holder + hook-up wire | €2 |
| Pending | Microphone hardware | TBD — decide first |
| **Subtotal** | | **~€135 + mic** |

All sourceable within a single trip to Motonet + one online order (Verkkokauppa for the shielded CAT6 + the embedded Qi pad). Nothing is on long lead-time.

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
| ~~Antenna Grommet (Upper)~~ | ~~A 129 827 02 98~~ | — | **DEPRIORITIZED 2026-04-20.** Earlier notes (and the retired `Karkkainen_Shopping_List.md`) claimed a cracked seal leaks water onto the PSE pump — on direct inspection this is **not observed**; antenna grommet rubber looks healthy, no water staining in the trunk around the PSE pump area. Claim appears to have been copied from a generic R129 known-issue list, not from actual AOK912 observation. Re-inspect if PSE pump develops water-related faults; otherwise do not order. |
| ~~Antenna Grommet (Lower)~~ | ~~A 129 827 03 98~~ | — | Same deprioritization as upper. |
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

*Last updated: 2026-04-26 (evening) — §6B Audio: added "DSP Mount & Ground Hardware" row capturing the passenger-cubby install hardware list (M6 ring + star washer + nyloc for the welded-stud chassis ground, optional M5 self-tappers for trim-panel retention, M4 wood screws for amp → base plate, base plate cut from sub-box MDF offcut). Driven by 2026-04-26 evening recon: passenger cubby has a friction-fit factory plastic trim panel as the mounting surface, an M6 welded chassis stud for grounding (dedicated audio reference, isolated from the Becker Verdeck-control return path), and a hand-sized pass-through to the driver-side cubby for the sub speaker run. See diary entry "April 26, 2026 (evening) — DSP install recon: passenger cubby ground point + attachment strategy" (pending) for full rationale.*

*Earlier: 2026-04-26 (early morning) — Sub-enclosure row updated to reflect Saturday 2026-04-25 shopping outcome: 40 × 120 cm MDF acquired (tight panel size triggered Strategy C silicone-fillet joinery flip, cleats dropped); Casco SuperFix+ SMP construction adhesive substituted for PVA D3 (better gap-fill + open time, elastic cure — net positive for this build); 4×40 mm wood screws acquired; terminal cup included in Helix IK S10-DVC2 shipment (saves Autoviihde trip, pending DVC2 isolation + gasket verification before install). Remaining Sunday-AM shopping: caulking gun, white spirit, neutral-cure silicone, polyfill ~135 g. Full rationale in `docs/diary/2026-04.md` "April 26, 2026 (early morning) — Saturday shopping outcome + Strategy-C joinery flip + adhesive substitution" entry.*

*Earlier: 2026-04-24 (6B DSP power & ground: Biltema 84-574 CCA kit retained with a documented mitigation plan — hex-crimp lugs, dielectric grease, 3/12-month re-torque checks. Reversed the Apr 19 "return kit" decision after reviewing actual current draw vs CCA ampacity, the shorter-than-worst-case route length, and the crimp-creep-not-thermal nature of the aluminum risk. Sub-enclosure row expanded with Bauhaus/Autoviihde sourcing and pointer to `work/subwoofer_enclosure/README.md`.)*
