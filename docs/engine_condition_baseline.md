# AOK912 — Engine Condition Baseline

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: `WDB 129066 1F 044414`
**Engine:** M119.960 V8 4 973 cc, KE-Jetronic, built **1991-09**, serial `119960 12 024990`

*This is a rolling record of **affirmative engine-health data points** — evidence that the engine is in good condition. Problems go in [known_issues.md](known_issues.md); this file is the counterbalance. The purpose is to prevent "unknown history" from silently becoming "assumed worn V8" as the file history grows. Each entry should be datable, reproducible, and ideally quantitative.*

---

## Executive Summary (2026-04-18)

Based on observations through 2026-04-18, the M119.960 internals are **cautiously healthy**. Bottom end shows no evidence of significant blowby, fuel dilution, coolant intrusion, or abnormal wear. Historical varnish in the valvetrain area is pre-purchase deposit, not current-oil product. Oiler tubes likely factory aluminum (the robust early-M119 spec), pending tap/wipe confirmation.

**Confidence level:** medium. We have multiple consistent indirect positive signals but no direct internal measurement (no compression test, no leakdown, no UOA yet).

**Next confidence upgrade:** used-oil analysis at the next oil change.

---

## Evidence Log

### 2026-04-18 — Oil Condition After 1 800 km of Owner Driving

**Observation.** Dipstick pull at overnight-cold engine, photographed against white paper towel under overhead fluorescent lighting. Oil appears **light honey amber, fully translucent, free-flowing, no sediment, no cloudiness**. Paper-towel absorbed spots are pale golden-yellow and see-through.

**Owner-claimed mileage on this oil fill:** ~1 800 km since purchase (Sweden → Kapellskär ferry + Vellinge→Kapellskär transit + Finnish registration + local Oulu driving).

**No oil added** in that period (no top-up).

**Interpretation.**

