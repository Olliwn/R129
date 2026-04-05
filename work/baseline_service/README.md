# Baseline Service — Unknown History (Spring 2026)

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | **Engine:** M119.960 V8 (KE-Jetronic) | **Trans:** 722.3

No written service history exists for this vehicle. Assume all consumables and wear items are overdue. This checklist establishes a known-good baseline for reliability and longevity.

---

## A. Engine Oil & Filtration

- [ ] **Engine Oil & Filter Change** — Drain and refill with MB 229.5 spec fully-synthetic (e.g., Mobil 1 0W-40 or Liqui Moly 5W-40). Replace oil filter with **MANN H 829/1 x**. Capacity: ~8L.
- [ ] **Oil Filter Housing Cap** — Inspect the plastic cap for cracks when removing (requires 36mm socket). Replace if cracked.

### Instructions

#### Parts
| Part | P/N / Spec | Qty | Status |
| :--- | :--- | :--- | :--- |
| Engine Oil | Mobil 1 0W-40 (MB 229.5) | 8L | On hand |
| Oil Filter | MANN H 829/1 x (cartridge) | 1 | On hand |
| Drain Plug Washer (copper, 14mm ID) | A 007 603 014 106 / Febi 07215 | 5 | **ORDERED from Autodoc 2026-04-04.** ETA ~1 week. |

#### Tools
- 13mm hex socket or Allen key (drain plug)
- 36mm socket **or** Bahco BE6307614F 74mm/14-flute oil filter wrench (housing cap)
- Oil drain pan
- Nitrile gloves, shop towels, brake cleaner for drips
- Torque wrench (3/8" or 1/2")

#### Step-by-Step Procedure

**Prep:**
1. Warm up the engine (5 min idle or a short drive). Warm oil drains faster and suspends more contaminants.
2. Lift the front of the car on jack stands (see [Jacking Instructions](Jacking_Instructions.md)). Side-skirt rubber pad method is easiest — no undershield removal needed.
3. Remove the plastic undershield if present (four 8mm bolts) for drain plug access.

**Phase 1 — Oil Filter (from above, engine bay):**

4. Locate the oil filter housing on the **passenger (right) side** of the block. It is a vertical canister with a plastic cap on top.
5. Use the 36mm socket or Bahco filter wrench to unscrew the plastic housing cap. **Turn slowly and carefully** — the cap is plastic and will crack if forced or cross-loaded.
6. Lift out the old filter cartridge. Oil from the housing will drain back into the sump — this is why the filter is done first.
7. **Inspect the plastic cap for cracks** (common M119 failure point). A cracked cap will weep oil and must be replaced.
8. Remove the old O-ring from the cap. Install the new O-ring (supplied with the MANN filter). Lightly oil the new O-ring with fresh engine oil.
9. Insert the new MANN H 829/1 x cartridge into the housing.
10. Hand-thread the cap back on, then snug with the wrench. **Do not overtorque** — approximately **25 Nm** (hand-tight + ~1/4 turn). Plastic cap threading into aluminum.

**Phase 2 — Drain Oil (from below):**

11. Place drain pan under the oil pan drain plug.
12. Remove the drain plug with the **13mm hex** socket. **Oil will be hot** — position the pan and keep hands clear.
13. Let it drain fully — at least 5–10 minutes. Tilt the drain pan slightly if needed to catch the last drips.
14. Inspect the copper crush washer on the drain plug. If it is flat and undamaged, it can be reused once. If deformed, cracked, or on its second use, replace it.
15. Reinstall the drain plug with washer. Torque to approximately **30–40 Nm**. The oil pan is aluminum — do not strip the threads.

**Phase 3 — Refill (car on stands, then level ground):**

16. Pour approximately **7L** of Mobil 1 0W-40 through the oil filler cap on top of the engine. Deliberately underfill at this stage.
17. Start the engine — the oil pressure warning light **must** go out within 2–3 seconds. If it stays on, shut off immediately and check the filter cap and drain plug.
18. Let the engine idle for 30 seconds to fill the new filter and circulate oil. Shut off.
19. **Lower the car off the stands** onto level ground.
20. Wait 2–3 minutes for oil to settle back into the pan.
21. Check the dipstick on level ground. Top up in small increments (0.25L at a time) to the **max** mark. Total capacity with filter is approximately 8L.

**Phase 4 — Leak Check:**

