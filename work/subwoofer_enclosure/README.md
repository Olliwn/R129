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

† **Build simplification:** the cubby intrusion is only 15 × 15 at the lid-line level, but the box's top plate uses the bottom plate's larger 15 × 23 cut anyway. This makes the corner-cut wall a single flat MDF panel (with the same 18.4° tilt as the back wall) instead of a twisted/multi-faceted surface. The dead air this leaves at the top corner — an 8 × 15 cm wedge tapering to nothing at the floor — costs ~0.5 L of external volume but eliminates a hard joinery problem. See §3 for the full trade-off analysis.

---

## 3. Dimensioning — single-axis-tapered single-corner-chamfered box

### 3.1 Geometry summary

The box is a prismatoid with:

- **Constant width** (37 cm) on the left-right axis — front wall and back wall are full-width.
- **Tapered depth** on the front-back axis (27 cm at floor → 33 cm at lid line) — left and right side walls are TRAPEZOIDS with parallel edges of 27 cm (bottom) and 33 cm (top), and slant height ≈ 19 cm.
- **Chamfered corner** (15 × 23 cm right-triangle removed from the back-right corner, same cut at top and bottom) — adds a single flat diagonal corner-cut wall.
- **Two tilted walls:** the back wall and the corner-cut wall both tilt 18.4° from vertical, in the same direction (away from the box interior as you go up). The front wall and side walls are vertical.

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

Cut-list area for the 7-panel build (see §4):

- Top plate (37 × 33 with 15 × 23 cut): 1049 cm²
- Bottom plate (37 × 27 with 15 × 23 cut): 827 cm²
- Front wall (37 × 18): 666 cm²
- Back wall (22 × 19, allowing for slant length): 418 cm² — note: the back wall only spans from x=0 to where the corner cut starts at x=22, not the full 37 cm box width
- Left side wall (trapezoid, parallel sides 27 + 33, height 18): 540 cm²
- Right side wall (trapezoid, parallel sides 4 + 10, height 18): 126 cm² (this is the SHORT right side, between front edge and corner cut)
- Corner-cut wall (rectangle, 27.5 × 19): 523 cm²
- **Total panel area: 4149 cm² ≈ 0.41 m²**
- Plus kerf + waste + spare (20 %, higher than rectangular build because of the angled cuts): **0.50 m²**
- Plus 4 cleat strips (16 × 16 mm cross-section, 22 + 22 + 27.5 + 27.5 = 99 cm length total): negligible — cut from offcuts.

A single **60 × 100 cm** raw sheet of 16 mm MDF from Bauhaus with panel-saw cuts is enough, with margin for one mistake or one re-cut.

---

## 4. Cut list — 7-panel single-axis-tapered build

Construction style: **bottom-and-top plates capture the four side walls between them**. The two trapezoidal side walls and the two tilted walls (back, corner-cut) all sit on the bottom plate edges; the top plate caps them. This style assembles square more naturally than full-height bookends when the side walls are trapezoidal.

### 4.1 Panel cut list

