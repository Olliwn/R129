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

### Central Locking (PSE) -- Fuse 6 Replaced, PSE Still Untested
**Status:** INVESTIGATING | **Priority:** MEDIUM | **Since:** 2026-03-13

Pneumatic pump completely silent since purchase. Trunk fuse holder F20 (P/N A 129 540 04 50, 6 torpedo positions) **fuse 6 (8A white, bottom position) was blown** (found 2026-03-30). **Fuse replaced 2026-04-03 — fuse is holding.** Replacing the fuse immediately brought the power antenna and IRCL module back to life, confirming fuse 6 powers multiple trunk-area systems. PSE central locking actuation has not yet been explicitly tested post-fuse.

**Next:** Test PSE central locking — lock/unlock from key, interior switch, and IRCL remote.

[work/pse_central_locking/README.md](../work/pse_central_locking/README.md)

### Battery / Parasitic Drain
**Status:** INVESTIGATING | **Priority:** MEDIUM | **Since:** 2026-03-27 | **Updated:** 2026-04-03

Voltage drops ~13V to ~12V in ~2 days idle. Battery is Varta Silver Dynamic H3 (100Ah, 890A CCA), manufactured August 2025. Experienced at least one deep discharge. Trickle charger keeping it alive.

**CCA test performed (2026-04-03):** Owon HDS242 cranking waveform at battery terminals (2V/div, 200ms/div). Resting voltage ~12.4V. Cranking dip ~4V to approximately 8.5V. **Ambient temperature was 3°C** — cold soak significantly worsens the dip. Engine caught immediately (very short crank). Assessment: borderline at 3°C but not alarming. Re-test in warmer conditions (~15-20°C) for a fair comparison.

**IRCL (Pin 12) confirmed alive** after fuse 6 replacement — 1 blink, no faults. ATA (Pin 11) confirmed dead (genuine module fault, deprioritized — see ATA entry below).

**Next:** Re-test CCA in warm weather. Parasitic draw test still needed to identify the drain source. Prime suspect now is the dead ATA module (static glow on Pin 11 = constant small draw?).

### Power Antenna -- Functional, One Segment Slightly Stiff
**Status:** MOSTLY RESOLVED | **Priority:** LOW | **Since:** 2026-03-29 | **Updated:** 2026-04-03

**Root cause was blown trunk fuse 6.** After fuse replacement (2026-04-03), antenna motor immediately came alive. Upper segments extended/retracted with radio. Two lowest segments were initially stuck — freed with WD-40 penetrant and light manual assist. Antenna now fully operational. One segment is not perfectly smooth but does not get stuck.

**Follow-up:** Apply silicone spray (aerosol) into the mast tube for long-term lubrication. Silicone spray added to `parts_to_order.md`.

### Windshield Wiper / Washer
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-15

Wiper does not consistently park correctly. Washer fluid only from 2 of 4 nozzles.

[work/wiper_system/README.md](../work/wiper_system/README.md)

### Engine Mounts
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-13

Slight vibration at 700-800 RPM idle. Corteco replacement mounts received (2026-03-30).

[work/engine_trans_mounts/README.md](../work/engine_trans_mounts/README.md)

### Engine Belt Noise -- Glazed Belt Confirmed
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-21 | **Updated:** 2026-04-03

Squeals/chirps on startup. **V-belt friction spray test (2026-04-03): noise disappeared instantly.** This confirms the belt surface is glazed and slipping — not a bearing issue. Spray is a temporary fix only.

**Next:** Replace V-belt set. Confirm belt P/Ns with MB-osat (M119 uses multiple V-belts). Already listed in `parts_to_order.md` Priority 4 under inspect-first — now confirmed as needing replacement.

### Headlight Switch Knob Worn
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02

The headlight switch rotary knob is worn out / soft. Feels mushy and imprecise. Needs replacement or refurbishment.

### Seat Adjustment Panels (Door) Loose
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02 | **Updated:** 2026-04-03

Both door seat control panels (P/N 129 820 71 10, "W.-Germany") loose at the bottom. **Cause identified (2026-04-03):** front lower plastic locating clip broken (age embrittlement). Metal mounting clips at corners are intact. Biltema double-sided tape attempted — failed. 

**Next:** Source proper 3M VHB trim tape, or fabricate a fix by cutting remaining plastic and repurposing the existing screw mount point for a new clip.

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
