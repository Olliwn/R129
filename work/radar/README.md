# Radar Cockpit — MIMO mmWave Front/Rear View on the RPi5 OLED

**Status:** 🔵 **Parked for Winter 2026–27.** Design captured; not on the 2026 summer work queue. Revisit once the baseline-service + center-console-refresh + audio-upgrade queue clears.

**Vehicle:** 1991 Mercedes-Benz 500 SL (R129) | Primary integration target: RPi5 in the upper cubby, existing PyQt5 UI stack (see `UI_rpi5/`).

---

## The Vision

Two automotive MIMO mmWave radars — one behind the front bumper, one behind the rear bumper — feeding a custom **top-down radar cockpit** on the 5.5" OLED. Amber-on-black to match the VDO cluster and BE2210. Small vector R129 silhouette in the centre, live radar returns plotted around it at ~20 Hz, range rings at 1 / 2 / 3 / 5 m, tracked objects persisted with short fading velocity-vector trails. Always-on (not just in reverse) so it doubles as a live traffic-awareness display at speed.

Zero external modifications to the car — mmWave penetrates painted plastic bumpers cleanly. No holes, no pods, no surface-mounted devices. Aesthetic win that the rejected camera options couldn't touch.

## Why Not Camera / Ultrasonic (Decision Record)