| # | Panel | Qty | Dimensions (cm) | Cut style | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Bottom plate | 1 | 37 × 27 with 15 × 23 corner cut at back-right | Pentagonal (5-sided) | All edges 90°. Mark cut lines on a 37 × 27 rectangle; cut diagonally from (22, 27) to (37, 4). |
| 2 | Top plate (= driver baffle) | 1 | 37 × 33 with 15 × 23 corner cut at back-right | Pentagonal (5-sided) | All edges 90°. Same diagonal direction as bottom but from (22, 33) to (37, 10). **Driver cutout (Ø 221 mm) cut LAST**, after carcass cure — see §8.2. |
| 3 | Front wall | 1 | 37 × 18 | Rectangle | All edges 90°. Faces front of cubby. |
| 4 | Back wall | 1 | **22** × 19 (slant length, oversize by ~5 mm and trim flush after assembly) | Rectangle | All edges 90°. Width is 22 cm — the back wall only spans from x=0 to where the corner cut starts at x=22, not the full box width. The remaining back-of-box area (x=22 to x=37) is covered by the corner-cut wall. Tilts 18.4° from vertical in the assembled box; see §5.4 for joinery. |
| 5 | Left side wall (trapezoid) | 1 | Parallel edges 27 + 33, height 18, slant edge sqrt(6² + 18²) ≈ 19.0 | Right-trapezoid | Front edge vertical 18 cm; bottom edge horizontal 27 cm; top edge horizontal 33 cm; back edge slants 19.0 cm at 18.4° from vertical. All edges 90° square cuts. |
| 6 | Right side wall (small trapezoid, ahead of corner cut) | 1 | Parallel edges 4 + 10, height 18, slant edge ≈ 19.0 | Right-trapezoid | Mirror of #5 but truncated by the corner cut. Front edge vertical 18 cm; bottom edge 4 cm; top edge 10 cm; back edge slants 19.0 cm meeting the corner-cut wall. Small panel, easy to mis-cut — measure twice. |
| 7 | Corner-cut wall | 1 | 27.5 × 19 (slant length, oversize by ~5 mm and trim flush after assembly) | Rectangle | All edges 90°. Tilts 18.4° from vertical. Diagonal-direction face. **Terminal cup hole pre-cut here, before installation** — see §5.3. Position: centred on the panel, ~5 cm up from bottom edge. |
| 8 | Cleat strips (4 × triangular) | 4 | 16 × 16 × ~22 / ~22 / ~27.5 / ~27.5 cm long | Right-triangle cross-section, ripped on table saw at 18.4° bevel | One pair (top/bottom of the back wall joint, ~22 cm) provides the bevelled landing for the back wall; second pair (~27.5 cm) does the same for the corner-cut wall. See §5.4. |

**Verification of internal volume:** prismatoidal formula with internal cross-sections (§3.3) → 11.3 L raw → 12.5 L effective with polyfill ✓

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
> - Etuseinä: 370 × 180 (1 kpl)
> - Takaseinä: 220 × 195 (1 kpl) — ylimittainen, höylätään asennuksen jälkeen
> - Kulmaseinä: 275 × 195 (1 kpl) — ylimittainen, höylätään asennuksen jälkeen
>
> Trapetsit (suorakulmainen trapetsi, lyhyempi sivu vasemmalla):
> - Vasen sivu: korkeus 180, alaosa 270, yläosa 330 (1 kpl)
> - Oikea sivu: korkeus 180, alaosa 40, yläosa 100 (1 kpl)
>
> Viisikulmiot (suorakulmio, jonka oikeasta yläkulmasta leikataan kolmio pois — terä jolla 15 × 23 cm):
> - Pohjalevy: 370 × 270, kolmio 150 × 230 oikea yläkulma (1 kpl)
> - Kansilevy: 370 × 330, kolmio 150 × 230 oikea yläkulma (1 kpl)
>
> Lisäksi rimoja (alkuperäisestä levystä leikatut):
> - 4 kpl 18° viistettyä rimaa, n. 16 × 16 mm, pituudet 220 / 220 / 275 / 275 mm (kotona viimeistely riittää, ei panel-saw)
>
> Kiitos."

Ask them to cut in this order: large rectangles first, then trapezoids, then pentagonal pieces (most fiddly last). 3 mm kerf per cut is normal; budget for it in the sheet-area math.

The cleat strips (item 8) are ripped at home on a table saw or hand-cut with a guide — too small for a panel saw and need a specific bevel angle. If you don't have a table saw, the silicone-fillet alternative (see §5.4) avoids the cleat strips entirely.

---

## 5. Assembly order

Materials on hand before starting: PVA D3 wood glue, 4 × 40 mm wood screws (28–36 pcs), 3 mm pilot drill bit, neutral-cure silicone (one full tube), masking tape, clamps or heavy weights, square, pencil, tape measure, sliding bevel gauge (for marking the 18.4° tilt and laying out cleat strips), dust mask (MDF dust is irritant), shop vac.

The build proceeds in three phases:

- **Phase 1: Sub-assemblies.** Cleat strips glued to bottom and top plates (§5.1), terminal cup wired into the corner-cut wall (§5.3), pilot holes drilled (§5.2). Each step is independent and can be done in any order.
- **Phase 2: Carcass glue-up.** Bottom plate is the foundation; vertical walls (front, sides) go up next; tilted walls (back, corner-cut) lean in against the cleat strips; top plate caps it (§5.5).
- **Phase 3: Cure + seal.** 24-hour PVA cure, then silicone fillet pass on every interior seam (§6.4), then 48-hour silicone cure before any further work.

