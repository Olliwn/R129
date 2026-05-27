# Post-MB-osat Drivability Follow-Up — Warm Idle, Kickdown, and Smoothness Baseline

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | **Engine:** M119.960 V8 (KE-Jetronic) | **Transmission:** 722.3 (4-speed auto, vacuum-modulator + kickdown-cable)

**Trigger:** Three new drivability observations in the first 24 hours after the 2026-05-22 MB-osat steering/suspension visit (see `docs/diary/2026-05.md` 2026-05-22 entry and `docs/known_issues.md` "Idle Quality" entry). Two are new symptoms, one is a positive baseline shift. They are tracked together because the most plausible single root-cause class — something changed in the throttle / vacuum / trans-modulator area during the engine-bay work — explains all three coherently.

---

## Three Observations

### Obs 1 (2026-05-22 → 2026-05-25) — Warm idle elevated, but on a clear downward trajectory

Three measurements over 60 hours, all at warm engine (full operating temperature):

| Date | P/N warm | D warm | Conditions |
| :--- | :--- | :--- | :--- |
| 2026-05-22 (drive home, ~6 km) | ~750–800 (est.) | not recorded | First post-MB-osat drive, ~6 km mostly low-speed urban |
| 2026-05-23 (after longer drive) | **800–900** | not recorded | Idle stable, not hunting |
| 2026-05-25 (after 30 min + a few hard accelerations) | **750** | **~600** | Best conditions for steady-state measurement so far |

Spec is **600–700 rpm in P/N** and **580–680 rpm in D** for M119.960 / 722.3. So as of 2026-05-25:

- **D is in spec** (600 rpm sits in the lower half of the 580–680 range).
- **P/N is 50 rpm over max** — marginal, no longer alarming. The May 23 800-900 number now reads as the peak of a settling curve, not a steady state.
- **P/N → D drop of ~150 rpm is healthy** — exactly the converter-drag pull that the 722.3 should produce. The relationship being correct means closed-loop idle control is working; it's just settling on a target that's slightly high in P/N. Mechanically-stuck-LLR-open hypothesis becomes less likely (that would tend to elevate both positions roughly equally, because the LLR doesn't have authority to compensate either way).

**Three self-resolving mechanisms** all of which would predict the observed trajectory (900 → 750 in 60 hours), any or all of which could be contributing:

1. **5th-cyl silicone-tape interim has finished self-amalgamating.** Silicone tape's bond completes after the first 1–2 hot soak cycles; if the tape was leaking 80 % through on day 1, may be ~20 % through now. Less unmetered air → LLR closes less → idle drops toward target.
2. **Vacuum-hose connections MB-osat re-seated have bedded in.** Rubber-to-metal vacuum-port seals are typically "loose on day 1, tight by day 5" after heat cycles compress the rubber against the port. Same direction.
3. **LLR pintle freeing up with regular use.** If the cause includes a sticky LLR (the Step 3 candidate), regular driving exercises it through its range — sticky pintles often free themselves over a few dozen idle cycles.

**Next measurement gate:** one more 30-min-warm reading in 3–5 days at the same conditions. If the trend continues toward ~700 P/N → effectively closed, no further diagnostic action needed beyond the already-planned proper 5th-cyl breather hose swap. If it stabilizes at ~750 P/N → marginal-tolerable, Step 2 + Step 3 remain available as a fully-close option (owner choice). If it bounces back above 800 → urgency returns, Steps 2 + 3 become active.

MB-osat's own May 22 narrative warned "*tyhjäkäynti jää hieman korkealle*" / "idle stays slightly high" — their post-tape test drive was within minutes of the silicone-tape application, so they saw essentially the peak-leak condition. The trajectory now suggests their note will end up being accurate in the long run (idle slightly high, but tolerable), not the early-day-1 worst-case impression.

### ~~Obs 2 (2026-05-23)~~ — Kickdown "glitching" — RESOLVED 2026-05-25 as misread of normal 722.3 1st-gear behaviour

**Initial observation (2026-05-23):** on 2 of 4 sequential WOT events, the 722.3 produced what looked like a rapid downshift → immediate upshift sequence at pedal-down.

**Resolution (2026-05-25):** further driving with controlled-condition tests showed clean kickdown-and-hold behaviour in both diagnostic regions:
- WOT launched from a low-enough speed that 1st gear would correctly engage → ran cleanly to redline.
- WOT launched above the 1st-gear range (i.e. kickdown 4→3 or 4→2 only, never to 1st) → also ran cleanly to redline.

Reinterpretation: the 2-of-4 events that triggered the "glitch" impression were almost certainly **WOT punches at the edge of the 1st-gear engagement zone**, where the 722.3 correctly drops to 1st for a few hundred milliseconds and then upshifts to 2nd as engine RPM crosses the 1→2 shift point. That short 1st→2nd sequence feels like a "very brief boost then a step-back" — exactly the "glitch" sensation the owner reported — but it is **normal kickdown behaviour for the 722.3 at low road speed**, not a fault. The factory shift logic is designed to put the engine in the right gear for the current speed; on a 4-speed with relatively tall gearing, the 1st-gear window is narrow and brief.

The owner's original "this might be due to my actions" caveat was correct: it was a misinterpretation of normal behaviour driven by route variance (different starting speeds producing different shift patterns), not a real symptom.

**Removed from known-issues** (was conflated under "Idle Quality + Kickdown Glitch"; that entry is now back to just "Idle Quality"). **Watch posture remains:** if the symptom reappears in the kickdown-above-1st region (where it definitely should not happen), reopen this section and resume the diagnostic ladder from Step 4. Until then, no action.

**Knock-on effect on the diagnostic ladder:** Step 4 of the ladder targeted the 722.3 vacuum modulator + kickdown cable adjustment specifically because of this symptom. With the symptom resolved as normal operation, **Step 4 is deprecated** as a kickdown-debug step. The kickdown-cable position check folds back into Step 1 because the cable's effect on the throttle linkage rest position is still relevant to the high-idle question (if the cable adjustment has drifted such that it's slightly taut at idle and lifting the throttle lever off its stop, that would produce the high idle even without affecting kickdown timing). The 722.3 vacuum modulator ATF-intrusion check is dropped — modulator only affects shifts, not idle.

