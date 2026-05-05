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
| ADS Shock Absorber Dust Boot (front) | A 129 323 01 92 (≡ `1293230192`) | 2 | **ORDERED from Autodoc 2026-04-20. ARRIVED 2026-04-27.** MEYLE 014 032 0032 (ORIGINAL Quality, "Etuakseli"), €8.29 each = €16.58 total. Front-axle separation at lower compression seal confirmed via photograph 2026-04-20 (see diary) — matches Apr 2 katsastus "lower sections missing" observation. Passenger-side front not yet photographed but ordered 2× on the assumption of symmetric degradation (matched ADS corners typically age together). **Install at next jack-stand session** — exposed front strut shafts will pit and destroy the irreplaceable ADS internal seals. |
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
| **Main Poly-V Serpentine Belt** (alternator / PS / water pump) | **A 010 997 99 92** | 1 | **ORDERED Autodoc 2026-04-20. ARRIVED 2026-04-27** | **ContiTech 6PK2523** (51% off RRP, €32.49). Spec 6PK2523 (6 ribs × 2523 mm). Cross-listed as A 011 997 68 92 / A 119 997 01 92. Correct specifically for M119.960 *with catalytic converter* (AOK912 match). Do NOT substitute the 6PK2510 (late M119.982 w/ A/C), 6PK2425 (M119.982 w/o A/C), 6PK2535 / 6PK2540 (M119.972) — all are different M119 variants with different accessory drive layouts. |
| **A/C Compressor V-Belt** (separate classic V-belt) | **A 004 997 05 92** | 1 | **ORDERED Autodoc 2026-04-20. ARRIVED 2026-04-27** | **ContiTech AVX13X950** (43% off RRP, €10.49). Modern raw-edge cogged replacement for the factory 12 × 960 wrapped V-belt — same application, same OEM cross-reference, functional upgrade. Early M119.960 uses a dedicated V-belt for the A/C compressor in addition to the main poly-V. |
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
| Distributor Caps | A 119 158 01 02 | 2 | **DELIVERED + INSTALLED 2026-05-05** | Bosch caps, fitted by MB-osat 2026-05-05. Combined invoice with rotors + labour: **€426.70 total** (parts + labour bundled — line-item split not separately invoiced). Subjective post-install: idle *may* be smoother but no pre/post video baseline was captured (lesson logged for future swaps — always shoot a 30 s pre-change video). Cabin vibration persists → most likely engine mounts, deferred until after the suspension job. |
| Distributor Rotors | A 119 158 06 88 (Bosch) | 2 | **DELIVERED + INSTALLED 2026-05-05** | Bosch rotors, fitted same session as the caps. See cap line above for combined €426.70 invoice and post-install notes. |
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

## PRIORITY 4B — Steering / Suspension Wear (MB-osat Quote Received 2026-05-05 — Authorisation Pending)

*MB-osat inspection 2026-04-30 found multiple loose steering/suspension joints. Quote returned 2026-05-05: **€2545 total** (~€1502 labour + ~€1043 parts), 9-line scope including mandatory wheel alignment. Authorisation deferred pending answers to seven open questions (see below) and bundling decision with engine-mount inspection. Target authorisation date: 2026-05-12.*

