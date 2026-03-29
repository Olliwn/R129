# Center Console Refresh — Wood Polish, Switch Cleaning & Cable Routing

## Overview
The R129's center console Zebrano/Burl Walnut wood trim panels are original and in decent cosmetic condition but would benefit from a proper removal, cleaning, polishing, and re-clear-coating. At the same time, the console switches (soft-top, hazard, seat heater, etc.) all function electrically but feel "sticky" and lack the crisp tactile click of new switches — 35 years of dust, skin oils, and nicotine residue accumulating around the rocker mechanisms.

This project combines three objectives into a single console disassembly:

1. **Wood Trim Removal & Polish** — Remove all center console wood panels, clean, polish, and optionally re-lacquer/clear-coat on the bench.
2. **Switch Refresh** — Remove, disassemble, clean, and re-lubricate all center console switches to restore crisp tactile feel.
3. **RPi5 Cable Routing** — While the console is apart, route all cables for the RPi5 infotainment system (AUX from BE2210, CAT6 for Alps joystick from ashtray, display cable, 5V power) in a clean hidden loom behind the trim. *(See: [UI_rpi5/radio_uiknob.md](../../UI_rpi5/radio_uiknob.md))*

## Motivation
- The cubby lid above the radio slot needs to be removed permanently for the RPi5/OLED installation. Removing the wood trim gives full access to the void behind the center stack — the only reliable way to confirm cable routing paths and drill neat grommet holes through the plastic dividers if needed.
- Polishing the wood on the bench (not in-situ) avoids getting polish compound on the dashboard leather and climate control unit.
- Switch cleaning is only practical with the panels removed — the switches clip into the wood/plastic from behind.

## Switches on the Center Console
*All switches on the R129 center console are rocker-type, illuminated, and clip into rectangular cutouts in the wood trim or plastic surround. They are mechanically simple (spring + rocker contact) and can be cleaned without replacement.*

| Switch | Location | Status | Notes |
| :--- | :--- | :--- | :--- |
| ADS Sport/Comfort | Center console, below radio | Working (LED ok) | Feels slightly mushy |
| Hazard Warning (triangle) | Center console | Working | OK feel |
| Rear Window Defroster | Center console | Working | Slightly sticky |
| Seat Heater L | Center console | TBD | Not yet tested |
| Seat Heater R | Center console | TBD | Not yet tested |
| Soft-Top (roof) | Center console, upper right | Working | OK feel |
| ESP/ASR Off (if present) | Center console | TBD | Verify if equipped |

## Parts & Materials

### Wood Polish & Protection
* **Furniture polish / wood cleaner** — for initial cleaning (e.g., Howard Feed-N-Wax or similar beeswax-based product for lacquered wood)
* **Microfiber cloths** — lint-free, for polishing
* **Clear lacquer / polyurethane spray** — ONLY if the existing clear coat is visibly cracked, crazed, or worn through. If the existing finish is intact, do NOT re-lacquer — just clean and wax.
* **Fine-grit sandpaper (1500–2000)** — only if sanding is needed before re-lacquer (unlikely)

### Switch Cleaning
* **Contact cleaner (electrical)** — e.g., WD-40 Specialist Contact Cleaner or CRC QD Electronic Cleaner. Must be plastic-safe and residue-free.
* **Isopropyl alcohol (IPA) 99%** — for cleaning the switch housings and rocker mechanisms
* **Cotton swabs / small brushes** — for getting into the rocker pivot points
* **Silicone-free switch lubricant** — a tiny dab of dielectric grease or PTFE dry lubricant on the pivot points to restore the crisp "click" without attracting dust

### Cable Routing (RPi5 integration)
* **Tesa cloth tape (19mm, black)** — for period-correct loom wrapping
* **Rubber grommets (6–8mm)** — to protect cables where they pass through drilled holes in the plastic dividers
* **Cable ties (small, black)** — for securing the loom to existing harness clips

## Action Plan

### Phase 1: Documentation & Removal
- [ ] **1.1 — Photo-document everything** before touching it. Photograph every panel, every screw location, every clip position. The R129 trim clips are brittle and some may break — knowing exactly where they go is essential.
- [ ] **1.2 — Remove the cubby lid** (2–4 screws on the hinge mechanism). Set aside.
- [ ] **1.3 — Remove the radio** (pull BE2210 forward with DIN extraction keys, disconnect ISO + antenna).
- [ ] **1.4 — Remove the center console wood panels.** The R129 console wood is held by a combination of:
  - Phillips screws (hidden behind rubber grommets or at panel edges)
  - Spring clips that push into the plastic frame
  - Gentle prying with plastic trim tools — start from the bottom and work up. Do NOT use metal tools on the wood.
