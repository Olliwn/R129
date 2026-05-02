# R129 Audio Upgrade Blueprint — Fully Active 2.1 System

## Philosophy

Modern, high-fidelity audio with full DSP control, while maintaining 100% factory aesthetic. Every speaker gets its own dedicated amplifier channel, time-alignment, and EQ — no passive crossovers in the signal path. The Becker BE2210 stays in the DIN slot for period-correct cassette/FM. All digital streaming audio flows through the RPi5 to the DSP via lossless USB.

2-way active front stage (woofer + tweeter per side) was chosen over 3-way after thorough analysis. In the R129's noisy convertible environment, a dedicated midrange driver provides diminishing returns while tripling door wiring complexity and risking the fragile PSE vacuum lines in the door boots. The Hertz MP 28.3 tweeter's low resonance frequency (900 Hz) allows a low crossover point (~2.5 kHz) that covers the critical vocal presence range normally handled by a midrange. Factory door wiring is reused for the woofers — no new wires through the door boots.

---

## System Architecture

```
                                 ┌─ Ch 1: L Tweeter (65W @ 4Ω)  ── Hertz MP 28.3
                                 ├─ Ch 2: R Tweeter (65W @ 4Ω)  ── Hertz MP 28.3
iPhone ──BT/CarPlay──→ RPi5     ├─ Ch 3: L Woofer  (65W @ 4Ω)  ── Hertz MP 165P.3
                         │      ├─ Ch 4: R Woofer  (65W @ 4Ω)  ── Hertz MP 165P.3
                    USB (UAC)   ├─ Ch 5: Sub coil 1 (160W @ 2Ω) ── Helix IK S10-DVC2
                         │      └─ Ch 6: Sub coil 2 (160W @ 2Ω) ── Helix IK S10-DVC2
                         ▼
                   Match UP 6DSP
                   + MEC HD-USB
```

The RPi5 acts as the audio source (Bluetooth A2DP sink or CarPlay via Carlinkit dongle). PipeWire routes audio to the Match UP 6DSP via the MEC HD-USB module — fully digital, lossless USB Audio Class. The DSP handles all crossovers, time alignment, level matching, and EQ. No analog conversion until the amplifier output stage.

All 6 channels utilized — zero waste.

---

## Finalized Bill of Materials

### 1. DSP Amplifier — Match UP 6DSP

| Spec | Value |
| :--- | :--- |
| Channels | 6 amplified (4 × 65W @ 4Ω + 2 × 160W @ 2Ω) |
| DSP | 7-channel, 64-bit fixed-point |
| Inputs | 4 high-level speaker, 1 optical SPDIF, MEC slot |
| Dimensions | 46 × 130 × 153 mm |
| Price | **€649** (Kärkkäinen) |
| Status | **ORDERED 2026-04-04** |

Chosen over the UP 8DSP (€749) for €100 savings — the 2-way front stage needs only 4 speaker channels + 2 sub channels, matching the UP 6DSP exactly. The UP 8DSP's extra 2 × 65W channels for a dedicated midrange would sit unused.

The 7-channel DSP includes a virtual center channel (RealCenter) and bass processing (Augmented Bass Processing) that compensate for the asymmetric driver position in the R129. Tuning via laptop using Audiotec Fischer's DSP PC-Tool software.

