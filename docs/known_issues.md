# AOK912 -- Known Issues

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | VIN: WDB 129066 1F 044414

*Current state of confirmed defects. History and investigation details are in the [monthly diaries](diary/). Detailed work plans are in the linked `work/` READMEs.*

---

## OPEN

### ADS System (Suspension) -- OVP Relay Re-Solder Pending Test
**Status:** INVESTIGATING | **Priority:** HIGH | **Since:** 2026-03-13

Two independent subsystems:
- **Adaptive Damping (N51):** Module confirmed alive (1 blink, 2026-03-23). Console switch and Fahrzeugniveau switch both functional. Front Right accumulator sphere is ruptured/hydro-locked.
- **Level Control (Niveauregulierung):** Rear height remains static. Phase 1 flush completed (4L ZH-M, fluid clear), air entrapment confirmed. System went offline mid-flush (2026-03-29).
- **Root cause found (2026-03-30):** OVP relay has 3-4 cracked solder joints (thermal fatigue). Worst on 87L pin (N51 power feed). Re-soldered 2026-03-31 -- **awaiting reinstall and test.**
- **Cluster swap confirmed:** Indicator strip has no ADS symbol -- non-ADS cluster. Odometer accuracy in question.

[work/ads_diagnostic/README.md](../work/ads_diagnostic/README.md) | [work/ads_blink_reader/README.md](../work/ads_blink_reader/README.md)

### Central Locking (PSE) -- Fuse #6 Replaced, Awaiting Test
**Status:** INVESTIGATING | **Priority:** MEDIUM | **Since:** 2026-03-13

Pneumatic pump completely silent. Rear fuse block **fuse #6 found blown** (2026-03-30). All 8 torpedo fuses replaced with copper/ceramic units. Awaiting test: if PSE pump activates with new fuse, issue is resolved. If fuse blows again, short circuit downstream.

[work/pse_central_locking/README.md](../work/pse_central_locking/README.md)

### Battery / Parasitic Drain
**Status:** INVESTIGATING | **Priority:** HIGH | **Since:** 2026-03-27

Voltage drops ~13V to ~12V in ~2 days idle. Battery is Varta Silver Dynamic H3 (100Ah, 890A CCA), manufactured August 2025. Experienced at least one deep discharge. Trickle charger keeping it alive. Candidates: PSE circuit, ATA/IRCL modules (static glow on X11), stuck relay.

**Next:** Test CCA/internal resistance, then parasitic draw test if battery is healthy.

### Power Antenna -- Stuck Extended
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-29

Hirschmann antenna stuck fully raised. No motor activity on radio on/off with either old Sony or new Becker. Pre-existing condition (not a BE2210 wiring issue). Likely dead motor, stuck relay, or blown fuse.

**Next:** Manual reverse-polarity test at motor connector.

### Windshield Wiper / Washer
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-15

Wiper does not consistently park correctly. Washer fluid only from 2 of 4 nozzles.

[work/wiper_system/README.md](../work/wiper_system/README.md)

### Engine Mounts
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-13

Slight vibration at 700-800 RPM idle. Corteco replacement mounts received (2026-03-30).

[work/engine_trans_mounts/README.md](../work/engine_trans_mounts/README.md)

### Engine Belt Noise
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-21

Squeals/chirps immediately after cold start. Needs diagnosis (slipping belt vs. bad tensioner bearing).

### Hardtop Fitment
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-13

Front latches bind from excess headliner thickness. Requires manual pull-down assist.

### Paint & Body
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-15

Minor paint cracking on rear fender (below trunk lid). Small deep scratch on aluminum hood. Bare steel behind front wheels needs rust-prevention touch-up.

### Instrument Cluster Faults
**Status:** OPEN | **Priority:** MEDIUM | **Since:** 2026-03-18

Clock adjustment stuck/locked. Temperature LCD delaminated/washed out. Both to be addressed during Phase 3 cluster pull. Cluster is a non-ADS swap -- no ADS warning lamp symbol on indicator strip.

---

## RESOLVED

*(None yet -- issues will be moved here with date and one-line resolution when fixed.)*
