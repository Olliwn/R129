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

### Central Locking (PSE) -- Trunk Fuse 6 Blown, Awaiting Replacement
**Status:** INVESTIGATING | **Priority:** MEDIUM | **Since:** 2026-03-13

Pneumatic pump completely silent since purchase. Trunk fuse holder F20 (P/N A 129 540 04 50, 6 torpedo positions) **fuse 6 (8A white, bottom position) found blown** (2026-03-30, confirmed by photo 2026-04-01). **No fuses replaced yet** -- all 6 positions still have original aluminum torpedo fuses; copper/ceramic replacements on hand but not installed. **Fuse identification caveat (2026-04-01):** the fuse designation card in the data repository (P/N 129 545 25 00) is for the **post-facelift F4 box** and does NOT apply to this 1991 car. Forum evidence (BenzWorld, 1995 SL500) suggests pre-facelift F20 fuse 6 = central locking, consistent with the original diary hypothesis. However, this is unverified from factory documentation. The correct F20 assignments should be read from the fuse box cover or the ETM.

**Next:** Replace fuse 6, test PSE actuation. If fuse blows immediately, disconnect PSE pump connector and retry to isolate a shorted pump motor. Also re-test ATA (X11/4 Pin 11) -- the "dead ATA module" from March may have been unpowered due to a related trunk fuse.

[work/pse_central_locking/README.md](../work/pse_central_locking/README.md)

### Battery / Parasitic Drain
**Status:** INVESTIGATING | **Priority:** HIGH | **Since:** 2026-03-27

Voltage drops ~13V to ~12V in ~2 days idle. Battery is Varta Silver Dynamic H3 (100Ah, 890A CCA), manufactured August 2025. Experienced at least one deep discharge. Trickle charger keeping it alive. Candidates: PSE circuit, ATA/IRCL modules (static glow on X11), stuck relay. **Note (2026-04-01):** The "ATA/IRCL static glow" observed on March 18/26 may have been caused by trunk fuse 6 being blown (module unpowered). Re-test ATA blink codes after fuse replacement before concluding module fault.

**Next:** Test CCA/internal resistance (still not done as of 2026-04-02 — either Owon scope cranking test or free Motonet counter test). Then parasitic draw test if battery is healthy. Re-test ATA/IRCL blink codes after trunk fuse 6 replacement. **Full X11/4 diagnostic sweep should be run once fuse 6 is replaced** — all ECUs should then be powered and give valid blink codes.

### Power Antenna -- Stuck Extended
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-03-29

Hirschmann antenna stuck fully raised. No motor activity on radio on/off with either old Sony or new Becker. Pre-existing condition (not a BE2210 wiring issue). Antenna is factory-fitted (option 538 includes antenna + speakers, confirmed lastvin.com 2026-04-01). Likely dead motor, stuck relay, or blown fuse. **Note (2026-04-01):** Forum evidence suggests the power antenna may share trunk fuse 6 with central locking on pre-facelift F20. If antenna resumes working after fuse 6 replacement, the blown fuse was the root cause for both PSE and antenna failures.

**Next:** Observe antenna behavior after trunk fuse 6 replacement. If still dead, do manual reverse-polarity test at motor connector.

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

Squeals/chirps immediately after cold start. Needs diagnosis (slipping belt vs. bad tensioner bearing). **First aid:** Try belt friction spray (on hand) to determine if squeal is slipping belt vs. bearing. If spray eliminates squeal → belt tension or glazed belt. If squeal persists → bearing.

### Headlight Switch Knob Worn
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02

The headlight switch rotary knob is worn out / soft. Feels mushy and imprecise. Needs replacement or refurbishment.

### Seat Adjustment Panels (Door) Loose
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02

Both driver and passenger door seat adjustment panels are loose at the bottom. Clips/fasteners likely broken or missing. Inspect mounting method and source replacement clips or fabricate a fix.

### Front Grille — Clean & Polish
**Status:** OPEN | **Priority:** LOW | **Since:** 2026-04-02

Front grille needs thorough cleaning and polishing (Autosol Metal Polish on hand). Cosmetic item, no urgency.

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

## RESOLVED

### ADS Factory Origin Unknown
**Status:** RESOLVED | **Resolved:** 2026-04-01

Lastvin.com factory build data shows option **216** (self-leveling suspension all-around with ADS). The earlier mbdecoder.com decode missed this code. All ADS hardware is original factory equipment. The non-ADS instrument cluster is a confirmed previous-owner swap.