### Obs 3 (2026-05-23) — Engine markedly smoother at low rpm, identical in P/N/D/R

**Positive finding.** Visible engine vibration at idle and low-rpm cruise is gone (or near-gone), and **the smoothness is the same in P, N, D, and R**. The P/N-vs-D/R independence is the diagnostic key: P/N has the engine spinning the torque-converter shell under no load; D/R loads the engine via the converter against the brake. If the vibration source were mounts, exhaust hangers, or driveline geometry, the load state would change the amplitude. It doesn't. That points squarely at an **engine-combustion-side** source that's now no longer happening.

This is consistent with — and substantially closes — the May 14 UMIK-1 acoustic analysis question. The 1×-rev infrasonic line documented in `work/audio_exhaust_synth/m119_sideband_diagnosis.md` was originally interpreted as engine-block rocking on worn mounts. With this observation, the simpler explanation is **cylinder-to-cylinder firing inconsistency from the loose vacuum hoses** — small unmetered-air leaks bias individual cylinders lean by different amounts each combustion cycle, producing a 1×-rev variability signature that *looks* like rocking but is really irregular firing energy. MB-osat reconnected the loose hoses → firing variance dropped → 1×-rev line should be substantially attenuated.

This has implications for the engine-mount priority (see "Knock-on Effects" below).

---

## Working Hypothesis — Root-Cause Candidates for the Remaining Symptoms

With Obs 2 (kickdown) resolved as normal operation (2026-05-25), the working hypothesis simplifies: only Obs 1 (high warm idle) is now an active symptom. Obs 3 (smoothness improvement) is a positive baseline shift consistent with the loose-vacuum-hose fix MB-osat performed and is already explained by that.

The MB-osat engine-bay walkthrough on 2026-05-22 touched three things in the throttle / vacuum area: (a) reconnected "a couple of loose vacuum hoses", (b) ran a smoke test, (c) applied silicone tape to the cracked 5th-cyl injector breather hose. Any of those touch-points could have left a downstream artifact that's now showing as the elevated warm idle:

