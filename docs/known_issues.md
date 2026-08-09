# AOK912 -- Known Issues

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

*Current state of confirmed defects. History and investigation details are in the [monthly diaries](diary/). Detailed work plans are in the linked `work/` READMEs.*

---

## OPEN

### Head Unit Touch — Intermittent Dropout on Interim Display Mount
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-08-09

Touch works, but the digitiser's USB link is **mechanically unreliable while the panel is on its interim mount.** On 2026-08-09 it enumerated, ran for 61 s, then threw `usb 1-2: USB disconnect` with nothing touching it; re-seating every adapter brought it back and it has been stable since. Symptom while dropped is a lit, correctly-rendering panel with no touch at all — easily mistaken for a dead digitiser.

**Root cause is the adapter chain, not the panel or the software.** The panel, its touch controller, and the whole software path are proven good (see RESOLVED entry below for the verified stack). The interim setup daisy-chains a micro-USB cable through a 180° adapter with nothing taking strain, so vibration or a nudge parts the inner data pins while the outer power pins still contact.

**Fix:** manufacture the proper display-to-cubby-frame adapter so the panel is rigidly mounted and the USB tail is strain-relieved — tracked in `work/display_mount/README.md`. Until then, expect dropouts after any cabin work and re-seat the adapters first.

**Diagnostic:** `sudo dmesg | grep -iE "0712|usb 1-2"` shows the enumerate/disconnect history with timestamps; live-watch with `sudo dmesg -W | grep --line-buffered -iE "0712|Waveshare|disconnect"`. Triage recipe in `docs/RPi5_Bring-up_Plan.md` Step 6.

### ADS System (Suspension) -- Hydraulic/Mechanical Faults Remaining
**Status:** OPEN | **Priority:** HIGH | **Since:** 2026-03-13

Electrical side resolved:
- **OVP Root Cause Fixed (2026-04-01):** OVP relay 87L pin re-soldered. N51 module online, diagnostic bus stable. Only code 14 (steering calibration) present.

Damping side now working:
- **Adaptive Damping (N51):** Sport/Comfort modes CONFIRMED WORKING on first drive (2026-04-02). All four accumulator spheres healthy — inspector independently commented on smooth ride. Earlier FR stiffness was air-lock.

Level control still needs work:
- **Level Control (Niveauregulierung) — refined diagnosis 2026-04-19.** Rear height remains static. **Fahrzeugniveau switch electrical side RESOLVED:** LED now toggles on/off correctly with the center-console switch (observed during 2026-04-19 test drive, first normal switch behavior since Apr 2). Likely self-healed via new battery (Apr 18) + exercised contacts + ZH-M flush. **Hydraulic side still inoperative:** raise commands produce no observable ride-height change, so the rear-droop problem is now **confirmed hydraulic**, not electrical. Candidates: rear mechanical level valve (ARB linkage stuck/misadjusted), solenoid valve in manifold, weak pump discharge pressure, slow internal leak, or degraded rear sphere pre-charge. **Next:** manual valve test (disconnect ARB linkage, move lever by hand on jack stands), read Pin 9 immediately after a raise command, measure pump discharge pressure if manual valve test doesn't isolate the cause.
- **Cluster swap confirmed:** Indicator strip has no ADS symbol -- non-ADS cluster (option 216 factory ADS confirmed via lastvin.com).

✅ **Front ADS dust boots / bump stops — INSTALLED 2026-05-22 by MB-osat.** Sachs dust-boot + bump-stop kit (receipt line `SACHS SUOJAKUMI-POHJAANLYÖTI SRJ MB`, €44.00) fitted alongside the §4B steering/suspension work. The on-hand 2× MEYLE 014 032 0032 pair (arrived 2026-04-27) was *not* used — the Sachs kit is one-piece and was not splittable per the May 5 open question #4 — so the MEYLE pair is now surplus and parked as a future spare set / next-owner handover stock (€17 sunk cost, acceptable). Rear ADS dust boots remain intact per 2026-04-18 photograph.

Rear ride-height ripple in alignment data:
- **Wheel alignment 2026-05-22 (Ari Vuorela)** captured rear camber as L −2°35' / R −2°19' against the −2°00'/−1°00' spec (both out, more negative than allowed). R129 rear camber is geometry-fixed — no shims, no eccentrics — so this is a direct mechanical consequence of the still-low rear ride height. Will resolve **automatically** when the level-control hydraulic side does (no geometry adjustment available or needed). Plan: re-run alignment after the rear-droop hydraulic diagnosis closes.

[work/ads_diagnostic/README.md](../work/ads_diagnostic/README.md) | [work/ads_blink_reader/README.md](../work/ads_blink_reader/README.md)

### Steering & Suspension Wear — RESOLVED 2026-05-22 (MB-osat full overhaul + 4-wheel alignment)
**Status:** RESOLVED | **Priority:** — | **Since:** 2026-04-30 | **Resolved:** 2026-05-22