**Mounting location:** **Rear passenger-side storage cubby** (revised 2026-04-25 evening — the driver-side cubby is fully occupied by the sub box at 97 % volume utilisation; only ~0.5 L of triangular dead air remains, insufficient for the DSP's 1.7 L footprint with the mandatory 40 mm heatsink ventilation clearance). The passenger-side cubby has the same ~17 L envelope as the driver-side and is otherwise empty. The center console cavity behind the climate control is a heat trap and must be avoided.

**Co-located with the RPi5 + nRF93M1 cellular modem + Carlinkit dongle** (revised 2026-05-02 evening). The Pi stack moved from the front cubby to share this rear cubby with the DSP — primary drivers were service access (rear cubby reachable from behind the passenger seat without disturbing the dash), collapse of the Pi ↔ DSP USB Audio Class long pull into a 10 cm in-cubby cable, and stack-growth headroom. Combined dissipation ~50–60 W steady fits the cubby volumetrically; thermal verification is a commissioning gate (per `work/center_console_refresh/README.md` §6.5b). Pi power comes from the same DSP +12 V rail (Biltema 84-574 8 mm² CCA, 40 A AGU) via a small in-cubby 12 V → 5 V buck — no separate Pi power feed needed. See `work/center_console_refresh/README.md` Work Log entry "Pi → rear passenger cubby" for full rationale and Cable Manifest impact (drops C2/C3/C11 long pulls, adds C16 HDMI / C17 display USB / C18 cabin-node USB-CDC as new front ↔ rear pulls at ~2 m each).

Cable-run impact of moving DSP to passenger-side: the only run that lengthens meaningfully is the DSP → sub speaker leg (0.4 m → ~1.6 m via under-carpet routing along the rear bulkhead, OR through the center console if it's already apart for the BE2210 tap). Resistance contribution at 2.5 mm² over the extra 1.2 m is ~9 mΩ per leg, ~0.9 % of the 2 Ω DVC2 load — power loss < 0.1 dB, inaudible. All other runs (battery → DSP power, BE2210 tap → DSP signal, DSP → front doors) are roughly the same length or slightly shorter on the passenger side.

### 2. USB Audio Interface — MEC HD-USB (M142045)

| Spec | Value |
| :--- | :--- |
| Resolution | Up to 192 kHz / 32-bit |
| Interface | USB Audio Class (UAC) — driverless on Linux |
| Compatibility | UP 6DSP, UP 8DSP, UP 8BMW |
| Price | **€149** (Kärkkäinen) |
| Status | **ORDERED 2026-04-04** |

Plugs into the MEC expansion slot inside the UP 6DSP. The RPi5 sees it as a standard USB audio sink via PipeWire — no proprietary drivers. Full Speed mode (up to 96 kHz) works without any driver on any OS; more than sufficient for car audio.

### 3. Front Stage — Hertz MPK 1650.3 (Mille Pro 2-Way)

| Driver | Model | Size | Sensitivity | Impedance | Depth | Opening |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Woofer | MP 165P.3 | 6.5" (165mm) | 94 dB | 3Ω | **63mm** | 141mm |
| Tweeter | MP 28.3 | 28mm Tetolon dome | 91 dB | 4Ω | **17mm** | 35mm |

| Spec | Value |
| :--- | :--- |
| System sensitivity | 93 dB SPL |
| Tweeter resonance (Fs) | 900 Hz |
| Frequency range | 45 Hz – 28 kHz |
| Crossover (passive, unused) | MPCX 165.3 (bi-metallic caps, air-wound inductors, 3-pos tweeter level) |
| V-cone profile | Yes (improved off-axis dispersion) |
| Made in | Italy |
| Price | **€331.26** (masori.de, free shipping to FI, 3-year warranty) |
| Status | **ORDERED 2026-04-04** |

**Why MPK 1650.3 over alternatives:**
- **MP 28.3 premium tweeter** — Tetolon dome with 900 Hz Fs allows crossing at ~2.5 kHz in the active setup, covering the critical vocal presence range that a midrange driver would handle in a 3-way system. This is the key driver that makes the 2-way approach viable.
- **63mm woofer depth** — fits behind R129 factory door grilles with the MR129 adapter brackets, unlike the Focal PS 165 F3E at 72.7mm.
- **93 dB sensitivity** — excellent match for the UP 6DSP's 65W channels. Compared to the MPK 130.3 (5"/88 dB), the 5 dB advantage means ~3× less amplifier power needed for equivalent volume.
- **3Ω impedance** — draws slightly more current from the 4Ω-rated amp channels, effectively extracting more power.

**Alternatives evaluated:**
- *Focal PS 165 F3E (3-way, €499):* Warm tone but 72.7mm woofer depth won't clear R129 grilles. 3-way adds door wiring complexity.
- *Hertz MPK 163.3 (3-way, €377):* Excellent 3-way set but requires 6 wires per door through the R129 rubber boots — high risk to PSE vacuum lines. The midrange benefit is diminished in a convertible.
- *Hertz MPK 130.3 (5" 2-way, €235):* Smaller woofer reduces beaming but ships with inferior MP 25.3 tweeter (higher Fs, crosses higher) and has 5 dB lower sensitivity. The Genelec-inspired approach doesn't translate to car audio without a waveguide.
- *Hertz MPK 165.3 (2-way, €298):* Good value but uses the standard MP 25.3 tweeter. The €33 premium for the 1650.3 buys the significantly better MP 28.3.

The kit includes passive crossovers (MPCX 165.3) which will not be used — every driver connects directly to its own UP 6DSP channel. Crossovers kept as spares.

**Mounting:**
- **Woofer (6.5"):** Factory door speaker location with MR129.com 3D adapter brackets. 2 brackets per door (4 total). The 63mm woofer depth + bracket should clear the factory grille.
- **Tweeter (28mm):** Factory dash tweeter location (surface or flush mount). 17mm depth — fits anywhere. Wire routed through cabin (under dash trim, along A-pillar) — no door boot penetration needed.
- **STL files:** ~$39 from mr129.com. Print test-fit prototypes in PLA first, then PETG/ABS final. Verify Hertz MP 165P.3 mounting hole (141mm) and depth (63mm) against STL dimensions before final print.

### 4. Subwoofer — Helix IK S10-DVC2

| Spec | Value |
| :--- | :--- |
| Size | 10" (250mm) |
| Voice coil | Dual 2Ω (DVC2) |
| Power handling | 300W RMS / 600W peak |
| Mounting depth | 84.5mm |
| Sealed box volume | 14L net |
| Sealed box F3 (-3dB) | 46 Hz |
| Qts | 0.51 |
| Fs | 37 Hz |
| Xmax | ±6.0mm |
| Includes | Grille, gasket, terminal plate |
| Manufacturer | Audiotec Fischer (same as Match) |
| Price | **€199** (Kärkkäinen) |
| Status | **ORDERED 2026-04-04** |

The DVC2 configuration is ideal for the UP 6DSP: each voice coil connects to its own 160W sub channel (Ch 5 and Ch 6) at 2Ω. The DSP processes both coils independently for optimal thermal and distortion management. Total combined power to the sub: 320W RMS.

**Enclosure:** Sealed 12.5L (effective) single-axis-tapered MDF box in the rear driver-side storage cubby — 16.9 L external in a 7-panel build with one chamfered corner matching the cubby's wheel-well intrusion. Geometry locked 2026-04-25 from cardboard mock-up; full build doc at `work/subwoofer_enclosure/README.md`. Realised F3 ~47–48 Hz vs datasheet 46 Hz at 14 L — within audibility threshold of reference, no DSP correction required. The Helix datasheet recommends a DSP highpass filter at 45 Hz (Q = 1.3) and a parametric cut at 100 Hz (Q = 1.0, -3 dB) for the sealed alignment.

**Alternatives evaluated:**
- *Hertz Mille Pro MPS 250:* Impressive specs (500W RMS, 16.8mm Xmax) but wants more amplifier power than the UP 6DSP provides. Single voice coil. ~€217+.
- *Eton MW8:* 140mm mounting depth — too deep for the shallow R129 cubby.

### 5. Wiring & Installation

| Item | Qty | Notes |
| :--- | :--- | :--- |
| OFC speaker wire 2×1.5mm² | ~10m | Tweeter runs (cabin routing only) + sub run. |
| OFC speaker wire 2×2.5mm² | ~5m | Sub feed (higher current). |
| Spade / ring terminals | assorted | For DSP and speaker connections. |
| MDF (16mm) | ~0.5m² | Sub enclosure. |
| Polyfill damping | 200g | Sealed sub box fill. |
| MR129.com bracket kit (STL) | 1 set | 3D adapter brackets for R129 doors. ~$39 for STL files. 4 pieces (2 per door, woofer only). |

**No professional door wiring needed.** The 2-way setup eliminates the most difficult and expensive part of the installation:
- **Woofers:** Connected via existing factory door speaker wiring (0.75–1.0mm² adequate for 65W @ 3Ω over short runs). No new wires through door boots.
- **Tweeters:** Mounted in the dash/A-pillar area. New wire routed entirely within the cabin — under dash trim, along A-pillar. Never enters the door boot.
- **Subwoofer:** In the rear driver-side cubby; the DSP lives in the rear passenger-side cubby (revised 2026-04-25 — sub box fully fills the driver-side cubby). The DSP→sub leg is ~1.6 m of 2.5 mm² speaker cable routed under the rear-bulkhead carpet OR through the center console (whichever access is convenient given the BE2210 tap work). Resistance over the longer run is acoustically negligible (< 0.1 dB loss into the 2 Ω DVC2 load).

This was the decisive factor in choosing 2-way over 3-way. Running 3 pairs of new wire per door through the R129's rubber boots (which contain 35-year-old PSE vacuum lines) would require professional labor (€150–300) and risk damaging the pneumatic central locking system.

---

## Budget Summary

| Component | Source | Cost (€) | Status |
| :--- | :--- | :--- | :--- |
| Match UP 6DSP | Kärkkäinen | 649 | ORDERED 2026-04-04 |
| MEC HD-USB (M142045) | Kärkkäinen | 149 | ORDERED 2026-04-04 |
| Hertz MPK 1650.3 | masori.de | 331 | ORDERED 2026-04-04 |
| Helix IK S10-DVC2 | Kärkkäinen | 199 | ORDERED 2026-04-04 |
| MR129.com brackets (STL) | mr129.com | ~36 | Pending |
| Wiring & hardware | inventory + local | ~40 | Pending |
| MDF + polyfill | local | ~30 | Pending |
| **Total** | | **~€1,434** | |

Savings vs. original 3-way plan (UP 8DSP + MPK 163.3 + professional door wiring): **~€336**.

---

## Installation Plan

### Phase 1 — Rear Cubbies (Self-Install)
1. Build the sealed ~12.5 L (effective) MDF enclosure for the Helix IK S10-DVC2 in the **driver-side cubby**. Per `work/subwoofer_enclosure/README.md`.
2. Mount the Match UP 6DSP in the **passenger-side cubby** (driver-side cubby is fully occupied by the sub box).
3. Install the MEC HD-USB module in the DSP's MEC slot.
4. Run USB cable from RPi5 (behind dash) to the MEC HD-USB in the passenger-side cubby.
5. Run high-level input wires from BE2210 speaker outputs to the UP 6DSP (backup analog path / signal detection for auto-on). Per `work/center_console_refresh/README.md` §4.
6. Connect sub to Ch 5 + Ch 6 (one coil per channel) — speaker cable routes from passenger-side cubby to driver-side cubby via under-bulkhead-carpet OR through the center console.
7. Test sub + DSP with laptop tuning before touching the doors.

### Phase 2 — Door Wiring
**No professional door wiring needed.** Factory speaker wires (already in doors) are reused for the woofers. Tweeter wires run entirely within the cabin.

1. Identify factory speaker wire pairs at the door connector and at the DSP end (sill plate area).
2. Extend/splice factory wires to reach the DSP in the passenger-side cubby if needed.
3. Run new tweeter wire pairs from DSP → under sill plates → up A-pillar → to dash tweeter locations. Entirely within the cabin — never enters door boots.

### Phase 3 — Speaker Mounting (Self-Install)
1. Remove door panels (trim removal tools on hand).
2. Remove factory door speakers.
3. Install MR129.com 3D-printed woofer adapter brackets (2 per door).
4. Mount Hertz MP 165P.3 woofers. Connect to factory speaker wires.
5. Reassemble door panels.
6. Mount Hertz MP 28.3 tweeters in dash/A-pillar locations. Connect to new tweeter wires.

### Phase 4 — DSP Tuning
1. Connect laptop to UP 6DSP via USB (DSP PC-Tool software).
2. Set crossover points (starting points, refine by ear):
   - Tweeter HP: ~2.5 kHz (Linkwitz-Riley 24 dB/oct) — MP 28.3's low Fs allows this
   - Woofer BP: ~80 Hz HP / ~2.5 kHz LP
   - Sub LP: ~80 Hz with HP ~45 Hz (subsonic protection)
3. Time-align all drivers (measure distances from listening position).
4. Level-match tweeter and woofer (compensate for sensitivity difference: 94 dB woofer vs 91 dB tweeter).
5. Apply room correction EQ if needed (pink noise + measurement mic).
6. Save tuning preset to DSP internal memory.

---

## Audio Signal Paths

### Path 1 — Bluetooth Streaming (Primary)
```
iPhone → BT A2DP (AAC) → RPi5 PipeWire → USB (UAC) → MEC HD-USB → UP 6DSP → Speakers
```

### Path 2 — CarPlay Audio (Wireless)
```
iPhone → WiFi Direct → Carlinkit CPC200-CCPA → USB → RPi5 PipeWire → USB (UAC) → MEC HD-USB → UP 6DSP → Speakers
```

### Path 3 — Legacy (Cassette/Radio)
```
Becker BE2210 → factory speaker wiring → factory speakers (or high-level input to UP 6DSP)
```
The BE2210's high-level outputs can also feed the UP 6DSP's speaker-level inputs for amplified cassette/FM playback through the new speakers. The DSP auto-detects signal presence and switches on.

### Path 4 — Backup Analog
```
RPi5 → HDMI audio → Waveshare 3.5mm HP jack → BE2210 AUX input
```
Fallback if the MEC HD-USB is unavailable.

---

## Reversibility

The entire system is non-destructive and fully reversible:
- No factory wiring is cut or removed — only unplugged and extended/spliced.
- The BE2210 stays functional in the DIN slot.
- Tweeter wiring runs parallel to existing harness (cabin only).
- The rear cubby enclosure and DSP (driver- and passenger-side cubbies, respectively) can be removed, restoring the original storage space.
- Door speakers can be swapped back to factory units by reconnecting the original harness.
