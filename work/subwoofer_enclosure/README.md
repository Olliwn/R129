# Subwoofer Enclosure — Sealed for Helix IK S10-DVC2 (cubby-constrained tapered geometry)

Durable build doc for the rear-cubby sealed subwoofer enclosure. Design, dimensioning, cut list, assembly order, sealing, polyfill, and terminal cup wiring. Driver mounting is a separate step deferred until the carcass has fully cured.

**Design reference:** `work/audio_upgrade_blueprint.md` §5 and §7. **Bench test procedure:** `work/audio_bench_test.md`.

**Geometry locked 2026-04-25** following Saturday-evening cardboard mock-up. The cubby's complex 3D shape (depth tapers from 27 cm at the floor to 33 cm at the lid line, plus a wheel-well/trim intrusion at the back-right corner) drove a single-axis-tapered box with a chamfered corner — see §2 and §3.

---

## 1. Design targets

| Parameter | Target | Source |
| :--- | :--- | :--- |
| Driver | Helix IK S10-DVC2 (10″, DVC 2×2 Ω, 300 W RMS) | `audio_upgrade_blueprint.md` |
| Mounting depth | 84.5 mm | Helix datasheet |
| Driver cutout Ø | 221 mm | **verify on driver before cutting** — measure outer frame cutout clearance ring |
| Driver outer flange Ø | ~254 mm | Helix datasheet — verify |
| Driver displacement | ~0.5–0.9 L | 10″ sealed-alignment motor |
| Enclosure alignment | Sealed, Qtc ≈ 0.7 target | Helix datasheet recommendation |
| Internal volume (geometric) | 14.0 L (datasheet); **realised ~11.3 L raw, ~12.5 L effective with polyfill** | Cubby-constrained — see §3 volume math |
| Walls | 16 mm MDF | Standard for this enclosure class |
| Internal damping | ~135 g polyester fibre fill, ~40 % compression | Apparent-volume uplift ~15–20 % brings effective volume to ~12.5 L (vs 14 L target) |
| Sealing | Neutral-cure silicone on all interior seams | Acetic silicone attacks driver aluminum |
| F3 target | ~47 Hz (−3 dB), Qtc ~0.72 — **within 1 Hz of datasheet 14 L alignment** | Realised geometry + polyfill |

**Design choice: accept the ~10 % volume shortfall.** The cubby physically can't accommodate a 14 L geometric box without the box protruding through the lid. The realised box delivers ~12.5 L effective volume, which yields F3 ≈ 47–48 Hz vs. the datasheet's 46 Hz at 14 L — a 1–2 Hz difference that is at or below audibility threshold and well within DSP correction range (a +1.5 dB low shelf at 50 Hz on the sub channel restores the response if desired). The DSP has plenty of headroom for this nudge given the amp/driver match.

---

## 2. Cubby geometry — measured 2026-04-25 evening

The R129 rear driver-side cubby has a complex 3D envelope:

- **Floor footprint:** 37 cm wide × 27 cm front-to-back, with a back-right corner intrusion that removes a triangle with legs 15 cm (along the back wall) and 23 cm (along the right wall). Net floor area ≈ 826.5 cm².
- **Lid-line footprint:** 37 cm wide × 33 cm front-to-back, with the same back-right intrusion shrunken to a 15 × 15 corner triangle. Net top area ≈ 1108.5 cm².
- **Height (floor to underside of factory lid):** 18 cm.
- **Depth taper:** the back wall of the cubby leans inward as you descend — the floor sits 6 cm forward of the lid-line at the back, giving the cubby its "wedge" cross-section.

The cubby total envelope (prismatoidal volume) is **17.4 L**.

### Box design strategy

The box was sized to fit flush at all four sides with the cubby walls (no air gap on the L/R sides or front), tapering on the depth axis to match the cubby's depth taper, with the back-right corner chamfered to clear the intrusion. The lid is decorative-only (thin substrate + upholstery, not structural) — the box's own top plate carries the driver and forms the acoustic baffle. See §5.6 for the lid construction notes.

### Cardboard mock-up — completed Saturday evening 2026-04-25

The mock-up confirmed the cubby's depth taper, the corner intrusion shape, and the available height. The original measurement sketch is saved as `cubby_mock-up_2026-04-25.png` alongside this README. Final box external dimensions selected from the mock-up:

| Plate | Width × Depth | Corner cut (legs) | Net area |
| :--- | :---: | :---: | :---: |
| Top plate (decorative-side, baffle-side) | 37 × 33 cm | 15 × 23 cm† | 1048.5 cm² |
| Bottom plate (sits on cubby floor) | 37 × 27 cm | 15 × 23 cm | 826.5 cm² |
| Height (flush with cubby lid line) | 18 cm | — | — |

† **Build simplification:** the cubby intrusion is only 15 × 15 at the lid-line level, but the box's top plate uses the bottom plate's larger 15 × 23 cut anyway. This makes the corner-cut wall a single flat MDF panel (with the same 22.1° tilt as the back wall) instead of a twisted/multi-faceted surface. The dead air this leaves at the top corner — an 8 × 15 cm wedge tapering to nothing at the floor — costs ~0.5 L of external volume but eliminates a hard joinery problem. See §3 for the full trade-off analysis.

---

## 3. Dimensioning — single-axis-tapered single-corner-chamfered box

### 3.1 Geometry summary

The box is a prismatoid with:

- **Constant width** (37 cm) on the left-right axis — front wall and back wall are full-width.
- **Tapered depth** on the front-back axis (27 cm at floor → 33 cm at lid line) — left and right side walls are TRAPEZOIDS with parallel edges of 27 cm (bottom plate footprint) and 33 cm (top plate footprint), wall height **14.8 cm** (the gap between top and bottom plates after subtracting their 16 mm thickness from the 18 cm external box height), and slant edge **16 cm** (= sqrt(14.8² + 6²)).
- **Chamfered corner** (15 × 23 cm right-triangle removed from the back-right corner, same cut at top and bottom) — adds a single flat diagonal corner-cut wall.
- **Two tilted walls:** the back wall and the corner-cut wall both tilt **22.1° from vertical** (= atan(6 / 14.8)), in the same direction (away from the box interior as you go up). The front wall and side walls are vertical.