22. Start the engine, let it idle for 1 minute.
23. Shut off. Check the drain plug and filter housing cap area for leaks. Both should be dry.
24. Recheck oil level after 2 minutes — adjust if needed.

#### Warnings
- **Plastic filter cap** is the most fragile part of this job. Never use an impact driver. If it's seized, apply penetrating oil around the base and wait — do not force it.
- **Aluminum oil pan** — the drain plug threads are soft. Always hand-start the plug before using a wrench.
- **Do not overfill.** Excess oil can be forced into the crankcase ventilation system and foul the intake. If over the max mark, extract excess with the fluid syringe.
- The dipstick reading is only accurate on **level ground** with the engine off for at least 2 minutes.

---

## B. Ignition System (M119 Twin-Distributor)

- [x] **Spark Plugs** — ✅ Replaced all 8 (2026-04-05). **NGK BCP5ES** (7496) non-resistor copper plugs, 16mm hex, 0.8mm gap, torqued to 22 Nm.
- [x] **Distributor Caps & Rotors (×2)** — ✅ Inspected 2026-04-05. Both caps and rotors in serviceable condition — no carbon tracking, no deep pitting, no cracks. Clean with minor oxidation. Replace as preventive during valve cover gasket service.
- [ ] **Spark Plug Wires** — Inspect resistance (should be <10 kΩ per wire). Replace full set if any are out of spec or brittle. *(Not yet measured — Owon current fuse blown, voltage/resistance still works but deferred.)*

### Instructions

**⚠️ IMPORTANT: Correct spark plug for M119.960 (KE-Jetronic) is NGK BCP5ES or Bosch F8DC4 — both are 16mm hex.** The commonly suggested NGK BP5ES has a 20.8mm hex that is too large for the M119 spark plug wells. The "C" in BCP5ES = compact (16mm) hex.

| Plug | Hex | Thread | Reach | Gap | Resistor | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NGK BCP5ES** (7496) | **16mm** ✅ | M14×1.25 | 19mm | 0.8mm | Non-resistor (SOLID) | **Installed 2026-04-05** |
| **Bosch F8DC4** | **16mm** ✅ | M14×1.25 | 19mm | 0.8mm | Non-resistor | OEM equivalent |
| ~~NGK BP5ES~~ | ~~20.8mm~~ ❌ | M14×1.25 | 19mm | 0.8mm | Non-resistor | **WRONG — too large** |

*The M119 KE-Jetronic requires non-resistor plugs because the factory plug wire boots already contain resistors. Using resistor plugs (like Bosch FR8DC+) will cause a weak spark and rough idle.*

**Spark plug well oil leak finding (2026-04-05):** 6 of 8 wells contain oil — only front cylinders (1 and 5) are dry. Both banks affected. Root cause: degraded spark plug tube seals. Oil is external only (valve cover → well), not entering combustion chambers (all electrode tips were clean/healthy). **Both valve cover gasket sets + 8× tube seals needed** — schedule with Priority 2 timing chain guide inspection.

**Procedure:** Remove plastic spark plug wire covers (2 per bank, large flat screwdriver on twist-fasteners). Pull wire boots by twisting and pulling straight up. 16mm magnetic spark plug socket + extension + ratchet. Hand-thread new plugs first to avoid cross-threading aluminum heads. Torque: 20–25 Nm. Cap screws are Phillips (not Torx).

---

## C. Fuel System

- [ ] **Fuel Filter** — Replace the inline fuel filter (located under the car, passenger side) with **MANN WK 830/3**.
- [ ] **Fuel Accumulator** — Inspect (holds residual pressure for hot restart). If hard-start when hot, replace.

### Instructions
*TODO: Add fuel filter location diagram, line depressurization procedure, and flow direction arrow.*

---

## D. Drive Belts

- [ ] **Belt Squeal First Aid** — Apply belt friction spray (on hand) to V-belts during cold start squeal. Squeal stopped immediately
- [ ] **Serpentine / V-Belts** — Inspect all belts for cracking, glazing, and tension. The M119 uses multiple V-belts (not a single serpentine). No cracking, but since squal was fixed with v-belt spray the belt is to be replaced (age unknown but likely very old)
- [ ] **Belt Tensioners & Idler Pulleys** — Check for bearing play/noise. No noise, play is not checked yet.

### Instructions
*TODO: Add belt routing diagram, belt part numbers, and tension specs.*

---

## E. Cooling System

