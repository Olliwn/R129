# Baseline Service — Unknown History (Spring 2026)

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | **Engine:** M119.960 V8 (KE-Jetronic) | **Trans:** 722.3

No written service history exists for this vehicle. Assume all consumables and wear items are overdue. This checklist establishes a known-good baseline for reliability and longevity.

---

## A. Engine Oil & Filtration

- [ ] **Engine Oil & Filter Change** — Drain and refill with MB 229.5 spec fully-synthetic (e.g., Mobil 1 0W-40 or Liqui Moly 5W-40). Replace oil filter with **MANN H 829/1 x**. Capacity: ~8L.
- [ ] **Oil Filter Housing Cap** — Inspect the plastic cap for cracks when removing (requires 36mm socket). Replace if cracked.

### Instructions
*TODO: Add step-by-step procedure, torque specs, and drain plug washer part number.*

---

## B. Ignition System (M119 Twin-Distributor)

- [ ] **Spark Plugs** — Replace all 8 with **NGK BP5ES** non-resistor copper plugs. Gap to 0.8mm.
- [ ] **Distributor Caps & Rotors (×2)** — Inspect both left and right distributor caps and rotors for carbon tracking and corrosion. Clean or replace as needed.
- [ ] **Spark Plug Wires** — Inspect resistance (should be <10 kΩ per wire). Replace full set if any are out of spec or brittle.

### Instructions
*Note: The M119 KE-Jetronic requires non-resistor plugs because the factory plug wire boots already contain resistors. Using resistor plugs (like Bosch FR8DC+) will cause a weak spark and rough idle.*
*TODO: Add firing order, distributor cap orientation marks, and torque specs for spark plugs.*

---

## C. Fuel System

- [ ] **Fuel Filter** — Replace the inline fuel filter (located under the car, passenger side) with **MANN WK 830/3**.
- [ ] **Fuel Accumulator** — Inspect (holds residual pressure for hot restart). If hard-start when hot, replace.

### Instructions
*TODO: Add fuel filter location diagram, line depressurization procedure, and flow direction arrow.*

---

## D. Drive Belts

- [ ] **Serpentine / V-Belts** — Inspect all belts for cracking, glazing, and tension. The M119 uses multiple V-belts (not a single serpentine). Replace the full set if age/condition is unknown.
- [ ] **Belt Tensioners & Idler Pulleys** — Check for bearing play/noise. Replace any that are rough.

### Instructions
*TODO: Add belt routing diagram, belt part numbers, and tension specs.*

---

## E. Cooling System

- [ ] **Full Coolant Flush** — Drain, flush, and refill with MB 325.0 spec (Glysantin G48, 50/50 mix).
- [ ] **Thermostat** — Replace (known M119 failure point, causes overcooling or overheating). OEM temp: 80°C.
- [ ] **Coolant Hoses** — Inspect all rubber hoses for swelling, cracking, and softness. Replace any suspect hoses (prioritize the lower radiator hose and heater hoses).
- [ ] **Radiator Cap** — Replace (cheap insurance; a weak cap lowers boiling point).

### Instructions
*TODO: Add drain plug locations, thermostat housing torque, bleed procedure, and coolant capacity.*

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

- [ ] **Battery** — Test CCA and internal resistance. Replace if marginal (Nordic winters are brutal on old batteries).
- [ ] **Alternator Output** — Verify 13.8–14.4V at idle with loads on. Check for AC ripple (indicates failing diodes).
- [ ] **All Exterior Lights** — Walk-around test: headlights (low/high), fog lights, turn signals, brake lights, reverse lights, license plate lights, side markers.
- [ ] **Fuse Box Inspection** — Open both fuse boxes (underhood + interior). Inspect for corrosion, melted terminals, and incorrect fuse ratings.

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
* Air Intake Hoses & Engine Air Filters → [Engineering Diary Task #6](../../docs/AOK912%20Engineering%20Diary.md)
* Power Steering Flush & Filter → [Engineering Diary Task #6](../../docs/AOK912%20Engineering%20Diary.md)
* Engine Mounts & Steering Damper → [Master Plan Phase 4](../../docs/R129%20Master%20Plan.md)
* Suspension Refresh (LCA, Links, Bushings) → [Engineering Diary Task #4](../../docs/AOK912%20Engineering%20Diary.md)
* ADS Diagnostics → [ADS Blink-Code Reader](../ads_blink_reader/README.md)
* PSE Central Locking → [PSE Project](../pse_central_locking/README.md)

## Parts List

*TODO: Consolidate all parts with MB part numbers, quantities, and sourcing (MB-osat, Autodoc.fi, Kärkkäinen/Motonet).*

## Service Log

*Record completed items here with date, mileage, and notes.*

| Date | Section | Item | Notes |
| :--- | :--- | :--- | :--- |
| | | | |
