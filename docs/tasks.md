# AOK912 -- Active Tasks

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

*Work queue for open engineering and maintenance tasks. Detailed procedures live in the linked `work/` READMEs. Known issues are tracked separately in [known_issues.md](known_issues.md).*

---

## HIGH Priority

### 13. Battery Health Verification
Measure internal resistance and cranking voltage drop (Owon HDS242). Varta H3, 100Ah, 890A CCA, manufactured Aug 2025. One deep discharge event. If CCA is marginal → replace at Motonet.
**Method:** V_oc vs V_load under high beams (target R_internal <25 mΩ). Cranking voltage must hold >10V.

### 10. M119 Upper Timing Components & Valve-Cover Service
Valve cover-off inspection of upper timing chain guides (plastic, brittle — replacement guides on hand from MB-osat). Replace valve cover gaskets, spark plug tube seals, breather hose, spark plugs. **Oiler-tube upgrade deprecated** — AOK912 (1991-09 build) should already have factory aluminum oiler tubes (P/N 119 187 00 87); plastic didn't appear until ~1993. Pre-inspect via oil filler hole before committing to any tube work. URO aftermarket aluminum (the earlier recommendation) dropped — European forum feedback negative on casting/O-ring quality.
**Work plan:** [work/m119_upper_timing/README.md](../work/m119_upper_timing/README.md)

### 14. Predictive Electronics Maintenance -- Capacitor & Solder Joint Audit
Prompted by OVP relay failure. Inspect/reflow solder joints and electrolytic capacitors in N4/1 (E-Gas), MAS (fuel pump), instrument cluster, and EZL (thermal paste refresh). See hit list with ranked priorities in [work/electronics_audit/README.md](../work/electronics_audit/README.md).

### 11. Baseline Service -- Unknown History
Full consumables flush: engine oil, ATF, brake fluid, coolant, power steering fluid. Filters, spark plugs, belts, hoses. 30-item checklist.

**Engine oil sub-plan refined 2026-04-18:** Apr 18 dipstick check (light honey amber at ~1800 km of owner-driven use, no top-up) indicates the previous owner did a change immediately before the sale and the engine has low blowby. Oil change therefore **demoted from urgent to normal schedule** (end of season, or ~8 000 km from the previous-owner change, whichever first). No double-drain, no flush additive. Next change will be paired with: (a) used-oil analysis via Oelcheck (~€30–40), (b) filter element removal and post-drain inspection / cutting for particulate, (c) installation of a magnetic sump plug as a passive ferrous-particle early-warning. Track darkening rate with periodic dipstick photos (same paper towel, same lighting) at ~500 km intervals as a cheap ongoing engine-health metric. See `docs/engine_condition_baseline.md`.

**Work plan:** [work/baseline_service/README.md](../work/baseline_service/README.md)

### 4. Suspension Refresh (ADS & Mechanical)
Front: replace LCA complete units. Rear: replace 5-link set + squeak bushings. Steering: replace damper + idler arm bushing. ADS: replace nitrogen accumulators if needed after OVP fix.
**Work plan:** [work/ads_diagnostic/README.md](../work/ads_diagnostic/README.md)

---

## MEDIUM Priority

### 5. Central Locking (PSE)
Fuse #6 (8A white, F20 position 6) found blown (2026-03-30). Not yet replaced. Replace all 6 torpedo fuses with copper/ceramic units. If pump activates → resolved. If fuse 6 blows again → investigate short (disconnect PSE pump to isolate).
**Work plan:** [work/pse_central_locking/README.md](../work/pse_central_locking/README.md)

### 6. Engine Bay Maintenance (Intake, Filters & Fluids)
Air filters: DONE (2026-03-30). Remaining: replace intake hoses (L: A 119 094 00 82, R: A 119 094 01 82), power steering flush + filter, coolant top-up.
**Work plan:** [work/power_steering_flush/README.md](../work/power_steering_flush/README.md)

### 9. Center Console Refresh
Wood polish, switch cleaning/re-lubrication, RPi5 cable routing (AUX, CAT6, power). Three jobs, one disassembly.
**Work plan:** [work/center_console_refresh/README.md](../work/center_console_refresh/README.md)

### 8. Hood Insulation Pad Replacement
Part received (2026-03-30). Pending: remove old adhesive from aluminum hood, then install.
**Work plan:** [work/hood_pad_replacement/README.md](../work/hood_pad_replacement/README.md)

