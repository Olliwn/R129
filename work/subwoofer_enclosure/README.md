# Subwoofer Enclosure — Sealed 14 L for Helix IK S10-DVC2

Durable build doc for the rear-cubby sealed subwoofer enclosure. Design, dimensioning, cut list, assembly order, sealing, polyfill, and terminal cup wiring. Driver mounting is a separate step deferred until the carcass has fully cured.

**Design reference:** `work/audio_upgrade_blueprint.md` §5 and §7. **Bench test procedure:** `work/audio_bench_test.md`.

---

## 1. Design targets

| Parameter | Target | Source |
| :--- | :--- | :--- |
| Driver | Helix IK S10-DVC2 (10″, DVC 2×2 Ω, 300 W RMS) | `audio_upgrade_blueprint.md` |
| Mounting depth | 84.5 mm | Helix datasheet |
| Driver cutout Ø | 221 mm | **verify on driver before cutting** — measure outer frame cutout clearance ring |
| Driver outer flange Ø | ~254 mm | Helix datasheet — verify |
| Driver displacement | ~0.9 L | typical for 10″ sealed-alignment motor |
| Enclosure alignment | Sealed, Q ≈ 0.7 target | Helix datasheet recommendation |
| Internal volume (geometric) | **14.0 L** | Helix datasheet for sealed |
| Walls | 16 mm MDF | Standard for this enclosure class |
| Internal damping | ~200 g polyester fibre fill, ~40 % compression | Apparent-volume uplift ~10–15 % |
| Sealing | Neutral-cure silicone on all interior seams | Acetic silicone attacks driver aluminum |
| F3 target | 46 Hz (−3 dB) | Helix datasheet with 14 L + polyfill |

**Design choice: treat 14 L as geometric internal volume,** not net-acoustic. Driver magnet displacement (~0.9 L) is absorbed by polyfill's apparent-volume uplift — the two approximately cancel, which is the convenient reason Helix publishes a geometric figure.

---

## 2. Cubby geometry — validated by cardboard mock-up (Sunday AM)

R129 rear driver-side storage cubby typical inside-usable envelope:

- Width (L–R): ~350 mm
- Height (floor to underside of factory locking lid, closed): ~250–280 mm
- Depth (front wall to rear bulkhead): ~300 mm

**These are approximate. The cardboard mock-up is the only authoritative measurement.** Real-world cubbies vary with trim wear and regional market options.

### Mock-up procedure

1. Cut six cardboard rectangles roughly matching one of the three dimensional options below (Table 3.1), tape to form a box.
2. Dry-fit in the cubby with the factory lid closed. Verify:
   - Lid seats without pressure on the box top. A 5–10 mm air gap is ideal.
   - Box does not block the DSP mounting location alongside (UP 6DSP footprint 46 × 130 × 153 mm — note the DSP needs ~40 mm ventilation clearance on the heatsink side).
   - Baffle angle: straight-up firing into the lid is simplest and sonically fine (the lid acts as a pressure reinforcer at low frequencies). Tilt only if the lid fails to seat.
3. Record the final chosen external dimensions on paper **before** any MDF cut. Transcribe to the panel-saw request form at Bauhaus with kerf allowance (≈3 mm).
4. Photograph the mock-up in the cubby from three angles → paste into the 2026-04-26 diary entry with the chosen option marked.

---

## 3. Dimensioning — three geometric options

### 3.1 Options (all target 14 L internal ± 3 %, all accept the 254 mm flange driver)

| Option | External W × H × D (cm) | Internal W × H × D (cm) | Internal V (L) | Baffle dim (cm) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A — Taller, squarer baffle** | 31.2 × 31.2 × 21.2 | 28.0 × 28.0 × 18.0 | 14.11 | 28.0 × 28.0 | Good if cubby height ≥ 22 cm. Minimum sheet area. Baffle has 9.5 mm edge around 254 mm flange — tight but fine. |
| **B — Compromise** | 33.2 × 33.2 × 19.2 | 30.0 × 30.0 × 16.0 | 14.40 | 30.0 × 30.0 | Good all-rounder. 23 mm edge around flange — comfortable. |
| **C — Shallow, wide baffle** | 37.7 × 37.7 × 15.0 | 34.5 × 34.5 × 11.8 | 14.04 | 34.5 × 34.5 | Only if cubby is short. Bigger baffle = more flare real-estate = slightly easier on baffle-diffraction response. 45 mm edge — generous. |