Full Priority 4B scope executed at MB-osat 2026-05-22. €2 447,00 invoiced (€1 425 labour + €1 022 parts) vs €2 545 quote from 2026-05-05 (~€98 under). Mileage at handover: 142 205 km. See `docs/diary/2026-05.md` 2026-05-22 entry for the line-by-line cost breakdown, alignment numbers, and test-drive impressions.

What was replaced or repaired:
- Rear lower control arm outer-joint bushings, L+R (closed the `narina` complaint).
- Right front lower ball joint (was the loose one).
- Left front wheel bearing (was the one with play).
- All four tie rod ends — both L+R tie rods replaced as complete assemblies (inner + outer ends, with new outer boots).
- Idler arm bushings — original idler-arm bolt reused (answer to May 5 open question #3).
- Both front lower control arms replaced as complete assemblies with new W124 adjustment bolts.
- Front shock dust boots + bump stops — Sachs kit fitted (see "ADS System" entry above for the MEYLE-vs-Sachs trade and the surplus-MEYLE-pair note).
- Front exhaust heat shields re-secured with clamps.
- **4-wheel alignment** by Ari Vuorela (Pyöränsuuntausraportti 22.5.2026 13:16): front total toe corrected from −1.4 mm net toe-out (LH at −5.0 mm!) to 2.9 mm mid-spec; rear toe also re-set; thrust angle effectively zero.

Post-work road impression (~5 km drive home): on-centre dead-zone gone, straight-line tracking calm hands-off, front-end thunk over expansion joints gone. Steering loads up immediately off-centre. Suspension feels appropriately tight for fresh bushings.

Watch items / residual notes:
- **Right-front caster** measures 10°37' against 10°30' max (7' over). Logged for next alignment session — may surface a next-to-wear item on the right front sub-frame side; not actionable today.
- **Rear camber** out of spec (L −2°35' / R −2°19') — geometry consequence of the still-low rear ride height, captured in the ADS entry above. Will re-measure after the level-control hydraulic diagnosis.
- Cabin vibration at idle is **lower in amplitude but not gone** — chassis-side noise floor has dropped, making the still-pending engine + transmission mount swap the highest-yield next diagnostic.

### Central Locking (PSE) -- FUNCTIONAL (Passenger Side), Driver Lock Disconnected
**Status:** PARTIALLY RESOLVED | **Priority:** LOW | **Since:** 2026-03-13 | **Updated:** 2026-04-05

**Root cause was blown trunk fuse 6** (replaced 2026-04-03). PSE pump confirmed alive on 2026-04-04 (first actuation from driver key). System progressively improved with repeated use as seized pneumatic valves freed up.

**2026-04-05:** Full central locking now operational from **passenger side key** — both keys work, red/green dashboard lights, all doors lock/unlock, pump runs reliably. System is fully functional.

**Driver side key lock:** Both keys turn freely (after WD-40 lubrication) but do **not** actuate the lock mechanism at all — no click, no latch movement, no PSE signal. Diagnosis: **lock cylinder coupling/linkage disconnected or broken.** The metal rod connecting the lock cylinder to the door lock mechanism has likely detached (brittle plastic retaining clip, common R129 age issue). Requires driver door panel removal to inspect and reconnect.

**IRCL remote — DEPRIORITIZED (2026-04-06):** Both key fobs tested with fresh CR2025 batteries. Key 1: IR LED fired 2-3 times then stopped (hardware fault). Key 2: dim IR output, tested on car — **no response.** Either transmission too weak or rolling code out of sync after years of disuse. Re-pairing requires MB Star Diagnosis tool (~€200+ dealer visit) — not cost-effective for a convenience feature. IRCL module on car is healthy (Pin 12 = 1 blink).

**Decision:** IRCL repair abandoned. Phone-based keyless lock/unlock will be implemented by the **always-on cabin signal node (`nRF54L15`)** driving the PSE signal directly. More secure (BLE bonded encryption vs 1991 IR), no line-of-sight required, and already part of the telemetry architecture. Requires identifying the IRCL→PSE signal wire during door panel / trunk-trim removal.

**Architectural note (updated 2026-04-26):** This responsibility was previously assigned to a separate "sentry" node (`nRF5340`). It is now folded into the cabin signal node so there is exactly one always-on Nordic MCU in the car. The cabin node lives in the front cubby alongside the Pi, is permanently powered from `F20_6`, drives a small trunk-side PSE drive board over a control wire that reuses one spare CAT6 pair on the existing passenger-side BE2210 trim run. The tap on the IRCL→PSE wire is *additive* (parallel to the factory IRCL output) so any future re-paired IR fob would still work. Full design + bring-up plan: [`docs/cabin_signal_survey.md`](cabin_signal_survey.md) §"Always-On Operation and BLE Keyless Lock/Unlock" and [`work/cabin_signal_node/README.md`](../work/cabin_signal_node/README.md) Stages 6–7.

**Next:** Driver side key lock linkage repair (low priority — passenger side key works for daily use). BLE lock/unlock implementation tracked in Phase 2.2 architecture.

[work/pse_central_locking/README.md](../work/pse_central_locking/README.md)

### Battery / Parasitic Drain
**Status:** BATTERY REPLACED — PARASITIC DRAW RETEST PENDING | **Priority:** LOW | **Since:** 2026-03-27 | **Updated:** 2026-04-18

**Battery replaced 2026-04-18** — new battery from Kärkkäinen Oulu (€159). Resolves the sulfated incumbent (Varta H3, 100 Ah, mfg Aug 2025) which tested at ~67 mΩ DC impedance (3–4× healthy) with cranking dip to 8.5 V at 3 °C. Trickle charger disconnected. Clean Owon cranking waveform to be captured at next opportunity as the new baseline.

**Historical data below is retained for context** — but all further parasitic-draw measurements must be taken on the new battery, since the old battery's elevated impedance made every sub-100 mA reading ambiguous (0.2 mV per fuse circuit was below the Owon's resolution).

*History — incumbent Varta H3 (retired 2026-04-18):* Voltage drops ~13 V to ~12 V in ~2 days idle. Manufactured August 2025. Experienced at least one deep discharge before AOK912 purchase.

**CCA test performed (2026-04-03):** Owon HDS242 cranking waveform at battery terminals (2V/div, 200ms/div). Resting voltage ~12.4V. Cranking dip ~4V to approximately 8.5V. **Ambient temperature was 3°C** — cold soak significantly worsens the dip. Engine caught immediately (very short crank). Assessment: borderline at 3°C but not alarming. Re-test in warmer conditions (~15-20°C) for a fair comparison.

**IRCL (Pin 12) confirmed alive** after fuse 6 replacement — 1 blink, no faults. ATA (Pin 11) confirmed dead (genuine module fault, deprioritized — see ATA entry below).

**Parasitic draw test (2026-04-05):** First valid reading was 400mA with trunk open + car unlocked — invalid (modules in standby, trunk light on). Attempt to measure with trunk closed blew the Owon HDS242 current fuse due to battery reconnection inrush surge (>8A).

**24h voltage decay test (2026-04-06→07):**
- 12.88V (Apr 6 13:00, 3h post-charger) → 12.46V (Apr 7 13:00) = 420 mV/24h. Trunk light ON, car unlocked → ~790 mA average (trunk light accounts for ~600 mA).
- 12.46V (Apr 7 13:00) → 12.38V (Apr 7 21:37) = 80 mV in 8.5h. Trunk light OFF, car unlocked → **~226 mV/day rate** — much lower, consistent with <100 mA parasitic draw.

**Fuse-by-fuse test (2026-04-07 evening):**
- All 16 main fuse box fuses are on switched power (no 12V with key out). Permanent 30 circuits route through auxiliary boxes F19 and F20 only.
- F20-6 (PSE, IRCL, antenna, trunk light): 1 mV change on Owon — negligible steady-state draw. MAS830 multimeter blew instantly on inrush when reconnected (capacitor charge surge from PSE/IRCL modules).
- Remaining F20 fuses (1-4, 7): no measurable voltage change on Owon.
- **Conclusion: no rogue consumer.** Per-fuse voltage changes are below Owon's 1 mV resolution because battery impedance × individual circuit current ≈ 0.2 mV.

**Battery internal resistance — ELEVATED:**
- Trunk light (0.6 A known load) causes **40 mV drop at battery terminals** → 67 mΩ DC impedance.
- Healthy 95 Ah battery: 5–10 mΩ. This battery: ~20 mΩ dynamic (from cranking sag to 8.5V at ~200 A) and ~67 mΩ DC (from 0.6 A trunk light, includes polarization).
- **Battery is 3–4× higher impedance than expected.** Consistent with deep discharge damage or internal sulfation from the previous neglect period. Car starts reliably now but may fail on first cold Oulu morning.

**Next:** Morning voltage reading (Apr 8, trunk closed, car unlocked) for clean overnight decay rate. Consider battery replacement before autumn. Re-test CCA in warmer weather. Owon current fuse replacement still pending.

### Power Antenna -- Functional, One Segment Slightly Stiff
**Status:** RESOLVED | **Priority:** — | **Since:** 2026-03-29 | **Resolved:** 2026-04-05

**Root cause was blown trunk fuse 6.** After fuse replacement (2026-04-03), antenna motor immediately came alive. Upper segments extended/retracted with radio. Two lowest segments were initially stuck — freed with WD-40 penetrant and light manual assist. CRC silicone spray applied into mast tube (2026-04-04). **All segments now fully smooth after silicone lubrication (confirmed 2026-04-05).** Issue fully resolved.

### Windshield Wiper / Washer
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-15

Wiper does not consistently park correctly. Washer fluid only from 2 of 4 nozzles.

**Likely cause identified (2026-04-05, video research):** Wiper park position switch — a circular contact disc inside the wiper motor assembly. Metal dust/debris accumulates on the contact tracks over time, causing the switch to misread blade position and stop at the wrong point. The R129 mono-wiper uses this same principle. Symptom is milder than severe cases (blade doesn't keep running, just parks incorrectly) — suggests dirty contacts rather than full failure. **Fix: disassemble wiper mechanism, clean park switch contact tracks with isopropanol or electrical contact cleaner.** Mechanism is accessible from underneath the cowl cover.

[work/wiper_system/README.md](../work/wiper_system/README.md)

### Idle Quality — Post-MB-osat Warm-Idle Elevation
**Status:** OPEN — DIAGNOSTIC LADDER PARTIALLY EXECUTED | **Priority:** MEDIUM | **Since:** 2026-04-30 | **Updated:** 2026-05-25

**Original observation (2026-04-30, MB-osat):** engine does not fire all cylinders cleanly at idle. Suspected distributor-related.

**Customer action (2026-05-05):** Bosch distributor caps + rotors replaced at MB-osat (€426.70 combined invoice with labour, no separate pre/post baseline captured — lesson logged). Subjective: idle *may* be smoother but cabin vibration persisted, weakening the case for caps/rotors as the actual root cause.

**Root cause found 2026-05-22 (MB-osat engine-bay walkthrough during the steering/suspension visit):** **a couple of disconnected vacuum hoses in the engine bay.** Reattached, and idle quality "improved markedly" per the receipt narrative (page 3: `käynti parani huomattavasti`). This is the exact failure mode that would survive a cap+rotor swap on a KE-Jetronic engine — small vacuum leaks dump unmetered air the system can't sense, and the air-fuel ratio goes lean on the affected branch(es). The May 5 cap+rotor swap was therefore likely premature; the parts are fresh and not a regression.

**Residual symptom:** **warm idle stays slightly elevated** (~50–100 rpm above the old base) after the engine reaches operating temperature. MB-osat narrative continues: ran a **smoke test** and found the **5th-cylinder injector breather/vent hose (huohotinletku) cracked**, applied a bit of silicone tape as a field fix. Confirmed during a short MB-osat test drive and during the drive home. The silicone-tape fix is **interim only** — heat-cycled rubber/plastic injector breather hoses don't seal long-term against tape. Tracked as its own open issue ("5th-Cylinder Injector Breather Hose" below) along with the "inspect all 8 breather hoses at next valve-cover-off opportunity" follow-up.

**Demoted from HIGH to LOW (2026-05-22).** The disturbance MB-osat flagged on Apr 30 is now substantially fixed, the remaining warm-idle elevation is small, the cause is known, and the proper fix folds into the existing Priority 2 valve-cover gasket / spark plug tube seal work.

**Re-promoted to MEDIUM (2026-05-23) — two real observations within 24 h of the visit (a third initially-suspected symptom resolved as normal operation on 2026-05-25):**

1. **Warm idle initially captured as 800–900 rpm in P/N (2026-05-23), now improving — see trajectory below.**
2. **Visible engine vibration at low rpm is gone, identical in P, N, D, and R.** Positive finding. The P/N-vs-D/R independence is the diagnostic key: load state doesn't change amplitude → source was engine-combustion-side (cylinder-to-cylinder firing variance from the loose vacuum hoses), not mounts or driveline. **Substantially weakens the case for engine mounts as the residual-vibration root cause** (see "Engine Mounts" entry below).

*(Initially-suspected third observation — kickdown "glitching" on 2 of 4 WOT events — was resolved on 2026-05-25 as a misread of normal 722.3 1st-gear behaviour: WOT punches at the edge of the 1st-gear engagement zone correctly produce a brief 1st-gear interval before upshifting to 2nd, which felt like a "glitch" but is factory-correct shift logic. Reverified in two clean tests, deep in the 1st-gear zone and above it, both kicked down cleanly to redline. Removed from active scope; watch posture only — reopen if it ever returns in the above-1st region where it should not happen.)*

**Warm-idle trajectory (three measurements, 60 hours, no intervention beyond driving):**

| Date | P/N warm | D warm | Conditions |
| :--- | :--- | :--- | :--- |
| 2026-05-22 (drive home, ~6 km) | ~750–800 (est.) | — | First post-MB-osat drive |
| 2026-05-23 (after longer drive) | **800–900** | — | Idle stable, not hunting |
| **2026-05-25** (after 30 min + a few hard accelerations) | **750** | **~600** | Best steady-state measurement so far |

Spec is **600–700 rpm in P/N** and **580–680 rpm in D**. As of 2026-05-25: **D is in spec**, **P/N is 50 rpm over max** (marginal, no longer alarming). The ~150 rpm P/N → D drop matches the healthy 722.3 converter-drag signature, which means closed-loop idle control is working — just settling on a target slightly high. The May 23 800-900 number now reads as the peak of a settling curve, not steady state.

**Working hypothesis (updated 2026-05-25 PM):** with the P/N-vs-D split being healthy, a mechanically-stuck-open LLR is **weakened** (such a fault would elevate both positions roughly equally; the LLR has no authority to compensate either direction). Leading explanation is now a **small residual leak** — most likely the silicone-tape 5th-cyl breather + possibly one more not-yet-found hose — that the LLR is largely compensating for. The throttle-linkage-preloaded hypothesis was substantially weakened after the 2026-05-25 Step 1 check (throttle plate seated visually OK both engine-off and engine-running); only the kickdown-cable position sub-check remains unverified.

**Three self-resolving mechanisms** could explain the improving trajectory: (a) silicone tape on the 5th-cyl breather hose finishing self-amalgamation over the first 1-2 hot soak cycles, (b) MB-osat-re-seated vacuum hoses bedding in with thermal cycling, (c) the LLR pintle freeing up from regular use. Any/all could be contributing.

**Diagnostic ladder progress** (full procedure in [`work/post_mbosat_drivability/README.md`](../work/post_mbosat_drivability/README.md)):

- **Step 1 (throttle linkage visual / hand check) — PARTIAL 2026-05-25.** Throttle plate, idle stop, accelerator cable, cruise rod all visually OK both engine-off and engine-running. Kickdown cable at engine-end not yet located → that one sub-check still pending.
- **Step 2 (vacuum hose sweep) — PARTIAL 2026-05-25.** Superficial sweep done, no obvious dangling hoses. **Systematic per-hose tug-test list (FPR, brake booster, cruise servo, HVAC vacuum tree, distributor vacuum advance ×2, EVAP) not yet completed.** De-prioritised after the 2026-05-25 PM measurement but still on the books for full close-out.
- **Step 3 (LLR unplug test) — NOT DONE.** 30-second binary test; de-prioritised after the 2026-05-25 PM measurement (P/N-vs-D split weakens the LLR fault hypothesis) but still useful as binary confirmation.
- ~~Step 4 (722.3 modulator + kickdown cable)~~ — deprecated after the kickdown symptom resolution.
- **Step 5 (smoke test) — gate.** Only if Steps 1–3 are clean.

**Next measurement gate:** one more 30-min-warm reading in 3–5 days at the same conditions. If the trend continues toward ~700 P/N → demote this entry back to **LOW**, mark "trajectory-resolved, proper breather hose still pending." If it stabilizes at 750 P/N → keep at MEDIUM with marginal-tolerable note. If it bounces back above 800 → urgency returns, execute Steps 2 + 3.

**Separately still tracked:** 5th-cylinder injector breather hose proper-fix (silicone tape interim from MB-osat) — see "5th-Cylinder Injector Breather Hose" entry below. The proper hose swap is now the **most likely intervention to land idle cleanly in spec** (close the small residual leak that the LLR is partly compensating for).

### Engine Mounts
**Status:** OPEN — PREVENTIVE MAINTENANCE (no longer the diagnostic gate) | **Priority:** LOW (was MEDIUM; downshifted 2026-05-23) | **Since:** 2026-03-13 | **Updated:** 2026-05-23

Corteco replacement mounts on hand since 2026-03-30 (80001913 ×2 engine + 21652116 trans). The May 5 plan to do the DIY swap alongside the belt swap (May 9–10) slipped; MB-osat May 22 visit did not include mounts per the May 5 late decision to keep them DIY.

**Diagnostic context updated 2026-05-23:**
- 2026-05-22 observation captured visible cabin vibration as "lower in amplitude but not gone" after the steering/suspension overhaul, elevating the mount swap to "next highest-yield diagnostic".
- **2026-05-23 observation supersedes that:** visible engine vibration at low rpm is gone, **and the smoothness is identical in P, N, D, and R**. Load-state independence means the source was engine-combustion-side (cylinder firing variance from the loose vacuum hoses MB-osat reconnected), not mounts or driveline. See "Idle Quality + Kickdown Glitch" entry above for the full three-observation analysis.
- The May 14 UMIK-1 "1× engine-rotation infrasonic line" interpretation in `work/audio_exhaust_synth/m119_sideband_diagnosis.md` should be re-read in this light — the line was most likely firing-variance-driven (from the loose hoses), not block-on-mount rocking. A post-fix UMIK-1 re-capture would confirm by showing the line substantially attenuated.

**Net:** the mounts are still 35 years old and the Corteco replacements are still on the shelf, but **the urgency is now "do during the next opportunistic front-belly-pan-off session" rather than "book a dedicated Saturday with pre/post measurements."** The vibration justification has largely evaporated. Preventive value remains (35-year-old fluid-filled mounts are statistically near end-of-life), but it's no longer a diagnostic-driven job.

**Next:** fold into a future front-axle / belly-pan-off session (e.g. brake flex hose inspection, oil change with magnetic plug install, or a return to MB-osat for any not-yet-scheduled work). Pre-swap UMIK-1 capture still recommended for the record but no longer the primary justification.

[work/engine_trans_mounts/README.md](../work/engine_trans_mounts/README.md)

### 5th-Cylinder Injector Breather Hose — Cracked, Silicone-Tape Interim
**Status:** OPEN — INTERIM FIX IN PLACE | **Priority:** MEDIUM | **Since:** 2026-05-22

Found during the MB-osat smoke test on 2026-05-22 while investigating the residual warm-idle elevation after the vacuum-hose fix (see "Idle Quality" entry). The injector breather / vent hose (`huohotinletku`) on the 5th-cylinder injector cup was cracked. MB-osat applied a piece of silicone tape as a field fix.

The M119 KE-Jetronic injector cup design has one breather hose per cylinder (8 total) — small braided rubber/silicone hoses prone to age cracking. A cracked breather is a small vacuum leak in series with the injector cup, and it's exactly the kind of micro-leak that smoke-tests reveal and idle-quality measurements show as a small elevated warm-idle rpm.

**Interim posture:** silicone tape will likely hold for short-term driving (weeks, not months — heat-cycled tape doesn't seal long-term on rubber).

**Proper fix:** source the correct 5th-cyl injector breather hose for M119.960 (P/N TBD — ask MB-osat at the next visit, EPC is open for this VIN; M119 injector cup vent hoses are cheap when found OEM, generally <€10 each) and replace properly.

**Follow-up scope:** **inspect all 8 injector breather hoses** at the next valve-cover-off session (folds into the Priority 2 valve-cover gasket + spark plug tube seal work — the valve covers come off anyway, so this is a zero-marginal-time inspection). If more than 1–2 are visibly aged, replace as a set.

### Engine Cooling Fan Viscous Clutch — Possibly Locked-Up (Watch Item)
**Status:** OPEN — ADVISORY ONLY | **Priority:** LOW | **Since:** 2026-05-22

MB-osat flagged on 2026-05-22 that the engine cooling fan viscous coupling "seems too stiff" (`moottorin tuulettimen visko vaikuttaa olevan liian jäykkä`). This is an **advisory**, not a confirmed fault.

M119 viscous fan clutches fail in two modes:
- **(a) Fluid leak / freewheel** — fan spins free regardless of temperature, the engine under-cools under high thermal load.
- **(b) Silicone fluid degradation / lock-up** — fan stays *engaged* regardless of temperature, putting permanent parasitic load on the front of the engine. Symptoms: small power loss, small mpg loss, accelerated belt + pulley wear, audible fan roar at sustained highway speed (the fan running at engine speed instead of cycling).

MB-osat's observation is consistent with mode (b).

**Next:**
1.  At the next jack-up session, measure cold-vs-hot freewheel resistance by hand (engine off, fan should spin a few turns cold and stop quickly; should be progressively stiffer hot). Compare to known-good R129/W124 behaviour from forum write-ups.
2.  Listen for fan roar at sustained 100–120 km/h cruise. If present, this is corroborating evidence.
3.  Defer replacement until enough evidence accumulates. Replacement is a Behr/Sachs viscous clutch + 32 mm flat-wrench job; part roughly €60–120 OEM, ~30 min labour.

### Crankshaft Position Sensor — RESOLVED (New Topran Sensor Installed)
**Status:** RESOLVED | **Priority:** — | **Since:** 2026-04-04 | **Resolved:** 2026-04-19

**Topran 408 205 installed 2026-04-19.** Old sensor had been routed around a bolted-on engine feature; wire was cut during extraction. New sensor uses same endpoints but bypasses the last "top of engine" loop (see Apr 19 diary for thermal-exposure notes on the re-routed section).

**Verification:**
*   **First-start (1–2 min idle) 2026-04-19:** engine caught immediately, no unusual noises, no leaks.
*   **Pin 8 post-drive 2026-04-19 (engine still running, ~15 km drive incl. revs to ~6 k):** **1 blink, no faults.** This is the definitive test — the Apr 4 failure mode was "Code 17 returns after every drive" with the old sensor, and that no longer occurs.
*   **KOEO artifact documented** — Pin 8 reads 17 blinks with ignition on, engine stopped. This is a normal variable-reluctance-sensor reading (zero signal at zero RPM, EZL can't distinguish "stopped" from "broken"). **All future Pin 8 reads must be done with engine running or within seconds of shutdown.**

**Related remaining task** (tracked in Apr 19 diary, not reopened here): walk the new sensor wire hot after the next drive and decide whether the "top of engine" section needs heat-shielded loom. Not a fault per se; a durability precaution.

### Valve Cover Gaskets & Spark Plug Tube Seals — Oil in Wells
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-04-05

6 of 8 spark plug wells contain oil. Only front cylinders (1, 5) are dry. Both banks affected. Root cause: degraded spark plug tube seals allowing valve cover oil to leak into the wells. Oil is external only — all combustion chambers healthy (clean electrode tips on all 8 plugs). Risk: oil eventually soaks plug wire boots causing misfires/arcing.

**Fix:** Replace both valve cover gasket sets + 8× spark plug tube seals. Combine with Priority 2 timing chain guide inspection (valve covers must come off for both jobs). Parts needed — add to MB-osat order.

### Engine Belt Noise -- Resolved by Serpentine Belt Swap
**Status:** CLOSED — RESOLVED 2026-05-06 | **Priority:** MEDIUM | **Since:** 2026-03-21 | **Updated:** 2026-05-06

Squeals/chirps on startup. **V-belt friction spray test (2026-04-03):** noise disappeared instantly, confirming glazed/slipping belt (not a bearing issue).

**Re-emerged 2026-04-19 during test drive.** Spray applied again to silence — but this confirms the Apr 3 prediction that spray is temporary only. The friction modifier wears off / washes off in days to weeks, and the underlying glaze is still present. Further spray applications are band-aid only; belt replacement is now the mandatory fix.

**Resolved 2026-05-06:** ContiTech 6PK2523 single serpentine belt fitted. Job went smoothly and the belt squeal disappeared as expected. Removed belt looked nearly new, so the failure mode may have been weak tension/preload rather than belt material condition alone. Old belt retained as a clearly marked **used** emergency road-trip spare in the car.

**Follow-up:** At the next front-access session, inspect the rubber-bushed tensioner assembly, tensioner rod, and idler/guide pulleys. The symptom is closed, but the "old belt looked new" observation keeps tensioner/preload on the watch list.

### Exhaust — Front Heat Shields Resolved; Centre-Silencer Heat-Shield Rust Watch
**Status:** RESOLVED (front) / WATCH (centre-silencer heat shield) | **Priority:** LOW | **Since:** 2026-04-19 | **Resolved:** 2026-05-22

**Symptom (observed 2026-04-19 test drive):** light resonance/drone in the 2–3.2 k RPM band, **load-dependent only** (absent in neutral at the same RPM, absent above ~3.5 k). Reduces as the engine warms.

**Visual finding (photo 2026-04-19):** centre-silencer shell shows a visible crack / through-hole on the lower portion, surrounded by heavy scale and rust staining. External heat-shield partially detached. Adjacent mid-pipe section also heavily corroded.

**MB-osat finding (2026-04-30):** resonance was due to loose heat shields in the front exhaust pipe area (`etuputkien lämpösuojapellit irti`). Centre-silencer heat shield also rusted and rattling (`keskimmäisen vaimentajan lämpösuojapelti ruostunut ja rämisee myös`); MB-osat advised against changing cats or any other exhaust parts.

**Resolved 2026-05-22:** MB-osat secured the front exhaust heat shields with clamps as part of the steering/suspension visit (receipt page 1 line 8: "Kiinnitetään pakoputkien lämpösuojapellit esimerkiksi pakoputkiklemmarein"). The load-range resonance source is now eliminated; expected to be inaudible on the next sustained 2.5–3 k cruise. Confirm on next motorway drive.

**Remaining watch item:** centre-silencer heat-shield rust + rattle. MB-osat re-confirmed 2026-05-22 that this **does not need fixing now**. Leave alone unless the rattle becomes intrusive or repair is convenient during other lift work (e.g. an engine-mount session that already needs the front belly pan off).

### Headlight Switch Knob Worn
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02

The headlight switch rotary knob is worn out / soft. Feels mushy and imprecise. Needs replacement or refurbishment.

### Seat Adjustment Panels (Door) Loose
**Status:** RESOLVED | **Priority:** — | **Since:** 2026-04-02 | **Resolved:** 2026-04-05

Both door seat control panels (P/N 129 820 71 10, "W.-Germany") loose at the bottom. **Cause identified (2026-04-03):** front lower plastic locating clip broken (age embrittlement). Metal mounting clips at corners are intact. Biltema double-sided tape attempted — failed.

**Fix (2026-04-04/05):** Scotch Fix Extreme Exterior tape (3M VHB-class) applied at broken clip locations on both sides. Driver side done April 4, passenger side April 5 (old duct tape + hot glue bodge by previous owner removed first). Both panels now secure. Minor leather wear/whitening from panel movement — will address during door card removal for speaker installation.

### Front Grille — Clean & Polish
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02

Front grille needs thorough cleaning and polishing (Autosol Metal Polish on hand). Cosmetic item, no urgency.

### Driver Door -- Window Too High, Hard to Close
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-03

Driver door occasionally requires more force to close than passenger side. **Cause:** driver side window sits slightly too high and contacts the door seal on closing. Frameless R129 windows have adjustable upper limit stops.

**Next:** Adjust driver window maximum height (stop position) to prevent seal contact and long-term seal wear.

### Hardtop Fitment
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-13

Front latches bind from excess headliner thickness. Requires manual pull-down assist.

### Paint & Body
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-15

Minor paint cracking on rear fender (below trunk lid). Small deep scratch on aluminum hood. Bare steel behind front wheels needs rust-prevention touch-up.

### Instrument Cluster Faults
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-18

Clock adjustment stuck/locked. Temperature LCD delaminated/washed out. Both to be addressed during Phase 3 cluster pull. Cluster is a confirmed non-ADS swap -- no ADS warning lamp symbol on indicator strip. ADS is factory-fitted (option 216, confirmed lastvin.com 2026-04-01), so the original cluster would have had the ADS lamp. A previous owner swapped in a non-ADS cluster at an unknown date.

---

## DEPRIORITIZED / WON'T FIX

### ATA Anti-Theft Alarm Module -- Dead (Pin 11 Static Glow)
**Status:** WON'T FIX | **Priority:** NONE | **Since:** 2026-03-18 | **Decision:** 2026-04-03

X11/4 Pin 11 shows weak static glow, no blink response. Module remained unresponsive even after trunk fuse 6 replacement (2026-04-03), confirming genuine ATA module fault (not a power issue).

**Decision to leave as-is:** The ATA (option 551) is purely a noise-deterrent alarm — horn honk + hazard flash on intrusion. The 1991 R129 has **no electronic immobilizer** whatsoever; the engine starts on the mechanical key alone regardless of ATA status. Repairing the ATA means maintaining a complex sensor network (door/trunk/hood contacts, interior motion sensors, horn relay, hazard relay, PSE arming logic) across 35-year-old wiring for no practical security benefit. The IRCL (remote lock/unlock) works independently and handles all daily convenience. The ATA module is a potential parasitic drain source through its static glow state.

**If revisited:** Plug-and-play trunk module swap (P/N likely 129 820 xx xx). Only worth pursuing if Finnish insurance ever requires a factory alarm, or if eliminating it as a parasitic drain source becomes necessary.

---

## RESOLVED

### Head Unit Touchscreen -- Not Enumerating (UI unusable in car)
**Status:** RESOLVED | **Resolved:** 2026-08-09

Returning to the car after ~10 weeks the UI booted and rendered but ignored all touch. The digitiser was absent from the Pi entirely: no `0712:000a` in `dmesg` since boot, no touch device in `/proc/bus/input/devices`, and `lsusb` listing only the Audiotec Fischer DSP and the Carlinkit dongle. A `blueman-applet` notification popup was cleared first and turned out to be an unrelated red herring.

**Cause: the digitiser's USB connection, in the interim display mount.** Re-seating all adapters restored it — it enumerated on port `1-2`, bound `hid-multitouch`, and touch worked. No component had failed.

The full stack was verified good once the link came up, which is worth recording as a known-working baseline:

| Layer | Verified state |
|---|---|
| Device | `0712:000a` "Waveshare Waveshare", serial `20231224X8`, full-speed on `1-2` |
| Driver | `hid-multitouch` bound, nodes `event6` + `mouse0` |
| libinput | `/dev/input/event6`, `Capabilities: touch`, seat0 |
| Mapping | `rc.xml`: `<touch deviceName="Waveshare  Waveshare " mapToOutput="HDMI-A-1" mouseEmulation="yes"/>` |
| Output | `HDMI-A-1` 1080x1920@60.6, `Transform: 90` |

Two details that cost time and are worth knowing next visit. The kernel always logs `config 1 has an invalid interface number: 1 but max is 0` for this panel — a benign Waveshare descriptor quirk, not the fault. And `libinput debug-events --device` fails with `Invalid path` when the node is absent, which reads like a tool error but simply means the device is gone.

The residual mechanical unreliability is tracked as a separate OPEN entry above; `mouseEmulation="yes"` is what lets touch drive the Qt mouse handlers.

### ADS Factory Origin Unknown
**Status:** RESOLVED | **Resolved:** 2026-04-01

Lastvin.com factory build data shows option **216** (self-leveling suspension all-around with ADS). The earlier mbdecoder.com decode missed this code. All ADS hardware is original factory equipment. The non-ADS instrument cluster is a confirmed previous-owner swap.
