# AOK912 -- Known Issues

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

*Current state of confirmed defects. History and investigation details are in the [monthly diaries](diary/). Detailed work plans are in the linked `work/` READMEs.*

---

## OPEN

### ADS System (Suspension) -- Hydraulic/Mechanical Faults Remaining
**Status:** OPEN | **Priority:** HIGH | **Since:** 2026-03-13

Electrical side resolved:
- **OVP Root Cause Fixed (2026-04-01):** OVP relay 87L pin re-soldered. N51 module online, diagnostic bus stable. Only code 14 (steering calibration) present.

Damping side now working:
- **Adaptive Damping (N51):** Sport/Comfort modes CONFIRMED WORKING on first drive (2026-04-02). All four accumulator spheres healthy — inspector independently commented on smooth ride. Earlier FR stiffness was air-lock.

Level control still needs work:
- **Level Control (Niveauregulierung):** Rear height remains static. Fahrzeugniveau switch STUCK (red LED permanently on, toggle has no effect — new symptom post-OVP-fix). Flush completed. Next: manual valve test (disconnect ARB linkage, move lever manually on jack stands).
- **Cluster swap confirmed:** Indicator strip has no ADS symbol -- non-ADS cluster (option 216 factory ADS confirmed via lastvin.com).

⚠️ **URGENT — Dust boots missing lower sections.** Chrome ADS shock shafts exposed to road debris. Order and install A 129 323 01 92 (×4) before further driving.

[work/ads_diagnostic/README.md](../work/ads_diagnostic/README.md) | [work/ads_blink_reader/README.md](../work/ads_blink_reader/README.md)

### Central Locking (PSE) -- FUNCTIONAL (Passenger Side), Driver Lock Disconnected
**Status:** PARTIALLY RESOLVED | **Priority:** LOW | **Since:** 2026-03-13 | **Updated:** 2026-04-05

**Root cause was blown trunk fuse 6** (replaced 2026-04-03). PSE pump confirmed alive on 2026-04-04 (first actuation from driver key). System progressively improved with repeated use as seized pneumatic valves freed up.

**2026-04-05:** Full central locking now operational from **passenger side key** — both keys work, red/green dashboard lights, all doors lock/unlock, pump runs reliably. System is fully functional.

**Driver side key lock:** Both keys turn freely (after WD-40 lubrication) but do **not** actuate the lock mechanism at all — no click, no latch movement, no PSE signal. Diagnosis: **lock cylinder coupling/linkage disconnected or broken.** The metal rod connecting the lock cylinder to the door lock mechanism has likely detached (brittle plastic retaining clip, common R129 age issue). Requires driver door panel removal to inspect and reconnect.

**IRCL remote — DEPRIORITIZED (2026-04-06):** Both key fobs tested with fresh CR2025 batteries. Key 1: IR LED fired 2-3 times then stopped (hardware fault). Key 2: dim IR output, tested on car — **no response.** Either transmission too weak or rolling code out of sync after years of disuse. Re-pairing requires MB Star Diagnosis tool (~€200+ dealer visit) — not cost-effective for a convenience feature. IRCL module on car is healthy (Pin 12 = 1 blink).

**Decision:** IRCL repair abandoned. The planned **BLE sentry node (nRF5340)** will implement phone-based keyless lock/unlock by driving the PSE signal directly. More secure (BLE bonded encryption vs 1991 IR), no line-of-sight required, and already part of the telemetry architecture. Requires identifying the IRCL→PSE signal wire during door panel removal.

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

### Engine Mounts
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-13

Slight vibration at 700-800 RPM idle. Corteco replacement mounts received (2026-03-30).

[work/engine_trans_mounts/README.md](../work/engine_trans_mounts/README.md)

### Crankshaft Position Sensor — Active Fault (EZL Code 17)
**Status:** PARTS ORDERED | **Priority:** HIGH | **Since:** 2026-04-04

Pin 8 Code 17 returns after every drive. Sensor is marginal/intermittent — car starts and runs but EZL falls back to base timing map. A full failure will cause a no-start. **Topran 408 205 ordered from Autodoc 2026-04-04** (€50.99, ETA ~1 week). Installation is a 5-minute job (6mm Allen bolt, rear of engine near bellhousing). No calibration required.

### Valve Cover Gaskets & Spark Plug Tube Seals — Oil in Wells
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-04-05

6 of 8 spark plug wells contain oil. Only front cylinders (1, 5) are dry. Both banks affected. Root cause: degraded spark plug tube seals allowing valve cover oil to leak into the wells. Oil is external only — all combustion chambers healthy (clean electrode tips on all 8 plugs). Risk: oil eventually soaks plug wire boots causing misfires/arcing.

**Fix:** Replace both valve cover gasket sets + 8× spark plug tube seals. Combine with Priority 2 timing chain guide inspection (valve covers must come off for both jobs). Parts needed — add to MB-osat order.

### Engine Belt Noise -- Glazed Belt Confirmed
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-21 | **Updated:** 2026-04-03

Squeals/chirps on startup. **V-belt friction spray test (2026-04-03): noise disappeared instantly.** This confirms the belt surface is glazed and slipping — not a bearing issue. Spray is a temporary fix only.

**Next:** Replace V-belt set. Confirm belt P/Ns with MB-osat (M119 uses multiple V-belts). Already listed in `parts_to_order.md` Priority 4 under inspect-first — now confirmed as needing replacement.

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

### ADS Factory Origin Unknown
**Status:** RESOLVED | **Resolved:** 2026-04-01

Lastvin.com factory build data shows option **216** (self-leveling suspension all-around with ADS). The earlier mbdecoder.com decode missed this code. All ADS hardware is original factory equipment. The non-ADS instrument cluster is a confirmed previous-owner swap.