| Finding | Side / Qty | Posture | Notes |
| :--- | :--- | :--- | :--- |
| Rear lower control arm outer joint loose | Left + right | **QUOTED €291.40 labour + parts** | Finnish note: `taka alatukivarren ulkopään nivel, vasen ja oikea väljät`. Quote line: "Taka-akselin alatukivarren alapallonivel (molemmat) ulompi kumityyny vaihto". |
| Lower ball joint loose | Right | **QUOTED — possibly bundled with control arm** | Finnish note: `oikea alapallonivel väljä`. Quote line: "Olka-akselin oikean alemman kannatinnivelen vaihto" €28.20 + ball joint part €30.00. **Open question:** ball joint may be included with the lower control arm if item below is in scope ("alapallo sis alatukivarteen, jos vaihdetaan ne?"). |
| Tie rod inner + outer end loose | Left | **QUOTED — full tie rod replacement** | Finnish note: `vasen raidetanko sisä ja ulkopää väljä`. Full assembly replaced (€140.00). |
| Tie rod inner end loose | Right | **QUOTED — full tie rod replacement** | Finnish note: `oikea raidetanko sisäpää väljä`. Full assembly replaced (€143.50). |
| Tie rod outer-end protective boot torn | Right | **QUOTED — covered by tie rod replacement** | Finnish note: `ulkopäässä suojakumi rikki`. Tie rod assembly comes complete with new boots. |
| Tie rod labour | — | **QUOTED €112.80 + €263.20** | "Raide- ja yhdystanko irrotus ja asennus" + "Raidetangon kannatinvivun helat vaihto". |
| Idler arm play | — | **QUOTED — bushing replacement** | Finnish note: `apusimpukassa välys`. Bushings only (rebuild kit unavailable, ~1 week loose); €185.00 parts. **Open question:** bolt requirement TBD ("pultti tarve?"); €111.50 bolt line currently quoted at qty 0. |
| Front lower control arm rear bushings deteriorated | Left + right | **QUOTED — full control arm replacement** | Finnish note: `alatukivarsien taaemmat puslat huonossa kunnossa ja paloja lähtenyt`. Both arms replaced as complete assemblies: €300.00 + €177.12 + €50.00 adjustment bolts. **Open question:** asymmetric pricing + "TT" suffix on the €300 line — confirm L/R + part grade (OEM vs. MEYLE/TRW). Lead times: left ~1 week (Germany / EU), right in stock, bolts 1–2 days. Quote line: "Etuakselin vasemman ja oikean alemman poikittaistukivarren irrotus ja asennus" €206.80 labour. |
| Left front wheel bearing | Left | **QUOTED €94.00 + €18.80 labour, kit €31.50, grease €6.00** | "Vasen etulaakeri välys". Quote lines: "Pyörännavan etu irrotus ja asennus, tiivisterenkaiden vaihto" + "Pyörännavan pyöränlaakerin etu vaihto". MB hub bushings ×2 €54.00 + M14×90 bolts ×2 €32.00 + bushing nuts ×2 €6.60. |
| Front shock dust covers + bump stops | Front ×2 | **PARTS ON HAND (MEYLE boots) + Sachs bump-stop kit quoted €44.00** | Finnish note: `etuiskarien pölysuojat ja pohjaan lyöntikumit`. MEYLE 014 032 0032 dust boots arrived 2026-04-27. Quoted "2 vaimennintuen etu irrotus ja asennus" €206.80 labour + Sachs suojakumi-pohjaanlyönti srj. €44.00. **Open question:** can MB-osat use the on-hand MEYLE boots and only invoice the bump-stop portion of the Sachs kit, or is the kit not splittable? |
| Exhaust heat shields loose | Front + middle | **QUOTED in pientarvikkeet/labour** | Quote line: "Kiinnitetään pakoputkien lämpösuojapellit esimerkiksi pakoputkiklemmarein". Etuputkien shield loose; centre muffler shield rusted + rattling. Closes out the "loose front heat shields" item from `docs/known_issues.md`. |
| Wheel alignment | — | **QUOTED €99.00** | "Aurauskulmien säätö". Required after tie rod + ball joint replacement. **Open question:** front-only or 4-wheel alignment? R129 has rear toe-settable independent suspension. |

**€2545 total breakdown (rough split): ~€1502 labour + ~€1043 parts + pientarvikkeet €5.48.**

**Lead times:** tie rods ~2 weeks (longest pole); idler arm bushings ~1 week loose; left lower control arm ~1 week from Germany; everything else short order.

**Open questions to resolve with MB-osat before authorisation (transcribed to diary 2026-05-05):**