Summer 2026 investigation (see April 2026 diary + this conversation's thread) ruled these out in order:

1. **Rear camera.** Dropped because no invisible mounting location exists on the R129's trunk-lid/plate-recess composition. Plate-bolt replacements don't fit R129 pod geometry. Surface-mounted box ruins the Sacco rear-end lines. Camera was "wow factor" not need, and wow factor with visible mounting hardware is negative value.
2. **Ultrasonic (4× pucks in rear bumper valance).** Works, period-plausible (OEM fitted these to R129 facelifts from 1998), ~€40 total. **Still requires 4× 18 mm holes in the valance.** Reversibility is "replace the valance", which is real but imperfect.
3. **Radar behind bumper.** Penetrates painted plastic with no visible modification. OEMs have converged on this since ~2018. Signal processing is done on-chip by the radar's own DSP; the Pi side is purely parsing + visualisation. Right answer.

## Architecture — The Three-Layer Stack

The single biggest insight: we are **not building a signal-processing chain**. TI's chip firmware does it. The work lives at the visualisation layer.

```
┌─────────────────────────────────────────────────┐
│  Layer 3: Visualisation  (OUR work, PyQt5)      │  ← Days–weeks
│  - Top-down cockpit scope, amber/black          │
│  - Range rings, tracked-target blobs            │
│  - Velocity-based colour, fading trails         │
│  - Mode switcher via Alps encoder               │
├─────────────────────────────────────────────────┤
│  Layer 2: UART parser  (open source, Python)    │  ← Hours
│  - TLV packet → numpy arrays                    │
│  - Fork from ibaiGorordo or pymmw parsers       │
├─────────────────────────────────────────────────┤
│  Layer 1: MIMO signal processing  (TI firmware) │  ← Zero
│  - FMCW, 3 TX × 4 RX = 12 virtual channels      │
│  - Range-FFT / Doppler-FFT / CFAR / AoA         │
│  - Clustering + multi-object tracking           │
│  - Streams point cloud @ 10–20 Hz over UART     │
└─────────────────────────────────────────────────┘

Front radar ── USB/UART ──┐
                          ├── RPi5 (front cubby, PyQt5)  ──►  OLED
Rear  radar ── USB/UART ──┘
```

## Hardware

### Radar modules — two candidates

**Primary pick: `IWR6843AOPEVM` (Antenna on Package)**
- 60 GHz band, 3 TX × 4 RX MIMO
- Very compact (~25 × 30 mm antenna footprint)
- Onboard FTDI — shows up as `/dev/ttyUSB0` on the Pi
- Free TI firmware demos (incl. parking) run entire DSP chain on-chip
- ~€200–250 each at Mouser / Digi-Key
- **Rationale:** smallest form factor for bumper-hidden mount, cheapest MIMO, known-good through-bumper performance

**Automotive-band alternative: `AWR1843BOOST`**
- 77 GHz (proper automotive radar band)
- Slightly better through heavily metallic paint
- Larger BoosterPack form factor
- ~€300 each
- **Rationale:** only needed if 60 GHz attenuation through `744 Brilliantsilber` (our paint) turns out to be marginal. 60 GHz is expected to be fine for <5 m ranges — verify on-bench early.

### Supporting hardware

- **2× 3D-printed mounting brackets** for the EVMs, with VHB-tape backing to bond to bumper inner skin. Design after on-bench evaluation establishes the correct aiming angle (approximately parallel to ground, centred laterally).
- **2× USB cables to Pi** — EVM to USB-A, routed to the cubby. Already share the Phase-5 cable path for the rear run (one more cable in the bundle).
- **Power:** EVMs run from the USB 5 V supplied by the Pi / hub. No separate power feed needed. Current draw ~0.4 A each.
- **USB hub** if the Pi's direct USB ports are saturated by DSP + capture + cellular. Likely needed — check count during integration.

## Open-Source Software Stack

Matured through mid-2026. Division of labour: TI chip runs the DSP; Python on the Pi consumes the point-cloud UART stream and renders the scope.

| Project | Status | Fit for this project |
| :--- | :--- | :--- |
| [ibaiGorordo/IWR1443-Read-Data-Python-MMWAVE-SDK-1](https://github.com/ibaiGorordo/IWR1443-Read-Data-Python-MMWAVE-SDK-1) | Simple, focused | **Starting point.** Explicitly documented as working on Raspberry Pi. ~200 lines. pyqtgraph scatter. Fork target. |
| [m6c7l/pymmw](https://github.com/m6c7l/pymmw) | Last updated Nov 2021, 335 stars | Steal the TLV parsers + range-Doppler and azimuth-range heatmap code. Replace the plotting. |
| [PreSenseRadar/OpenRadar](https://github.com/PreSenseRadar/OpenRadar) | Active to Apr 2024, 861 stars, Apache-2 | The comprehensive reference. Cherry-pick tracker/clustering helpers if on-chip tracking isn't enough. |
| [lightinfection/TI_IWR6843AOP](https://github.com/lightinfection/TI_IWR6843AOP) | Updated Jan 2026, ROS2 + Docker | Richest built-in visualisations but ROS2 is overkill for this setup. Reference for heatmap UX. |
| [Tkwer/MVRADAR](https://github.com/Tkwer/MVRADAR) | Qt-based multi-view | Closest existing thing to the "impressive live view" we want. Inspiration for layout. |

**TI firmware path:** flash the `IWR6843AOPEVM` with the **TIDEP-01011 automated-parking reference** or the **3D People Counting** demo firmware (both in TI's Radar Toolbox). Either streams a clean point cloud; parking is closer to our application. No custom firmware needed for MVP — revisit only if we want lower latency or custom chirp parameters.

## UI Vision (for later detailed design)

Primary view — **top-down cockpit scope:**

- R129 silhouette (small vector outline, front-up or north-up — user preference) centred
- Range rings at 1.0 / 2.0 / 3.0 / 5.0 m, amber thin strokes
- Radar returns plotted as glowing dots at their (x, y) in car coordinates (front radar → positive y, rear radar → negative y)
- Colour by velocity: amber (static), warm yellow (slow moving), green-amber (moderate), red pulsing (approaching under 1 m)
- Short (~250 ms) fading trail per tracked object for motion perception
- Heading vector drawn from each tracked target showing velocity direction

Secondary views (cycle via Alps encoder):

- **Range-Doppler heatmap** (per-radar) — professional radar aesthetic, also useful for debugging
- **Azimuth-range heatmap** — wide "sonar waterfall" style
- **Raw point cloud without tracking** — firehose view for diagnostics

Behaviour modes:

- **Parking mode** — engaged when the reverse-light trigger is active. Full scope, audible warning at <0.5 m.
- **Drive mode** — engaged above ~10 km/h. Dimmer scope, focus on moving targets (pedestrian / cyclist / overtaking car), static clutter suppressed.
- **Always-on background** — scope visible but non-intrusive when neither condition triggers.

## Mounting & Installation (Planning Notes)

### Rear radar
- Inside rear bumper valance, upper-centre position
- Target height: roughly at licence-plate centre height (~60 cm off ground) for horizontal aim
- Aimed parallel to ground, centred laterally (0° azimuth points directly rearward)
- Bonded to a fibreglass or ABS backing plate, itself bonded to the inside of the valance with 3M VHB 5952
- USB cable joins the Phase-5 rear-bundle run (front cubby ↔ rear cubby), then continues out through the trunk/rear-wheel-arch into the bumper cavity

### Front radar
- Behind front bumper, upper-centre position (behind the MB star grille area, mounted on the bumper reinforcement or a custom bracket to the radiator support)
- Aimed parallel to ground, centred laterally (0° points forward)
- USB cable: out of bumper cavity → up behind the radiator support → through the firewall (existing harness grommet) → along the A-pillar → down behind the dash → into the front cubby

### Calibration
- Each radar reports targets in its own local frame (x forward, y lateral, z up).
- Pi-side coordinate transform applies a fixed translation (radar position in car frame) + rotation (radar yaw offset, measured on-bench) to put both point clouds into a single car-centred frame.
- One-time calibration: place a known corner reflector at a measured (x, y) and confirm each radar reports it correctly. Document transforms in `config/radar_mount.yaml`.

## Effort Estimate

| Phase | Effort |
| :--- | :--- |
| Flash IWR6843AOPEVM with TI parking-demo firmware, verify UART output on bench | 1 evening |
| Fork ibaiGorordo + adapt TLV parser to current IWR6843 firmware (reference pymmw) | 1–2 evenings |
| Bench visualisation with pyqtgraph — confirm point cloud quality | 1 evening |
| Mount one radar temporarily in the rear bumper, verify through-paint performance | 1 weekend |
| PyQt5 cockpit scope in R129 amber aesthetic (primary view only) | 2–4 weekends |
| Second radar install (front bumper) + coordinate-frame fusion | 1 weekend |
| Polish: tracking trails, mode switcher, Alps encoder integration, audible alerts | Ongoing |

**MVP to working-demo: ~3–4 weekends + supporting evenings.** Gated almost entirely by Pi-side software effort, not by radar complexity.

## Open Questions / Decisions Deferred to Winter

1. **60 GHz vs 77 GHz** — default to IWR6843AOP (60 GHz) unless bench test through `744 Brilliantsilber` paint shows attenuation >8 dB at 3 m. Test with one EVM before committing to two.
2. **Front radar integration with the MB star grille** — the Mercedes star assembly in the grille is steel; aiming directly through it is impossible. Radar must mount offset (either above or below the star) or behind the plastic grille inserts flanking it. Decide during mock-up.
3. **USB or direct UART to Pi?** — EVM onboard FTDI gives USB out of the box. Direct UART via header pins would shave latency and free a USB port but adds wiring work. Default: USB for MVP, reconsider if USB port budget gets tight.
4. **Audio alerts through the DSP path** — parking warning should be audible. Route through the already-planned UP 6DSP bluetooth/AUX input? Or a separate small speaker in the cubby? Defer.
5. **Privacy / legality of always-on driving radar** — DIY install of 60 GHz radar for personal use is covered by ETSI EN 305 550 short-range-device rules; off-the-shelf EVMs comply. No licence required in EU. Recording point-cloud data of surrounding vehicles has no GDPR implication (no PII). Noting here so future-me doesn't re-research it.
6. **Should the radar also drive an adaptive-cruise or forward-collision alert?** — Tempting scope creep. **No.** MVP is a visualisation, not a control system. Active safety features (braking, throttle) are strictly out of scope. Passive alerts (a warning tone when closing fast on the car ahead) are optional and should come only after the MVP is solid.
7. **Integration with existing RPi5 UI stack** — `home_view.py` pattern suggests this becomes `radar_view.py` in the same `stacked_widget`. Decide whether radar is its own top-level view or an overlay on others.

## References

- [TI Radar Toolbox (landing page)](https://www.ti.com/tool/RADAR-TOOLBOX) — firmware images, demos, TIDEP reference designs
- [TIDEP-01011](https://www.ti.com/tool/TIDEP-01011) — the automated-parking reference design, closest off-the-shelf match to our use case (AWR1843, 4 cm – 40 m range, ±50° azimuth, ±15° elevation)
- [IWR6843AOPEVM datasheet + user guide](https://www.ti.com/tool/IWR6843AOPEVM)
- [AWR1843BOOST datasheet + user guide](https://www.ti.com/tool/AWR1843BOOST)
- Open-source repos listed in the software stack table above

## Related Work in This Project

- [work/center_console_refresh/README.md](../center_console_refresh/README.md) — Phase 5 cable pull. The rear-radar USB cable would share the rear-bundle path; the front-radar cable takes a separate route via the firewall. Neither is pulled during the summer console-out, but the rear bundle has spare capacity if that's later regretted.
- [UI_rpi5/radio_uiknob.md](../../UI_rpi5/radio_uiknob.md) — existing cockpit architecture. The Alps encoder in the ashtray is the natural input for mode switching on the radar scope.
- [work/audio_upgrade_blueprint.md](../audio_upgrade_blueprint.md) — audio routing. If parking-warning tones are routed through the DSP, this is the integration point.

## Work Log

| Date | Status | Notes |
| :--- | :--- | :--- |
| 2026-04-20 | Parked for Winter 2026–27 | Design captured after investigation into camera/ultrasonic/radar trade-offs. Camera rejected on aesthetic grounds (no invisible R129 mount). Ultrasonic viable but still needs 4 bumper holes. Radar-behind-bumper is the only zero-exterior-modification option. Key insight: TI's chip firmware does all MIMO signal processing; Pi-side work is purely UART parsing + PyQt5 visualisation, leveraging existing open-source Python stack (ibaiGorordo / pymmw / OpenRadar). Hardware pick: 2× IWR6843AOPEVM (60 GHz) as primary, AWR1843BOOST (77 GHz) as automotive-band fallback. Summer queue is full — revisit October/November 2026. |