**Construction-style note (critical for the cut list):** the bottom and top plates capture the four side walls between them (see §4 prose). With 16 mm plates and 18 cm external box height, the wall vertical extent is `180 - 16 - 16 = 148 mm = 14.8 cm`. The tilted-wall slant length is `sqrt(148² + 60²) = 159.7 mm ≈ 16 cm`. The tilt angle reflects the corrected geometry: `atan(60 / 148) = 22.1°` from vertical, NOT the 18.4° figure that earlier drafts of this doc used (which was based on the external silhouette `atan(60 / 180) = 18.4°` — the angle the rear face would have if walls extended through the plate thicknesses, which they don't).

### 3.2 Volume math (prismatoidal formula)

For a prismatoid with linearly varying cross-section: $V = \frac{h}{6}(A_{bottom} + 4 A_{middle} + A_{top})$.

| Cross-section | Rectangle | Corner triangle | Net area |
| :--- | :---: | :---: | :---: |
| Bottom (z = 0) | 37 × 27 = 999 | 15 × 23 / 2 = 172.5 | 826.5 cm² |
| Middle (z = 9, interpolated) | 37 × 30 = 1110 | 15 × 23 / 2 = 172.5 | 937.5 cm² |
| Top (z = 18) | 37 × 33 = 1221 | 15 × 23 / 2 = 172.5 | 1048.5 cm² |

$V_{ext} = \frac{18}{6} \times (826.5 + 4 \times 937.5 + 1048.5) = 3 \times 5625 = 16{,}875 \text{ cm}^3 \approx \textbf{16.9 L external}$

### 3.3 Internal volume

After 16 mm walls reduce each axis by 32 mm and internal height drops to 14.8 cm. Approximate internal cross-sections (rectangle shrunk by 32 mm each axis, minus a wall-offset-corrected corner-cut triangle of ~145 cm²):

- Internal bottom area ≈ 33.8 × 23.8 − 145 ≈ 659 cm²
- Internal middle area ≈ 33.8 × 26.8 − 145 ≈ 761 cm²
- Internal top area ≈ 33.8 × 29.8 − 145 ≈ 862 cm²

$V_{int,raw} \approx \frac{14.8}{6} \times (659 + 4 \times 761 + 862) = \frac{14.8}{6} \times 4565 \approx 11{,}260 \text{ cm}^3 \approx \textbf{11.3 L raw}$

After driver displacement (~0.5 L) and polyfill apparent-volume uplift (~15–20 %):

$V_{eff} = (11.3 - 0.5) \times 1.15 \approx \textbf{12.4 L effective}$ (conservative)
$V_{eff} = (11.3 - 0.5) \times 1.20 \approx \textbf{13.0 L effective}$ (optimistic)

### 3.4 Acoustic response (sealed alignment for Helix IK S10-DVC2)

| Volume | F3 | Qtc | Audible character |
| :---: | :---: | :---: | :--- |
| Datasheet 14 L | ~46 Hz | ~0.70 | Reference |
| **Realised 12.5 L (this build)** | **~47–48 Hz** | **~0.73** | **Indistinguishable from datasheet in cabin** |
| Hypothetical 11 L | ~49 Hz | ~0.75 | Slight punch / Q lift, just-detectable on familiar tracks |

The 1 Hz F3 difference is below audibility. The 0.02 Qtc shift is within the variance of polyfill packing density itself, i.e. how tightly you stuff the polyfill controls Qtc with similar variance. **No DSP correction required**; if desired later, a +1.5 dB low-shelf at 50 Hz on the sub channel pushes F3 down by ~1 Hz at negligible headroom cost.

### 3.5 Trade-off chosen: build simplicity over 3 % volume

The exact cubby geometry has the corner intrusion shrinking from 15 × 23 at the floor to only 15 × 15 at the lid line. Matching the cubby exactly would require the corner-cut wall to be a non-planar twisted surface (verified analytically: the four corner points of an exact-fit corner-cut wall are not coplanar, ruling out a single flat MDF panel). The trade-offs:

| Variant | External V | Effective V | Buildable from flat MDF? | Verdict |
| :--- | :---: | :---: | :---: | :--- |
| Exact cubby fit (15 × 15 top, 15 × 23 bottom) | 17.4 L | ~13.0 L | No — corner-cut wall is twisted | Rejected |
| **Adopted: 15 × 23 cut at both top and bottom** | **16.9 L** | **~12.5 L** | **Yes — single flat corner-cut panel** | **Adopted** |
| 15 × 15 cut at both top and bottom | 18.0 L | ~13.2 L | Yes — vertical corner-cut panel | Rejected: bottom doesn't clear cubby intrusion |
| Multi-faceted corner-cut wall (2 panels with horizontal seam) | 17.4 L | ~13.0 L | Yes — but adds an extra panel + seam | Rejected: 0.5 L gain not worth the joinery complexity |

The 0.5 L volume cost of the simplification is acoustically below audibility. Build effort drops significantly.

### 3.6 Material needed

Cut-list area for the 7-panel build (see §4) — **corrected 2026-04-26 noon** for proper wall height (= 14.8 cm between plates, NOT the full 18 cm external box height):

- Top plate (37 × 33 with 15 × 23 cut): 1049 cm²
- Bottom plate (37 × 27 with 15 × 23 cut): 827 cm²
- Front wall (37 × 14.8): **548 cm²**
- Back wall (22 × 16, slant length): **352 cm²** — note: the back wall only spans from x=0 to where the corner cut starts at x=22, not the full 37 cm box width
- Left side wall (trapezoid, parallel sides 27 + 33, height 14.8): **444 cm²**
- Right side wall (trapezoid, parallel sides 4 + 10, height 14.8): **104 cm²** (this is the SHORT right side, between front edge and corner cut)
- Corner-cut wall (rectangle, 27.5 × 16, slant length): **440 cm²**
- **Total panel area: 3764 cm² ≈ 0.38 m²**
- Plus kerf + waste + spare (15 %, slightly lower because the corrected smaller pieces leave more nesting room): **0.43 m²**
- Plus 4 cleat strips (16 × 16 mm cross-section, ~22 + 22 + 27.5 + 27.5 = 99 cm linear total, ~158 cm² panel face area at rip width 48 mm × bevel-cut waste-half) — only if cleats are used; see §5.4 below.

#### Panel-size options (corrected wall heights)

| Panel | Area | Slack (no cleats) | Slack (with cleats) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **60 × 100 cm** | 6000 cm² | 2236 cm² (37 %) | 2078 cm² (35 %) | Originally specified, generous. |
| **40 × 120 cm** (acquired 2026-04-25) | 4800 cm² | **1036 cm² (22 %)** | **878 cm² (18 %)** | **Comfortable margin for either Strategy A (cleats) or Strategy C (no cleats).** The earlier "tight ~5 % slack" assessment was based on a wall-height bug (18 cm vs the correct 14.8 cm) — see decisions log §11 row "2026-04-26 noon — wall height corrected". With the corrected dimensions the strict strip layout is no longer geometrically forced into a single narrow strip; an operator can lay walls in a 16-cm-wide strip running the full 120 cm length and plates in a parallel 33-cm-wide × 60 cm strip, with room left for cleats. |
| Other sizes | — | — | — | Any rectangle ≥ 4000 cm² with one dimension ≥ 37 cm works. |

**Decision (2026-04-25, partly invalidated 2026-04-26 noon):** 40 × 120 panel acquired Saturday. Strategy C (silicone-fillet, no cleats) was originally chosen because the panel was thought to be ~5 % short of cleat-inclusive layout; the wall-height correction shows the panel actually has 18 % slack with cleats. **Strategy C is retained as the default for build-simplicity reasons** (saves ~2 hours of Phase 1 cleat ripping + pre-gluing) but is no longer forced by material constraint — see §5.4 for the choice rationale, and the §11 decisions log row "2026-04-26 noon" for the bug history. If you want a more rigid joint and the table-saw + extra-time investment is acceptable, reverting to Strategy A is now feasible without buying more MDF.

---

## 4. Cut list — 7-panel single-axis-tapered build

Construction style: **bottom-and-top plates capture the four side walls between them**. The two trapezoidal side walls and the two tilted walls (back, corner-cut) all sit on the bottom plate edges; the top plate caps them. This style assembles square more naturally than full-height bookends when the side walls are trapezoidal.

### 4.1 Panel cut list

| # | Panel | Qty | Dimensions (cm) | Cut style | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Bottom plate | 1 | 37 × 27 with 15 × 23 corner cut at back-right | Pentagonal (5-sided) | All edges 90°. Mark cut lines on a 37 × 27 rectangle; cut diagonally from (22, 27) to (37, 4). Plate footprint, NOT affected by the wall-height correction. |
| 2 | Top plate (= driver baffle) | 1 | 37 × 33 with 15 × 23 corner cut at back-right | Pentagonal (5-sided) | All edges 90°. Same diagonal direction as bottom but from (22, 33) to (37, 10). **Driver cutout (Ø 221 mm) cut LAST**, after carcass cure — see §8.2. Plate footprint, NOT affected by the wall-height correction. |
| 3 | Front wall | 1 | **37 × 14.8** | Rectangle | All edges 90°. Faces front of cubby. Height = external box height 18 cm − 2 × 16 mm plate thickness = 14.8 cm. (Plates capture the wall between them — see §3.1 construction-style note + §4 prose.) |
| 4 | Back wall | 1 | **22 × 16 (slant length, oversize by ~5 mm and trim flush after assembly)** | Rectangle | All edges 90°. Width 22 cm — the back wall only spans from x=0 to where the corner cut starts at x=22, not the full box width. The remaining back-of-box area (x=22 to x=37) is covered by the corner-cut wall. Tilts **22.1° from vertical** in the assembled box (= atan(6/14.8)); see §5.4 for joinery. Slant length = sqrt(14.8² + 6²) = 15.97 cm; cut at 16.5 cm to allow trim-flush. |
| 5 | Left side wall (trapezoid) | 1 | **Parallel edges 27 + 33, height 14.8, slant edge sqrt(6² + 14.8²) ≈ 16.0** | Right-trapezoid | Front edge vertical 14.8 cm; bottom edge horizontal 27 cm; top edge horizontal 33 cm; back edge slants 16.0 cm at 22.1° from vertical. All edges 90° square cuts. |
| 6 | Right side wall (small trapezoid, ahead of corner cut) | 1 | **Parallel edges 4 + 10, height 14.8, slant edge ≈ 16.0** | Right-trapezoid | Mirror of #5 but truncated by the corner cut. Front edge vertical 14.8 cm; bottom edge 4 cm; top edge 10 cm; back edge slants 16.0 cm meeting the corner-cut wall. Small panel, easy to mis-cut — measure twice. |
| 7 | Corner-cut wall | 1 | **27.5 × 16 (slant length, oversize by ~5 mm and trim flush after assembly)** | Rectangle | All edges 90°. Tilts **22.1° from vertical**. Diagonal-direction face — the 27.5 cm width is the chord across the corner cut (= sqrt(15² + 23²) at both top and bottom plates, identical because the corner cut translates rigidly between plates). Slant length = sqrt(14.8² + 6²) = 15.97 cm; cut at 16.5 cm to allow trim-flush. **Terminal cup hole pre-cut here, before installation** — see §5.3. Position: centred on the panel, ~4 cm up from bottom edge. |
| ~~8~~ | ~~Cleat strips~~ | ~~4~~ | ~~16 × 16 × ~22 / ~22 / ~27.5 / ~27.5 cm long~~ | ~~Right-triangle cross-section~~ | **NOT USED in default Strategy C** — see §5.4. The earlier panel-area justification for skipping cleats was based on a wall-height bug; with corrected dimensions the panel has 18 % slack with cleats included. Strategy C retained as default for build-simplicity (saves ~2 h Phase 1) but Strategy A (cleats) is materially feasible if preferred. |

**Verification of internal volume:** prismatoidal formula with internal cross-sections (§3.3, which uses the correct internal height of 14.8 cm) → 11.3 L raw → 12.5 L effective with polyfill ✓ (volume math was already correct — only the cut-list dimensions were affected by the bug.)

### 4.2 Where the terminal cup goes

The terminal cup is mounted on the **corner-cut wall (panel 7)**, not on the back wall. Reasoning:

- The corner-cut wall faces toward the back-right of the driver-side cubby — the side closest to the passenger-side cubby across the rear bulkhead, where the DSP lives (relocated 2026-04-25; see `work/audio_upgrade_blueprint.md` §1 and `work/center_console_refresh/README.md` §5.7b for the cubby-to-cubby speaker run). Wiring exits the box on the same wall it travels along, no awkward back-of-box access needed.
- The back wall faces straight back, into a less-accessible space.
- A wired terminal cup on the corner-cut wall puts the binding posts within easy reach when the box is dropped into the cubby.

Pre-cut the terminal cup opening on panel 7 BEFORE installing it (much easier to work on a flat panel than inside an assembled box). Standard sizes: 80 × 60 mm rectangular cup or 70 mm-diameter circular cup. Size to whatever cup is on hand.

### 4.3 Panel-saw request — to Bauhaus cutting desk

The panel saw can do the trapezoidal cuts (it tilts the workpiece, not the blade — straight angled cuts in plan view are a single-axis cut for the saw). Bring the cardboard mock-up to the cutting desk for visual reference.

> "Leikataan 16 mm MDF-levystä seuraavat palat (mitat millimetreinä):
>
> Suorakulmiot:
> - Etuseinä: 370 × 148 (1 kpl)
> - Takaseinä: 220 × 165 (1 kpl) — ylimittainen, höylätään asennuksen jälkeen (lopullinen viisteleikkaus 160 mm)
> - Kulmaseinä: 275 × 165 (1 kpl) — ylimittainen, höylätään asennuksen jälkeen (lopullinen viisteleikkaus 160 mm)
>
> Trapetsit (suorakulmainen trapetsi, lyhyempi sivu vasemmalla):
> - Vasen sivu: korkeus 148, alaosa 270, yläosa 330 (1 kpl)
> - Oikea sivu: korkeus 148, alaosa 40, yläosa 100 (1 kpl)
>
> Viisikulmiot (suorakulmio, jonka oikeasta yläkulmasta leikataan kolmio pois — terä jolla 15 × 23 cm):
> - Pohjalevy: 370 × 270, kolmio 150 × 230 oikea yläkulma (1 kpl)
> - Kansilevy: 370 × 330, kolmio 150 × 230 oikea yläkulma (1 kpl)
>
> Kiitos."
>
> *Wall heights corrected 2026-04-26 noon (vs the 2026-04-25 evening draft): the four wall pieces drop from 180 → 148 mm height (front + sides) and 195 → 165 mm slant (back + corner-cut) because the plates capture the walls between them, leaving 18 cm − 2 × 16 mm = 14.8 cm of vertical extent for the wall pieces. Plates unaffected. See §3.1 construction-style note + §11 decisions log.*
>
> *Cleat strips removed from the cut request 2026-04-25; see §5.4 for current strategy. Cleats remain materially feasible if you change your mind — request 4 cleat strips (rimaa) ~16 × 16 × 220 / 220 / 275 / 275 mm separately, or rip them from offcuts at home.*

Ask them to cut in this order: large rectangles first, then trapezoids, then pentagonal pieces (most fiddly last). 3 mm kerf per cut is normal; budget for it in the sheet-area math.

**Layout note for the 40 × 120 panel (revised 2026-04-26 noon after wall-height correction):** with corrected wall heights (max wall slant 16 cm), a 16-cm-wide wall strip and a 33-cm-wide plate strip together need 49 cm of panel width — still over 40 — but the corrected smaller pieces leave significant slack on the long dimension. **Recommended layout:** plates section 37 × 60 cm (top + bottom plates stacked along the long axis, 37 along width with 3 cm side scrap); walls section 40 × 60 cm with two 16-cm-tall rows hosting the 4 walls comfortably. Total panel utilisation ~78 % with 22 % slack. The operator should not need any clever nesting — the corrected dimensions fit straightforwardly. Bring the cardboard mock-up and this README in case any clarification is needed at the cutting desk.

---

## 5. Assembly order

**Adhesive in use (revised 2026-04-25):** **Casco SuperFix+** (SMP / silane-modified polymer) construction adhesive substituted for the originally-spec'd PVA D3 wood glue. SF+ is gun-applied as a 5–10 mm bead, has ~20 min open time, cures elastically (Shore A 45–50, ~500 % elongation at break) by atmospheric humidity, reaching 3 mm depth in 24 h. **Net effect on this build is positive:**

- Gap-filling up to 10 mm — forgiving on imprecise panel-saw cuts, unlike PVA.
- 20 min open time vs PVA's ~5 min — ample breathing room for square-checking each joint.
- Elastic cure resists hairline-crack development at MDF joints under bass pressure (PVA in MDF can creak over time).
- Cure schedule unchanged: still plan 24 h before any further handling.

**Application differences from PVA:**

- Apply as a **continuous bead** (5–10 mm) along the joint edge, not spread thin.
- Drive screws to clamp, but **do not over-clamp** — SMP joints want 1–3 mm bond line for full strength; squeezing the bead to nothing weakens the joint. "Snug, not aggressive" on the screws.
- Squeeze-out is messier than PVA. Wipe with white spirit (mineraalitärpätti) before skin-over (~10–15 min).
- Bead application means more squeeze-out — keep paper towels and white spirit at hand.

Materials on hand before starting: **Casco SuperFix+** cartridge (~290 ml, one is enough for this build) + caulking gun, 4 × 40 mm wood screws (28–36 pcs), 3 mm pilot drill bit, neutral-cure silicone (one full tube), masking tape, clamps or heavy weights, square, pencil, tape measure, dust mask (MDF dust is irritant), shop vac, **white spirit + paper towels for SMP squeeze-out cleanup**.

The build proceeds in three phases:

- **Phase 1: Sub-assemblies.** Terminal cup wired into the corner-cut wall (§5.3), pilot holes drilled (§5.2). Each step is independent and can be done in any order.
- **Phase 2: Carcass glue-up.** Bottom plate is the foundation; vertical walls (front, sides) go up next; tilted walls (back, corner-cut) butt directly against the plate edges (Strategy C silicone-fillet, §5.4); top plate caps it (§5.5).
- **Phase 3: Cure + seal.** 24-hour SMP cure, then silicone fillet pass on every interior seam INCLUDING the tilted-wall gaps (§5.4 + §6.4), then 48-hour silicone cure before any further work.

### 5.1 ~~Cleat strip preparation~~ — SKIPPED (Strategy C adopted)

The cleat-strip preparation step is omitted as of 2026-04-25 because the 40 × 120 panel doesn't have material margin for the cleat stock. Strategy C (silicone-fillet, no cleats) is now the default joinery — see §5.4. This saves ~2 hours of Phase 1 work (cleat ripping + pre-gluing) and removes 4 cuts from the cut list.

If you later acquire more MDF and want to retrofit cleats for a more rigid build, the original cleat plan is preserved in §5.4 Strategy A. For this build, jump straight to §5.2.

### 5.2 Drill pilot holes

Mark screw positions:

- Bottom plate / top plate to wall joints: every 6–8 cm along the joint, 4 cm in from each end.
- Wall-to-wall joints (front-to-side, side-to-back, back-to-corner-cut): every 8 cm along the joint.
- Tilted-wall joints (back wall, corner-cut wall to top and bottom plates): every 6–8 cm along the joint, screws driven from outside through the wall into the plate edge. Screws bite at 22.1° into the plate edge — pre-drill with a longer pilot hole (3 mm × 35 mm) to minimise splitting.

Drill 3 mm pilot holes **through the outer panel into the edge of the inner panel**. Depth 25–30 mm. 16 mm MDF splits if you skip the pilot holes — non-negotiable. Countersink lightly so screw heads sit flush.

### 5.3 Terminal cup wiring + install on the corner-cut wall

Wire the terminal cup BEFORE installing the corner-cut wall in the carcass — much easier on a flat panel.

1. Cut the terminal cup opening on the corner-cut wall (panel 7) per its hardware spec — typically jigsaw for a rectangular cup, hole saw for a circular one.
2. Wire the cup per §6 (DVC2 isolation — critical step).
3. Test continuity per §6.3 — log DCR values in the build diary BEFORE the panel is buried in the carcass.
4. Set the wired panel aside, taped face-down on a clean surface so the binding posts aren't damaged during handling.

### 5.4 Tilted-wall joinery — Strategy C as default (silicone-fillet, no cleats); Strategy A is also feasible

The back wall (panel 4) and corner-cut wall (panel 7) both tilt **22.1° from vertical** (= atan(6 / 14.8) — corrected 2026-04-26 noon from the earlier 18.4° figure, which mistakenly used the external box height instead of the wall-between-plates height; see §3.1 + §11). Their top and bottom edges meet the top and bottom plates at 22.1° dihedrals (not 90°). Three strategies were considered:

**Strategy C (DEFAULT — silicone-fillet + SMP gap-fill): all 90° edges, fill the gaps.** Every panel cut at 90°. When the tilted walls are installed, their bottom and top edges sit at 22.1° against the plates, leaving a triangular gap of `16 mm × tan(22.1°) ≈ 6.5 mm` at the maximum point on the inside corner. **Two-stage sealing strategy:**

1. **During glue-up (Phase 2):** Casco SF+ bead along each plate edge fills the triangular gap as the wall is pressed into place. The 6.5 mm gap is within SF+'s 10 mm gap-filling spec, with margin. Squeeze-out from the gap will be visible on the inside; tool with a wet finger or scrape after skin-over (~15 min).
2. **After 24 h SMP cure (Phase 3):** silicone fillet pass per §6.4 along every interior seam (back wall to plates, corner-cut wall to plates, back-to-corner-cut wall, all four side seams). The silicone is the airtight seal — acoustically critical for a sealed-Q sub box. The SF+ underneath is structural; the silicone is hermetic.

This combined approach gives a structurally and acoustically equivalent result to the cleat-based Strategy A. The visible interior seams may look a hair less crisp than a clean cleat-bevelled landing, but the box is hidden behind a decorative lid in a barely-visible cubby, so this doesn't matter.

**Strategy A (cleat strips) — feasible alternative if you prefer the more rigid joint.** Pre-glue four right-triangular cleats (bevelled at 22.1° on a table saw, ~16 × 16 mm cross-section) to the inside of the bottom and top plates along the back-wall and corner-cut-wall landings. The tilted walls then sit against the cleats with square 90° edges. Strongest joint, cleanest interior seam line. Requires ~158 cm² of MDF stock for the cleats and an additional Phase 1 step (~2 hours: rip cleats, glue + screw to plates, 1 h dry before main assembly). The earlier blanket "Strategy A skipped — panel doesn't have margin" justification was based on a wall-height bug; with corrected dimensions the 40 × 120 panel has 18 % slack with cleats. **Skipped here purely on build-simplicity grounds, not material constraint.** If you want to revert to Strategy A, the table saw must be set to 22.1° (NOT 18.4° — the bevel angle is also corrected).

**Strategy B (bevelled wall edges) — for reference.** Cut the top and bottom edges of the back wall and corner-cut wall at a 22.1° bevel (router + chamfer bit, or block plane). Bevelled edges mate flush with unmodified top/bottom plate edges. Cleanest visual joint, no cleats, but the bevel cuts are tedious on panel edges with no jig. Skipped because Strategy C achieves equivalent acoustics with less precision work.

**For the back-wall to corner-cut-wall seam** (interior dihedral 55.5° — independent of the tilt angle; only depends on the corner-cut geometry in plan view): bevel both edges at 27° each for a clean butt joint, OR use silicone fillet in the seam (Strategy C carries through here naturally). Recommended: silicone fillet — the 27° bevels are awkward to cut precisely and the joint is hidden inside the box.

**For the back wall ↔ side wall seams** (interior dihedral 90° — the back wall tilts toward the box interior, the side wall is vertical, the dihedral remains 90° because the tilt direction is perpendicular to the side wall plane): standard 90° butt joint. Drill pilot holes perpendicular to the back wall surface — the screws go in at the natural 22.1° tilt relative to horizontal, which is fine for the joint.

### 5.5 Glue + screw assembly sequence (Casco SuperFix+ + Strategy C)

Each step: bead-apply SMP + position panel + drive screws (snug, not aggressive — see §5 intro) + tool / scrape squeeze-out + square-check.

1. **Bottom plate** sits on a flat work surface, inside face up. (No pre-glued cleats — Strategy C.)
2. **Front wall ← bottom plate.** 5–8 mm bead of Casco SF+ along the front edge of the bottom plate; stand front wall on it; drive screws from below the bottom plate up into the front wall edge. 4 screws across the 37 cm joint. Snug only — the bead wants 1–3 mm of bond line. Tool any squeeze-out on the inside face with a wet fingertip or scrape after skin-over (~15 min).
3. **Left side wall (large trapezoid) ← bottom plate AND ← front wall.** SF+ bead on both contact edges; position the side wall so its bottom edge sits along the bottom plate's left edge AND its front edge mates with the left edge of the front wall; drive screws on both joints (3 from below into the side wall, 3 from the side wall into the front wall edge).
4. **Right side wall (small trapezoid) ← bottom plate AND ← front wall.** Mirror of step 3. The right side wall is small (4 cm at bottom, 10 cm at top) and sits between the front wall and where the corner-cut wall will go. Be especially careful with this small panel — its size makes it easy to over-compress the bead. Drive screws gently.
5. **Back wall ← bottom plate (Strategy C butt joint) AND ← left side wall.** This is the first tilted wall. SF+ bead along the back edge of the bottom plate; position the back wall so it leans **22.1° away from vertical** (use a sliding bevel gauge or a paper template cut at 22.1°); also bead-apply along the contact edge to the left side wall's slanted back edge; drive screws from outside the back wall into the bottom plate edge (3 screws — the screws bite at 22.1° into the plate edge, which is fine for a butt joint with SF+ filling the wedge gap) and into the left side wall edge (3 screws). The triangular gap on the inside (~6.5 mm at peak) fills with the SF+ bead's squeeze-out — tool any visible squeeze-out flat on the inside corner before skin-over. The wall is now held square in two of three axes; the corner-cut wall will pin it in the third.
6. **Corner-cut wall ← bottom plate AND ← back wall AND ← right side wall.** The wired terminal-cup panel goes in here. Three SF+ bead lines: bottom plate edge (Strategy C butt joint, same 22.1° tilt), back wall (left edge of corner-cut wall meets right edge of back wall along the 55.5° interior dihedral — SF+ fills the seam, silicone fillet later), and right side wall's slanted back edge. Drive screws from outside into all three. Carcass is now complete except for the top plate. Total of ~10–12 screws driven this step.
7. **30-minute pause.** Let SF+ skin over. Verify carcass is square: measure diagonals on the bottom plate (corner to corner, two diagonals — should agree within 2 mm); measure that the front wall is vertical with a square; verify the tilted walls' tops are symmetric about the box's centre line. Use this pause to scrape any inside-face squeeze-out flat — it'll wipe with white spirit on a paper towel before full cure.
8. **Wire-tuck and polyfill loose-fill.** Tuck the terminal cup's internal coil leads against the right side wall (out of the way of the driver cutout). Stuff polyfill loosely through the still-open top opening, ~135 g, lightly fluffed (final compression happens when the top closes). Tape a strip of masking tape across the wiring to keep polyfill clear of the terminal posts and the future driver cutout.
9. **Top plate (= driver baffle) ← all five wall edges (front, left side, right side, back wall, corner-cut wall — Strategy C butt joints on the two tilted-wall edges).** SF+ bead on all five wall top edges. Position the top plate from above. The two tilted-wall edges (back, corner-cut) form 22.1° contact with the underside of the top plate — the SF+ bead fills the wedge gaps (same triangular gap as on the bottom). Drive screws from above through the top plate into every wall edge — about 12–16 screws total around the perimeter and the corner cut. **Don't cut the driver hole yet** — see §8.2 (deferred to next weekend after full cure).
10. **24-hour SMP cure** before any further handling. Place a heavy weight (full 5 L ATF jug, car battery, etc.) on the top plate to ensure it presses fully into the SF+ beads. Don't apply more weight than needed to seat the panels — see §5 intro re. over-clamping SMP joints.

**Square-check between each step:** measure corner-to-corner diagonals on the bottom plate and the perimeter walls; if any diagonal disagrees with its pair by more than 2 mm, clamp the long diagonal until the glue sets. The single-axis taper makes a couple of natural square-checks impossible (the side walls aren't rectangles), so rely on the bottom plate's perimeter and the front wall's verticality as your main reference checks.

### 5.6 Decorative lid (separate from the box build)

The box's top plate IS the acoustic baffle and is structural. The cubby's factory lid (or a custom replacement) is a separate **decorative cover** that sits over the box, hiding it from view when the cubby is closed.

This lid is non-structural: thin substrate (3–6 mm hardboard, plywood, or foam-core composite) wrapped in upholstery fabric matched to the surrounding interior. It needs:

- A speaker grille opening cut to match the driver's grille (typically Ø 240–250 mm — driver will arrive with a clip-on grille of that size).
- Attachment to the cubby's factory hinges (or replacement hinges if originals are seized) — same screw pattern as factory.
- Adequate clearance over the box's top plate (at least 5 mm air gap so the driver's grille and any baffle-mounted screw heads don't bind on the lid as it closes).

The lid can be designed and built **after** the box is fully assembled and dropped into the cubby, since the lid's exact dimensions depend on the final box position. There is no rush; the box is acoustically complete with just its own top plate sealed.

### 5.7 Clamp / weight strategy

Where clamps are thin, stack phonebooks / full 5 L ATF jugs / car batteries on top of each joint while the SF+ skins over. **Important: SMP joints want a 1–3 mm bond line — don't over-weight.** Screws give 80 % of the clamp force; weights close the last 20 % of hairline gaps but should not squeeze the bead to nothing. For the tilted walls, use a strip of masking tape across the joint to hold them at the **22.1°** angle against the bottom (and later top) plate while the SF+ skins over — they'll otherwise tend to slump backward off the plate edge before tack-up. A scrap of plywood or a paper template cut at 22.1° dihedral, taped to the inside corner, gives a positive angle reference during the 20-minute open time.

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

After the carcass has cured 24 hours and is fully closed (top plate installed), run a 5–8 mm bead of neutral-cure silicone along every interior seam — there are about a dozen of them in this geometry. Work through a hand access (the driver cutout, once cut, is the easiest port — but for the current build phase the driver hole is not yet cut, so reach through the still-open terminal cup hole or open the box momentarily before the top plate goes on if needed).

Seams to caulk:

- Bottom plate ↔ front wall, left side wall, right side wall, back wall, corner-cut wall (5 seams along the bottom)
- Top plate ↔ all five walls (5 seams along the top)
- Front wall ↔ left side wall (1 vertical seam)
- Front wall ↔ right side wall (1 vertical seam)
- Left side wall ↔ back wall (1 slanted seam, dihedral 90°)
- Right side wall ↔ corner-cut wall (1 slanted seam, dihedral 90°)
- Back wall ↔ corner-cut wall (1 slanted seam, dihedral 55.5° — the sharp interior corner; load this one with extra silicone since it's also serving as the structural fillet for the awkward-angle joint per §5.4)

Tool each bead with a wet fingertip to push silicone into the seam. Hairline gaps at panel joints are the enemy of sealed-alignment Q — the silicone is insurance on top of the SF+ adhesive, AND it's the airtight final seal for the tilted-wall joints (Strategy C, §5.4). Pay particular attention to the back-wall-to-plate seams and the corner-cut-wall-to-plate seams; the SF+ filled the gross 5 mm wedge gap during glue-up, but the silicone seals the final hairline at the inside corner.

Cure time before any further work: **48 hours minimum.** Premature handling can crack the silicone fillet.

---

## 7. Polyfill

- **~135 g** of polyester fibre fill (Autoviihde "vaimennusvilla", or pillow-stuffing from Sinelli / Tokmanni — same material). Quantity scaled for the realised 11.3 L raw internal volume at ~12 kg/m³ packing density.
- Fill to approximately **40 % compression** — fluffed up to roughly fill the box with light mounding above the top opening, then press down so the top plate (baffle) compresses it to snug-but-not-packed.
- Test rule: when you close the top plate, the polyfill should offer mild resistance but not prevent the plate sitting flat. Over-stuffing is worse than under-stuffing — packed fill acts more like rigid volume loss than like damping.
- Do **not** let polyfill drape over the wiring or the terminal cup binding posts on the corner-cut wall — it can get pulled into the driver cutout during installation. Tuck the internal coil leads against the right side wall, away from the driver cutout's path through the polyfill cloud. Run a strip of masking tape across the polyfill near the cutout area to hold fill clear of the central driver position.
- Polyfill packing density also affects realised Qtc by ~0.02 — i.e., the same magnitude as the volume shortfall in §3.4. If during the eventual bench test (`work/audio_bench_test.md`) the sub sounds slightly punchy, slightly looser packing (less polyfill or less compression) trades Qtc back down. This tuning headroom is in your favour.

---

## 8. Driver install — DEFERRED to the weekend after cure

Do **not** mount the driver on Sunday. The silicone and Casco SF+ need 24–48 hours to reach full cure, and a premature gasket compression can distort the baffle or drag on the wet silicone.

### 8.1 When to do it

After ≥48 hours from the silicone pass. Paint/seal the baffle cutout raw edge with thinned PVA, silicone, or polyurethane wipe-on (edge moisture barrier) before seating the driver.

### 8.2 Baffle cutout

The top plate (= driver baffle) is a 37 × 33 cm pentagonal panel with the 15 × 23 corner cut at the back-right. The driver cutout needs to be positioned so the Ø 254 mm flange (with mounting screw bolt circle) clears all panel edges including the diagonal corner cut.

- **Centre position:** 18.5 cm from each side edge (centred on the 37 cm width axis), and **13 cm back from the front edge** of the top plate.
- **Verify clearance** before drilling: at the cutout's far-right (x = 31.2 cm from the left edge), the top plate's diagonal cut sits at y = 18.9 cm from the front; the cutout's nearest point on that side is at y = 13 cm. Clearance to the diagonal edge: ~6 cm at the closest point. Plenty for the flange + mounting screws.
- Diameter: **221 mm** (confirm on driver with calipers — some datasheet figures are nominal).
- Draw the circle with a compass or trammel points pinned at (18.5, 13). Drill a 10 mm starter hole inside the line.
- Jigsaw with fine wood blade + circle jig, or a 221 mm hole saw if owned.
- Cut on the waste side of the line. Sand back to the line with 80-grit on a flat block — slow, but gives a driver-fits-cleanly finish.
- Vacuum all dust. MDF dust inside the box is fine (polyfill catches it), but dust on the driver magnet gap is bad.

### 8.3 Driver seating

1. Check the driver's foam gasket for damage. If compressed or torn, substitute with 3 mm closed-cell foam ring cut to match the flange.
2. Connect internal coil leads to driver terminals A+ / A− / B+ / B− per labelling from §6. Double-check polarity — Helix datasheet shows the terminal polarity on the driver rear cover.
3. Seat the driver into the cutout with the foam gasket between the flange and the baffle.
4. Drive driver mounting screws — typically 6 × M4 × 30 mm wood screws (or whatever the driver hardware specifies). Pilot-drill all six holes first. Torque snug + 1/8 turn — **don't crush the gasket**, don't over-torque and split the MDF. 2–3 Nm is the target.
5. Work in a diagonal pattern: top → bottom → left → right → top-right → bottom-left. Gradual even compression.

### 8.4 M6 stabilizer screw — DEFERRED

The Helix datasheet calls out an M6-threaded hole on the magnet pole piece, intended for back-bracing the driver to the bottom plate via a spacer to prevent magnet sag in high-excursion installs.

**Decision (2026-04-27): skip the stabilizer install.** Recommended by Autoviihde staff who noted they do not install it on this class of build. Rationale:

- The stabilizer matters most in **ported boxes** and **competition / high-Xmax setups** where reaction forces on the magnet are large and sustained.
- For a 10″ sealed box at 300 W RMS in ~12.5 L effective, sealed loading naturally limits Xmax to safe levels — magnet sag is essentially a non-issue at this excursion regime.
- Skipping avoids: (a) drilling and sealing a clearance hole through the cured bottom plate, (b) measuring and procuring the correct spacer length, (c) introducing an additional mechanical resonance path between driver and box.

The threaded hole on the pole piece **stays available** — if any sag is ever observed (very unlikely), a retrofit is straightforward: drill a 7 mm clearance hole in the bottom plate from underneath, insert spacer + M6 bolt, seal with neutral-cure silicone. Documented here so the option isn't lost.

---

## 9. Finish

The decorative lid (§5.6) covers the entire box from view, so the box's external finish is primarily a moisture-barrier and dust-repellence concern, with the secondary benefit of hiding the proud-screw-head cosmetic issue from glue-up.

**Decision (2026-04-27): wrap with acoustic carpet.** Acquired from Autoviihde — 2 m² dark-grey acoustic carpet (subwoofer cover material), enough for the box outer surfaces (~0.45 m²), the decorative lid top + edges (~0.30 m²), and ~1.25 m² spare. Adhesive: spray contact (3M Super 77 / equivalent — confirm Autoviihde's recommended brand at application time). Stretches over the proud screw heads and the slight angular wobble at the corner-cut wall — both disappear under the wrapped fabric. Standard car-audio install practice for a cubby-hidden box, and the spare material lets the decorative lid match the box's appearance for a unified look if the lid is ever opened.

Application order: cure-confirm the SF+/silicone (≥48 h since glue-up) → mask the driver cutout opening → spray adhesive on box face + carpet backing → press, smooth, edge-tuck → trim opening with a sharp blade. Repeat for each face.

**Alternatives kept on file for reference:**

- **Raw MDF** — fastest path. Fine if storage is dry. MDF absorbs ambient cabin moisture over years; if the car is regularly garaged in damp conditions, consider painting or polyurethane wipe-on instead.
- **Paint** — Hammerite black or similar, 2 coats; sand edges first. Good moisture barrier; doesn't hide the proud screws.
- **Polyurethane wipe-on** — single thinned coat. Negligible thickness change, low aesthetic commitment, good moisture barrier; doesn't hide the proud screws either.

---

## 10. References and cross-links

- Design origin: `work/audio_upgrade_blueprint.md` §5, §7
- Part sourcing + CCA kit decision: `docs/parts_to_order.md` Priority 6B
- Bench test of the completed-enough box: `work/audio_bench_test.md`
- Permanent DSP mounting + wiring finalisation (next weekend): `work/center_console_refresh/README.md` §4
- Build diary entries: `docs/diary/2026-04.md` Apr 24 (weekend plan), Apr 25 (cubby measurement + geometry lock), Apr 26 (to be written during/after build)

## 11. Geometry decisions log

Maintain this section as decisions are made or revised. The geometry was iterated three times before lock-in:

| Date | Decision | Rationale |
| :--- | :--- | :--- |
| 2026-04-24 | Initial design: rectangular 33.2 × 33.2 × 19.2 cm box, 14.4 L internal, 6 panels, all 90° joints | Clean simple shape from datasheet target |
| 2026-04-25 morning | Cubby dimensions reported approximately 25 × 30 cm at floor, 35 × 40 cm at lid line, 18 cm height — original rectangular design wouldn't fit; explored frustum and stepped-rectangle alternatives | First geometry reality check |
| 2026-04-25 evening | Cardboard mock-up complete; cubby measured exactly: floor 37 × 27 with 15 × 23 corner cut, lid line 37 × 33 with 15 × 15 corner cut, height 18 cm. Decorative-lid architecture chosen (thin substrate covers structural box top plate) | Mock-up is authoritative; lid separation simplifies the box's structural duty |
| 2026-04-25 evening | Build simplification: corner-cut wall must be flat MDF, requires 15 × 23 cut at BOTH top and bottom (top cut enlarged from 15 × 15 by 8 cm × 15 cm wedge of dead air at the back-right corner of the lid plane). External volume drops 0.5 L (17.4 → 16.9 L), effective volume drops ~0.5 L (~12.5 L final). Joinery becomes tractable. | Inaudible volume cost vs. major build complexity savings; verified analytically that exact cubby fit requires non-planar twisted corner-cut wall |
| 2026-04-25 evening | Final dimensions locked. Cleat-strip joinery chosen for the tilted back wall and corner-cut wall (Strategy A in §5.4); silicone-fillet fallback documented as Strategy C if cleats prove fiddly. | Build doc executable as written |
| 2026-04-25 (Sat shopping) | Joinery flipped: **Strategy C silicone-fillet adopted as default**, cleats dropped. Cause: 40 × 120 cm MDF acquired Saturday (vs the 60 × 100 originally spec'd) — ~5 % too tight to include cleat-strip stock with realistic kerf. Strategy C requires no cleats, removes 4 cuts and one Phase 1 step, and combines naturally with the SMP gap-filling adhesive (next row). | Material constraint forced the simpler joinery; acoustically and structurally equivalent per analytical comparison. Strategy A preserved in §5.4 for future retrofit reference. |
| 2026-04-25 (Sat shopping) | Adhesive substituted: **Casco SuperFix+** (SMP / silane-modified polymer construction adhesive) replaces PVA D3. Properties: 100 % solids, ~20 min open time, gap-filling up to 10 mm, Shore A 45–50 cured (semi-elastic), tensile 2.2 MPa, 500 % elongation at break, moisture-cure 3 mm/24 h. | SF+ is **better matched** to this build than PVA: gap-filling absorbs panel-saw kerf inaccuracy (helpful given the tight 40 × 120 layout), 20 min open time eases square-checking, elastic cure resists hairline-crack development at MDF joints under bass pressure, Strategy C butt-joint gaps fill cleanly during glue-up. Application change: bead-apply, don't over-clamp (1–3 mm bond line preferred). |
| 2026-04-25 (Sat shopping) | Terminal cup acquired: **included in Helix IK S10-DVC2 shipment** — no separate purchase needed. Verify before install: (a) 4 binding posts (two pairs, one per coil) for DVC2 isolation, (b) gasket present (or substitute thin silicone ring during install). | Saves the Autoviihde trip from the shopping list; if the included cup is single-pair, fall back to drilling a 4-post cup or buying a dual at Autoviihde during the week. |
| 2026-04-25 evening | DSP relocated to passenger-side cubby. The 16.9 L sub box fully consumes the driver-side cubby; the DSP's 1.7 L footprint plus heatsink ventilation clearance does not fit. The terminal-cup placement on the corner-cut wall (§4.2) remains unchanged — that wall already faces the passenger-side cubby across the rear bulkhead, so the speaker leg routes naturally. See `work/audio_upgrade_blueprint.md` §1 and `work/center_console_refresh/README.md` §5.7b. | Geometry consequence; no build-side change beyond a shorter local pigtail from the cup (the long run is the cubby-to-cubby leg, owned by the console-refresh task). |
| **2026-04-26 noon — wall-height correction (cut-list bug fix)** | **Cut list panels 3–7 (front wall, back wall, both side trapezoids, corner-cut wall) had wall heights set to 18 cm — the full external box height — but §4 prose explicitly says "bottom-and-top plates capture the four side walls between them". With 16 mm plates top and bottom, walls span only `180 − 16 − 16 = 148 mm` vertically. Tilted-wall slant length is therefore `sqrt(148² + 60²) = 159.7 mm ≈ 16 cm`, NOT 19 cm; tilt angle is `atan(60 / 148) = 22.1°`, NOT 18.4°.** Updated panels: front 37 × 14.8, back 22 × 16 slant, left side trap h=14.8, right side trap h=14.8, corner-cut wall 27.5 × 16 slant. Tilt angle changed from 18.4° to 22.1° in §3.1, §5.4, §5.5, §5.7. | User catch (Sun ~12:10) on the cut-list math. Volume math in §3.3 was already correct (it always used 14.8 cm internal height) — only the cut-list dimensions were affected. Total panel area drops from 4149 → 3764 cm² (a 9 % reduction), which means the 40 × 120 cm panel actually has 18 % slack with cleats included (Strategy A would fit) — the earlier "panel too tight, force Strategy C" rationale was based on the buggy higher area number. Strategy C retained as default for build-simplicity reasons (saves ~2 h Phase 1 cleat-rip + pre-glue), but Strategy A is now an open option if the user prefers a more rigid joint. The SF+ wedge gap on Strategy C joints grows from 5 mm to 6.5 mm — still well within the SF+ 10 mm gap-filling spec. |
| 2026-04-27 evening — M6 stabilizer screw deferred + acoustic carpet acquired | (1) **M6 stabilizer install (§8.4) deferred.** Autoviihde staff recommended skipping; consistent with industry practice for sealed-box / non-competition installs at this excursion class. Threaded hole on driver pole piece stays available for future retrofit. (2) **Box finish (§9) finalised: acoustic carpet wrap.** 2 m² dark-grey acoustic carpet acquired from Autoviihde for the sub box (~0.45 m²) + decorative lid (~0.30 m²) + spare (~1.25 m²). Wraps over proud screw heads and corner-cut-wall angle wobble cleanly. Spray adhesive to be confirmed at application time per Autoviihde's recommendation. | Build-decision day after the cure started. M6 skip removes one step from the post-cure driver-install sequence; carpet wrap removes the proud-screw cosmetic issue without the counterboring detour and gives moisture protection as a bonus. Both decisions reduce remaining workload before driver install. |

---

*Originally created 2026-04-24 as a weekend-prep artifact with three rectangular options (A/B/C). Substantially revised 2026-04-25 evening following cardboard mock-up measurement, with single-axis-tapered geometry and tilted-wall joinery strategy locked in. Build execution on 2026-04-26.*