| Possible artifact | Symptom mechanism | Status after 2026-05-25 Step 1 check |
| :--- | :--- | :--- |
| **Throttle linkage preloaded** (cruise rod, accelerator cable misseated after the work, throttle plate off its idle stop) | Air past partially-open throttle plate is uncompensable by the LLR (it's already commanded fully closed) → idle settles at the wrong target | **Partially ruled out.** Step 1 visual / hand check on 2026-05-25 (engine off and engine running) found nothing visually abnormal — throttle plate appears seated, no obvious linkage preload. **Caveat:** the kickdown-cable position at the engine-end barrel has not yet been verified, so a kickdown-cable-driven preload is still possible. |
| **Idle stop screw nudged** | Same as above — plate not seating against its stop because the stop itself has moved | **Partially ruled out** by the same Step 1 check (the stop screw and its locknut were visually in their original position; no obvious signs of recent adjustment). |
| **Different vacuum hose loose now** (a third hose neither MB-osat noticed nor the smoke test caught, or one that's worked loose since the visit) | Unmetered air bypass → LLR closes to compensate → as long as the leak is smaller than the LLR's air-bypass authority, the LLR pulls idle back to spec. If the leak exceeds LLR authority, idle goes high | **Open — still the leading hypothesis.** Step 2 vacuum hose sweep was done superficially on 2026-05-25 but not completed per the named-hose list. **High-priority next action.** |
| **LLR (Leerlaufsteller) sticky / contaminated**, exposed now that the chronic leaks aren't masking it | Pintle stuck partially open → air passes regardless of ECU command → idle settles high | **Weakened (2026-05-25 measurement).** A mechanically-stuck-open LLR would elevate *both* P/N and D idle roughly equally (LLR has no authority to compensate either direction). The observed ~150 rpm P/N → D drop matches the healthy 722.3 converter-drag signature, so closed-loop idle control is clearly working — just settling on a target slightly high. Step 3 unplug test still useful as the binary confirmation, but no longer the leading candidate. |
| **Small residual leak (silicone-tape 5th-cyl breather + maybe one more not-yet-found hose)** | Small amount of unmetered air → LLR compensates by closing → idle target is met, but the LLR may run out of closing authority slightly and the system settles a touch above spec | **Now the most likely steady-state explanation** given the May 25 numbers (P/N just 50 rpm over max, D in spec, P/N-vs-D relationship healthy). Step 2 systematic hose sweep + the planned proper 5th-cyl breather hose swap would close this completely. |
| **Loose-hose-driven firing variance was real, now resolved** | Explains Obs 3 (smoothness improvement) | Confirmed by Obs 3 itself. |

**Posture as of 2026-05-25 (post-30-min-drive measurement):** the high warm idle is on a **clear downward trajectory** (~900 → ~750 in P/N over 60 hours), now only 50 rpm over spec in P/N and in spec in D. The throttle-linkage-preloaded and stuck-LLR hypotheses are both weakened — the leading explanation is now a **small residual leak** (silicone-tape on the 5th-cyl breather + possibly one more hose not yet found) that the LLR is mostly compensating for. **Urgency has dropped:** Steps 2 + 3 are still the right diagnostics if a full close-out is wanted, but no longer urgent. The already-planned proper 5th-cyl breather hose order (Priority 2 in `docs/parts_to_order.md`, expected to come through MB-osat) is now the most likely intervention to land the idle cleanly in spec. **Next measurement gate:** one more 30-min-warm reading in 3–5 days to see where the trajectory flattens.

---

## Knock-On Effects on Existing Open Items

### Engine + Transmission Mounts — priority drops from "next diagnostic" to "preventive maintenance"

The May 22 diary and the `known_issues.md` "Engine Mounts" entry both elevated the mount swap to **the next highest-yield diagnostic** for residual cabin vibration. Obs 3 today substantially weakens that case: if the vibration is gone *because firing is even now*, the mounts were probably never the dominant contributor. They were transmitting the firing-variance shake, not generating it.

This doesn't mean the mounts are fine — they're still 35 years old and Corteco replacements are still on the shelf — but the urgency is now "do during the next opportunistic front-belly-pan-off session" rather than "book a Saturday in early June for the swap with pre/post UMIK-1 captures." Update `known_issues.md` "Engine Mounts" entry to reflect this once Obs 3 holds for a week of driving.

### "Idle Quality" known-issue — re-promoted to MEDIUM 2026-05-23, may demote again if trajectory holds

Original Apr 30 state was "largely resolved — small residual warm-idle elevation" at LOW. On 2026-05-23 the entry was re-promoted to MEDIUM with the 800-900 P/N reading, scope expanded to include the kickdown (later resolved), and pointed at this work item. **As of 2026-05-25 the steady-state idle has dropped to 750 P/N / 600 D** (50 rpm over spec on P/N, in spec on D), with a clear improving trend. If the next 30-min-warm reading in 3-5 days lands at ~700 P/N or below, the entry should be demoted back to LOW and marked "trajectory-resolved by self-amalgamating tape / hose seating / LLR exercise — proper breather hose order still in flight." If it holds at 750, leave at MEDIUM but note the marginal status. If it bounces back above 800, leave at MEDIUM and execute Steps 2 + 3.

### May 14 acoustic-signature investigation — interpretation refinement worth capturing

`work/audio_exhaust_synth/m119_sideband_diagnosis.md` — the 1×-rev infrasonic line interpretation should get a footnote / addendum: "post-2026-05-22 vacuum-hose fix, the visible idle vibration is gone, consistent with the line being firing-variance-driven (from the loose hoses) rather than block-on-mount rocking. A post-fix UMIK-1 re-capture would confirm." This shifts the M119 diagnosis from "healthy V8 with worn mounts" to "healthy V8 (verbatim), period."

---

## Diagnostic Ladder

In order, cheapest / least-invasive first. Each step is gated on the previous one — stop and reassess when a fault is localised.

### Step 1 — Visual / hand check of throttle linkage (cold, engine off, ~5 min) — **PARTIAL 2026-05-25**

**Why first:** zero cost, zero risk, addresses the highest-probability single artifact (throttle linkage preloaded).

**Method:**
1. Hood open, engine cold. Locate the throttle body (intake side, between MAF and intake plenum).
2. Identify the throttle plate, the idle stop screw (small adjustable screw with locknut on the throttle body casting), and the throttle lever / linkage cluster.
3. Confirm the throttle plate is **fully against** the idle stop screw at rest. Look from above — there should be no visible gap between the lever and the stop.
4. Push the throttle plate gently toward the stop with a finger or screwdriver tip. **It should not move at all.** If it moves even a millimeter, the lever isn't fully seated → linkage is preloaded somewhere.
5. Inspect each cable / rod arriving at the throttle linkage cluster:
   - **Accelerator cable** — should have a small amount of free play at the lever (typically 1–2 mm); the lever should not be lifted off the stop by the cable.
   - **Cruise control actuator rod** — should be at its rest position (actuator vacuum chamber not pressurised); rod should not be pulling the lever.
   - **Kickdown cable** (722.3 — connects to the throttle linkage and runs back to the trans) — should be slack at idle, taut only at WOT. If it's holding the lever lifted, the cable adjustment has drifted or it's been hooked on the wrong notch.
6. Manually open the throttle to ~30 % and release. Lever should snap back **crisply** against the stop with no hesitation, no binding, no "almost-but-not-quite" return.

**Pass criteria:** throttle plate fully seated against the stop, all cables / rods at rest position, snap-back is clean.

**Fail action:** localise which cable / rod is preloading the lever, re-seat or re-adjust to spec. Re-verify warm idle drops back to ~650-700 rpm.

**2026-05-25 status:** Owner performed the throttle plate + cable visual on a cold engine and again on a running engine; nothing visually abnormal observed (plate appears seated, no obvious cable preload, no binding). **One piece still missing: the kickdown cable at the engine end has not been located yet, so the kickdown-cable-position check (sub-step 5c above) is incomplete.** The kickdown cable on a 722.3 M119 runs from the throttle linkage cluster at the engine back to the front of the transmission (usually a thin black sheathed cable, terminating at the throttle lever via a small barrel-and-clip, with the outer sheath anchored to a small bracket on the throttle body or intake manifold). Worth tracing on the next garage session: with the engine off and the throttle lever at idle, the kickdown cable's inner wire should be **slack** with the barrel resting freely at its outer-cable end, not tensioned. If it's preloaded (cable slightly taut at idle, holding the lever lifted), that would explain the high idle even with everything else looking visually fine.

**Throttle-linkage-preloaded hypothesis is partially ruled out** but cannot be fully closed out until the kickdown cable rest position is verified. Move forward with Steps 2 and 3 in parallel; close out Step 1 the next time the cable is located.

### Step 2 — Visual sweep of all reachable vacuum hoses (cold, engine off, ~10 min) — **PARTIAL 2026-05-25**

**Why second:** addresses Obs 1; catches both "a different hose came loose since MB-osat" and "MB-osat connected a hose to the wrong port".

**Method:** with the engine cold and ignition off, visually trace and gently tug-test every vacuum line you can reach:

- **Fuel pressure regulator (FPR)** — small hose on the regulator (passenger side of the fuel rail). Pull off and re-seat to confirm fit.
- **Brake booster** — large hose from the back of the intake plenum to the booster diaphragm. Confirm clamp tight.
- ~~**Trans vacuum modulator**~~ — deprecated since Obs 2 (kickdown) was resolved as normal operation. Modulator only affects shifts, not idle; not on the Obs 1 critical path. Skip unless other shift symptoms appear.
- **Cruise control servo** — vacuum line to the servo (typically on the left fender or near the booster). Cruise functional verification: does cruise engage / hold speed?
- **HVAC vacuum tree** — multiple small hoses at the firewall feeding the HVAC mode actuators. A loose HVAC line wouldn't affect idle much (small leaks), but worth visually confirming.
- **Distributor vacuum advance** — both distributors have vacuum advance cans with hoses to ported-vacuum sources. Confirm both connected.
- **Charcoal canister / EVAP** — purge line from the canister to a manifold port.

**Pass criteria:** every hose seated, no collapsed/cracked hose segments visible, no port left open / capped with finger-pressure-only.

**Fail action:** re-seat or replace the affected hose. Re-verify idle.

**2026-05-25 status:** owner performed a **superficial sweep** — no obvious dangling hoses caught the eye — but **did not work through the named list above hose-by-hose with the tug-test.** This is the highest-priority remaining diagnostic since (a) the throttle-linkage hypothesis has weakened after Step 1, making "another vacuum hose loose" the leading candidate, and (b) it's the same class of fault MB-osat found and partly fixed — finding a third loose hose would be entirely consistent with the data so far. Plan: 10–15 minute systematic walk-through next session, ticking each named hose off the list.

### Step 3 — LLR (idle air control valve) unplug test (warm engine, ~30 seconds) — **NOT DONE 2026-05-25**

**Why third:** localises whether the high warm idle is the LLR being asked to work it can't do (= leak / throttle stop), or the LLR itself being mechanically stuck.

**Method:**
1. Engine fully warm, idling, hood open. Note the current warm idle rpm.
2. Locate the LLR (Leerlaufsteller) — small cylindrical valve mounted to the intake somewhere near the throttle body, with a 2-wire electrical connector.
3. Unplug the electrical connector for **~10 seconds maximum**. Watch the tachometer.
4. Reconnect the connector immediately.

**Outcomes:**
- **Idle drops sharply toward stall, engine struggles to keep running** → LLR is functioning correctly. The high idle is *not* an LLR fault — it's a leak somewhere that the LLR has compensated for by closing. Proceed back to Step 1 / Step 2.
- **Idle barely changes** → LLR is mechanically passing air regardless of command. Stuck-open pintle, contaminated, or wiring fault. Clean or replace.
- **Idle drops slightly but stays elevated** → mixed: partial LLR fault + something else (leak or throttle stop).

**Safety:** do not drive with the LLR unplugged. Reconnect immediately after the observation.

### ~~Step 4 — 722.3 vacuum modulator + kickdown cable verification~~ — **DEPRECATED 2026-05-25** (Obs 2 resolved as normal operation)

The trans vacuum modulator check is dropped — modulator only affects shifts, not idle, and the shift symptom (Obs 2) was reinterpreted as normal 722.3 1st-gear behaviour. **Re-open only if a real kickdown symptom returns** (specifically: kickdown stutter in the *above-1st-gear* region, where it should not happen). Original method retained below for that case.

The kickdown-cable position check folds back into **Step 1** because the cable's effect on the throttle linkage rest position is still relevant to the high-idle question — see Step 1 above for the updated scope.

<details>
<summary>Original Step 4 method (retained for reference if kickdown symptom returns)</summary>

**Method (vacuum modulator):**
1. Locate the vacuum modulator — small can on the side of the transmission (passenger side, near the rear of the trans pan), with a single vacuum hose entering it from the engine and a small adjustment in the centre.
2. Pull the vacuum hose off the modulator. Inspect the inside of the hose for **transmission fluid** — even a smear means the modulator diaphragm is ruptured (fluid is being sucked into the intake via the vacuum line). This is a confirmed fault and requires modulator replacement.
3. With the engine running, apply mouth vacuum (gently!) to the modulator hose. The trans should respond — the modulator influences line pressure. Released vs held should produce slightly different idle characteristics in D.
4. Confirm both ends of the modulator hose are seated and crack-free.

**Method (kickdown cable):**
1. Locate the kickdown cable — runs from the throttle linkage (engine bay) back to the transmission. At the engine end, it connects to the throttle lever cluster with a small barrel-and-clip arrangement.
2. With engine off and throttle at idle (lever against stop), the kickdown cable inner wire should be **slack** with the barrel resting at its outer-cable end, free to move slightly.
3. With throttle held wide open (lever to its full-throttle stop), the kickdown cable inner wire should be fully tensioned and the barrel pulled hard against the cable's full-travel stop.
4. If the cable barrel is mid-travel at idle, the adjustment has drifted — re-position per FSM (adjustment is at the cable's outer-sheath collar at the engine end).

</details>

### Step 5 — If still unresolved: smoke test

If Steps 1-4 are clean and the high idle / kickdown stutter persist, time for a proper smoke test on the intake / vacuum system. Options:
- **DIY** — fog-machine-based or solder-iron-heated baby-oil smoke generator into a sealed intake (block off MAF or intake snorkel, pressurise to 0.3 bar with the smoke source). Visible smoke leaks pinpoint the fault.
- **Borrow** — call MB-osat and ask if they'll let you bring the car back for a 30-min re-smoke on a goodwill basis. Given the symptom appeared within 24 h of the visit, this is a reasonable ask and they should accommodate.

---

## Quick-Reference: Spec Values

| Item | Spec | Source |
| :--- | :--- | :--- |
| Warm idle, P/N, no A/C, no electrical load | **600–700 rpm** | M119.960 FSM, R129 owner's manual |
| Warm idle, D, no A/C, no electrical load | **580–680 rpm** | (above) |
| Idle-up with A/C compressor engaged | **+50–100 rpm** | (above) |
| Vacuum modulator hose inner condition | Dry (no ATF) | 722.3 FSM |
| Kickdown cable position at idle | Slack at outer-cable end | 722.3 FSM |
| Throttle plate at idle | Fully seated against idle stop screw | KE-Jetronic service manual |

---

## Tools

- Bright flashlight + inspection mirror — Step 1 / 2 / 4 visual checks.
- Phone camera with macro — document throttle linkage state before/after any adjustment (so any rollback is straightforward).
- Vacuum gauge — Step 3 / 4 verification of vacuum readings at modulator, intake, FPR.
- Brake cleaner + lint-free cloth — clean LLR pintle if Step 3 implicates the valve.
- LLR cleaning solvent (CRC throttle body / MAF-safe) — if removal-and-clean is the action out of Step 3.

---

## Decision Gates

After each step, the decision is **stop / proceed / refer**:

- **Stop** = symptom resolved, log result and update `known_issues.md` "Idle Quality" entry + this work item's outcome line.
- **Proceed** = symptom persists, move to next step.
- **Refer** = step revealed a fault that's outside the DIY scope (e.g., LLR replacement needed, vacuum modulator failed with fluid intrusion). Add to next MB-osat visit or schedule a dedicated session.

---

## Work Log

| Date | Status | Notes |
| :--- | :--- | :--- |
| 2026-05-23 | Created | Three observations captured (high warm idle, kickdown glitch, smoothness improvement). Hypothesis: throttle linkage / vacuum / trans modulator artifact from the 2026-05-22 MB-osat visit. Diagnostic ladder defined. **Next:** execute Step 1 (throttle linkage visual check) on the next dry-weather garage session. |
| 2026-05-25 (AM) | Step 1 partial; Obs 2 resolved; Steps 2–3 still open | **Obs 2 (kickdown glitch) resolved as misread of normal 722.3 1st-gear behaviour** — further driving showed clean kickdown both deep in the 1st-gear engagement zone and above it; the original 2/4 "glitch" events were almost certainly WOT punches at the 1st-gear edge where the trans correctly spends a few hundred ms in 1st before upshifting to 2nd. Removed from `docs/known_issues.md`. **Step 1 (throttle linkage visual / hand check) executed partially** — engine off and engine running, nothing visually abnormal on the throttle plate, idle stop, accelerator cable, or cruise rod; throttle-linkage-preloaded hypothesis substantially weakened. **One sub-step still open:** the kickdown cable at the engine-end has not been located yet, so its rest-position check (slack at idle, taut at WOT) is incomplete — fold this in next garage session before fully closing Step 1. **Step 2 (vacuum hose sweep) done superficially** — no obvious dangling hoses seen — but the named-hose tug-test list was not worked through systematically. **Now the highest-priority remaining diagnostic** since the leading hypothesis after Step 1 is "another loose vacuum hose". **Step 3 (LLR unplug test) not done** — should be done same session as the Step 2 systematic walk-through; takes ~30 s with a warm engine. **Step 4 deprecated** following Obs 2 resolution. **Working hypothesis posture:** leading candidates are now (i) another loose vacuum hose MB-osat didn't catch / one that's worked loose since, (ii) sticky/contaminated LLR exposed now that the chronic leaks aren't masking it. Both addressed by completing Steps 2 + 3. |
| 2026-05-25 (PM, after 30-min drive + a few hard accelerations) | Obs 1 dropped to 750 P/N / 600 D; urgency lowered | **New steady-state measurement: 750 rpm P/N, ~600 rpm D, warm engine.** Down from 800-900 P/N two days ago — a ~150 rpm improvement with no intervention beyond driving the car. P/N is now only 50 rpm over the 700 rpm spec max; D is in spec (580-680 range). The P/N → D drop of ~150 rpm matches the healthy 722.3 converter-drag signature, which **weakens the mechanically-stuck-LLR hypothesis** (a stuck-open LLR would tend to elevate both positions roughly equally; closed-loop idle control is clearly working). **Leading hypothesis now:** a small residual leak — most likely the silicone-tape 5th-cyl breather + possibly one more not-yet-found hose — that the LLR is largely compensating for. **Plausible self-resolving drivers** for the improving trajectory: (a) silicone tape on the breather hose has finished self-amalgamating over the first 1-2 hot soak cycles, (b) MB-osat-re-seated vacuum hoses have bedded in with thermal cycling, (c) the LLR pintle is freeing up from regular use. Any/all could be contributing. **Action:** Steps 2 + 3 de-prioritised but still on the books. The already-planned proper 5th-cyl breather hose order (Priority 2 in `docs/parts_to_order.md`) is now the most likely intervention to land idle cleanly in spec. **Next measurement gate:** one more 30-min-warm reading in 3-5 days at the same conditions to see where the trajectory flattens — that data point will determine whether to demote `known_issues.md` "Idle Quality" entry back to LOW. |

---

## References

- `docs/diary/2026-05.md` 2026-05-22 entry — MB-osat visit narrative including the vacuum-hose + 5th-cyl-breather findings that triggered the post-visit observations.
- `docs/known_issues.md` "Idle Quality" entry — current open-issue state for the warm-idle elevation; will be updated to reference this work item.
- `work/rough_idle_debug/README.md` — predecessor work item for the Apr 30 misfire investigation; largely closed by the May 22 vacuum-hose finding. Useful background on the M119 KE-Jetronic idle control architecture (LLR, EHA, AFM, EZL).
- `work/audio_exhaust_synth/m119_sideband_diagnosis.md` — May 14 acoustic-signature analysis; the 1×-rev infrasonic line interpretation should be revisited in light of Obs 3 (smoothness improvement post vacuum-hose fix).
- `r129_data/SKILL.md` — search for "722.3 vacuum modulator", "kickdown cable adjustment", "Leerlaufsteller M119", "KE-Jetronic idle stop adjustment" for FSM extracts.