**Primary recommendation: Option B.** Square baffle is visually clean, the 23 mm edge accepts driver gasket + mounting screws comfortably, and 16 cm internal depth gives 75 mm clearance behind the 84.5 mm driver + 16 mm rear wall — adequate for polyfill circulation and short internal speaker-wire leads without the driver magnet touching anything.

### 3.2 Material needed

Option B cut-list area:

- Sides (L+R, 2 pcs): 33.2 × 19.2 cm = 637.4 cm² each → 1274.9 cm² total
- Top + Bottom (2 pcs): 30.0 × 19.2 cm = 576.0 cm² each → 1152.0 cm² total
- Baffle + Back (2 pcs): 30.0 × 30.0 cm = 900.0 cm² each → 1800.0 cm² total
- **Total panel area: 4226.9 cm² ≈ 0.42 m²**
- Plus kerf + waste + spare (15 %): **0.49 m²**

A single **60 × 90 cm** (0.54 m²) pre-cut MDF panel is enough. A 60 × 100 cm raw sheet from Bauhaus with panel-saw cuts covers Option A, B, or C with margin.

---

## 4. Cut list — Option B (primary)

Construction style: **full-height side bookends** capture the top, bottom, baffle, and back between them. This is the simplest style to assemble square and gives the cleanest external appearance.

| # | Panel | Qty | Dimensions (cm) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Left side | 1 | 33.2 × 19.2 | Full-height, full-depth bookend. Outside face shows. |
| 2 | Right side | 1 | 33.2 × 19.2 | Same, mirror. |
| 3 | Top | 1 | 30.0 × 19.2 | Fits **between** the sides. |
| 4 | Bottom | 1 | 30.0 × 19.2 | Same. |
| 5 | Baffle | 1 | 30.0 × 30.0 | Fits in the front opening between sides and top/bottom. **Driver cutout 221 mm, centered, cut last.** |
| 6 | Back | 1 | 30.0 × 30.0 | Same as baffle. **Terminal cup hole cut before install** (size depends on cup chosen — typically 80 × 60 mm rectangle or 70 mm dia circle). |

Internal volume sanity check: 30.0 × 30.0 × (19.2 − 2 × 1.6) = 30 × 30 × 16.0 = 14 400 cm³ = **14.40 L** ✓

### 4.1 Panel-saw request — to Bauhaus cutting desk

> "Leikataan 16 mm MDF-levy seuraaviin paloihin:
> - 2 kpl 332 × 192 mm
> - 2 kpl 300 × 192 mm
> - 2 kpl 300 × 300 mm
> Kiitos."

Ask them to cut in that order (long axis first, then cross-cuts) — minimises handling. 3 mm kerf per cut is normal; budget for it in the sheet-area math.

---

## 5. Assembly order

Materials on hand before starting: PVA D3 wood glue, 4 × 40 mm wood screws (24–32 pcs), 3 mm pilot drill bit, neutral-cure silicone, clamps or heavy weights, square, pencil, tape measure, dust mask (MDF dust is irritant), shop vac.

### 5.1 Dry-fit (no glue)

1. Stand left side on its long edge, outside face down.
2. Place bottom panel perpendicular against it, flush-aligned.
3. Add the back panel into the L-shape from behind.
4. Add right side. Add top.
5. Verify all joints are gap-free and corners square (measure diagonals — should agree within 1 mm). If not, recheck the cuts before committing glue.

### 5.2 Drill pilot holes

- Mark screw positions: 3 per short joint (30 × 16 cm faces), 4 per long joint (30 × 19.2 cm and 33.2 × 19.2 cm faces). Space evenly ~4 cm in from each end, then equal spacing between.
- Drill 3 mm pilot holes through the **outer** panel into the **edge** of the inner panel. Depth: 25–30 mm. 16 mm MDF splits if you skip the pilot holes.
- Countersink lightly so screw heads sit flush.

### 5.3 Terminal cup hole on back panel