- [ ] **1.5 — Disconnect and label all switch connectors** as you remove each panel. Use masking tape + marker to label every connector (e.g., "ADS SW", "HAZARD", "SEAT HTR L").
- [ ] **1.6 — Remove switches from the panels.** Most R129 console switches unclip from behind (squeeze two side tabs and push through). Note orientation.

### Phase 2: Wood Cleaning & Polish
- [ ] **2.1 — Inspect the clear coat.** If the lacquer is intact and just dull/dirty, skip sanding — go straight to cleaning and waxing. If it's cracked, crazed, or peeling, it needs stripping and re-application (bigger job — scope separately).
- [ ] **2.2 — Clean.** Wipe each panel with a damp microfiber (water + mild soap). Remove all accumulated grime, especially around switch cutouts and clip holes.
- [ ] **2.3 — Polish / Wax.** Apply a thin coat of beeswax-based wood polish (e.g., Howard Feed-N-Wax). Buff with a clean microfiber. This restores depth and protects the existing finish.
- [ ] **2.4 — Set aside to cure.** Let the wax fully absorb/dry before handling or reinstalling.

### Phase 3: Switch Cleaning & Refresh
- [ ] **3.1 — Blow out loose debris.** Use compressed air to blast dust out of each switch housing.
- [ ] **3.2 — Clean the rocker mechanism.** Spray contact cleaner into the switch body (through the rocker gap). Work the rocker back and forth 20–30 times to flush out grime. Let dry completely.
- [ ] **3.3 — Clean the housing exterior.** Wipe the plastic housing with IPA and cotton swabs. Clean the illumination window and any printed symbols.
- [ ] **3.4 — Lubricate pivot points.** Apply a tiny amount of PTFE dry lube or dielectric grease to the rocker pivot pins. Work the switch — it should feel crisp and positive, with a clean "click."
- [ ] **3.5 — Test continuity.** Before reinstalling, use a multimeter in continuity mode to verify each switch makes and breaks cleanly.

### Phase 4: Cable Routing (RPi5 Infotainment)
- [ ] **4.1 — Survey the void.** With the trim removed, photograph and map the space behind the center stack. Identify existing factory harness routing clips and any pass-throughs between the DIN cavity, cubby void, and ashtray channel.
- [ ] **4.2 — Drill grommet holes (if needed).** If the plastic divider between the DIN slot and cubby has no existing pass-through, drill a neat 8mm hole at the rear of the divider. Install a rubber grommet.
- [ ] **4.3 — Route cables:**
  - **AUX cable** (3.5mm): From BE2210 rear AUX jack → up through divider → into cubby (RPi5 DAC input)
  - **CAT6** (Alps joystick GPIO): From ashtray void → down through cigarette lighter channel → up behind console → into cubby
  - **Display cable** (HDMI or DSI ribbon): Internal to cubby (short run from RPi5 to OLED)
  - **5V power**: From ignition-switched source → into cubby (for RPi5 + display)
- [ ] **4.4 — Wrap the loom.** Bundle all cables with Tesa cloth tape to match the factory harness aesthetic. Secure to existing harness clips with black cable ties.

### Phase 5: Reassembly
- [ ] **5.1 — Reinstall switches** into the wood panels (clip from behind, correct orientation).
- [ ] **5.2 — Reconnect all switch harnesses** (use the labels from Phase 1.5).
- [ ] **5.3 — Reinstall wood panels.** Replace any broken clips with new ones (source: Biltema universal trim clips or MB-specific). Screws finger-tight — do not overtorque into plastic.
- [ ] **5.4 — Reinstall BE2210** with AUX cable connected to rear jack.
- [ ] **5.5 — Functional test.** Verify every switch works (ADS, hazard, defroster, seat heaters, soft-top). Verify radio powers on and AUX input is routed.

## Work Log
| Date | Status | Notes |
| :--- | :--- | :--- |
| 2026-03-28 | Planned | Project created. Combines wood refresh, switch cleaning, and RPi5 cable routing into a single console disassembly. |