### 5.1 Cleat strip preparation (do this first)

Four 16 × 16 mm triangular strips, each with one face bevelled at 18.4°:

- 2 strips (~22 cm) for the back-wall landing — one glues to the inside of the bottom plate along its rear edge (from x=0 to x=22 — i.e., only the portion of the rear edge that the back wall covers, not extending into the corner-cut region), one glues to the inside of the top plate along the matching position.
- 2 strips (~27.5 cm) for the corner-cut-wall landing — same arrangement, along the diagonal cut edge of the bottom and top plates.

Cutting the strips on a table saw: rip a 16 mm-wide strip from offcut MDF with the blade tilted 18.4°. The result is a right-triangular cross-section — the 90° face glues to the plate, the bevelled face receives the tilted wall. If no table saw is available, hand-plane a 18.4° bevel on a square-section strip with a block plane and a marking gauge — slow but very doable for 4 × 30 cm of work.

Pre-glue the cleats to the **inside faces** of the bottom plate and top plate before any other assembly. Glue + drive 3-4 small screws (3 × 25 mm) per cleat from the OUTSIDE of the plate into the cleat. Let dry 1 hour minimum before plate-to-wall assembly.

**Alternative path (no cleats):** if cleats feel like too much fuss, skip them entirely and use the silicone-fillet butt-joint method (§5.4 below). The build will be ~2 hours faster but the joints rely on the silicone fillet for both sealing AND structural reinforcement at the tilted-wall edges. Acoustically equivalent, structurally adequate for this driver, but less robust against rough handling.

### 5.2 Drill pilot holes

Mark screw positions:

- Bottom plate / top plate to wall joints: every 6–8 cm along the joint, 4 cm in from each end.
- Wall-to-wall joints (front-to-side, side-to-back, back-to-corner-cut): every 8 cm along the joint.
- Through cleat strips: 3 screws per cleat, evenly spaced along the strip's length, into the receiving wall edge.

Drill 3 mm pilot holes **through the outer panel into the edge of the inner panel**. Depth 25–30 mm. 16 mm MDF splits if you skip the pilot holes — non-negotiable. Countersink lightly so screw heads sit flush.

### 5.3 Terminal cup wiring + install on the corner-cut wall

Wire the terminal cup BEFORE installing the corner-cut wall in the carcass — much easier on a flat panel.

1. Cut the terminal cup opening on the corner-cut wall (panel 7) per its hardware spec — typically jigsaw for a rectangular cup, hole saw for a circular one.
2. Wire the cup per §6 (DVC2 isolation — critical step).
3. Test continuity per §6.3 — log DCR values in the build diary BEFORE the panel is buried in the carcass.
4. Set the wired panel aside, taped face-down on a clean surface so the binding posts aren't damaged during handling.

### 5.4 Tilted-wall joinery — choose ONE strategy at the start

The back wall (panel 4) and corner-cut wall (panel 7) both tilt 18.4° from vertical. Their top and bottom edges meet the top and bottom plates at 18.4° dihedrals (not 90°). Three strategies to handle this — pick one and use it consistently:

**Strategy A (recommended): cleat strips.** As prepared in §5.1. Both tilted walls have square 90° edges and rest against the bevelled cleats. The walls are screwed THROUGH from outside into the cleat (the cleat absorbs the angled bite). Strongest, cleanest joint.

**Strategy B (alternative): bevel the wall edges.** Cut the top and bottom edges of the back wall and corner-cut wall at an 18.4° bevel (using a router with a chamfer bit set to 18°, OR a block plane and patience). The bevelled edges then mate flush with the unmodified top and bottom plate edges. Cleanest visual joint, no cleat strips, but the bevel cuts are tedious on long panel edges.