---

## LOW Priority

### 1. Windshield Wiper Parking Issue
Lubricate mechanism first, check linkage nuts, then investigate N10 relay.
**Work plan:** [work/wiper_system/README.md](../work/wiper_system/README.md)

### 2. Washer Fluid Nozzles
Clean and unclog nozzles. Inspect fluid lines.
**Work plan:** [work/wiper_system/README.md](../work/wiper_system/README.md)

### 3. Paint Inspection (Rear Fender & Hood)
Test hood with magnet (aluminum vs steel). Source OEM touch-up paint (744 Brilliant Silver Metallic, confirmed via VIN decode 2026-04-01). Inspect once weather improves.

---

## Backlog (no active work, park for later)

### Microphone integration (RPi5 / car audio)  ⚠ decision needed before Task #9 (Center Console Refresh)
Goal: get a microphone into the RPi5 audio stack, primarily so phone calls routed through CarPlay can use the car's speakers + an in-cabin mic (hands-free). Secondary: future on-Pi voice features if the iPhone-as-primary-AI stance ever changes.

**Why this blocks the dash-out:** the mic cable has to be pulled during Task #9 together with the AUX/CAT6/power loom. Running trim twice is unacceptable. A decision on *where the mic lives* and *what cable it needs* must be locked in before the console is opened.

**Hardware options considered (2026-04-16):**

| Option | Mic | Cable to Pi | Mounting | Notes |
| :--- | :--- | :--- | :--- | :--- |
| A. ReSpeaker 2-Mic Pi HAT + remote analog capsule | 2× MEMS on HAT *or* 3.5mm TRRS external | Short to HAT, then external 3–4m shielded analog for remote capsule | HAT in cubby, capsule in headliner near dome light | Best voice-tuned option, hardware AEC/DOA, occupies GPIO header. Analog run is the weak point over 3m. |
| B. I2S MEMS (INMP441 / SPH0645) direct to Pi GPIO | Digital MEMS | 4-wire I2S (BCLK/LRCLK/DATA/GND + 3.3V), max ~1–2m reliable | Capsule in headliner or A-pillar | Cheapest, cleanest digital signal, **but I2S length limit is marginal for headliner → cubby run**. Needs ferrite + twisted pairs. Software AEC only. |
| C. USB conference mic puck | USB | 3–4m USB (active cable / hub if needed) | On-dash or headliner | Plug-and-play. PipeWire sees it as a standard input. Aesthetically least OEM. |
| D. Automotive OEM-style electret + USB sound card | Analog electret (e.g. MB gooseneck replica) | 3–4m shielded analog → USB ADC in cubby | Near dome light / A-pillar, OEM look | Most period-correct visually. Needs a decent USB ADC (e.g. Behringer UCA202-class) and bias for the electret. |

