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
| Thermostat (82°C) | A 119 200 04 15 (verify) | 1 | **ORDERED from MB-osat 2026-04-02.** |
| Radiator Cap | A 124 500 04 06 (verify) | 1 | Cheap insurance — weak cap lowers boiling point. |

**MB-osat (2026-04-02):** Thermostat confirmed and ordered (82°C). Radiator cap not yet ordered.

### Transmission Fluid (722.3)
*No filter to change on the 722.3 — just fluid. Need enough for 2–3 drain-and-fill cycles (~5L per cycle).*

| Part | Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ATF (MB 236.1 spec) | e.g., Fuchs TITAN ATF 3353 or Febi 08971 | 10–15 L | 722.3 capacity ~7L total; 2–3 drain cycles needed for near-complete exchange. |

**Source:** Motonet or MB-osat. Confirm MB 236.1 (NOT 236.10 or 236.14 — those are for later transmissions).

### ADS Hydraulic System

| Part | OEM Number | Qty | Notes |
| :--- | :--- | :--- | :--- |
| ADS Suction Filter | A 129 327 00 91 | 1 | **ORDERED from MB-osat 2026-04-02.** Old one cleaned on 2026-03-29 as interim fix. |
| ZH-M Hydraulic Fluid (MB 343.0) | 000 989 91 03 (Febi 02615) | 1–2 L | Top-up for closed-loop bleed. 4L used in open-loop flush on 03-29. Check remaining level. |

### Predictive Electronics Maintenance (Task #14)

| Part | Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Thermal Compound | Arctic MX-6 or Noctua NT-H1 | 1 tube (4g) | EZL ignition module thermal paste refresh — original has dried to chalk after 35 years. Non-conductive type required. Also useful for any heat-sinked power modules. |

---

## PRIORITY 2 — Upper Timing & Valve Cover Service (M119)

*Preventive inspection of timing chain guides and upgrade of oil bridge clips. The single most important M119 preventive maintenance task. All parts needed before the valve covers come off.*

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Valve Cover Gasket Set (Right bank) | 119 010 03 30 | 1 | **ORDERED from MB-osat 2026-04-02.** Incl. spark plug hole seals. |
| Valve Cover Gasket Set (Left bank) | 119 010 04 30 | 1 | **ORDERED from MB-osat 2026-04-02.** Incl. spark plug hole seals. |
| Upper Timing Chain Guide (Slide rail) | 119 050 02 16 | 2 | **ORDERED from MB-osat 2026-04-02.** >100 € per side. |
| Upper Timing Chain Guide (U-shape) | 119 052 09 16 | 1–2 | Depending on M119 sub-version — confirm with MB-osat. |
| Aluminum Camshaft Oiler Tubes | URO 1191800266PRM (OEM: 119 180 02 66) | 16 | [RockAuto](https://www.rockauto.com/en/catalog/mercedes-benz,1990,500sl,5.0l+v8,1195141) (Engine → Camshaft Oiler Kit). URO Parts anodized aluminum w/ Viton FKM o-rings. ~€14.15/ea × 16 = ~€226 + FedEx/customs/VAT ≈ **€285 delivered.** Use FedEx "Pay import duties in advance." **Verify qty 16 with MB-osat EPC before ordering.** |
| Breather Hose (Crankcase vent) | 119 094 03 82 | 1 | **NOT ORDERED** — will inspect condition first. |

**MB-osat (2026-04-02):** Timing guides confirmed and ordered. Breather hose deferred to inspect-first. Future orders to be sent by email.

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
| One-Person Pressure Bleeder | Gunson Eezibleed or similar | 1 | **Needed** | Connects to brake reservoir cap, pressurizes to ~1 bar. Best for ABS-equipped cars. |
| Brake Fluid (extra) | ATE TYP200 DOT4 | 1 L | **Needed** | Second bottle for a full flush if fluid is dark (1L already on hand). |
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

## PRIORITY 6 — Electrical Consumables & Small Items

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Torpedo Fuses (8A white) | — | 5+ | For trunk F20 fuse box. Need enough to replace all positions + spares. Check current ratings: 16A, 16A, 25A, 8A, 16A, 8A. |
| Torpedo Fuses (16A red) | — | 5+ | Most common in F20 box (3 positions). Copper/ceramic preferred over aluminum. |
| Torpedo Fuses (25A blue) | — | 2+ | One position in F20 box. |
| Headlight Switch Knob | (verify P/N w/ MB-osat by VIN) | 1 | Current knob is worn/soft. Check if the knob is replaceable separately or if the entire switch assembly is needed. |

---

## PRIORITY 7 — Body & Trim (Whenever Convenient)

| Part | OEM Number / Ref | Qty | Notes |
| :--- | :--- | :--- | :--- |
| Antenna Grommet (Upper) | A 129 827 02 98 | 1 | Cracked seal leaks water onto the PSE pump in the trunk. |
| Antenna Grommet (Lower) | A 129 827 03 98 | 1 | Order with upper. |
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
6. **Aluminum oil bridge clips:** They won't have these (aftermarket only), but ask if they've seen M119 cam lobe pitting from loose bridges — shop experience is valuable.
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
- Spark Plugs: NGK BP5ES ×8
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

*Last updated: 2026-04-02*