1. Lower ball joint (qty 1, €30.00) bundled into lower control arm (item 6) → drop the standalone line if so.
2. Lower control arm L/R + grade clarification (`Tukivarsi (TT)` €300 vs `Alatukivarsi oikea` €177.12 — asymmetric pricing).
3. Idler arm bolt: original reusable, or add the €111.50 line?
4. Bump-stop kit splittable from MEYLE boots already on hand, or full Sachs kit only?
5. MEYLE dust boots accepted as substitute parts by MB-osat?
6. Wheel alignment scope (front only vs 4-wheel).
7. Engine-mount inspection bundle while front lower control arms are out (cabin vibration finding from 2026-05-05 diary).

**Decision posture:** authorisation deferred until 2026-05-12 (after belt swap next weekend — see Priority 1B / diary 2026-05-05) so cabin-vibration variable can be partly de-confounded by the belt + tensioner inspection, and so MB-osat answers above can be incorporated.

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
| Shielded CAT6 cable (F/UTP or S/FTP) | 4 twisted pairs, 23 AWG solid-core preferred, overall foil shield + drain wire | ~2.5 m | **ACQUIRED from inventory 2026-05-02 walkthrough** — used 1 of 2 × 3 m CAT6 patch cables on hand (with RJ45 connectors cut off), inner conductors terminated with ferrules into Wago 221-413 at the BE2210 end and into the DSP terminal blocks at the rear cubby. Pair assignment per plan: Blue = LF+/LF−, Orange = RF+/RF−, Green = future UP 6DSP line-level input (uncommitted), Brown = reserved for cabin signal node PSE control to the trunk drive board (per `work/cabin_signal_node/README.md` Stage 7). Overall shield grounded at DSP end only. **Decision rationale (2026-04-20):** substituted for originally-planned Sommer/Cordial audio multi-core because (a) CAT6 is the right technical fit — twisted pairs + overall shield; 100 Ω impedance is irrelevant at audio frequencies; 23 AWG gauge is fine for high-Z DSP input (≥10 kΩ, μA-level signal current, not a speaker-drive application); (b) pro-audio precedent (Rane, Radial, Whirlwind, BSS Soundweb all use CAT5/6 for balanced analog runs); (c) trivially sourceable in Finland vs. multi-week EU order for Sommer / Cordial. |
| ~~Motonet 7 × 1.5 mm² unshielded cable (art. 0000606156)~~ | ~~7-conductor automotive cable, 7 m~~ | — | **RE-PARKED to inventory 2026-04-20.** Initially purchased 2026-04-20 to substitute for a proper shielded cable, with a manual twist-pairs + pseudo-shield install plan. Superseded same day by the shielded-CAT6 decision above (cleaner, no jacket-strip-and-retwist labour, no long-term Tesa-glue dependency for re-sheathing). **Probable future use:** Hertz door-woofer multi-conductor harness during the Priority 6B speaker upgrade — 2× woofer pairs + tweeter pair + spare = 7 conductors, speaker-level signals so unshielded is fine. Parked in electrical stock until that task opens. |
| Wago 221-413 (3-way lever nut) | 0.2–4 mm² clamp range | 4 pcs | **ACQUIRED from Motonet 2026-04-20** (art. 0000728703, "Wago 3-napainen vipuliitin 0,2[–4 mm²]", €9.99/pack). Parallel tap at the BE2210 ISO speaker pigtail — one per signal (LF+, LF−, RF+, RF−). Spares retained. |
| Bootlace ferrules | 0.75 mm², insulated, red | ~10 pcs | DSP-end terminal entry (4 signals) + spares. Assortment kit from Motonet/SP Elektroniikka is fine. ~€5 for the kit. |
| Ring terminal | M6, insulated, 0.5–1.5 mm² | 1 pc | Shield drain → DSP chassis ground bolt. **Motonet assortment.** |
| Heat-shrink labels | 6 mm black + 3 mm black | — | Already in inventory (Stage 1 heat-shrink kit). Use a fine-tip marker + clear shrink-over for durable labels. |