- [ ] **Full Coolant Flush** — Drain, flush, and refill with MB 325.0 spec (Glysantin G48, 50/50 mix).
- [ ] **Thermostat** — Replace (known M119 failure point, causes overcooling or overheating). OEM temp: 80°C.
- [ ] **Coolant Hoses** — Inspect all rubber hoses for swelling, cracking, and softness. Replace any suspect hoses (prioritize the lower radiator hose and heater hoses).
- [ ] **Radiator Cap** — Replace (cheap insurance; a weak cap lowers boiling point).

### Instructions

#### Parts
| Part | P/N / Spec | Qty | Status |
| :--- | :--- | :--- | :--- |
| Coolant Concentrate | Motox Classic G11 Blue (MB 325.0 / G48 equiv.) | 10L | On hand |
| Distilled Water | — | 10L | On hand |
| Thermostat (82°C) | A 119 200 04 15 | 1 | **ORDERED from MB-osat 2026-04-02.** |
| Radiator Cap (1.4 bar) | A 124 500 04 06 / Febi 06568 | 1 | **ORDERED from Autodoc 2026-04-04.** |
| Thermostat Gasket / O-ring | *(supplied with thermostat — verify)* | 1 | Check with thermostat delivery |

Total system capacity: ~11.5L. Final fill is 50/50 mix (≈5.5–6L concentrate + 5.5–6L distilled water). Extra concentrate and water is consumed by the flush cycles.

#### Tools
- Drain pan (≥12L, or empty and reuse between cycles)
- 19mm socket (block drain plugs — verify size before starting)
- Flathead screwdriver or pliers (radiator petcock)
- Funnel with narrow neck (expansion tank filler)
- Nitrile gloves, shop towels
- Garden hose with low-pressure nozzle (optional, for running-water flush)

#### Drain Points (M119 in R129)
1. **Radiator petcock** — lower right (passenger) side of radiator. Plastic valve, turn by hand or with pliers. Drains the radiator (~4L).
2. **Engine block drain plugs** — one per bank, lower sides of the block. 19mm hex (verify before starting — some blocks use a different size). Drains the water jackets (~4–5L combined).
3. **Heater core** — no dedicated drain. Flushed by flow during the flush cycles with the heater valve open.

#### Step-by-Step Procedure

**⚠️ Engine must be COLD. Pressurized coolant at 90°C+ will cause severe burns.**

**Phase 1 — Drain Old Coolant:**

1. Open the expansion tank cap (left/driver side of engine bay) to break vacuum.
2. Place drain pan under the radiator. Open the radiator petcock (lower right side). Let it drain.
3. Open both engine block drain plugs. Let everything drain — at least 10 minutes. Rock the car gently if accessible to help clear trapped pockets.
4. Total recovered: typically 8–10L (some remains trapped in the heater core and hoses).

**Phase 2 — Flush (Distilled Water):**

5. Close the block drain plugs and radiator petcock.
6. Fill the system through the expansion tank with plain distilled water (or clean tap water for flush cycles only). Fill slowly to reduce air pockets.
7. Set the cabin heater to **full hot** (opens the heater valve so water flows through the heater core).
8. Start the engine, let it idle with the expansion tank cap **off**. Watch for air bubbles rising in the tank.
9. Let the engine run until the thermostat opens (temp gauge rises then stabilizes, upper radiator hose gets hot). This circulates water through the entire system including the heater core.
10. Shut off the engine. Let it cool enough to handle safely (~15–20 min, does not need to be fully cold).
11. Drain again from all three points (radiator petcock + both block plugs).
12. **Inspect the drained water.** If it's brown, rust-colored, or has visible particles, repeat steps 5–11 until it runs reasonably clear. Two flush cycles is typical; heavily contaminated systems may need three.

**Phase 3 — Fill with Coolant (50/50 Premix):**