- Cut the terminal cup hole **before** gluing the back to the carcass — much easier to work on a flat panel than inside an assembled box.
- Use a jigsaw for a rectangular cup or a hole saw for a circular one. Whatever the cup calls for.
- Position: centered horizontally, ~5 cm up from the bottom edge. Low placement keeps the posts accessible when the box is sitting in the cubby.
- Test-fit the cup. Should sit flush with rubber gasket compressed ~1 mm when screwed down.

### 5.4 Glue + screw assembly

Work through in this order — each step is glue-up + screw-drive + wipe-off excess before the next:

1. **Left side ← bottom.** Bead of PVA along the bottom edge of the side; position bottom; drive screws.
2. **Left side ← top.** Same.
3. **Left side ← back.** Same. Now you have a 4-panel U with back.
4. **Right side ← (top, bottom, back) in one go.** Dry-fit confirms the right side lines up; glue all three contact edges; press into place; drive screws on all three joints.
5. Let this carcass sit 30 min.
6. **Wire and install terminal cup** (see §6) — at this point the back is fixed but the front is wide open, which is the best access for internal wiring.
7. Stuff polyfill loosely through the front opening (see §7).
8. **Baffle (no driver cutout yet).** Bead of glue on all four edges. Press on. Drive screws. Wipe excess.
9. Let full assembly cure 24–48 hours before attempting the silicone pass (§6.4) or the baffle driver cutout (next weekend).

**Square-check between each step:** measure corner-to-corner diagonals; if they disagree by more than 2 mm, clamp the long diagonal until the glue sets.

### 5.5 Clamp / weight strategy

If clamps are thin on the ground, stack phonebooks / car batteries / full 5 L ATF jugs on top of each joint while the glue sets. Screws alone give 80 % of the clamp force; clamps close the last 20 % of hairline gaps.

---

## 6. Terminal cup wiring — DVC2 isolation (critical)

This is the one step where getting it wrong kills the design intent and potentially the DSP channel.

### 6.1 What the UP 6DSP expects

- Channel 5 drives **coil A** only (a 2 Ω load on its own).
- Channel 6 drives **coil B** only (a 2 Ω load on its own).
- The DSP thermally load-balances between the two channels under heavy bass. This is why the sub is specified as DVC2 rather than a single 4 Ω coil driven from a bridged channel pair.

### 6.2 What **NOT** to do

- ❌ Do NOT short COIL A + to COIL B + (parallel wiring at the cup). This presents a 1 Ω load to any single channel feeding both — the UP 6DSP is not rated for 1 Ω, and you'd be paralleling a pair of bridged channels, which is worse.
- ❌ Do NOT series-wire the coils (COIL A − to COIL B +). This gives a 4 Ω load but collapses the dual-channel thermal sharing and loses ~50 % of the driver's power handling.
- ❌ Do NOT use "audiophile" push-fit spring terminals. Binding posts only — they accept the Biltema 2.5 mm² cable cleanly without crushing the strands.

### 6.3 Correct wiring

Four binding posts, labelled externally:
- `COIL A +`
- `COIL A −`
- `COIL B +`
- `COIL B −`

Internal leads from each post go **directly and only** to the corresponding driver coil terminal — no cross-connection between coils. Label the internal cable at both ends with heat-shrink `A` / `B` markers so the driver install next weekend can't be misidentified.

Cable: **Biltema 2.5 mm² speaker cable** from the 84-574 kit, cut short (~30 cm each coil). Internal lead ends:
- Post end: soldered + heat-shrink, or ring terminal under the cup's internal clamp screw. Solder preferred for the permanent install.
- Driver end: spade or ring terminal (open-barrel crimp + solder), so the driver can be disconnected for removal without breaking the cup wiring.

Continuity test after wiring, before adding polyfill or closing the baffle:

| Test | Expected |
| :--- | :--- |
| `COIL A +` to driver A+ tab | ~0 Ω (continuous) |
| `COIL A −` to driver A− tab | ~0 Ω |
| `COIL B +` to driver B+ tab | ~0 Ω |
| `COIL B −` to driver B− tab | ~0 Ω |
| `COIL A +` to `COIL B +` | **open** (infinite; key isolation check) |
| `COIL A +` to `COIL A −` | ~2 Ω (coil DCR, slightly less than 2 Ω nominal) |
| Any post to enclosure/cup body | **open** |