### 6C.2 — DSP-Direction Cable Pull (now in-cubby short cables — Pi co-located with DSP per 2026-05-02 architecture revision)

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| USB 2.0 cable, shielded | Type-A → **Mini-B** (the small trapezoid, NOT full-size Type-B printer connector — connector type clarified at Verkkokauppa pickup 2026-05-02) | 2 m | **ACQUIRED from Verkkokauppa 2026-05-02:** Fuj:tech USB-A ↔ Mini-B 2 m, art. 908881, **€9.99**. RPi5 → MEC HD-USB inside the rear cubby — now an in-cubby short cable, not a long pull (Pi moved from front to rear cubby alongside the DSP, 2026-05-02 evening). 2 m length is more than needed in-cubby but was the available off-shelf length. ⚠ **Only 1 piece bought, no spare** (originally planned for 1 + 1 spare) — add cold-spare to next Verkkokauppa order. |
| Tweeter / speaker wire | **OFC 2 × 1.5 mm² twin-lead** | ~10 m | **ACQUIRED from Motonet 2026-05-02:** **FOUR Connect STAGE2 OFC speaker cable**, art. 0000648404, **€26.90**. Pure-copper OFC twin-lead from Motonet's car-audio department; covers C4 + C5 (and possibly C6) front-stage speaker runs. Twin-lead jacket (both conductors molded together) → loop area ≈ 0, no need to twist or zip-tie pairs. Existing 10 m OFC inventory (SP Elektroniikka) + 5 m CCA 2×2.5 mm² returned to general cable stock as backup. |

### 6C.3 — Pi-Direction Cable Pull (ashtray / BE2210 → rear passenger cubby per 2026-05-02 Pi-rear-move; BE2210 AUX now extends rear, not forward to a front-cubby Pi)