**Software path (common to all options):**
- PipeWire is already present on the Pi. Add `module-echo-cancel` (WebRTC AEC) *unless* the mic hardware provides its own (ReSpeaker does).
- LIVI / Carlinkit path: the dongle exposes an audio sink + source pair to CarPlay; the iPhone expects mic audio on the source. Needs a PipeWire route: `alsa_input.<mic>` → (AEC) → `carplay_source`.
- Car-audio playback path is unchanged (already routed via BE2210 AUX per Task #9 plan).

**Placement constraints:**
- Best SNR: headliner near dome light, aimed down at driver.
- A-pillar works but picks up more HVAC noise.
- Dash-top is worst for echo (speakers below, glass in front).
- Whichever chosen, the cable run is: mic location → down A-pillar → along headliner → under dash → into center stack void → into RPi5 cubby.

**Current leaning (revised 2026-05-02 evening — mic location locked to front cubby):**
- **Mic location locked: front cubby, co-located with the OLED display, behind the fascia.** Decision rationale: the cable path simplifies dramatically — single ~2 m run alongside C16 (HDMI) / C17 (display USB) / C18 (cabin-node USB-CDC) in Bundle G of the §5.8 loom, all going front cubby ↔ rear passenger cubby (Pi). No headliner / A-pillar trim work, no separate cable run.
- **Acoustic caveat to accept:** mid-dash position is closer to the HVAC vent than the headliner / A-pillar would be. Voice quality will be acceptable for hands-free CarPlay phone calls (the primary use case here) but not studio-grade. Pick hardware with software/HW AEC.
- **Hardware leaning revised:** **Option C (USB conference mic puck)** is now primary — single 2 m USB cable, plug-and-play, no GPIO conflict with the Alps RKJXT1F42001 joystick wiring (which already takes the Pi GPIO header for 7 inputs + GND). Aesthetics aren't a concern because the mic capsule lives behind the display fascia, not visible in the cabin.
- **Option A (ReSpeaker 2-Mic Pi HAT + analog electret in front cubby, ~2 m shielded analog up to the HAT in the rear cubby)** remains a viable fallback if Option C's voice quality disappoints — better hardware AEC, but adds GPIO arbitration with the Alps joystick (the joystick uses 7 GPIOs; ReSpeaker HAT uses 6 — potential overlap on at least 2 pins, would need pin-by-pin check).
- Rejected: Option B (I2S length limit, even at the new 2 m it's marginal), Option D (USB sound card + analog electret = same complexity as A without the AEC win).

**Decisions to finalize before dash-out (status 2026-05-02 evening):**
1. ~~Pick option A / B / C / D.~~ → **Option C primary, Option A fallback.** Final hardware order can wait, but cable path is locked.
2. ~~Decide mic physical location (headliner dome vs. A-pillar vs. visor).~~ → **Front cubby, behind the OLED display fascia. Locked.**
3. ~~Spec the exact cable type + length for that option.~~ → **Shielded USB 2.0 A-to-C 2 m (Option C) or shielded analog pair 2 m (Option A fallback). Joins Bundle G of the §5.8 loom.**
4. ~~Confirm no GPIO conflict with the Alps joystick wiring~~ → **N/A for Option C (USB-only). For Option A fallback, pin-by-pin GPIO arbitration check still required.**
5. **Still open:** order the mic hardware. Worst-case insurance: pull a fish-string in the Bundle G sleeve so the eventual USB cable can be drawn through later without re-opening the trim.

### Radar cockpit — MIMO mmWave front/rear view on the RPi5 OLED  📅 Winter 2026–27
Two automotive MIMO mmWave radars (one behind each bumper) feeding a custom amber-on-black top-down radar scope on the 5.5" OLED. Zero external vehicle modifications — mmWave penetrates painted plastic bumpers. Replaces the originally-considered rear camera (rejected: no invisible R129 mount) and ultrasonic sensors (viable but still needs 4 bumper holes).

**Key insight:** no custom signal-processing chain to build — TI's free chip firmware (IWR6843AOPEVM or AWR1843BOOST) runs the full MIMO DSP pipeline (range-FFT, Doppler-FFT, CFAR, AoA, tracking) on-chip and streams a point cloud over UART. Pi-side work is purely parsing + PyQt5 visualisation, leveraging existing open-source Python libraries (ibaiGorordo / pymmw / OpenRadar). Estimated MVP effort: 3–4 weekends.

**Parked for Winter 2026–27.** Summer 2026 queue is full (baseline service, center console refresh, audio upgrade, electronics audit). Revisit October/November 2026.

**Work plan:** [work/radar/README.md](../work/radar/README.md)

### In-car AI assistant access
CarPlay only surfaces OpenAI's ChatGPT today; no CarPlay build exists for Gemini, Grok, or Claude (the ones with active subscriptions). A custom PyQt5 "AI" view on the Pi was considered and **rejected** because a native client wouldn't share the real web/app session history, which is the main reason to return to a chat (picking up older threads when context changes).

**Preferred workarounds when this becomes worth pursuing:**
- Browser session to `claude.ai` / `gemini.google.com` / `grok.com` inside a Pi-side chromium tab, reusing the real logged-in session (and therefore the persistent chat history).
- Or a Cursor session on Linux with a dedicated "in-car" workspace/repo that acts as long-term context storage (notes, ongoing threads, vehicle state). More flexible than a browser tab, plus gives file-level memory Cursor can search.

**Revisit when:** one of Google/xAI/Anthropic ships CarPlay support, or the need for quick in-car AI use becomes frequent enough to justify the browser-tab / Cursor-workspace path.

---

## Finnish Registration (Admin)

Autovero paid (€837.05, 2026-03-27). Waiting for rekisteröintilupa. Full vehicle insurance (liikennevakuutus + kasko) based on VIN is already active. Then: siirtolupa → rekisteröintikatsastus → ensirekisteröinti → Finnish plates.
