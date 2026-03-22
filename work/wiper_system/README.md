# Windshield Wiper & Washer System Investigation

## Overview
The windshield wiper and washer system on the 1991 Mercedes-Benz 500 SL (R129) is functioning but exhibits two specific faults: the wiper blade does not park in the correct resting position when turned off, and the windshield washer fluid only sprays from 1 or 2 of the 4 available nozzles. The wiper mechanism is the iconic Mercedes "mono-wiper" (eccentric jumping wiper), which requires specific maintenance to operate smoothly.

## Symptoms
- **Wiper Parking Issue:** The windshield wiper operates but stops at random positions on the glass rather than returning to the designated horizontal park position.
- **Washer Fluid Issue:** Fluid is successfully pumped, but only sprays out of 1 or 2 nozzles (out of 4 total), indicating clogs or line restrictions.

## Known Architecture
- **Mono-Wiper Mechanism:** A complex eccentric gear system that physically extends and retracts the wiper arm as it sweeps to cover maximum glass area. It resides under a plastic "turtle shell" cover at the base of the windshield.
- **N10 Combination Relay:** A multi-function relay (located in the rear engine bay module box) that controls wiper intervals, turn signals, and rear window defroster. It works in tandem with internal park-detection contacts inside the wiper motor.
- **Washer System:** Fluid reservoir (passenger side front) with an electric pump. The lines run up to the hood where two nozzle assemblies (each with two jets) are mounted. The fluid is electrically heated in some models.

## Diagnostic Steps / Action Plan

### Phase 1: Washer System (Quick Fixes)
- [ ] **1.1 — Inspect and Unclog Nozzles**
  - Locate the 4 washer nozzles on the hood.
  - Use a fine needle, sewing pin, or specific nozzle-cleaning tool to clear any wax, dirt, or mineral buildup from the nozzle orifices.
  - Test spray pattern. If fixed, carefully adjust the spray aim using the needle so it hits the center-upper part of the windshield.
- [ ] **1.2 — Inspect Fluid Lines**
  - Open the hood and trace the rubber fluid lines from the reservoir pump to the nozzles.
  - Look for pinched lines, cracked brittle rubber, or disconnected T-splitters.
  - *Note:* If the lines are extremely hard/brittle, order silicone replacement tubing.

### Phase 2: Wiper Mechanism Lubrication (Crucial Maintenance)
- [ ] **2.1 — Remove the Wiper Assembly**
  - *Note:* Unlike the W124 which has a plastic "turtle shell" that clips off from the top, the R129 wiper mechanism is housed in a solid metal casing. The Allen bolt at the base only removes the wiper arm itself. To fully access the internal eccentric gears, the **entire wiper assembly must be removed from the car**.
  - Raise the hood to the full vertical/perpendicular service position using the latches on the hood hinges.
  - Pull off the rubber weatherstripping/seal that runs across the cowl (separating the engine bay from the windshield area).
  - Carefully lift and remove the plastic water deflector panels covering the cowl.
  - Unplug the electrical connector for the wiper motor.
  - Unbolt the main wiper mounting bracket from the firewall/bulkhead (usually held by nuts/bolts requiring a socket set and a 5mm Allen).
  - Carefully maneuver the entire wiper motor and linkage assembly out of the vehicle.
- [ ] **2.2 — Clean and Lubricate (On the Bench)**
  - With the assembly removed, turn it over and unscrew the metal cover plate on the back (typically held by Phillips screws).
  - Clean out all old, hardened grease from the large main gear, transmission, and sliding track using brake cleaner.
  - Liberally apply fresh lithium grease or MB multi-purpose grease to the gear teeth and sliding rod.
  - Reassemble the plate and cycle the mechanism by hand to ensure smooth operation before reinstalling.
  - *Why this matters:* A binding dry mechanism creates huge resistance, which can confuse the motor's parking circuitry or cause the N10 relay to drop out early due to high current draw.

### Phase 3: Parking Circuit Diagnostics
If lubricating the mechanism doesn't fix the parking issue:
- [ ] **3.1 — Check Wiper Linkage Alignment**
  - Verify that the main nut holding the wiper linkage to the motor shaft hasn't slipped. If it slips, the motor's internal "park" position no longer matches the physical park position.
- [ ] **3.2 — N10 Combination Relay Inspection**
  - Locate the N10 combination relay in the main fuse/relay box (rear left of engine bay).
  - Pull the relay and inspect the pins for corrosion.
  - *Advanced:* Carefully pop the plastic cover off the N10 relay and inspect the internal circuit board for cracked solder joints (extremely common on R129/W124). Reflow any suspect joints with a soldering iron.
- [ ] **3.3 — Wiper Motor Internal Contacts**
  - If the N10 relay is perfect, the internal copper contact ring inside the wiper motor assembly may be dirty, worn, or coated in old grease, preventing it from signaling the "park" position. Requires removing the motor cover to clean.

## Parts & Tools Needed

| Item | Purpose | Status |
| :--- | :--- | :--- |
| Sewing pin / Nozzle cleaning tool | Unclogging washer jets | Needed |
| Lithium grease (White) | Lubricating eccentric mechanism | Needed |
| Allen key set (Metric) | Removing turtle shell cover | Acquired ✓ |
| Soldering iron & solder | Reflowing N10 relay (if needed) | Needed |
| T-splitters / Silicone tubing | Replacing cracked washer lines | Monitor |

## Related Work Items
- Engineering Diary Task #1 & #2 → [docs/AOK912 Engineering Diary.md](../../docs/AOK912%20Engineering%20Diary.md)
- Baseline Service (Vacuum / Rubber Lines) → [work/baseline_service/](../baseline_service/README.md)

## Diagnostic Log
*Record findings and completed steps here.*

| Date | Step | Finding | Action |
| :--- | :--- | :--- | :--- |
| 2026-03-15 | — | Initial observation on transit | Noticed poor spray pattern, erratic parking |
| | | | |