| Indicator | Reading | What it rules in / rules out |
| :--- | :--- | :--- |
| Translucency + pale color after 1 800 km | Better than typical | Low blowby — combustion gases (CO₂, soot, unburned HC) not significantly entering crankcase. Implies intact ring seal and bore condition. |
| No darkening | Better than typical | No fuel dilution from KE-Jetronic running rich; no excessive soot from cold-start enrichment lingering. |
| No milkiness or emulsification | Normal | No coolant intrusion (head gasket intact; no cracked head; no oil cooler cross-contamination). |
| No free particulate visible | Normal | No gross wear products suspended in oil (doesn't rule out fine metallic wear — UOA needed). |
| No oil consumption over 1 800 km | Better than typical | Good ring + valve stem seal condition; consistent with the no-blowby signal. |

**Reclassification.** Engine internals move from **"unknown"** to **"cautiously healthy"**. This is the first affirmative engine-health data point recorded for this vehicle.

**Caveats.**

- Single observation. A UOA would give quantitative wear-metal data and directly validate the low-blowby hypothesis.
- The "1 800 km" figure is owner-recalled; the next oil change should anchor km count to a recorded odometer reading (baseline to be captured Apr 19 morning).
- Previous-owner oil brand/grade is unknown. The dipstick color is consistent with modern full-synthetic 0W-40 / 5W-40, but we can't be certain the oil type is what we'd have chosen.

**Photo reference.** See diary `docs/diary/2026-04.md` Apr 18 evening entry.

---

### 2026-04-18 — Valvetrain Varnish (Observational — Note, Not a Problem)

**Observation.** LED flashlight inspection down the oil filler neck shows heavy orange-amber gum coating the filler neck interior, cam bearing area, and surrounding head surfaces. Deposits are thick, uniform, and clearly not of recent-oil origin (fresh oil would not produce this volume in 1 800 km).

**Interpretation.** Historical deposit, accumulated over decades of prior-owner operation with unknown oil-change discipline. Common on any 30+ year-old engine not run on modern detergent synthetic throughout its life.

**Not a health concern.** Varnish does not impede oil flow in passages, doesn't increase friction, doesn't affect sealing. It's cosmetic/historical. Modern synthetic oil slowly dissolves it back into solution across many oil changes — each subsequent drain will be a shade darker than otherwise expected as the valvetrain self-cleans.

**Not taking action.** No engine flush additive (Liqui Moly Motor Clean, Kleen Neutra, etc.) — risk of liberating debris and clogging oil pump pickup screen on an engine with unknown sump cleanliness. Let modern oil do the slow work.

---

### 2026-04-18 — M119 Oiler Tube Material (Pending Confirmation)

**Observation.** Same filler-hole inspection shows a horizontal silver/matte cylindrical object consistent in geometry with the M119 oiler tube sitting above the camshaft.

**Hypothesis.** The tube is **factory aluminum** (P/N 119 187 00 87) — the robust early-M119 spec used through ~1992 production. AOK912's 1991-09 build is firmly in the aluminum-tube era. The later plastic variant (P/N 119 180 02 66, ~1993 onward) would show matte black, not silver.

**Pending confirmation.** Tap/wipe test on Apr 19 morning:

- Tap test: long chopstick or pick, gentle contact on tube. Metal *ping* = aluminum; plastic *thud* = replacement.
- Wipe test: rag on long tool, press and rotate. Silver streak wiping through varnish = aluminum confirmed; dark/matte under varnish = plastic.

**Implication if confirmed aluminum.** Priority 2 upper-timing service (`work/m119_upper_timing/README.md`) is fully unblocked on the oiler-tube question. Scope reduces to valve cover gaskets + timing slide rails + spark plug tube seals + spark plugs + breather hose. No tube replacement, no retainer upgrade.

---

## Supporting Observations (from Prior Diary Entries — Included for Consolidation)

### Cranking Behavior (2026-04-03)

- Owon HDS242 cranking waveform at battery terminals showed ~4 V dip from ~12.4 V to ~8.5 V during cranking at 3 °C ambient. Engine caught immediately.
- **8.5 V is the battery dip, not a starter/engine signal** — the battery had 67 mΩ DC impedance (sulfated). On the new battery (installed 2026-04-18) the dip is expected to recover to ~10.5–11 V at similar ambient.
- Short crank duration is an indirect positive signal: engine fires on the first compression event, suggesting good compression, good fuel delivery (KE-Jetronic), and good spark.

### Idle Quality (2026-04-02)

- First real drive post-OVP-fix. Engine idled smoothly at ~700–800 RPM.
- Slight vibration at low idle attributed to engine mounts (Corteco replacements on hand, awaiting install — tracked as Engine Mounts known issue).
- No reported misfire, no stumbling, no hunting.

### Spark Plug Electrode Condition (2026-04-05)

- All 8 NGK BCP5ES plugs removed during spark plug replacement showed **clean tan/brown electrode tips** — no oil fouling on the firing surfaces, no black carbon deposits, no aluminum deposits (pre-ignition), no white glazing (lean).
- **Combustion chambers are therefore healthy across all 8 cylinders.** Oil in 6 of 8 spark plug wells is external-only (tube seal leakage), not internal combustion contamination.
- Clean electrodes are consistent with the low-blowby signal from oil condition.

### Coolant System (post-2026-04-01)

- No reports of overheat, pressure-cap release, or coolant loss during the ~1 800 km post-purchase driving period.
- Coolant fresh (Motox Classic G11 topped up March 2026).
- Supports "no head gasket issue" hypothesis from the dipstick-no-milkiness observation.

### Oil Pressure (Inference)

- R129 500 SL cluster has an oil pressure gauge (0–3 bar range typically).
- No owner-reported abnormal behavior (rapid drops, hunting needle, low-at-idle warnings).
- Inferred: oil pump, pickup screen, and bearing clearances are within spec. No direct measurement of oil pressure to factory spec at known RPM / oil temp has been done — this could be logged in a later entry if an aftermarket gauge is plumbed in.

---

## What Would Strengthen This Baseline

| Test | Confidence add | Cost | When |
| :--- | :--- | :--- | :--- |
| **Used-oil analysis (Oelcheck DE)** | High — quantitative Fe/Al/Cu/Pb/Si, fuel %, coolant %, viscosity, TBN | ~€30–40 | Next oil change |
| **Oil filter cut + visual** | High — catches anything the drain stream leaves behind | €0 (just tin snips + loupe) | Next oil change |
| **Compression test** (all 8 cylinders) | High — direct ring seal measurement | €0 with existing tools + hot-engine session | Any time spark plugs are out |
| **Leakdown test** (all 8 cylinders) | Very high — discriminates rings from valves from head gasket | Need leakdown gauge (~€80–150) | Any time spark plugs are out, engine at TDC per cylinder |
| **Oil pressure measurement** at 2 000 RPM / 80 °C at a tap near the filter housing | Medium — validates pump + bearings | Need mechanical gauge + T-fitting | During an upcoming service |
| **Valve cover off inspection** | High — direct visual of cams, lobes, lifters, chain, oiler tubes | Free (already planned Priority 2) | Scheduled |

**Recommended next:** UOA at next oil change is the highest-value, lowest-effort upgrade. Compression test is worth doing the next time the spark plugs are out anyway — no incremental cost beyond 20 minutes of time.

---

## Oil Darkening Rate — Tracking Table (Empty, Populate Over Time)

Track the oil color at regular intervals to build a trend. Same paper towel, same lighting, same page of the diary.

| Date | Odometer | km since last change | Color | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-18 | *(record Apr 19 morning)* | ~1 800 (owner-claim) | Light honey amber, translucent | Baseline. Owner-claim km. |
| | | | | |
| | | | | |

Rule of thumb for this engine (to be calibrated as data comes in):
- Light honey → light brown over 500–1 000 km = healthy
- Light honey → medium brown over <500 km = check for fuel dilution or abnormal blowby
- Light honey → near-black over 500–1 000 km = serious investigation warranted

---

*Last updated: 2026-04-18.*