**Strategy C (silicone-fillet shortcut): all 90° edges, fill the gap.** Cut every panel with 90° edges. When the tilted walls are installed, the bottom and top edges sit at 18.4° against the plates, leaving a triangular gap of ~5 mm at the maximum point on the inside corner. After full assembly and PVA cure, run a generous bead of neutral-cure silicone along each gap and tool with a wet fingertip. The fillet seals AND fills, providing a structural-glue bond to supplement the screws. Acoustically and structurally adequate; visually the seams look slightly less crisp than A or B (but the box is hidden in the cubby so this doesn't matter).

**For the back-wall to corner-cut-wall seam** (interior dihedral 55.5°, sharper than 90°): bevel both edges at 27° each for a clean butt joint, OR use silicone fillet in the seam (Strategy C carries through here naturally). Recommended: silicone fillet — the 27° bevels are awkward to cut precisely and the joint is hidden inside the box.

**For the back wall ↔ side wall seams** (interior dihedral 90° — the back wall tilts toward the box interior, the side wall is vertical, the dihedral remains 90° because the tilt direction is perpendicular to the side wall plane): standard 90° butt joint. Drill pilot holes perpendicular to the back wall surface — the screws go in at the natural 18.4° tilt relative to horizontal, which is fine for the joint.

### 5.5 Glue + screw assembly sequence

Each step: glue-up + screw-drive + wipe excess + square-check.

1. **Bottom plate** sits on a flat work surface, inside face up, with cleat strips already glued in place per §5.1.
2. **Front wall ← bottom plate.** Bead of PVA along the front edge of the bottom plate; stand front wall on it; drive screws from below the bottom plate up into the front wall edge. 4 screws across the 37 cm joint.
3. **Left side wall (large trapezoid) ← bottom plate AND ← front wall.** Glue both contact edges; position the side wall so its bottom edge sits along the bottom plate's left edge AND its front edge mates with the left edge of the front wall; drive screws on both joints (3 from below into the side wall, 3 from the side wall into the front wall edge).
4. **Right side wall (small trapezoid) ← bottom plate AND ← front wall.** Mirror of step 3. The right side wall is small (4 cm at bottom, 10 cm at top) and sits between the front wall and where the corner-cut wall will go. Be especially careful with this small panel — clamp it gently while screws drive.
5. **Back wall ← cleat strip on bottom plate AND ← left side wall.** This is the first tilted wall. Glue the cleat strip's bevelled face; position the back wall so its bottom edge rests on the cleat (the wall now leans 18.4° away from vertical, toward the back of the cubby); also glue the contact edge to the left side wall's slanted back edge; drive screws from outside the back wall into both the cleat strip (3 screws) and the left side wall edge (3 screws). The wall is now held square in two of three axes; the corner-cut wall will pin it in the third.
6. **Corner-cut wall ← cleat strip on bottom plate AND ← back wall AND ← right side wall.** The wired terminal-cup panel goes in here. Three glue lines this time: cleat (bottom), back wall (left edge of corner-cut wall meets right edge of back wall along the 55° interior dihedral — silicone fillet later), and right side wall's slanted back edge. Drive screws from outside into all three. Carcass is now complete except for the top plate.
7. **30-minute pause.** Let PVA tack up. Verify carcass is square: measure diagonals on the bottom plate (corner to corner, two diagonals — should agree within 2 mm); measure that the front wall is vertical with a square; verify the tilted walls are symmetric about the box's centre line.
8. **Wire-tuck and polyfill loose-fill.** Tuck the terminal cup's internal coil leads against the right side wall (out of the way of the driver cutout). Stuff polyfill loosely through the still-open top opening, ~135 g, lightly fluffed (final compression happens when the top closes). Tape a strip of masking tape across the wiring to keep polyfill clear of the terminal posts and the future driver cutout.
9. **Top plate (= driver baffle) ← cleat strips on top plate (back-wall and corner-cut-wall landings) AND ← all four wall edges (front, left side, right side).** Glue all four edges. Position the top plate from above; the cleat-strip-bevels on its underside register against the back wall and corner-cut wall, locking the assembly's tilt. Drive screws from above through the top plate into every wall edge — about 12-16 screws total around the perimeter and the corner cut. **Don't cut the driver hole yet** — see §8.2 (deferred to next weekend after full cure).
10. **24-hour PVA cure** before any further handling. Place a heavy weight (full ATF jug, etc.) on the top plate to ensure it presses fully into the glue.

**Square-check between each step:** measure corner-to-corner diagonals on the bottom plate and the perimeter walls; if any diagonal disagrees with its pair by more than 2 mm, clamp the long diagonal until the glue sets. The single-axis taper makes a couple of natural square-checks impossible (the side walls aren't rectangles), so rely on the bottom plate's perimeter and the front wall's verticality as your main reference checks.

### 5.6 Decorative lid (separate from the box build)

The box's top plate IS the acoustic baffle and is structural. The cubby's factory lid (or a custom replacement) is a separate **decorative cover** that sits over the box, hiding it from view when the cubby is closed.

This lid is non-structural: thin substrate (3–6 mm hardboard, plywood, or foam-core composite) wrapped in upholstery fabric matched to the surrounding interior. It needs:

- A speaker grille opening cut to match the driver's grille (typically Ø 240–250 mm — driver will arrive with a clip-on grille of that size).
- Attachment to the cubby's factory hinges (or replacement hinges if originals are seized) — same screw pattern as factory.
- Adequate clearance over the box's top plate (at least 5 mm air gap so the driver's grille and any baffle-mounted screw heads don't bind on the lid as it closes).

The lid can be designed and built **after** the box is fully assembled and dropped into the cubby, since the lid's exact dimensions depend on the final box position. There is no rush; the box is acoustically complete with just its own top plate sealed.

### 5.7 Clamp / weight strategy

Where clamps are thin, stack phonebooks / full 5 L ATF jugs / car batteries on top of each joint while the glue sets. Screws give 80 % of the clamp force; weights close the last 20 % of hairline gaps. For the tilted walls, use a strip of masking tape across the joint to hold them in position against the cleat strip while the glue sets — they'll otherwise tend to slump backward.

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

Tool each bead with a wet fingertip to push silicone into the seam. Hairline gaps at panel joints are the enemy of sealed-alignment Q — the silicone is insurance on top of the glue, AND it's load-bearing for the tilted-wall joints if Strategy C (no cleats) was chosen in §5.4.

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

Do **not** mount the driver on Sunday. The silicone and PVA need 24–48 hours to reach full cure, and a premature gasket compression can distort the baffle or drag on the wet silicone.

### 8.1 When to do it

After ≥48 hours from the silicone pass. Paint/seal the baffle cutout raw edge with thinned PVA or silicone (edge moisture barrier) before seating the driver.

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

---

## 9. Finish (deferred — optional)

Not required for acoustic performance. The decorative lid (§5.6) covers the entire box from view, so the box's external finish is purely a moisture-barrier and dust-repellence concern.

- **Raw MDF** — fine in the cubby since the decorative lid covers it. Fastest path. MDF will absorb ambient cabin moisture over years; if the car is regularly stored in a damp garage, consider one of the next two options.
- **Paint** — Hammerite black or similar, 2 coats. Sand edges first. Provides good moisture barrier.
- **Polyurethane wipe-on** — single coat of thinned wipe-on poly. Negligible thickness change. Good moisture barrier without much aesthetic commitment.

Carpet wrap (the original Option C) is unnecessary now that the lid is decorative-only. Save the effort.

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
| 2026-04-25 evening | DSP relocated to passenger-side cubby. The 16.9 L sub box fully consumes the driver-side cubby; the DSP's 1.7 L footprint plus heatsink ventilation clearance does not fit. The terminal-cup placement on the corner-cut wall (§4.2) remains unchanged — that wall already faces the passenger-side cubby across the rear bulkhead, so the speaker leg routes naturally. See `work/audio_upgrade_blueprint.md` §1 and `work/center_console_refresh/README.md` §5.7b. | Geometry consequence; no build-side change beyond a shorter local pigtail from the cup (the long run is the cubby-to-cubby leg, owned by the console-refresh task). |

---

*Originally created 2026-04-24 as a weekend-prep artifact with three rectangular options (A/B/C). Substantially revised 2026-04-25 evening following cardboard mock-up measurement, with single-axis-tapered geometry and tilted-wall joinery strategy locked in. Build execution on 2026-04-26.*
