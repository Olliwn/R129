# Center Console Refresh — Wood Polish, Switch Cleaning, BE2210 High-Level Tap & Cable Routing

## Overview
The R129's center console Zebrano/Burl Walnut wood trim panels are original and in decent cosmetic condition but would benefit from a proper removal, cleaning, polishing, and re-clear-coating. At the same time, the console switches (soft-top, hazard, seat heater, etc.) all function electrically but feel "sticky" and lack the crisp tactile click of new switches — 35 years of dust, skin oils, and nicotine residue accumulating around the rocker mechanisms.

All of this requires pulling the BE2210 and the wood trim — which is *also* the only reasonable opportunity to tap the BE2210's high-level speaker outputs for the Match UP 6DSP and to pull every cable the RPi5 + DSP system will ever need between the front cubby and the rear cubbies. Doing it all in a single console-out event avoids ever having to open this area again.

> **DSP location update (2026-04-25):** The UP 6DSP has been relocated to the **rear passenger-side cubby** (not driver-side as originally planned). The driver-side cubby is fully consumed by the subwoofer enclosure (geometry locked 2026-04-25, see `work/subwoofer_enclosure/README.md`). All "rear cubby" references below that concern the DSP / its inputs / its outputs to the front stage now mean the **passenger-side** cubby. The sub speaker leg is the only run that gains extra length (~1.6 m driver-to-passenger via under-bulkhead-carpet OR through the center console while it's open) — see §5.7b below.

This project combines five objectives into a single console disassembly:

1. **Wood Trim Removal & Polish** — Remove all center console wood panels, clean, polish, and optionally re-lacquer/clear-coat on the bench.
2. **Switch Refresh** — Remove, disassemble, clean, and re-lubricate all center console switches to restore crisp tactile feel.
3. **BE2210 → UP 6DSP High-Level Tap** — Tap the BE2210 ISO speaker outputs (L+, L−, R+, R−) and pull a **shielded CAT6 run** (4 pairs, using 2 pairs for LF/RF tap + 2 pairs reserved as future spares) from the radio all the way back to the rear cubby, so the Match UP 6DSP can (a) play cassette/FM through the new active front stage and subwoofer, and (b) auto-wake off the BE2210 signal without needing a dedicated remote wire. *(See: [work/audio_upgrade_blueprint.md](../audio_upgrade_blueprint.md) §5 and Path 3.)*
4. **RPi5 + DSP Cable Routing** — While the console is apart, pull *every* cable the infotainment and audio systems need, in both directions, in one pass. *(See: [UI_rpi5/radio_uiknob.md](../../UI_rpi5/radio_uiknob.md) and [work/audio_upgrade_blueprint.md](../audio_upgrade_blueprint.md).)*
5. **Wireless iPhone Charger (drawer cubby)** — Embedded Qi pad under the drawer floor behind the ashtray. Phone sits flat in the drawer and charges hidden, lid closed. Powered from the cigarette-lighter hot wire (KL15 / MAIN_12 8A — ignition-switched, zero parasitic draw with key out, field-verified 2026-04-07) via a small 12 V → 5 V buck. All wiring local to the center console — no long run.

## Motivation
- The cubby lid above the radio slot needs to be removed permanently for the RPi5/OLED installation. Removing the wood trim gives full access to the void behind the center stack — the only reliable way to confirm cable routing paths and drill neat grommet holes through the plastic dividers if needed.
- Polishing the wood on the bench (not in-situ) avoids getting polish compound on the dashboard leather and climate control unit.
- Switch cleaning is only practical with the panels removed — the switches clip into the wood/plastic from behind.
- **The BE2210's ISO speaker connector is physically on the back of the radio chassis in the DIN slot.** Tapping it while the radio is out is a 10-minute job; doing it later means a second full removal.
- Every long cable run (BE2210 ↔ rear cubby, ashtray ↔ front cubby, A-pillar ↔ front cubby) shares the same trim-removal path. Doing them all at once turns one disassembly into four deliverables.

## Switches on the Center Console
*All switches on the R129 center console are rocker-type, illuminated, and clip into rectangular cutouts in the wood trim or plastic surround. They are mechanically simple (spring + rocker contact) and can be cleaned without replacement.*

| Switch | Location | Status | Notes |
| :--- | :--- | :--- | :--- |
| ADS Sport/Comfort | Center console, below radio | Working (LED ok) | Feels slightly mushy |
| Hazard Warning (triangle) | Center console | Working | OK feel |
| Rear Window Defroster | Center console | Working | Slightly sticky |
| Seat Heater L | Center console | TBD | Not yet tested |
| Seat Heater R | Center console | TBD | Not yet tested |
| Soft-Top (roof) | Center console, upper right | Working | OK feel |
| ESP/ASR Off (if present) | Center console | TBD | Verify if equipped |

## BE2210 ISO Speaker Connector — Pin Map for the Tap

The BE2210 uses the standard ISO 10487 speaker block (brown connector, 8 pins). Only the **front pair** is wired on the R129 factory harness (the car has 2-channel stereo — two front-door speakers, no rear deck). That pair is what we tap.

| ISO Pin | Signal | Typical factory wire colour | Action |
| :--- | :--- | :--- | :--- |
| 1 | RR+ (rear right) | — (unused on R129) | Leave |
| 2 | RR− | — (unused) | Leave |
| 3 | **RF+** (right front) | *verify on car* | **Tap → DSP high-level R+** |
| 4 | **RF−** | *verify* | **Tap → DSP high-level R−** |
| 5 | **LF+** (left front) | *verify* | **Tap → DSP high-level L+** |
| 6 | **LF−** | *verify* | **Tap → DSP high-level L−** |
| 7 | LR+ (left rear) | — (unused) | Leave |
| 8 | LR− | — (unused) | Leave |

**Verify wire colours with a multimeter against the BE2210 ISO block before cutting anything.** The factory R129 harness colours are documented in the WIS, but the car has had at least one previous head-unit swap (old Sony CDX-410) — so the ISO pigtail may be aftermarket, with non-factory colour coding. A 2-second tone test with the BE2210 powered on and playing a test track per channel resolves any ambiguity.

The factory speaker wires continue to the door speakers — **we do not break that path**. The tap is parallel: the BE2210 still drives the factory door speakers (which will become the woofer channels re-used on the UP 6DSP after the speaker upgrade), and simultaneously feeds the DSP's high-level inputs. Once the UP 6DSP is operating, the factory door speakers will be disconnected at the sill-plate splice and re-fed from the DSP's amplified outputs instead. The high-level tap at the BE2210 remains as the *input* path for legacy FM/cassette.

### Why tap high-level and not line-level
The BE2210 has a rear AUX input (3.5mm) for *feeding it* audio from the RPi5 — that path already exists. It does **not** have a rear line-level preamp *output*. The only signal we can get *out* of the BE2210 for cassette/FM is at speaker level. The UP 6DSP is designed for this: it has 4 × high-level speaker inputs on its main harness, with auto-sense turn-on when it detects signal on those inputs.

### Wire & connector choice for the tap
- **Cable**: **Shielded CAT6 (F/UTP or S/FTP), ~3.5 m.** 4 twisted pairs (0.26 mm² each, 23 AWG) + overall foil shield + drain wire. Validated substitute for dedicated multi-core audio cable (decision log 2026-04-20):
  - Impedance spec (100 Ω) matters only at RF — irrelevant at audio frequencies. What matters is twisted-pair geometry + shield, which CAT6 has to better tolerances than most "audio" cables.
  - 23 AWG gauge is fine because the UP 6DSP high-level input is high-impedance (≥10 kΩ, μA-level signal current) — not a speaker-drive application.
  - Validated approach in pro audio: Rane, Radial, Whirlwind, BSS Soundweb all use CAT5/6 for long balanced analog runs.
  - Source: any shielded CAT6 patch cable (Deltaco / LogiLink / Digitus from Verkkokauppa.com, ~€8–15 for 5 m) or bulk solid-core install cable from Biltema (~€1.50/m — longest service life in fixed install). Buy extra and share the spool with the §5.4 Alps CAT6 run.
  - **Solid-core preferred for fixed install** (longer fatigue life than stranded patch cable). Stranded works but needs ferrules into Wago terminals.
- **Pair assignment (T568 colour code):**
  - **Blue / White-Blue pair** → LF+ / LF− (mnemonic: Blue = Left)
  - **Orange / White-Orange pair** → RF+ / RF− (mnemonic: Orange = Right)
  - **Green / White-Green pair** → **reserved** for future UP 6DSP line-level input (Bluetooth / phono / streamer). Terminate at both ends, cap with heat-shrink, label `SPARE-AUDIO-L/R`.
  - **Brown / White-Brown pair** → **reserved** for future DC control (remote-on, mute trigger, etc.). Label `SPARE-DC-1/2`.
  - **Critical: keep pair twist intact to within ≤13 mm of the termination point.** This is standard Ethernet install practice and preserves the magnetic rejection.
- **Tap method**: **Wago 221-413** lever nuts (3-way) at the ISO pigtail. The R129 factory speaker wires go into one port, the factory continuation into port two, the DSP tap conductor into port three. Fully reversible, no T-taps, no cutting the factory wire. Matches the approach already used during the BE2210 install (2026-03-28 diary). Solid-core CAT6 (0.26 mm²) is within the Wago 0.2–4 mm² range — direct insertion. Stranded CAT6 requires 0.25 mm² ferrules first.
- **Shield termination**: ground the overall foil shield + drain wire at the DSP end only (ring terminal → chassis bolt near the amp). Floating at the BE2210 end. Single-ended grounding prevents ground-loop hum.
- **Labelling**: heat-shrink label flags at both ends — `BE2210-LF+`, `BE2210-LF−`, `BE2210-RF+`, `BE2210-RF−`, `SPARE-AUDIO-L`, `SPARE-AUDIO-R`, `SPARE-DC-1`, `SPARE-DC-2`.

### DSP auto-on from the tap
In Audiotec Fischer DSP PC-Tool, set the UP 6DSP input source to `High-Level` and turn-on mode to `High-Level (DC offset sense)`. The amp will then power up within ~1 s of the BE2210 sending signal to its outputs and power down ~60 s after signal stops — no dedicated `REM` wire needed from the radio. This saves one wire and is more reliable than chasing the BE2210's illumination/amp-enable signal.

## Parts & Materials

### Wood Polish & Protection
* **Furniture polish / wood cleaner** — for initial cleaning (e.g., Howard Feed-N-Wax or similar beeswax-based product for lacquered wood)
* **Microfiber cloths** — lint-free, for polishing
* **Clear lacquer / polyurethane spray** — ONLY if the existing clear coat is visibly cracked, crazed, or worn through. If the existing finish is intact, do NOT re-lacquer — just clean and wax.
* **Fine-grit sandpaper (1500–2000)** — only if sanding is needed before re-lacquer (unlikely)

### Switch Cleaning
* **Contact cleaner (electrical)** — e.g., WD-40 Specialist Contact Cleaner or CRC QD Electronic Cleaner. Must be plastic-safe and residue-free.
* **Isopropyl alcohol (IPA) 99%** — for cleaning the switch housings and rocker mechanisms
* **Cotton swabs / small brushes** — for getting into the rocker pivot points
* **Silicone-free switch lubricant** — a tiny dab of dielectric grease or PTFE dry lubricant on the pivot points to restore the crisp "click" without attracting dust

### BE2210 High-Level Tap
* **Shielded CAT6 cable (F/UTP or S/FTP), ~3.5 m** — 4 twisted pairs + overall foil shield + drain wire (any reputable brand: Deltaco / LogiLink / Digitus from Verkkokauppa, ~€8–15 for 5 m; or Biltema bulk solid-core install cable at ~€1.50/m for best service life). Solid-core preferred for fixed install; stranded requires ferrules into Wago terminals. Pair assignment: Blue = LF, Orange = RF, Green + Brown = future spares. See §3 "Wire & connector choice for the tap" above for rationale and detailed wiring. One continuous run from BE2210 to the rear cubby. *(Note: the Motonet 7 × 1.5 mm² unshielded cable purchased 2026-04-20 was initially assigned here but re-parked to inventory 2026-04-20 after deciding shielded CAT6 was the cleaner solution — see diary.)*
* **Wago 221-413** (3-port lever nuts) × 4 — parallel tap at the ISO speaker block.
* **Heat-shrink** (3 mm and 6 mm, black) — for end labelling and shield termination.
* **Ring terminal M6** × 1 — for the shield drain to the DSP chassis ground point.
* **Ferrules** (0.75 mm² bootlace) × 4 — for the DSP high-level input screw terminals. Cold-end strip is not safe inside a screw terminal with stranded wire.

### DSP & Pi Cable Routing (new runs, all pulled in this task)
* **USB 2.0 A-to-B (or A-to-A, verify MEC HD-USB connector) shielded, 3 m** — RPi5 → MEC HD-USB inside UP 6DSP. Audio data path.
* **Tweeter wire, 2 × 1.5 mm² OFC, ~6 m** — two pairs (L + R) from DSP rear cubby → along driver-side sill → up A-pillar → dash tweeter locations. Entirely cabin-routed. *(Pulled during this task but terminated at the tweeter end only when the Hertz MP 28.3s are mounted in a later task.)*
* **CAT6 Ethernet, 1.5 m** — Alps RKJXT1F42001 (ashtray) → front cubby. 8 conductors for 7 GPIO + 1 GND, full shield against automotive noise. *(See radio_uiknob.md.)*
* **AUX cable, 3.5 mm TRS stereo, shielded, 0.5 m** — RPi5 3.5 mm HP output (via Waveshare or USB DAC) → BE2210 rear AUX jack. *Fallback analog path; primary digital path is USB to the DSP.*
* **Tesa cloth tape (19 mm, black)** — loom wrapping for period-correct aesthetic.
* **Rubber grommets (6–8 mm)** — any new drilled pass-throughs in plastic dividers.
* **Cable ties (small, black)** — to existing factory harness clips.
* **Split loom / convoluted tubing (6 mm ID)** — protecting the tweeter run along the sill kick panels.

### Shared hardware (already on hand or to source)
* Heat-gun, plastic trim tools, DIN extraction keys, multimeter, tone generator or phone with a channel-test track.

## Action Plan

### Phase 1: Documentation & Removal
- [ ] **1.1 — Photo-document everything** before touching it. Photograph every panel, every screw location, every clip position. The R129 trim clips are brittle and some may break — knowing exactly where they go is essential.
- [ ] **1.2 — Remove the cubby lid** (2–4 screws on the hinge mechanism). Set aside.
- [ ] **1.3 — Remove the radio** (pull BE2210 forward with DIN extraction keys, disconnect ISO + antenna). **Leave the BE2210 accessible on a soft cloth — do not re-case it, we need to tap the ISO block in Phase 4.**
- [ ] **1.4 — Remove the center console wood panels.** The R129 console wood is held by a combination of:
  - Phillips screws (hidden behind rubber grommets or at panel edges)
  - Spring clips that push into the plastic frame
  - Gentle prying with plastic trim tools — start from the bottom and work up. Do NOT use metal tools on the wood.
- [ ] **1.5 — Disconnect and label all switch connectors** as you remove each panel. Use masking tape + marker to label every connector (e.g., "ADS SW", "HAZARD", "SEAT HTR L").
- [ ] **1.6 — Remove switches from the panels.** Most R129 console switches unclip from behind (squeeze two side tabs and push through). Note orientation.
- [ ] **1.7 — Remove the ashtray insert** so the cigarette-lighter channel is accessible for the CAT6 pull.
- [ ] **1.8 — Open the rear passenger-side cubby** (the future DSP location, revised 2026-04-25). Verify line-of-sight along the passenger-side sill is clear for the cable pull. Pull the sill plate scuff strip if needed. *Also open the driver-side cubby* — the sub box lives there and the DSP→sub speaker leg routes between the two.

### Phase 2: Wood Cleaning & Polish
- [ ] **2.1 — Inspect the clear coat.** If the lacquer is intact and just dull/dirty, skip sanding — go straight to cleaning and waxing. If it's cracked, crazed, or peeling, it needs stripping and re-application (bigger job — scope separately).
- [ ] **2.2 — Clean.** Wipe each panel with a damp microfiber (water + mild soap). Remove all accumulated grime, especially around switch cutouts and clip holes.
- [ ] **2.3 — Polish / Wax.** Apply a thin coat of beeswax-based wood polish (e.g., Howard Feed-N-Wax). Buff with a clean microfiber. This restores depth and protects the existing finish.
- [ ] **2.4 — Set aside to cure.** Let the wax fully absorb/dry before handling or reinstalling.

### Phase 3: Switch Cleaning & Refresh
- [ ] **3.1 — Blow out loose debris.** Use compressed air to blast dust out of each switch housing.
- [ ] **3.2 — Clean the rocker mechanism.** Spray contact cleaner into the switch body (through the rocker gap). Work the rocker back and forth 20–30 times to flush out grime. Let dry completely.
- [ ] **3.3 — Clean the housing exterior.** Wipe the plastic housing with IPA and cotton swabs. Clean the illumination window and any printed symbols.
- [ ] **3.4 — Lubricate pivot points.** Apply a tiny amount of PTFE dry lube or dielectric grease to the rocker pivot pins. Work the switch — it should feel crisp and positive, with a clean "click."
- [ ] **3.5 — Test continuity.** Before reinstalling, use a multimeter in continuity mode to verify each switch makes and breaks cleanly.

### Phase 4: BE2210 High-Level Tap
- [ ] **4.1 — Identify the front-speaker pair on the ISO pigtail.** With the BE2210 powered up on the bench (temporary ISO power feed) and playing a channel-test track:
  - Probe with a multimeter in AC volts across each ISO speaker pin pair.
  - Confirm which two pairs carry audio — these are LF+/LF− and RF+/RF−. Mark them with masking tape.
  - Power off and disconnect the BE2210 before wiring.
- [ ] **4.2 — Strip & ferrule the tap cable.** Prepare both ends of the shielded 4-core cable:
  - **BE2210 end:** Strip and tin-free the 4 conductors. Do not ferrule — they go into Wago 221-413 levers.
  - **DSP end:** Strip, ferrule each of the 4 conductors. Terminate the shield with a ring terminal for the DSP chassis ground point.
- [ ] **4.3 — Install Wago 221-413 taps at the ISO speaker block.** For each of the 4 signals (LF+, LF−, RF+, RF−):
  - Open the factory splice OR insert a short 0.75 mm² pigtail inline with the ISO wire.
  - Insert *factory side*, *continuation to door speaker*, and *new DSP tap conductor* into the three lever ports.
  - Close the lever, tug-test.
- [ ] **4.4 — Route the tap cable from BE2210 to the rear passenger-side cubby.** Path:
  - Out the back of the DIN cavity → down behind the center console plastic divider → under the console carpet along the transmission tunnel (passenger side) → under the passenger seat → into the rear passenger-side cubby. Follow any existing factory harness if possible. *(Sym­metric to the originally-planned driver-side route, just on the other side; same cable length budget.)*
  - Use Tesa cloth tape in visible sections, split loom across metal edges.
  - Leave **~30 cm of slack** at each end for re-termination.
- [ ] **4.5 — Terminate at the DSP end (temporary).** The UP 6DSP is not yet installed in the passenger-side cubby. Leave the cable's ferrule ends coiled and labelled (`BE2210 LF+/LF−/RF+/RF−`) ready for the DSP-install phase. Shield ring terminal ditto.
- [ ] **4.6 — Test the tap end-to-end.** Re-install the BE2210 in the DIN slot temporarily, power up, play a channel-test track. With the multimeter (AC volts, low range) at the coiled passenger-side-cubby end, confirm ~1–4 V AC per channel at moderate volume. Confirms tap integrity before the console closes up.

### Phase 5: Full Cable Pull (RPi5 + DSP)
Every long cable the infotainment + audio system needs, pulled in a single pass while everything is open. Two directions:

**Front-cubby → rear-cubby (forward-to-aft runs):**
- [ ] **5.1 — USB 2.0 (RPi5 → UP 6DSP MEC HD-USB).** Route alongside the BE2210 tap cable down the transmission tunnel (passenger side). 3 m. Coil at the rear passenger-side cubby with label `RPi5 USB → MEC HD-USB`. Keep the Pi end slack inside the front cubby, ready for Pi install.

**Rear-cubby → front (aft-to-forward runs):**
- [ ] **5.2 — Tweeter pair L (DSP Ch 1 → left dash tweeter).** 2 × 1.5 mm² OFC. Route from rear passenger-side cubby → across under-rear-bulkhead carpet → up driver-side A-pillar → to left dash tweeter location, OR re-use the BE2210-tap loom path (passenger sill → under dash → across to driver A-pillar). Split loom through sill. Leave ~30 cm slack at both ends.
- [ ] **5.3 — Tweeter pair R (DSP Ch 2 → right dash tweeter).** From rear passenger-side cubby → up passenger sill → A-pillar → to right dash tweeter location. Shorter run than L, since the DSP is now on the same side. Leave ~30 cm slack at both ends.

**Inside the center console (short runs):**
- [ ] **5.4 — CAT6 (ashtray → front cubby).** 8-conductor, shielded. Down through the cigarette-lighter channel → behind center stack → into the cubby. ~1.5 m, label both ends `ALPS RKJXT1`.
- [ ] **5.5 — AUX (BE2210 rear → front cubby).** 3.5 mm TRS stereo cable, BE2210 rear AUX jack → up through divider → into the cubby. Label `BE2210 AUX`.
- [ ] **5.6 — 5 V power feed into the cubby.** From the ignition-switched source (the nRF5430 wake-switch output, per [nRF5430_Interface_Design.md](../../docs/nRF5430_Interface_Design.md)) to the cubby. 2 × 1.5 mm², fused 3 A at source. Label `PI 5V IN`.
- [ ] **5.6b — Wireless iPhone charger (drawer cubby behind the ashtray).** Embedded Qi pad mounted under the drawer floor, hidden from view. Phone sits flat in the drawer and charges with the lid closed. Wiring is local to the center console — no long run needed.
  - **Tap point:** cigarette lighter hot wire at the lighter connector backshell. Confirmed **KL15 (ignition-switched) on MAIN_12 (8A white)** — `permanent_12v: false`, field-verified 2026-04-07. Zero parasitic draw with key out.
  - **Tap method:** Wago 221-413 (3-port lever nut) into the lighter's hot lead — same approach as the BE2210 audio tap. Factory wire continues to the lighter; the new branch goes to the buck module.
  - **Step-down:** small automotive 12 V → 5 V / 3 A buck module, mounted inside the lighter cavity / behind-ashtray void where there's air and the heat stays away from the drawer plastic. Inline 3 A blade fuse on the 5 V output.
  - **Charger module:** **embedded Qi 7.5–15 W pad with USB-C input** (e.g., Ugreen / Choetech CH002 / Nillkin MagicCube class — see parts list 6C.8). Mounts UNDER the drawer floor with 3M VHB or a 3D-printed bracket. Field penetrates the floor plastic without modification.
  - **Cable:** 2 × 0.75 mm² red/black, ~30 cm from the lighter tap to the buck, then a short USB-C tail (often supplied with the module) from the buck output to the charger module.
  - **Heat note:** 7.5 W Qi dissipates ~2 W. Fine in normal use; if the drawer ever runs hot in direct sun, drill 2–3 × 4 mm vent holes in the underside of the drawer floor (invisible from above).
  - **Label:** `QI 5V IN` at the buck output, `LIGHTER TAP` at the Wago.
- [ ] **5.7 — Microphone cable** ⚠ **decision required before this step** — pick hardware/location per the "Microphone integration" backlog entry in [tasks.md](../../docs/tasks.md). Cable spec depends on the option chosen (USB active / shielded analog / I2S 4-wire). Whichever option wins, the cable run will be: mic at headliner or A-pillar → down A-pillar → along under-dash → into center stack void → into cubby. **Do not close the console without pulling this cable** — re-pulling trim in a month is not acceptable.

**Cubby-to-cubby (rear bulkhead, NEW 2026-04-25):**
- [ ] **5.7b — DSP → sub speaker leg (passenger-side cubby → driver-side cubby).** 2 × 2 m of 2.5 mm² OFC speaker cable (one pair per voice coil; total 4 conductors / 2 pairs). Two viable paths — pick whichever access is cleaner with the trim already off:
  - **Path A (preferred):** under the rear-bulkhead carpet, hugging the cross-car seam between rear deck and parcel shelf. Shortest physical run (~1.4–1.6 m), keeps the cable away from the audio-input loom.
  - **Path B (fallback):** through the center console while it's open — down the passenger sill, under the transmission tunnel carpet, up the driver sill, into the driver-side cubby. Longer (~2.0 m) but uses an already-pulled trim path; acceptable if Path A turns out to need additional disassembly.
  - Label both ends `SUB COIL A +/−` and `SUB COIL B +/−`. Keep separate from the BE2210 tap loom and the USB run — speaker-level current can crosstalk into high-impedance signal lines if bundled together.
  - Resistance check: at 2.5 mm² over 2 m round-trip the per-leg loop resistance is ~14 mΩ, ~0.7 % of the 2 Ω voice coil load. Loss < 0.1 dB, inaudible.

**Loom finishing:**
- [ ] **5.8 — Wrap the loom.** Bundle all cables sharing a segment with Tesa cloth tape to match the factory harness aesthetic. Secure to existing harness clips with black cable ties. Keep power, audio signal, and USB in *separate* bundles where possible to minimize noise coupling — ideally:
  - Bundle A: BE2210 tap + tweeter pairs + AUX (all low-level audio)
  - Bundle B: USB 2.0 (alone, or with AUX if space is tight)
  - Bundle C: 5 V power + CAT6 (low-voltage control, already shielded)

### Phase 6: Reassembly
- [ ] **6.1 — Reinstall switches** into the wood panels (clip from behind, correct orientation).
- [ ] **6.2 — Reconnect all switch harnesses** (use the labels from Phase 1.5).
- [ ] **6.3 — Reinstall wood panels.** Replace any broken clips with new ones (source: Biltema universal trim clips or MB-specific). Screws finger-tight — do not overtorque into plastic.
- [ ] **6.4 — Reinstall BE2210** with AUX cable connected to rear jack and the ISO block (with Wago taps) plugged in.
- [ ] **6.5 — Functional test.** Verify every switch works (ADS, hazard, defroster, seat heaters, soft-top). Verify radio powers on, AUX input is routed, and the factory door speakers still play from the BE2210 (the taps are parallel — they must not have broken the factory path).
- [ ] **6.6 — Sign off cable pull.** Check the coiled labels at both the rear cubby and the front cubby. Every cable from the Phase 5 checklist must be physically present with ~30 cm of slack. If anything is missing, re-open before closing the sill plates.

## Dependencies & Downstream Tasks
- **DSP install task** (rear passenger-side cubby build, per [audio_upgrade_blueprint.md](../audio_upgrade_blueprint.md) Phase 1) consumes the Phase 4 and Phase 5 cables at the rear end: BE2210 tap → UP 6DSP high-level inputs, USB → MEC HD-USB, tweeter pairs → DSP channels 1/2, sub speaker leg (§5.7b) → DSP channels 5/6.
- **RPi5 cubby install** consumes the Phase 5 front-cubby ends: USB, AUX, CAT6, 5 V, microphone.
- **Speaker upgrade task** (door woofers + dash tweeters) consumes the Phase 5.2/5.3 tweeter-end runs.
- This task's completion unblocks all three above — nothing should require another full console removal after this.

## Work Log
| Date | Status | Notes |
| :--- | :--- | :--- |
| 2026-03-28 | Planned | Project created. Combines wood refresh, switch cleaning, and RPi5 cable routing into a single console disassembly. |
| 2026-04-18 | Scope expanded | Added BE2210 → UP 6DSP high-level tap (4-wire shielded run, Wago 221-413 parallel taps at ISO block) and full DSP-direction cable pull (USB 2.0, tweeter pairs) to the same task. Single console-out event now delivers wood + switches + all long cable runs, front-to-rear and rear-to-front. |
| 2026-04-20 | Cable spec finalised | BE2210 tap cable decision: shielded CAT6 (F/UTP or S/FTP) substituted for the originally-planned 4-core audio cable. CAT6 is the right technical fit (twisted pairs + overall shield; 100 Ω impedance is irrelevant at audio frequencies; 23 AWG is fine for high-Z DSP input) and is trivially sourceable in Finland (Verkkokauppa / Motonet / Clas Ohlson / Biltema) versus the multi-week EU order needed for Sommer / Cordial multi-core audio cable. Pair assignment: Blue = LF, Orange = RF, Green + Brown = future spares (line-level input + DC control). Buy one bulk spool and share with §5.4 Alps CAT6 run. The Motonet 7 × 1.5 mm² cable (bought same day) re-parked to inventory — probable future use: Hertz door-woofer multi-conductor harness, speaker-level so unshielded is fine. |
| 2026-04-25 | Scope expanded | Added wireless iPhone charger as the fifth objective — embedded Qi pad mounted under the drawer floor of the cubby behind the ashtray. Power tap from the cigarette-lighter hot wire (MAIN_12 8A KL15, ignition-switched, `permanent_12v: false` field-verified 2026-04-07 — zero parasitic draw with key out) via a Wago 221-413 + 12 V → 5 V buck. Wiring is local to the center console, no long run. New step §5.6b in Phase 5. Parts captured in `docs/parts_to_order.md` §6C.8 — specific Qi module decision pending, recommendation is a Ugreen / Choetech / Nillkin USB-C-input embedded pad in the €20–30 range (rejected: Aircharge Slimline as overkill, MagSafe puck as visually intrusive in the drawer). |
| 2026-04-25 (eve) | DSP relocated to passenger side | Sub box geometry locked the same day — its 16.9 L external footprint fully consumes the driver-side rear cubby, leaving no room for the DSP's 1.7 L footprint plus its mandated 40 mm heatsink ventilation clearance. DSP moved to the (otherwise empty) passenger-side rear cubby. BE2210 tap, USB, tweeter pair, and DSP power runs follow the symmetric passenger-side path; only new cable is the §5.7b cubby-to-cubby sub speaker leg (~1.6 m of 2.5 mm² OFC, < 0.1 dB loss). All section text updated. See `docs/diary/2026-04.md` April 25 evening entry and `work/audio_upgrade_blueprint.md` §1. |