13. Close all drain plugs and the radiator petcock. Ensure block plugs are snug — aluminum block, do not overtorque.
14. Pre-mix coolant: 5.5–6L Motox G11 concentrate + equal volume distilled water in a clean container.
15. Fill slowly through the expansion tank. If there is a bleed screw on the thermostat housing (small screw on the housing where the upper radiator hose meets the engine), open it now — close it when coolant flows out bubble-free.
16. Fill to the **MAX** mark on the expansion tank. Install the cap loosely (not fully tightened).
17. Heater still on full hot. Start the engine, idle with the cap loose.
18. Watch the expansion tank — air bubbles will rise as the system purges. Top up as the level drops.
19. When the thermostat opens (upper hose gets hot, you'll see a sudden rush of bubbles and a level drop), top up again to the MAX mark.
20. Tighten the expansion tank cap fully. Let the engine idle for another 2–3 minutes. Shut off.

**Phase 4 — Thermostat & Radiator Cap Replacement (if parts have arrived):**

21. If replacing the thermostat: do it **before** Phase 3 (while the system is drained). The thermostat housing is at the front of the engine where the upper radiator hose connects. Remove the housing bolts, swap the thermostat and gasket/O-ring, reinstall. Torque housing bolts to ~10 Nm (small aluminum housing — do not overtorque).
22. The new radiator cap (Febi 06568, 1.4 bar) simply replaces the old one on the expansion tank — no tools needed. Install after the final fill.

**Phase 5 — Leak Check & Final Level:**

23. With the engine off, visually inspect all drain plugs, the radiator petcock, thermostat housing, and all hose connections for leaks.
24. Let the car cool completely (several hours or overnight).
25. Check the expansion tank level cold — should be between MIN and MAX. Top up if needed.
26. After the first drive, recheck the level once more. The system may purge a final air pocket and drop slightly.

#### Warnings
- **Never open the expansion tank cap on a hot engine.** The system is pressurized to 1.4 bar — boiling coolant will erupt.
- **Block drain plugs thread into aluminum.** Hand-start always. Snug only — no torque wrench needed, just firm-and-stop.
- **Coolant is toxic to animals.** Ethylene glycol is sweet-tasting and lethal. Clean up all spills and dispose of old coolant properly (Oulu waste station accepts it).
- **Heater valve must be open (full hot)** during both flushing and filling, or the heater core will trap old coolant / air.
- **Do not mix G11/G48 (blue-green, silicate) with G12/G13 (pink/purple, OAT).** If unsure what's in the system, the flush cycles will dilute any old coolant to negligible levels before the final fill.

---

## F. Transmission (722.3)

- [ ] **ATF Drain & Fill** — Drain and refill with MB 236.1 spec ATF. The 722.3 does not have a serviceable filter; fluid change is the maintenance item. Capacity: ~5L per drain cycle (do 2–3 drain-and-fill cycles for a near-complete exchange).
- [ ] **Transmission Mount** — Inspect for sagging/cracking. Replace if collapsed (causes drivetrain vibration).

### Instructions
*TODO: Add drain plug location, fluid level check procedure (dipstick at 80°C in Park), and mount part number.*

---

## G. Brakes

- [ ] **Brake Fluid Flush** — Complete flush with DOT 4+ (MB 331.0 spec). Brake fluid is hygroscopic; assume it hasn't been changed in years. Bleed all four corners (RR → LR → FR → FL).
- [ ] **Brake Pad Inspection** — Measure remaining pad thickness (front & rear). Replace if <3mm.
- [ ] **Brake Disc Inspection** — Check for scoring, lip, and minimum thickness markings. Measure with a micrometer.
- [ ] **Brake Hoses (×4)** — Inspect all four rubber flex hoses for cracking, swelling, or sponginess. Replace if any doubt (35-year-old rubber).

### Instructions
*TODO: Add bleeding sequence, bleeder valve sizes, minimum disc thickness specs, and pad part numbers.*

---

## H. Engine Mounts & Drivetrain Mounts

- [ ] **Engine Mounts (×2)** — Replace both fluid-filled mounts. Collapsed mounts cause idle vibration and allow excess engine movement.
- [ ] **Transmission Mount** — See section F above.

### Instructions
*TODO: Add mount part numbers, jack placement points, and torque specs.*

---

## I. Electrical Baseline

- [ ] **Battery Health Test** — Test CCA and internal resistance. Options: Owon HDS242 scope cranking test (2V/div, 1s/div, single-shot at 11V) or free Motonet counter test. Battery is Varta H3 100Ah/890A (Aug 2025), experienced one deep discharge. Target: >10V during cranking, <25 mΩ internal resistance. **Still pending as of 2026-04-02.**
- [ ] **Alternator Output** — Verify 13.8–14.4V at idle with loads on. Check for AC ripple (indicates failing diodes).
- [ ] **All Exterior Lights** — Walk-around test: headlights (low/high), fog lights, turn signals, brake lights, reverse lights, license plate lights, side markers.
- [ ] **Fuse Box Inspection** — Replace all trunk F20 torpedo fuses with fresh copper/ceramic units. Replace fuse 6 (8A, blown) first and test PSE + antenna. Need full assortment: 8A ×2, 16A ×3, 25A ×1 (+ spares). Inspect underhood and interior fuse boxes for corrosion, melted terminals, and incorrect ratings.
- [ ] **Full X11/4 Blink-Code Diagnostic Sweep** — After trunk fuse 6 is replaced (powers ATA/IRCL?), run all diagnostic pins: 7 (RB), 8 (DI/EZL), 9 (ADS), 10 (RST), 11 (ATA), 12 (IRCL), 14 (ESMC). Record all codes. The March "dead ATA/IRCL" diagnosis may have been caused by unpowered modules (blown fuse 6).
- [ ] **Front Grille** — Clean and polish with Autosol Metal Polish (on hand). Cosmetic.

### Instructions
*TODO: Add fuse box diagrams, bulb specs, and alternator bench-test procedure.*

---

## J. Vacuum System

- [ ] **Vacuum Lines** — The M119 KE-Jetronic relies heavily on vacuum. Inspect all rubber vacuum lines for cracks and hardening. Replace any brittle lines with silicone vacuum hose.
- [ ] **Idle Speed Check** — After addressing vacuum leaks (including intake hoses), verify idle speed settles at ~650–700 RPM in Drive with A/C off.

### Instructions
*TODO: Add vacuum line routing diagram, idle speed adjustment screw location, and target vacuum reading at idle.*

---

## K. Rubber, Seals & Weatherstripping

- [ ] **Door Seals** — Inspect and treat with rubber conditioner (Gummi Pflege). Check for tears or compression set.
- [ ] **Soft Top Seals** — Inspect the roof seals and rear window seal for leaks and hardening. Treat with conditioner.
- [ ] **Trunk Seal** — Inspect (water ingress to the trunk is common on R129s and can damage the PSE pump area).

### Instructions
*TODO: Add seal part numbers, conditioner product recommendations, and water leak test procedure.*

---

## L. Under-Car Visual Inspection

- [ ] **Exhaust System** — Inspect for rust-through, loose hangers, and leaks. Pay attention to the flex joints and catalyst connections.
- [ ] **Fluid Leaks** — Put clean cardboard under the car overnight. Map any drips (oil, ATF, PS fluid, coolant).
- [ ] **Underbody Rust** — Inspect floor pans, subframe, and rear wheel arches for corrosion.

### Instructions
*TODO: Add known rust-prone areas for R129, recommended rust treatment products, and exhaust hanger locations.*

---

## Related Work Items

* **[How to Safely Lift the R129 (Jacking Instructions)](Jacking_Instructions.md)**
* Air Intake Hoses & Engine Air Filters → [Active Tasks #6](../../docs/tasks.md)
* Power Steering Flush & Filter → [Active Tasks #6](../../docs/tasks.md)
* Engine Mounts & Steering Damper → [Master Plan Phase 4](../../docs/R129%20Master%20Plan.md)
* Suspension Refresh (LCA, Links, Bushings) → [Active Tasks #4](../../docs/tasks.md)
* ADS Diagnostics → [ADS Blink-Code Reader](../ads_blink_reader/README.md)
* PSE Central Locking → [PSE Project](../pse_central_locking/README.md)

## Parts List

*TODO: Consolidate all parts with MB part numbers, quantities, and sourcing (MB-osat, Autodoc.fi, Kärkkäinen/Motonet).*

## Service Log

*Record completed items here with date, mileage, and notes.*

| Date | Section | Item | Notes |
| :--- | :--- | :--- | :--- |
| 2026-04-05 | B | Spark plugs replaced ×8 | NGK BCP5ES 7496, 22 Nm. Old plugs were Bosch, all loose, 6/8 wells oily. |
| 2026-04-05 | B | Distributor caps & rotors inspected ×2 | Serviceable — no tracking, no cracks. Replace during valve cover service. |
| 2026-04-04 | I | All torpedo fuses replaced | Front + trunk F20, fresh ceramic. All aluminum fuses retired. |
| 2026-04-04 | I | Full X11/4 diagnostic sweep | Pin 8 Code 17 active (crank sensor). All others clean or expected. |
| 2026-04-04 | — | Power steering flush | 5-6 cycles Febi 08972, new MANN H 85 filter. Fluid clear. |
