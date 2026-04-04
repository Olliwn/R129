# Display Mount — Center Console Integration

Replace the R129 center console flip cubby (between Becker BE2210 and gear lever) with a 3D-printed integrated housing that holds the Waveshare 5.5" AMOLED display and the Raspberry Pi 5 behind a flush glass panel.

**Goal:** A single printed part that replaces the original cubby assembly, mounts the display and Pi, routes all cables, and presents a clean glass surface flush with the console trim.

---

## Components to Integrate

### Waveshare 5.5" AMOLED (on hand)

| Spec | Value |
| :--- | :--- |
| Resolution | 1080 × 1920 (portrait native, landscape via software) |
| Active area | ~121 × 68 mm (5.5" diagonal, 16:9) |
| Module size | ~140 × 75 × 10 mm (verify with calipers) |
| Mounting | M2.5 screw holes (4×, positions TBD — measure from unit) |
| Connectors | HDMI (full-size), micro-USB (touch/power), micro-USB (power, unused), 3.5mm HP jack (unused) |
| 180° adapters | Included — redirect HDMI and micro-USB straight rearward |
| Touch | Projected capacitive (PCAP), 10-point, toughened glass cover |
| Touch-through | Works through non-conductive material up to ~3–4 mm |

### Raspberry Pi 5 (on hand)

| Spec | Value |
| :--- | :--- |
| PCB size | 85 × 58 mm |
| Mounting holes | 4× Ø2.7 mm (M2.5), 49 × 58 mm pattern |
| Key connectors used | HDMI-0 (micro-HDMI), USB-A ×2 (touch + Carlinkit), USB-C (power) |
| Power draw | ~5–7 W typical, 12 W peak |
| Heatsink | Active cooler or passive aluminum block required |
| STEP file | [raspberrypi.com/rpi5 mechanical drawing](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf) |

### Glass Panel (to order)

| Spec | Target |
| :--- | :--- |
| Material | Tempered soda-lime glass or borosilicate |
| Thickness | **1.5–2.0 mm** (max 2.5 mm for reliable PCAP touch-through) |
| Dimensions | Matched to console opening (see measurements below) |
| Corner radius | Matched to original wood lid profile |
| Edge | Polished (all 4 edges visible) |
| Tint | Optional: light smoke tint for stealth when display is off. AMOLED true-black already helps. Test with and without. |
| Bonding to display | UV-cure LOCA (Liquid Optical Clear Adhesive) — eliminates air gap, kills reflections, improves touch response |

**Sourcing:** Custom-cut glass from AliExpress glass cutting services, or local glass shop. Specify dimensions, corner radii, thickness, and polished edges.

---

## Measurements Needed from the Car

**Take these with the center console accessible. Calipers + profile gauge recommended.**

### Cubby Opening (the cavity in the console)

| Dimension | Value | Notes |
| :--- | :--- | :--- |
| Opening width (mm) | `___` | Internal width of the cavity where the cubby assembly sits |
| Opening height (mm) | `___` | Visible lid area, top to bottom |
| Opening depth (mm) | `___` | How deep the cavity goes behind the lid plane — critical for Pi clearance |
| Surround lip width (mm) | `___` | How much the wood/plastic trim overlaps the opening edge |
| Corner radii (mm) | `___` | The rounded corners of the visible lid area (inner and outer) |

### Original Cubby Lid

| Dimension | Value | Notes |
| :--- | :--- | :--- |
| Lid outer width (mm) | `___` | Full width of the wood panel, edge to edge |
| Lid outer height (mm) | `___` | Full height |
| Lid thickness at center (mm) | `___` | Including wood veneer |
| Lid thickness at edges (mm) | `___` | If contoured/tapered |
| Surface curvature | `___` | Flat? Slight convex? Measure with straight edge |
| Hinge geometry | `___` | Spring arm locations, pivot axis position, clip dimensions |

### Mounting Interface

| Dimension | Value | Notes |
| :--- | :--- | :--- |
| Clip/snap positions (mm) | `___` | Where the cubby assembly locks into the console frame |
| Console frame material | `___` | Plastic? Metal bracket? Note thickness and rigidity. |
| Screw points (if any) | `___` | Some consoles use screws in addition to clips |
| Cable routing path | `___` | Where cables exit toward rear cubby (DSP) and toward 12V power |

### Clearance Behind the Lid

| Dimension | Value | Notes |
| :--- | :--- | :--- |
| Depth to first obstruction (mm) | `___` | What's behind the cubby? HVAC ducting? Wiring? |
| Available width behind (mm) | `___` | May be wider than the visible opening |
| Available height behind (mm) | `___` | May be taller than the visible opening |
| Ventilation path | `___` | Any natural airflow behind the console? (matters for Pi thermal) |

### Gear Lever Clearance

| Dimension | Value | Notes |
| :--- | :--- | :--- |
| Gap from bottom of lid to gear knob (mm) | `___` | Ensure no interference with the knob or shift boot |
| Gear knob sweep path | `___` | Does the knob pass in front of the cubby area when shifting P→D? |

**Tip:** Photograph everything with a ruler/caliper in frame for reference. Remove the original cubby assembly if practical — it clips out without removing the full center console (per the R129-Forum thread: "Die Mittelkonsole ist ja wirklich schnell ausgebaut").

---

## Design Concept

### Exploded View (front to back)

```
    FRONT (driver-facing)
    ─────────────────────
1.  Glass panel (1.5–2 mm)           ← Flush with console surface
2.  LOCA adhesive layer              ← Optically bonds glass to display
3.  Waveshare 5.5" AMOLED module     ← Mounted face-up against glass
4.  Display retention frame           ← Part of printed housing
    ─────────────────────
5.  Cable routing channel             ← Flat FPC HDMI + flat USB
6.  RPi5 on M2.5 standoffs           ← Oriented for connector access
7.  Heatsink (passive aluminum)       ← On Pi SoC, faces vent slots
    ─────────────────────
8.  Printed housing shell             ← Clips into console frame
    REAR (behind console)
```

### Housing Requirements

- **Material:** ASA (preferred) or PETG. NOT PLA — summer console temps can reach 60–70°C.
- **Color:** Black or very dark brown.
- **Tolerances:** Tight fit to console opening (+0.0 / -0.2 mm). Print test-fit shells first.
- **Glass retention:** Front lip or channel that the glass panel sits in. Bonded with silicone or thin foam gasket for vibration isolation.
- **Display retention:** M2.5 threaded inserts (heat-set brass) matching Waveshare mounting holes.
- **Pi retention:** M2.5 standoffs (10–15 mm height) matching Pi 5 hole pattern (49 × 58 mm).
- **Vent slots:** On the bottom/rear face for passive convection from the Pi heatsink. Avoid top vents (dust/crumbs falling in).
- **Cable exits:** Channels or grommeted holes for:
  - USB-C power (from ignition-switched 12V → 5V/5A buck converter)
  - USB-A to MEC HD-USB in rear cubby (audio)
  - USB-A to Carlinkit CPC200-CCPA (CarPlay, hidden behind console)
  - Optional: GPIO ribbon cable for rotary encoder (if adding the Kilo International knob)

### Console Interface

The printed housing replaces the original cubby assembly (A 129 680 00 91). It must replicate the clip/snap geometry that locks the assembly into the center console frame. Two approaches:

1. **Replicate factory clips** — measure and model the snap-fit features from the original assembly. Most reliable but requires precise measurement.
2. **Friction fit + set screws** — slightly oversize the housing, use small grub screws from the back to wedge it into the console cavity. Simpler to model, adjustable.

Approach 2 is recommended for prototyping. Refine to approach 1 for the final version.

---

## Thermal Management

| Source | Heat (W) | Mitigation |
| :--- | :--- | :--- |
| RPi5 SoC | 3–5 W sustained | Passive aluminum heatsink (e.g., Pimoroni or GeeekPi) + vent slots |
| RPi5 PMIC | 0.5–1 W | Thermal pad to housing wall (conducts to console metalwork) |
| AMOLED | <1 W | Negligible — OLED is efficient |
| Summer ambient | up to 70°C on dash surface | Console cavity is shaded, cooler than dash top. Glass panel reflects some solar. Pi throttles at 85°C junction — should be fine. |

**Worst case:** Parked in direct sun, everything is off. Console temp 70°C. Pi is not running, no thermal issue. On startup, Pi SoC starts at ambient and throttles only if junction exceeds 85°C — a 15°C margin from the worst starting point. With a passive heatsink and vent slots, sustained operation at 5W in a 40–50°C ambient cabin (engine running, HVAC on) is well within limits.

---

## Bill of Materials (Display Mount Specific)

| Item | Spec | Qty | Est. Cost | Status |
| :--- | :--- | :--- | :--- | :--- |
| Custom cut glass panel | 1.5–2 mm tempered, polished, rounded corners | 1 | ~€10–20 | Pending (order after measurements) |
| UV LOCA adhesive | 5 ml + UV lamp | 1 | ~€10–15 | Pending |
| ASA filament (black) | 1 kg spool | 1 | ~€25 | Check inventory |
| M2.5 heat-set inserts (brass) | 8+ (4 display + 4 Pi) | 1 bag | ~€5 | Pending |
| M2.5 × 6mm screws | 8+ | 1 bag | ~€3 | Pending |
| M2.5 standoffs 12mm | 4 (Pi mounting) | 1 bag | ~€3 | Pending |
| Passive aluminum heatsink | RPi5 compatible (e.g., Pimoroni) | 1 | ~€8–12 | Check inventory |
| USB-C PD trigger + buck converter | 12V → 5V/5A, ignition-switched | 1 | ~€10–15 | Pending |
| Flat FPC HDMI cable | Micro-HDMI → HDMI, 10–15 cm | 1 | On hand | ✅ |
| Flat micro-USB cable | 10–15 cm | 1 | On hand | ✅ |

**Estimated total for mount-specific parts: ~€75–95**

---

## Workflow

### Phase 1 — Measure (Easter break)
1. Remove original cubby assembly from console.
2. Take all measurements from the checklist above.
3. Photograph cavity, clips, cable paths, and obstructions with ruler in frame.
4. Measure the Waveshare module precisely (PCB outline, mounting holes, connector positions, active area offset from edges).
5. Measure RPi5 with heatsink attached.

### Phase 2 — CAD Model
1. Model the console cavity from measurements.
2. Model the Waveshare module (or import from Waveshare STEP if available).
3. Import the RPi5 STEP file from [raspberrypi.com](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf).
4. Design the housing shell: glass recess, display mount, Pi mount, cable channels, vent slots, console clips.
5. Export STL.

### Phase 3 — Prototype
1. Print test-fit shell in PLA (fast, cheap — just for dimensional check).
2. Test-fit into console cavity. Verify clip engagement, depth clearance, cable routing.
3. Test-fit display and Pi inside the shell. Verify screw alignment.
4. Measure glass panel dimensions from the printed prototype (the glass recess defines the final cut).
5. Order custom glass panel.

### Phase 4 — Final Build
1. Reprint housing in ASA (or PETG).
2. Install heat-set brass inserts.
3. Mount Pi on standoffs, attach heatsink.
4. Mount display with M2.5 screws.
5. Bond glass to display with LOCA + UV cure.
6. Route cables, install into console.
7. Power on, verify touch, verify thermals.

### Phase 5 — Refinement
- Adjust glass tint if needed (apply tint film, or order smoked glass).
- Add rotary encoder cutout if integrating the Kilo International knob.
- Final cable management and strain relief.
- Optional: vinyl wrap or paint the visible edges of the housing to match console.

---

## Open Questions

- [ ] Does the Waveshare have a published STEP/IGES file? (Would save hours of manual measurement.)
- [ ] Exact depth available behind cubby — is there room for Pi + heatsink (~25 mm) behind the display (~10 mm)?
- [ ] Does the gear knob interfere with the glass surface when shifting? (Photo suggests tight clearance.)
- [ ] Ignition-switched 12V source — where is the nearest tap point behind the center console?
- [ ] Should the housing be one piece or split (front bezel + rear Pi tray)? Split is easier to print and assemble.
- [ ] Rotary encoder: integrate into the glass panel edge, or mount separately on the console? The `partslist.md` mentions a 6mm hole in the panel — this needs thermal and clearance analysis.

---

## Reference Documents

- `docs/R129_Driver_UI_System_Design.md` — display specs, cabling, rotation, audio architecture
- `UI_rpi5/partslist.md` — original "black glass aesthetic" concept, encoder selection
- `UI_rpi5/src/` — PyQt5 gauge app running on the Pi
- RPi5 mechanical drawing: [PDF](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf)
- Waveshare wiki: [5.5inch HDMI AMOLED](https://www.waveshare.com/wiki/5.5inch_HDMI_AMOLED)
- R129 cubby assembly: A 129 680 00 91 (complete), A 129 680 01 78 (wood lid only)
- R129-Forum thread: [Deckel Ablagefach lose (unter Radio)](https://r129-forum.de/thread-12610.html)
