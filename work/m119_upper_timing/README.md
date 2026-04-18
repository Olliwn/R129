# M119 Upper Timing Components & Lubrication System Inspection

## Service Bulletin

**Vehicle:** 1991 Mercedes-Benz R129 500SL (M119.960 V8 with KE-Jetronic)

**Objective:** Preventive maintenance of the timing chain guides and upgrade of the camshaft oil bridge clips to aluminum versions. This addresses two of the M119's best-known weak points: brittle plastic timing chain guides (which can shed debris into the oil system or allow chain skip) and the plastic oil bridge clips (which loosen over time and starve the cam lobes of oil, causing lobe pitting/scoring).

**Priority:** HIGH — These are age-related, non-symptomatic failure modes. By the time symptoms appear (chain rattle, cam tick, low oil pressure at idle), damage is already done. Preventive inspection while the valve covers are off for the baseline service is the correct approach.

## Phase 1: Preparation & Disassembly

- **1.1 — Degrease valve cover area.** Thoroughly degrease the entire top of the engine around both valve covers. Any debris that falls into the open valvetrain will end up in the oil galleries and eventually the bearings.
- **1.2 — Remove spark plug covers, ignition wires, and breather hoses.** Label left/right bank wires to avoid swapping firing order on reassembly. Photograph the routing.
- **1.3 — Remove valve covers.** Loosen bolts in a cross-pattern (outside-in). Carefully lift the covers straight up to avoid damaging the mating surfaces. The M119 valve covers are magnesium/aluminum — they are fragile and warp easily if pried against.
- **1.4 — Replace spark plugs.** New NGK BP5ES plugs are already on hand (ordered 2026-03-22). Before discarding the old plugs, **inspect them as a KE-Jetronic health check:**
  - Tan/light grey electrode = healthy mixture
  - Sooty black = running rich (EHA current too high, O2 sensor, or leaking injector)
  - White/blistered = running lean (vacuum leak, fuel pressure regulator, or clogged injector)
  - Oily/wet = oil consumption (valve stem seals or piston rings)
  - Compare left bank vs. right bank — asymmetry points to a bank-specific issue.

## Phase 2: Inspection & Replacement

### Timing Chain Guides

- **2.1 — Inspect upper timing chain guides.** The plastic guides are located between the camshaft sprockets (one slide rail and one or two U-shaped tensioner guides per bank, depending on M119 sub-version).
  - **Pass criteria:** Plastic is light brown/amber, flexible, with no cracks, chips, or missing material.
  - **Fail criteria:** Plastic is dark brown/black, brittle, cracked, or has chunks missing. **Replace immediately** — broken guide fragments circulate through the oil system and can block oil galleries.
- **2.2 — Inspect timing chain.** While visible, check chain for excessive slack, stiff links, or discoloration. A stretched chain with worn guides = full timing chain job (much bigger scope — would be a separate work item).

### Camshaft Oil Tubes (Oilers)

**IMPORTANT — PART HISTORY CORRECTION (2026-04-18):** Earlier versions of this plan recommended "upgrading plastic oil bridges to aluminum" via URO Parts. That framing was wrong for this car. The correct history:

| Era | Part number | Material | Notes |
| :--- | :--- | :--- | :--- |
| ~1989 – ~1992 (AOK912's build: 1991-09) | **119 180 00 87 / 119 187 00 87** | **Factory aluminum** | Original design. Known to hold up well. |
| ~1993 onward | 119 180 02 66 | Plastic | Cost-reduction swap. This is the part prone to aging/loosening and causing the reputation issue. |

AOK912 (engine 119960 12 024990, built 1991-09, one of the earliest R129 500 SLs) should have **factory aluminum oiler tubes already installed.** There is likely nothing to "upgrade." The job becomes *inspect and leave alone*, not *replace with aftermarket*.

**URO 1191800266PRM (the earlier recommendation):** mixed European reception. Per BenzWorld/PeachParts: variable casting quality, rubber/O-ring components viewed skeptically. On a car with original factory aluminum tubes, there is no benefit to swapping to URO. Reserved as a last-resort only if the factory tubes are somehow found degraded and no used OEM 119 187 00 87 can be sourced.

- **2.3 — Non-invasive pre-inspection via oil filler hole.** *Do this BEFORE scheduling the valve-cover-off job.* Remove the engine oil filler cap and shine a bright LED flashlight (or small borescope, e.g. Bosch GIC 120 / cheap USB endoscope) down the neck. The top of one camshaft and a portion of the oiler tube are visible.
  - What to confirm: **material colour/finish of the oiler tube** — factory aluminum = dull matte silver, possibly with light oil film; plastic = ivory/cream or black.
  - Look for tube retention — tube should sit stationary against its mounts, no visible lateral shift, no fractured retainers.
  - Document with a phone photo through the oil filler hole for the diary.
  - **Outcome tree:**
    - If factory aluminum, intact → no tube replacement, no retainer upgrade needed. Priority 2 job proceeds with gaskets + slide rails only. This likely applies to AOK912.
    - If factory aluminum, visibly shifted or retainer broken → source a used OEM set P/N 119 187 00 87 (eBay Germany, R129 breakers, or ask MB-osat).
    - If plastic (unexpected — would imply a prior engine swap or post-warranty repair) → same sourcing path: used OEM aluminum 119 187 00 87 preferred over new URO.
- **2.4 — Valve-cover-off inspection (only if the non-invasive inspection is inconclusive, or as part of the scheduled gasket job).** With the valve cover off, check tube seating, any O-ring weepage, and retainer integrity directly.

### Camshaft Lobe Inspection

- **2.5 — Visually inspect all cam lobes.** With the valve covers off and the oil bridges removed for clip replacement, each cam lobe is fully visible. Slowly rotate the engine by hand (27mm socket on the crankshaft bolt) and inspect every lobe on both banks.
  - **Pass:** Smooth, mirror-finish lobes with no pitting or scoring.
  - **Fail:** Visible pitting (small craters), scoring (linear scratches), or material loss on the lobe tip. If found, this indicates historical oil starvation from the loose plastic clips. Mild pitting can be monitored; severe pitting/scoring requires camshaft replacement (major job — separate work item).

## Phase 3: Reassembly

- **3.1 — Clean mating surfaces.** Wipe both the cylinder head rail and the valve cover mating flange with brake cleaner on a lint-free cloth. Remove all old gasket material. The surfaces must be perfectly clean and dry for the new gaskets to seal.
- **3.2 — Install new valve cover gaskets.** Press new gaskets into the valve cover grooves (they should seat without adhesive). Ensure the spark plug hole seals are correctly seated — a leaking plug hole seal allows oil to pool around the spark plug, causing misfires.
- **3.3 — Reinstall valve covers.** Lower straight down. Tighten bolts in a cross-pattern to **9 Nm**. Do NOT overtighten — the M119 covers are thin-walled magnesium/aluminum castings and will crack or warp, creating a permanent oil leak.
- **3.4 — Reinstall breather hoses, ignition wires, and spark plug covers.** Verify correct wire routing (left/right bank, firing order). Install new breather hose if the old one shows any cracking.
- **3.5 — Start engine and check for leaks.** Let the engine reach operating temperature. Inspect both valve cover perimeters and spark plug wells for oil weepage. Re-torque to 9 Nm after the first heat cycle if needed.

## Required Parts & Part Numbers


| Part Description                   | Part Number (MB OEM / Ref) | Qty   | Notes                                           |
| ---------------------------------- | -------------------------- | ----- | ----------------------------------------------- |
| Valve Cover Gasket Set (Right)     | 119 010 03 30              | 1     | Includes spark plug hole seals                  |
| Valve Cover Gasket Set (Left)      | 119 010 04 30              | 1     | Includes spark plug hole seals                  |
| Upper Timing Chain Guide (Slide)   | 119 050 02 16              | 2     | Check fitment per VIN / sub-version             |
| Upper Timing Chain Guide (U-shape) | 119 052 09 16              | 1–2   | Depending on M119 sub-version                   |
| Camshaft Oiler Tubes (OEM aluminum, factory) | 119 187 00 87 (early) / 119 180 00 87 | 16 | **AOK912 (1991-09 build) almost certainly has these already fitted from factory.** Pre-inspect via the oil filler hole with a flashlight before sourcing anything. Only replace if inspection shows damage; then prefer used-OEM from R129 breakers over new URO aftermarket. |
| ~~Aluminum Camshaft Oiler Tubes (URO aftermarket)~~ | ~~URO 1191800266PRM (OEM: 119 180 02 66)~~ | — | **SUPERSEDED 2026-04-18.** Previous entry incorrectly assumed the car had the plastic post-1993 design. European forums report variable casting quality and skepticism of URO's rubber/O-ring components. Keep only as a last-resort fallback if factory aluminum is damaged AND no used-OEM 119 187 00 87 can be sourced. |
| Breather Hose (Crankcase)          | 119 094 03 82              | 1     | Old ones usually cracked — replace preventively |
| Spark Plugs (NGK BP5ES)            | —                          | 8     | Already on hand (ordered 2026-03-22)            |


## Sourcing Notes

- Valve cover gaskets and timing guides: Autodoc, MB-osat, or FCP Euro (OEM Elring or Victor Reinz preferred for gaskets).
- Camshaft oiler tubes: **inspect-first, likely no replacement needed.** AOK912 is a 1991-09 build — per BenzWorld/PeachParts, all M119s through ~1992 left the factory with aluminum oilers (P/N 119 187 00 87). Plastic tubes (P/N 119 180 02 66) only appear from ~1993 production onward. Do the oil-filler-hole inspection (Phase 2.3) before ordering anything. If replacement is somehow needed: used OEM aluminum 119 187 00 87 from German/NL R129 breakers is the preferred source. URO 1191800266PRM is a last-resort fallback only, due to European reports of variable casting quality and O-ring issues.
- Breather hose: Autodoc or MB-osat (OEM or URO Parts).

## Work Log


| Date       | Status  | Notes                                                                                                                                                           |
| ---------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-28 | Planned | Work item created. Scope: valve cover-off inspection of timing guides + oil bridge clip upgrade. Spark plugs already on hand. Gaskets and guides to be ordered. |