Log measured DCR values in the build diary. Deviations > 10 % from each other (Coil A vs Coil B) are worth flagging.

### 6.4 Silicone pass (interior seams)

After the cup is wired and continuity is clean, and before polyfill goes in:

- Apply a 5–8 mm bead of neutral-cure silicone along every interior corner seam: 4 × side-bottom, 4 × side-top, 4 × side-back (already partially blocked by top/bottom; work from the open baffle side with a flexible caulk tip).
- Tool the bead with a wet fingertip to push it into the seam.
- Hairline gaps at panel joints are the enemy of sealed-alignment Q — the silicone is insurance on top of the glue.

---

## 7. Polyfill

- ~200 g of polyester fibre fill (Autoviihde "vaimennusvilla", or pillow-stuffing from Sinelli / Tokmanni — same material).
- Fill to approximately **40 % compression** — fluffed up to roughly fill the box with light mounding above the top of the carcass, then press down so the lid (baffle) compresses it to snug-but-not-packed.
- Test rule: when you close the baffle, the polyfill should offer mild resistance but not prevent the baffle sitting flat. Over-stuffing is worse than under-stuffing — packed fill acts more like rigid volume loss than like damping.
- Do **not** let polyfill drape over the wiring or terminal cup posts — it can get pulled into the driver cutout during installation. Tuck the internal leads against a side wall, run a strip of masking tape across to hold the fill clear of the centre.

---

## 8. Driver install — DEFERRED to the weekend after cure

Do **not** mount the driver on Sunday. The silicone and PVA need 24–48 hours to reach full cure, and a premature gasket compression can distort the baffle or drag on the wet silicone.

### 8.1 When to do it

After ≥48 hours from the silicone pass. Paint/seal the baffle cutout raw edge with thinned PVA or silicone (edge moisture barrier) before seating the driver.

### 8.2 Baffle cutout

- Diameter: **221 mm** (confirm on driver with calipers — some datasheet figures are nominal).
- Draw the circle with a compass or trammel points. Drill a 10 mm starter hole inside the line.
- Jigsaw with fine wood blade + circle jig, or a 221 mm hole saw if owned.
- Cut on the waste side of the line. Sand back to the line with 80-grit on a flat block — slow, but gives a driver-fits-cleanly finish.
- Vacuum all dust. MDF dust inside the box is fine (polyfill catches it), but dust on the driver magnet gap is bad.

### 8.3 Driver seating

1. Check the driver's foam gasket for damage. If compressed or torn, substitute with 3 mm closed-cell foam ring cut to match the flange.
2. Connect internal coil leads to driver terminals A+ / A− / B+ / B− per labelling from §6. Double-check polarity — Helix datasheet shows the terminal polarity on the driver rear cover.
3. Seat the driver into the cutout with the foam gasket between the flange and the baffle.
4. Drive driver mounting screws — typically 6 × M4 × 30 mm wood screws (or whatever the driver hardware specifies). Pilot-drill all six holes first. Torque snug + 1/8 turn — **don't crush the gasket**, don't over-torque and split the MDF. 2–3 Nm is the target.
5. Work in a diagonal pattern: top → bottom → left → right → top-right → bottom-left. Gradual even compression.

---

## 9. Finish (deferred — optional)

Not required for acoustic performance. Aesthetic only. Options:

- **Raw MDF** — fine in the cubby since the lid covers it. Fastest path.
- **Paint** — Hammerite black or similar, 2 coats. Sand edges first.
- **Carpet wrap** — matches factory cubby carpet if available. Adds 2–3 mm thickness; factor into cubby-fit margin.

---

## 10. References and cross-links

- Design origin: `work/audio_upgrade_blueprint.md` §5, §7
- Part sourcing + CCA kit decision: `docs/parts_to_order.md` Priority 6B
- Bench test of the completed-enough box: `work/audio_bench_test.md`
- Permanent DSP mounting + wiring finalisation (next weekend): `work/center_console_refresh/README.md` §4
- Build diary entries: `docs/diary/2026-04.md` Apr 24 (weekend plan), Apr 26 (to be written during/after build)

---

*Created 2026-04-24 as a weekend-prep artifact. Build execution on 2026-04-26.*