| Part | Ref / Spec | Qty | Notes |
| :--- | :--- | :--- | :--- |
| CAT6 Ethernet cable (joystick) | Shielded (F/UTP or S/FTP) | ~2.5 m | **ACQUIRED from inventory 2026-05-02 walkthrough** — used 2nd of the 2 × 3 m CAT6 patch cables on hand (RJ45 ends cut off, conductors terminated with ferrules into a Pi GPIO Dupont/JST header at the rear cubby end and into the Alps RKJXT1F42001 PCB at the ashtray end). Alps joystick (ashtray) → Pi GPIO (rear passenger cubby — destination updated 2026-05-02 evening with the Pi rear-cubby move). 8 conductors = 7 GPIO + 1 GND. |
| **Spare CAT6 (BE2210 path)** | Shielded **CAT6A S/FTP** (foil-per-pair + overall braid — over-spec vs C1's plain F/UTP) | 2 m | **ACQUIRED from Verkkokauppa 2026-05-02:** Fuj:tech CAT6A S/FTP 2 m black, art. 877678, **€8.99**. Cold spare alongside the C1 BE2210 tap CAT6 — adds 4 fully-uncommitted twisted pairs since C1's "spare" pairs are already partially earmarked (Brown for cabin node PSE control, Green for future UP 6DSP line-level). |
| Stereo AUX cable, shielded | **3.5 mm TRS male ↔ female extension** | 2 m | **ACQUIRED from Verkkokauppa 2026-05-02:** InLine 3.5 mm uros TRS extension, art. 2333, **€8.99**. Length grew from 0.5 m to 2 m with the Pi-rear move (BE2210 AUX now extends back to the rear cubby Pi). The BE2210 already has an attached AUX wire ending in a 3.5 mm plug (inventory finding 2026-05-02) — this extension cable extends that plug to the rear cubby. |
| **HDMI cable (Pi → display)** | Shielded HDMI 1.4, micro-HDMI ↔ full-HDMI, 2 m | 1 | **ACQUIRED from Verkkokauppa 2026-05-02:** Fuj:tech HDMI ↔ micro-HDMI 2 m, art. 917827, **€19.99**. NEW long-pull added 2026-05-02 evening with the Pi rear-cubby move — Pi micro-HDMI HDMI-0 → front-cubby AMOLED display HDMI input. ⚠ **Right-angle full-HDMI adapter still to acquire** (~€5) for flush mounting at the panel end (the Waveshare's inward-facing flush adapter changes the bare panel HDMI to micro-HDMI — adapter at the panel end of our cable avoids re-buying a micro-HDMI both-ends cable). |
| **Display touch + power USB** | Shielded USB 2.0 A ↔ Micro-USB, 2 m, fast-charge / data | 1 | **ACQUIRED from Verkkokauppa 2026-05-02:** Fuj:tech USB-A ↔ Micro-USB 2 m, art. 908662, **€9.99**. NEW long-pull added 2026-05-02 evening with the Pi rear-cubby move — Pi USB-A → display touch micro-USB port (carries both touch HID data and 5 V power on the same cable, same as bench bring-up April 17). ⚠ **Right-angle micro-USB adapter still to acquire** (~€5) for flush mounting at the panel end. **Backup option:** front-cubby C12 → local 12 V → 5 V buck can feed the display's separate "power" micro-USB port if voltage drop bites; cable already pulled. |
| **Cabin node ↔ Pi USB-CDC** | Shielded USB 2.0 A ↔ USB-C, 2 m | 1 | **ACQUIRED from Verkkokauppa 2026-05-02:** Fuj:tech USB-C ↔ USB-A 2 m, art. 844156, **€15.99**. NEW long-pull added 2026-05-02 evening — front-cubby cabin signal node USB-C → Pi USB-A in the rear cubby. Standard data cable, no special requirements (USB-CDC is low-bandwidth telemetry). |
| Hook-up wire (now F20_6 +12 V to front cubby — was Pi forward power feed, **obsolete with Pi-rear move**) | 1.5 mm² red automotive | ~3 m | **C12** F20_6 permanent +12 V → front cubby for the cabin signal node low-Iq buck (per `work/cabin_signal_node/README.md` Stage 6) and optional display power buck fall-back. **Acquire from general 1.5 mm² hookup stock or Motonet single-conductor**, ~€5. Pull wasn't logged with the May 2 receipt explicitly — verify against actual cable run during Phase 6 sign-off. |
| Fuse holder + 5 A ATO fuse | In-line ATO 5 A | 1 | **ON HAND** — in-line ATO 5 A fuse holder + 5 A fuses already in inventory (verified during 2026-05-02 walkthrough). Goes on the **C12** F20_6 source. |

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
| Contact cleaner, plastic-safe | **PRF Kontakt 7-8 -puhdistusaine, 220 ml** (Finnish-brand equivalent of CRC QD / WD-40 Specialist) | 1 can | **ACQUIRED from Verkkokauppa 2026-05-02:** PRF Kontakt 7-8 220 ml, art. 32414, **€11.99**. Non-residue, plastic-safe. Do **not** use generic brake cleaner on the rocker switch plastics. Cleared as the cleaner of choice for Phase 3 non-disassembly spray-flush + selective full disassembly. |
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
| **Embedded Qi wireless charger module** | **FoneKit WP-15Q2 -langaton Qi2-latausalusta** (Qi2 spec, USB-C input, 15 W output, magnetic alignment) | 1 | **ACQUIRED from Verkkokauppa 2026-05-02:** FoneKit WP-15Q2, art. 932995, **€39.99**. *Upgraded to Qi2 spec* (Apple-MagSafe-derived, magnetic alignment for consistent phone-in-drawer placement, 15 W native to iPhone 13+) vs the planned plain Qi 7.5 W (~€25–30). USB-C input matches the planned C13 buck output. Verify pad disc thickness fits in the drawer void on first fit; mount with 3M VHB interim, 3D-printed bracket later (deferred until phone position preference is established by use). |
| Automotive 12 V → 5 V buck converter | 5 V / 3 A output, 12 V automotive input rated, with input transient protection | 1 | **DEFERRED 2026-05-02** — interim solution: repurpose a cigarette-lighter USB charger from inventory (most are 12 V → 5 V / 2.4 A bucks built in). Either gut the buck PCB and tap the lighter wiring directly, or initially just plug the adapter into the lighter socket and run a USB cable to the Qi pad. **Verify the FoneKit's USB-C input accepts plain 5 V** (vs requiring 9 V QC); if 5 V works, the interim is fine until a proper automotive load-dump-rated buck (~€5–10) is acquired on the next Motonet trip. Replacement is additive — no re-trim work needed. |
| Inline 3 A blade fuse + holder | ATO blade, inline | 1 | **ON HAND** — already in inventory (verified 2026-05-02 walkthrough). Goes on the buck's 5 V output. |
| **Wago 2-pole lever nut for the lighter tap** | **Wago 2-napainen vipuliitin (0.2–4 mm² range)** | 1 pc | **ACQUIRED from Motonet 2026-05-02:** Wago 2-pole lever connector, art. 0000728710, **€1.99**. 2-pole sized for the 2-wire lighter-hot tap (vs the 3-pole 221-413 used at the BE2210 ISO speaker block — the lighter tap only needs 2 ports: factory wire continuation + new branch to the buck). Same Wago 221-series quality as the BE2210 tap. |
| Hook-up wire | 2 × 0.75 mm² red/black automotive | ~30 cm | Lighter Wago tap → buck input. Trivial run inside the console void. **Probably already in inventory**; if not, included with any small Motonet hook-up wire roll. |
| 3D-printed mounting bracket (optional) | PETG or ABS, ~5 mm tall flange | 1 | Cleaner than VHB for holding the Qi module flat against the underside of the drawer floor. Print after the Qi module arrives so the bracket can be modeled to its exact dimensions. PLA is fine for first fit but PETG/ABS for the final to survive summer cabin temps. **Self-printed — no purchase.** |

**Net cost: ~€25–35 (charger module) + ~€8–10 (buck + fuse + wire) = ~€35–45 all-in.** All sourceable in a single Verkkokauppa or Motonet trip.

**Decision needed before ordering:** pick the specific Qi module. Recommendation is a Ugreen / Choetech / Nillkin USB-C-input embedded pad in the €20–30 range — confirm by spec sheet that it (a) accepts USB-C 5 V/2 A input (some need 9 V QC — we'd need a different buck), (b) supports through-surface install ≥10 mm, (c) has thermal cutoff and foreign-object detection (FOD).

---

### Summary — What was bought for Console-Out (updated 2026-05-03)

Console-out shopping run executed Saturday 2026-05-02 — Verkkokauppa pickup at 14:43 + Motonet Vasaraperä at 15:12. Total R129 spend €154.81. Full itemization in `docs/diary/2026-05.md` May 3 entry; rolled-up status:

| Category | Item | Source | Acquired | € |
| :--- | :--- | :--- | :--- | :--- |
| Audio signal | ~~Bulk shielded CAT6, 5 m~~ — used **2 × 3 m CAT6 patches** from inventory for **C1 + C8** | inventory | ✅ 2026-05-02 walkthrough | (on hand) |
| | **Fuj:tech CAT6A S/FTP 2 m black** for **C9** spare | Verkkokauppa | ✅ 2026-05-02 (art. 877678) | €8.99 |
| | ~~Wago 221-413 × 4~~ — ACQUIRED Motonet 2026-04-20 for the BE2210 tap | Motonet | ✅ 2026-04-20 | (on hand) |
| | Ferrules assortment | inventory / Motonet | (general stock) | — |
| | Ring terminal M6 | inventory / Motonet | (general stock) | — |
| Data — in-cubby | **Fuj:tech USB-A ↔ Mini-B 2 m** for Pi → MEC HD-USB *(connector finding 2026-05-02: Mini-B, NOT full Type-B)* | Verkkokauppa | ✅ 2026-05-02 (art. 908881) — **1 pc, no spare** | €9.99 |
| Data — long pulls (NEW with Pi-rear move) | **Fuj:tech HDMI ↔ micro-HDMI 2 m** for **C16** Pi → display | Verkkokauppa | ✅ 2026-05-02 (art. 917827) | €19.99 |
| | **Fuj:tech USB-A ↔ Micro-USB 2 m** for **C17** display touch + power | Verkkokauppa | ✅ 2026-05-02 (art. 908662) | €9.99 |
| | **Fuj:tech USB-C ↔ USB-A 2 m** for **C18** cabin node ↔ Pi USB-CDC | Verkkokauppa | ✅ 2026-05-02 (art. 844156) | €15.99 |
| Audio | **InLine 3.5 mm uros TRS extension 2 m** for **C10** BE2210 AUX | Verkkokauppa | ✅ 2026-05-02 (art. 2333) | €8.99 |
| Speakers | **FOUR Connect STAGE2 OFC 2 × 1.5 mm² twin-lead** for **C4 / C5 / (C6?)** front-stage | Motonet | ✅ 2026-05-02 (art. 0000648404) | €26.90 |
| Power | In-line ATO 5 A fuse holder + fuses for **C12** | inventory | ✅ on hand | (on hand) |
| | Inline 3 A blade fuse + holder for **C13** | inventory | ✅ on hand | (on hand) |
| Loom | Tesa cloth tape 19 mm × 25 m | (still to acquire — Motonet next trip) | ❌ pending | €10 |
| | Split loom 6 mm × 2 m | (still to acquire — Motonet next trip) | ❌ pending | €5 |
| | ~~Grommet assortment~~ | Motonet | ✅ 2026-04-20 (art. 0000648787) | (on hand) |
| Wood | ~~Beeswax~~ — using **King Carthur Reshine 3/3 + Soft99 'UUSI FUSSO' Coat White wax** from inventory (Kärkkäinen 2026-03-30) | inventory | ✅ on hand | (on hand) |
| Switches | **PRF Kontakt 7-8 contact cleaner 220 ml** | Verkkokauppa | ✅ 2026-05-02 (art. 32414) | €11.99 |
| Safety net | Universal trim clip kit | (still to acquire — Biltema next trip) | ❌ pending | €10 |
| Wireless charger | **FoneKit WP-15Q2 Qi2 wireless charging pad** (upgraded to Qi2 spec, USB-C input, 15 W, magnetic alignment) | Verkkokauppa | ✅ 2026-05-02 (art. 932995) | €39.99 |
| | **Wago 2-pole lever nut** for cigarette-lighter tap | Motonet | ✅ 2026-05-02 (art. 0000728710) | €1.99 |
| | Automotive 12 V → 5 V / 3 A buck | (deferred — interim via gutted cigarette-lighter USB charger) | ⚠ deferred | €5–10 future |
| Display flush mount | Right-angle full-HDMI adapter (panel end of C16) | (still to acquire — Verkkokauppa next order) | ❌ pending | €5 |
| | Right-angle micro-USB adapter (panel end of C17) | (still to acquire — Verkkokauppa next order) | ❌ pending | €5 |
| Pending | Microphone hardware (C14) — front-cubby location locked, hardware still to pick (Option C USB conference puck recommended) | — | ⚠ pending | €30–50 |
| **Subtotal — May 2 spend (R129 only)** | | | | **€154.81** |
| **Pending residual (loom tape, trim clips, display adapters, mic)** | | | | **~€55–75** |

The pending residual items don't gate Phase 6 trim close — loom tape and trim clips can be done after, display adapters can go on the next Verkkokauppa order, and mic hardware can join the trim later via the fish-string already pulled in the Bundle G sleeve.

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

*Last updated: 2026-05-03 — §6C bookkeeping pass for the Saturday 2026-05-02 cable-pull shopping run. §6C.1 / 6C.2 / 6C.3 / 6C.6 / 6C.8 entries marked ACQUIRED with actual product names + Verkkokauppa or Motonet article numbers + receipt prices. §6C.2 USB cable connector type corrected from "Type-A → Type-B (printer connector)" to **USB-A ↔ Mini-B** (the small trapezoid pre-micro-USB connector that the MEC HD-USB module actually uses) per the in-store finding 2026-05-02. §6C.3 expanded to include the three NEW front ↔ rear long-pull data cables (C16 HDMI, C17 display USB, C18 cabin-node USB-CDC) added 2026-05-02 evening with the Pi-rear-cubby move; AUX cable length grew from 0.5 m to 2 m for the same reason. §6C.8 Qi pad row updated for the **upgraded Qi2 spec** (FoneKit WP-15Q2, magnetic alignment, USB-C input) and the **interim cigarette-lighter-USB-charger buck** approach. Summary table at the bottom of §6C rebuilt as a status table with R129 spend rolled up to **€154.81 for May 2** and the pending residual (loom tape, trim clips, display adapters, mic hardware) called out separately. Full receipt itemization in `docs/diary/2026-05.md` May 3 entry.*

*Earlier: 2026-04-30 — MB-osat inspection updates: distributor caps + rotors ORDERED after idle-misfire assessment (delivery expected 2026-05-05); new Priority 4B steering/suspension quote-pending section added from MB-osat findings; front ADS dust boots / bump stops now independently confirmed by MB-osat. Exhaust parts are NOT needed for the resonance; loose front heat shields are a simple fix and tracked in `known_issues.md`.*

*Earlier: 2026-04-26 (evening) — §6B Audio: added "DSP Mount & Ground Hardware" row capturing the passenger-cubby install hardware list (M6 ring + star washer + nyloc for the welded-stud chassis ground, optional M5 self-tappers for trim-panel retention, M4 wood screws for amp → base plate, base plate cut from sub-box MDF offcut). Driven by 2026-04-26 evening recon: passenger cubby has a friction-fit factory plastic trim panel as the mounting surface, an M6 welded chassis stud for grounding (dedicated audio reference, isolated from the Becker Verdeck-control return path), and a hand-sized pass-through to the driver-side cubby for the sub speaker run. See diary entry "April 26, 2026 (evening) — DSP install recon: passenger cubby ground point + attachment strategy" for full rationale.*

*Earlier: 2026-04-26 (early morning) — Sub-enclosure row updated to reflect Saturday 2026-04-25 shopping outcome: 40 × 120 cm MDF acquired (tight panel size triggered Strategy C silicone-fillet joinery flip, cleats dropped); Casco SuperFix+ SMP construction adhesive substituted for PVA D3 (better gap-fill + open time, elastic cure — net positive for this build); 4×40 mm wood screws acquired; terminal cup included in Helix IK S10-DVC2 shipment (saves Autoviihde trip, pending DVC2 isolation + gasket verification before install). Remaining Sunday-AM shopping: caulking gun, white spirit, neutral-cure silicone, polyfill ~135 g. Full rationale in `docs/diary/2026-04.md` "April 26, 2026 (early morning) — Saturday shopping outcome + Strategy-C joinery flip + adhesive substitution" entry.*

*Earlier: 2026-04-24 (6B DSP power & ground: Biltema 84-574 CCA kit retained with a documented mitigation plan — hex-crimp lugs, dielectric grease, 3/12-month re-torque checks. Reversed the Apr 19 "return kit" decision after reviewing actual current draw vs CCA ampacity, the shorter-than-worst-case route length, and the crimp-creep-not-thermal nature of the aluminum risk. Sub-enclosure row expanded with Bauhaus/Autoviihde sourcing and pointer to `work/subwoofer_enclosure/README.md`.)*
