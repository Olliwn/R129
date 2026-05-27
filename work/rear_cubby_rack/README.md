# Rear Passenger Cubby — Electronics Installation Plate

**Status (2026-05-17):** Plate fabricated, layout iterated on the bench; in-car install pending wiring completion. Architectural simplification (May 17) replaces the original May 7 aluminum-T-slot extrusion + modular cassettes design with a single 4 mm plastic plate sandwich (CTK Standard Pro damping underneath), components mounted on the plate via screw-tower standoffs + zip-tie cable management, friction-fit retention via plate-edge cuts engaging cubby wall features. Power topology now includes a permanent manual hard-kill switch + ATO fuse box in series with the IRF4905 high-side MOSFET.

This doc is the source-of-truth for the rear-cubby integration: how all rear-cubby electronics — DSP, RPi5, nRF54L15 cabin node, nRF93M1 cellular modem, 85 W cigarette-lighter USB charger — are mechanically packaged, powered, cooled, and wired together. It also covers the two software integration tasks that close out the rack stage: DSP6-as-Pi5-soundcard (enabling CarPlay audio through the new system) and nRF54L15-driven Pi-wake control.

## Purpose

The rear passenger cubby is the consolidation point for the R129 distributed system's "compute + audio amplifier + always-on gate" subsystem. Three subsystems share this volume by design (per `work/audio_upgrade_blueprint.md` 2026-04-25 decision and `work/cabin_signal_node/README.md` 2026-05-05 re-architecture):

1. **Audio amplifier** (Match UP 6DSP + MEC HD-USB) — already mounted, powered, grounded, and wired (May 7 install).
2. **Compute** (RPi5 + NVMe + display pigtails + Carlinkit dongle) — currently bench-tested, needs in-car install.
3. **Cabin always-on** (nRF54L15 carrier with BLE proximity, USB-CDC link to Pi, 12 V high-side MOSFET gating the 85 W charger domain) — currently bench-tested, needs hardware build + in-car install.

**Without** a shared rack, the three subsystems would each get their own ad-hoc mounting with overlapping cable routes, vibration risks, and no clear thermal management story. **With** a shared rack, all three live as removable cassettes on a common aluminum-profile skeleton; the rack handles vibration, cabling, and thermal as one design problem.

This doc is the **packaging and integration spec**. It does NOT duplicate the audio system architecture (see `work/audio_upgrade_blueprint.md`), the cabin signal node electronics (see `work/cabin_signal_node/README.md`), or the Pi setup (see `docs/RPi5_Bring-up_Plan.md`). It lives at the seam where those three meet.

## Cubby Occupants — Final Inventory

| Component | Footprint | Heat (steady) | Service-access need | Status |
| :--- | ---: | ---: | :--- | :--- |
| Match UP 6DSP + MEC HD-USB | ~1.7 L (with 40 mm heatsink ventilation clearance) | ~6 W (Class GD ~85 % eff) | USB-C control port for re-tuning | Mounted in cubby May 7; relocates to plate during plate install ✅ |
| RPi5 + NVMe HAT | ~1.0 L | ~10–15 W typical, ~25 W peak | NVMe slot, 4× USB-A, 2× HDMI, 40-pin GPIO | Pending plate install |
| nRF54L15 DK | ~0.3 L | <1 W | RESET button, programming pins, **UART link to Pi via GPIO header** (3 wires; replaces planned USB-CDC link), BLE chip-antenna clearance | Pending plate install (firmware bring-up done bench-side; in-car cabin-node functions per cabin_signal_node README) |
| nRF93M1 DK | ~0.3 L | ~1–2 W avg, ~5 W TX peak | SIM tray, SMA antenna pigtail to LTE antenna (trunk-mounted via May 3 fish-string), USB-A to Pi for RNDIS + AT serial | Pending plate install (RNDIS bring-up done per `docs/diary/2026-04.md`) |
| Carlinkit CPC200-CCPA dongle | ~0.05 L | <1 W | USB-A to Pi; wireless CarPlay source from phone | Mounts on top of Pi cassette zone (USB-plugged, mechanical anchor needed — see Component Mounting §) |
| 85 W cigarette-lighter USB charger | ~0.3 L | ~3 W typical (20 W out @ ~85 % eff), peak ~12 W | USB-C + USB-A ports out (to Pi, Qi pad, spare) | Acquired May 3 |
| Female cigarette-lighter panel-mount socket | ~0.1 L | — | Charger plugs into this socket | New — see BOM |
| 50 A rocker hard-kill switch + ATO fuse box | ~0.1 L | — | Manual operator access (cubby-lid-open ergonomics); fuse swap | New, May 17 — see Power Topology § |
| Wago splice-block project box | ~0.4 L | — | Lift-off lid, every Wago lever accessible | New, May 17 — see Wago Splice Block § |
| Cabling + service loops + connectors | ~1–2 L | — | Strain relief at every entry/exit, service-loop slack | Designed in Cable Management § below |
| **Total used** | **~5–6 L of ~17 L** | **~25 W steady, ~50 W peak** | — | — |

**~11 L free** — generous physical headroom. The challenge is mechanical, thermal, EMI, and acoustic isolation (the OEM lid's noise-barrier function — see Cooling Architecture §), not volume.

## Design Approach

**4 mm plastic plate sandwich + plate-shape friction-fit + screw-tower standoffs + zip-tie cable management + foam underside.**

Re-architected 2026-05-17. The original (May 7) design — aluminum 20 × 20 mm T-slot extrusion + modular component cassettes + expansion-clamp friction mount — was good engineering for the spec written at the time, but in practice the build proceeded with a substantially simpler approach that achieves the same functional goals with material on hand:

| Element | Implementation | Function |
| :--- | :--- | :--- |
| **Plate** | Single piece of 4 mm plastic sheet, irregular polygon shape cut to match the cubby's footprint (the cubby has wall protrusions on the body-shell side from the wheel-well intrusion typical of R129 rear cubbies; the cabin side is straighter). Cut on a tablesaw / jigsaw from inventory plastic offcut. | Structural base. All components mount to it; it carries inertial loads through the friction-fit. |
| **Underside damping + decoupling** | One layer of CTK Standard Pro (butyl + foil, ~2 mm) bonded to the entire underside via the SuperFix+ self-adhesive backing. Plus multi-layer CTK shim stack at the back of the plate where the cubby step sits lower than the front (levels the plate flush with the cubby floor across its full footprint). | Mass-loading + vibration damping (replaces the structural-stiffness role of the extrusion); levels the plate on the cubby's stepped floor. |
| **Foam underside (over the CTK)** | One layer of CTK doorkit foam (Profildamp 7.5 mm closed-cell PE with fabric face), bonded with spray adhesive, single piece covering the underside footprint. | Vibration decoupling between the (now-rigid) plate and the cubby floor (point-contact transmission path eliminated); dielectric barrier between board solder side and any exposed cubby metal. |
| **Cubby retention** | Friction fit via cuts/notches in the plate edges that engage cubby wall features. Optional tape on edges for tighter wedge. **Zero holes drilled in the car.** | Mechanical retention; reversibility (entire plate lifts out, cubby restorable to factory in ~5 min). |
| **Component mounting** | "Screw-tower" plastic standoffs (typical 6–10 mm M3 standoffs) bolted directly through the plate; boards screwed onto the towers. No per-cassette base plate. | Component capture + serviceability (unscrew from tower → board lifts off, same granularity as cassette removal in the original design, less hardware). |
| **Cable management** | Zip ties to the plate edges + small loops anchored to standoff holes; bundles routed by signal class (see Cable Management §). | Strain relief, EMI separation, neat appearance. |
| **Top finish** | Bare plastic on the board-mount areas; carpet edge wrap (~10–15 mm tucked over from underside) for visual continuity with the sub-box wrap. **No fabric across the top interior** — boards are visible. | Cosmetics + service access (visible solder side of nothing; plastic is easy to wipe; no fraying around standoffs). |
| **Cooling** | 60 mm 12 V brushless case fan, foam-baffled side-trim intake from cabin air, exhaust either to opposite-side cabin or to trunk via existing rear-bulkhead pass-through. **OEM lid stays uncut** (it is a measured acoustic insulation barrier — see Cooling Architecture §). | Heat removal at ~20–25 W steady duty; preserves the lid's NVH function. |

**Why this works as well as the original aluminum design (or better):**

- **Same "zero holes drilled" principle**, achieved by plate geometry instead of expansion hardware.
- **Same service granularity** ("unscrew board from tower" = "remove cassette from frame", with less hardware).
- **Same vibration tolerance** — the CTK-damped plate is a constrained-layer-damped system (foil + butyl + plastic), the same physics that automotive sound deadeners use throughout the chassis. The May 7 extrusion's stiffness was one solution; the plate's mass loading is another to the same problem.
- **Significantly less material cost** (~€10–15 vs ~€85 in the original BOM) and significantly less fabrication time (~1 h vs ~5 h for the original frame + cassettes).
- **Uses inventory** — plastic offcut, doorkit CTK + foam, screw-tower standoffs, zip ties — all on hand or minor incremental purchase.

**Why not the alternatives** (rejected during the May 7 discussion, still rejected):

- 3D-printed PETG modular trays: PETG glass-transition is ~70 °C; in a car cubby in Finnish summer with 25 W of heat, the safety margin is too thin. Plastic 4 mm sheet (typically PP, HDPE, or PVC) has higher service temperature.
- Plywood / MDF: flammable in a confined space with heat sources, and adds ~1 kg of mass that doesn't help anything. The current 4 mm plastic is much lighter and non-hygroscopic.
- Original aluminum extrusion: superseded by this simplification (still preserved in the May 7 entry of `docs/diary/2026-05.md` for reference if the rack is ever re-architected for higher load / vibration / spec).

## Cubby Geometry

Two states tracked: working assumption (used for the May 17 plate fabrication) and the still-pending precise tape-measurement.

| # | Dimension | Working assumption | Why it matters |
| :--- | :--- | :--- | :--- |
| D1 | Cubby interior W × D × H above the trim panel | ~350 mm W × 300 mm D × 160 mm H (≈17 L), tapered following the wheel-well on the outboard side | Sets the plate footprint envelope; plate has been cut to a polygon shape matching the working assumption with tolerance for friction-fit notches. |
| D2 | Bottom welded-stud → cubby-edge distance (passenger-side ground stud) | TO MEASURE | Cable-entry side of the plate; where the DSP power-and-ground bundle exits to reach the factory ground stud. |
| D3 | Trim panel underside profile (does the OEM lid clear the tallest component on the plate?) | TO MEASURE | Determines whether the lid closes over the plate as-is or needs an internal relief notch. The DSP heatsink (~40 mm tall) is the height-limiting component. |
| **D4 (NEW)** | Bulkhead-side fish-string pass-through location (rear right corner? rear left? centre?) | TO MEASURE (next 30-second cubby-open window) | Determines (a) which corner the nRF93M1 occupies on the back of the plate so its SMA pigtail to the trunk-mounted LTE antenna takes the shortest path with no sharp connector bend, (b) whether the cooling exhaust uses the trunk-side route or the opposite-cabin-side route. |

The plate footprint was committed before the precise measurements via the working assumption above; if D1–D4 reveal mismatch, the friction-fit notches can be re-cut on the existing plate (additive — adds notches, doesn't fix bad geometry that's already cut).

## Plate Design

### Plate substrate

| Spec | Choice | Rationale |
| :--- | :--- | :--- |
| Material | **4 mm plastic sheet** (PP / HDPE / PVC, depending on inventory offcut) | On-hand, cheap, non-conductive, non-flammable enough for the heat budget. Service temperature for all three families is well above the ~50 °C cubby commissioning gate target. |
| Thickness | 4 mm | Stiff enough to span the cubby footprint without sag under ~2–3 kg of components. Thicker is unnecessary; thinner sags. |
| Footprint | Irregular polygon matching cubby outline (right side has notches for wheel-well intrusion; left side straighter) | Maximises usable area while clearing cubby wall protrusions. |

### Friction-fit retention

The plate is held in the cubby by **plate-edge geometry alone**, no expansion hardware:

```
                    ↓ OEM lid (uncut, acoustic insulation preserved)
   ┌──────────────────────────────┐  ← cubby ceiling
   │                              │
   │   [board][board][board]      │  ← 4 mm plastic plate (top, bare)
   │   [board]      [board]       │
   │ ─────────────────────────── │  ← CTK Standard Pro damping layer
   │ ─────────────────────────── │  ← CTK doorkit foam decoupling layer
   │   |                       |  │  ← plate-edge cuts engage cubby wall features
   │   ↓ multi-layer CTK shim ↓  │     (friction-fit retention; tape on edges
   │                              │      for tighter wedge if needed)
   └──────────────────────────────┘  ← cubby floor (stepped — back is lower)
```

Mechanism:

- Plate edges are cut with **notches** that engage cubby wall features (corners, body-shell protrusions, trim mounting bosses). Each engaged notch resists translation in one or two axes.
- Multi-layer CTK Standard Pro shim stack at the back of the plate (where the cubby step sits lower) levels the plate horizontally.
- Optional 3M VHB foam tape along edges for compliance + slight preload — turns "loose-with-clearance" fit into "preloaded against rubber."
- Removal: lift the front of the plate, slide back-out — same as putting it in. ~5 minutes from cubby-trim-open to plate-out.

**Vibration durability** is bounded by:

- The CTK butyl layer's compression set over time (re-check at 3-month and 12-month intervals — same schedule as the CCA crimps in `work/center_console_refresh/README.md`). Standard Pro is automotive-grade and survives Finnish summer cabin temperatures (60–70 °C in sun) without significant creep.
- Tape adhesion if used (3M VHB rated to ~90 °C continuous; standard masking/cloth tape will fail in months — VHB only on this surface).

### Cooling — see Cooling Architecture §

The plate itself is not the cooling system. See the dedicated Cooling Architecture § below for the foam-baffled side-trim intake + exhaust + lid-preserving design. Kept separate because the cooling design has its own constraints (the OEM lid's acoustic role) that reach beyond the plate.

## Component Mounting

Components mount directly to the plate via **screw-tower standoffs** — typically 6–10 mm M3 threaded standoffs bolted through the plate from underneath, with the board screwed onto the tower from above. No per-component base plate; no T-nuts; no cassette intermediate.

| Component | Mounting | Position priority | Notes |
| :--- | :--- | :--- | :--- |
| **UP 6DSP** | M4 screws or rubber-isolated grommets through the DSP's existing mounting flanges, into M4 standoffs anchored to the plate | **Front (cabin / fresh-air side), supported plate edge** | Heaviest component (~700 g). Inertial loading wants the mass close to a friction-fit-engaged plate edge, not floating in the middle. |
| **RPi5 + NVMe HAT** | 4 × M2.5 brass standoffs to Pi mounting holes; NVMe HAT stacks above on the same standoffs (or extension standoffs); 25 mm clearance above the Pi for the 40-pin GPIO header (used for UART link to nRF54L15 — see Cable Management §) | **Front (cabin / fresh-air side)** — second-highest heat source | Plate is non-conductive (plastic), so brass standoffs don't change the Pi's thermal path significantly; the heatsink/fan on the Pi SoC does the cooling work. **NVMe slot accessibility:** orient the Pi so the NVMe slot is on the cabin-facing side (slot is on the underside of the M.2 HAT+) — NVMe swap doesn't require unmounting the Pi from the plate. |
| **Carlinkit CPC200-CCPA** | USB-A plug into Pi + zip-tie body to the plate (NOT relying on the USB connector for mechanical retention) OR small bracket / pocket holding the dongle body | Adjacent to Pi (USB cable is integrated and short) | Without mechanical anchor, cabin vibration over months works the USB connector loose. Anchor the dongle body, not the cable. |
| **nRF54L15 DK** | 4 × M3 nylon standoffs through DK mounting holes (electrically isolated from the plate, though plate is plastic so isolation is moot) | **Back (bulkhead side), BLE antenna oriented toward cabin** | BLE antenna needs ~15 mm dielectric-clear space. Orient the DK so the antenna edge faces forward into the cabin (where phone-bearing user approaches), NOT into the trunk bulkhead. ≥50 mm clearance from DSP heatsink (RF deflector). UART link to Pi via GPIO header — see Cable Management § Bundle D. |
| **nRF93M1 DK** | 4 × M3 nylon standoffs through DK mounting holes | **Back (bulkhead side), corner closest to the May 3 fish-string pass-through** | The SMA pigtail to the trunk-mounted LTE antenna wants the shortest run with no sharp connector bend (RG-174/LMR-100 hates tight bends right at the SMA). SIM tray (J2 edge) faces an accessible side — lid-opening side, not buried — so SIM swap works with the lid open, no full disassembly. |
| **Female cigarette-lighter socket** | Panel-mount through a hole in the plate; charger plugs in normally and is removable | Anywhere with vertical clearance for the charger's body | The socket lets the 85 W charger be swapped without rewiring. Socket positive → 50 A rocker switch → ATO fuse → IRF4905 high-side MOSFET drain (when cabin node firmware is online; manual-only until then). See Power Topology §. |
| **50 A rocker hard-kill switch** | Panel-mount through a plate cutout, accessible when cubby lid is open | Front edge of plate, ergonomic from above with lid open | "ON" label orientation verified with continuity meter before final wiring (cheap rocker switches are sometimes mis-labeled). See Power Topology §. |
| **ATO fuse box** | Mounted to plate via through-bolts or strong adhesive; close to +12 V cubby entry point | Adjacent to switch, on the +12 V source side | Close-to-source per automotive convention. Spare slots reserved for cabin-node always-on rail (1–2 A fast-blow when added). See Power Topology §. |
| **Wago splice block (project box)** | Box mounts to plate via 4 M3 bolts; lid lift-off for service | Wherever cable bundles aggregate — typically near the +12 V entry side | See Wago Splice Block §. |

**Service access:** every component lifts off its standoffs by removing 2–4 screws. Same granularity as the original cassette design, less hardware. The plate stays put unless the entire rear-cubby integration is being re-done.

## Cable Management

Cabling is the secret killer of any rack install. Approach: **separate bundles by signal class**, **service loops at every cassette**, **strain relief at every entry/exit**.

### Bundles (color-coded with tape or cable ties)

| Bundle | Carries | Color tag | Routing |
| :--- | :--- | :--- | :--- |
| **A** Power high-current | 8 mm² CCA red (battery +12 V from AGU), 8 mm² CCA black (ground to factory stud), DSP REM jumper (currently +12 V) | **RED tape** | Enters cubby from outboard side, terminates at DSP +12 V terminal block. Wago `221-413` tap on the DSP +12 V terminal branches to: (a) cabin-node always-on buck, (b) IRF4905 MOSFET source, (c) lighter socket positive. |
| **B** Power low-current branches | 1.5 mm² red branches from the Wago tap to charger / nRF buck / aux 12 V outlet | **YELLOW tape** | Internal to the rack; strain-relief at the Wago and at each cassette terminal. |
| **C** Audio signal | BE2210 high-level CAT6 (already in cubby), DSP speaker outputs (4 × 2.5 mm² to fronts/sub) | **WHITE tape** | Enters cubby from inboard side (separate entry from Bundle A to avoid power-induced noise). DSP speaker outputs route through cassette-to-cassette spaces directly to vehicle-side. |
| **D** USB / data | Pi → MEC HD-USB (audio sink), Pi → nRF54L15 (USB-CDC), Pi → Carlinkit dongle, Pi → display USB-A | **BLUE tape** | Internal to the rack between Pi cassette and DSP / nRF cassettes. The Pi → DSP USB cable is the ~10 cm in-cubby pull that the May 1 bench test proved out. |
| **D2 (NEW)** UART link Pi ↔ nRF54L15 | 3 wires: Pi GPIO TX (e.g. UART2 on GPIO 0/1, or UART3, etc.) → nRF54L15 RX; Pi GPIO RX → nRF54L15 TX; common GND. **Replaces the originally-planned USB-CDC link** (decision May 17). | **BLUE tape** (continues with Bundle D) | Three-conductor jumper from Pi 40-pin GPIO header → nRF54L15 DK GPIO header. Both 3.3 V — no level shifter. Frees one Pi USB-A port for joystick / diagnostic / spare. |
| **E** Antenna / RF | nRF54L15 BLE chip antenna (PCB integrated, no cable), nRF93M1 SMA cellular antenna pigtail to trunk-mounted antenna via May 3 fish-string pass-through | **GREEN tape** | nRF BLE: clear-space requirement only (~15 mm dielectric-clear, oriented toward cabin). Cellular: SMA pigtail from nRF93M1 → bulkhead pass-through → trunk antenna (~4 m RG-174/LMR-100). |
| **F** Display + HDMI (front-cubby pulls already done) | C16 HDMI to display, C17 USB to display touch | **PURPLE tape** | Already pulled May 4; terminates at Pi position in the rear cubby. |

### Service loops

Each board gets ~10 cm of slack on every cable entering it — enough to lift the board off its standoffs and lay it on the cubby floor for service without disconnecting wires. This costs ~1 L of cable volume in aggregate but pays for itself the first time something needs to be reseated.

### Strain relief

- **At cubby entry:** rubber grommet through the trim panel cutout (cabin-side and outboard-side entries have separate grommets to keep Bundle A separated from Bundle C).
- **At each board terminal:** zip-tie anchoring the bundle to the plate (via standoff hole or dedicated zip-tie anchor point) before the conductors land in the screw terminal / connector. Stops vibration from working the terminal joint loose over years.
- **At the Wago splice block:** the 8 mm² CCA enters the project box straight through a strain-relieved grommet; the 1.5 mm² branches exit through their own grommets. See Wago Splice Block §.

## Power Topology

The +12 V → small-signal power chain has **two independent control elements** in series — one firmware-driven (the cabin signal node's IRF4905 high-side MOSFET), one firmware-independent (the manual 50 A rocker hard-kill switch). Either off → entire small-signal stack off. The manual switch is **permanent infrastructure**, not an interim placeholder.

```
   +12 V from cubby wiring (post-AGU 8 mm² CCA tap, factory lighter-circuit fuse 8 A upstream)
      │
      ▼
   ATO fuse (7.5 A slow-blow, charger branch)
      │   ← fuse close to source per automotive convention
      ▼
   50 A rocker hard-kill switch  ← MANUAL (permanent), independent of firmware
      │
      ▼
   IRF4905 P-channel high-side MOSFET (when cabin node firmware is online; manual-only until then)
      │   ← FIRMWARE-driven (BLE proximity, KL15 override, graceful-shutdown handshake)
      ▼
   Female cigarette-lighter panel-mount socket
      │
      ▼
   85 W cigarette-lighter USB charger
      │
      ├──► Pi5 USB-C (5 V power)
      ├──► Carlinkit dongle (5 V via Pi USB-A pass-through, OR direct from charger USB-A)
      ├──► nRF93M1 DK USB-A (5 V power + RNDIS data + AT serial)
      └──► nRF54L15 DK USB-A (5 V power only — data path is UART, see Cable Management § Bundle D2)

   Always-on rail (separate, ≤200 µA standby budget — see cabin_signal_node README §"Always-on power supply"):
   8 mm² CCA tap → 1 A ATO → reverse-polarity Schottky → low-Iq buck → cabin node nRF54L15 +3.3 V always-on
```

### Why both controls (architectural rationale)

| Control | Type | Roles | Failure modes it covers |
| :--- | :--- | :--- | :--- |
| **50 A manual rocker switch** | Firmware-independent | Service disable while plate is on bench; firmware-bug recovery if MOSFET ever latches in a bad state; long-storage zero-parasitic-drain mode; diagnostic forcing-on regardless of phone presence; transport mode | Cabin node firmware crash, MOSFET drive failure, runaway BLE proximity logic, dead bonded phone, accidental flash erase |
| **IRF4905 high-side MOSFET** | Firmware-driven (cabin signal node Stage 6b — see [`work/cabin_signal_node/README.md`](../cabin_signal_node/README.md) §"Cabin 12 V power-domain high-side switch") | Automatic BLE-proximity power-up; graceful shutdown handshake; KL15 ignition override | Manual switch left ON (forgetfulness); proximity-based wake / sleep without operator touch |

The two are **complementary**, not redundant. Production embedded vehicle ECUs typically have an analogous arrangement (e.g. a service-disable physical fuse pull combined with software KL15-conditional gating).

### Switch + fuse spec

| Component | Spec | Source | Notes |
| :--- | :--- | :--- | :--- |
| Manual hard-kill switch | 2-terminal rocker, 50 A continuous rated, no integrated illumination | Acquired May 17 (existing inventory / local automotive shop) | Overkill rating (~5–7×) → contact erosion essentially zero over install lifetime. **"ON" label orientation must be verified with continuity meter before final wiring** — cheap rocker switches are sometimes mis-labeled relative to internal contact state. |
| Charger-branch fuse | 7.5 A slow-blow ATO blade | Local automotive (Motonet/Biltema) | Sized to handle 85 W charger inrush (~8.4 A peak in) without false-tripping; tightly selective vs upstream factory 8 A lighter fuse (any local fault opens the local fuse first). |
| Spare fuse-box slots | 1–2 A fast-blow (when added: cabin-node always-on rail; future joystick / sensor branch) | Same | Reserved capacity in the fuse box; specific values depend on each branch's measured load. |
| Fuse box | ATO blade-fuse box, ≥4 slots, panel-mountable | Same | Mounted as close to +12 V cubby entry as practical. |

## Cooling Architecture

The cooling design has one absolute constraint that emerged from a measured observation on May 17: **the OEM cubby lid is acoustic insulation, not just trim.** With the lid OFF during install fitting, exhaust drone bled into the cabin audibly. With the lid ON, gone. The lid's noise-barrier function is a measurable NVH win that must not be sacrificed for cooling.

→ **No air paths through the lid.** All intake/exhaust goes through cubby trim side walls (replaceable plastic) or the rear bulkhead (already has a fish-string pass-through to the trunk from May 3).

### Heat budget vs cooling capacity

| Quantity | Value | Source |
| :--- | :--- | :--- |
| Steady heat dissipation | ~20–25 W | DSP ~6 W + Pi typical 10–15 W + nRFs ~2 W + charger ~3 W |
| Peak heat | ~50 W | Pi peak 25 W + DSP under load + everything-else simultaneous |
| 60 mm 12 V case fan typical airflow | 20–30 CFM at moderate RPM | Datasheet (Arctic F6 12 V, similar) |
| Air mass flow at 20 CFM | ~10 g/s | Air ρ ≈ 1.2 kg/m³ |
| ΔT across cubby at 20 CFM, 25 W | ~2.5 K | $\Delta T = Q / (\dot{m} \cdot c_p)$, with $c_p \approx 1$ kJ/(kg·K) |
| Commissioning gate (per `work/center_console_refresh/README.md` §6.5b) | ≤50 °C ambient at any point | — |

A 60 mm 12 V fan at moderate RPM has ~10× margin over the worst-case heat budget. Even a 40 mm 5 V fan would suffice mathematically. **Liquid cooling is overkill** — the threshold where a liquid loop pays off is ~80–100 W sustained, far above this system's actual heat budget. Skip.

### Architecture: side-trim intake + foam baffle + cross-flow exhaust

```
            ┌────────────[ OEM LID — uncut, acoustic seal preserved ]──────────┐
            │                                                                   │
   cabin    │   ╔═════════════════════════════════════════════════════════╗     │
   side     │   ║                                                          ║     │
   ←─[foam]─┤───║  [DSP front]  [Pi front]                                ║     │
   intake   │   ║  [nRF54L15 back]  [nRF93M1 back]                        ║     │
            │   ║                                                          ║─[foam]─→
            │   ╚═════════════════════════════════════════════════════════╝     │   exhaust
            │     ↑ 60 mm 12 V fan (rubber-grommet mount)                       │   (cabin
            │                                                                   │    or trunk)
            └───────────────────────────────────────────────────────────────────┘

   foam plenum on both vents (open-cell PU, 30–50 mm depth) replaces the lid's
   acoustic seal — kills high-frequency noise (electronics whine, fan blade noise,
   exhaust drone) while passing cooling air freely. Standard rack-cabinet
   noise-control technique.
```

Element-by-element:

| Element | Spec | Reason |
| :--- | :--- | :--- |
| **Intake** | ~50 mm hole in cubby trim **side wall** (NOT lid), low position, hidden behind passenger-seat back / carpet | Cool cabin air sinks → low intake gives best ΔT. Trim side wall is a replaceable plastic part (~€30–50 from a parts car if ever needed); lid is irreplaceable acoustically. |
| **Fan** | 60 mm 12 V brushless case fan (Arctic F6 12 V, Noctua NF-A6×25 5V on a buck, or equivalent), inline with intake, blowing **into** the cubby | One-fan push design is sufficient for this duty; no need for a second exhaust fan. |
| **Fan mount** | Rubber-grommet suspension to the plate or cubby trim — NOT rigid mount | Keeps fan vibration out of the structural NVH path; otherwise fan whine couples into the cubby walls and back into the cabin. |
| **Fan control** | Wired to DSP REM line (terminal-block tap), runs only when audio system is on | Avoids permanent fan whine when sitting in the car with the engine off but Pi on (rare case but real for stationary diagnostic sessions). PWM control from the cabin node based on a thermistor is a software-only retrofit later if needed. |
| **Intake foam plenum** | 30–50 mm of open-cell PU foam (PU foam, headliner foam, or studio "egg-crate" foam) on the cabin-side of the intake hole | Replaces the lid's acoustic seal. High-frequency attenuation through 30–50 mm of open-cell foam is significant; cooling air passes essentially unrestricted. |
| **Exhaust** | Passive vent — two location options pending bulkhead pass-through geometry verification (D4 in Cubby Geometry §): | (See sub-table below) |

### Exhaust location options

| Option | Path | Acoustic property | Heat property | Implementation cost |
| :--- | :--- | :--- | :--- | :--- |
| **A: Opposite side wall (mirror of intake)** | Cubby air flows through plate → exits through opposite trim side wall + foam plenum → returns into cabin | Cabin-internal cross-flow; foam-baffled both sides. Some hot-air return into cabin (acceptable, cabin volume is large vs cubby exhaust) | Hot air dumps back into cabin → AC works slightly harder in summer | Low — mirror the intake hardware on the other side |
| **B: Through rear bulkhead → trunk** | Cubby air flows through plate → through bulkhead pass-through (already has the May 3 fish-string) → into trunk | **Best**: no return path into cabin; trunk acoustic environment is naturally separated from cabin | **Best**: hot air dumps into trunk (less-conditioned space), zero impact on cabin AC load | Slightly higher — needs a sealed adapter at the bulkhead pass-through (heat-shrink-and-foam ducting OK) |

**Recommendation: Option B if the May 3 fish-string pass-through is dimensionally adequate** (≥30 mm clear bore for ~20 CFM flow without significant restriction). If the pass-through is a tight cable conduit, Option A is the fallback.

### Service / commissioning checks

The cooling architecture passes the Stage 7 commissioning gate (≤50 °C ambient at sustained load) with comfortable margin per the heat-budget math above. **Verify by direct measurement** (thermocouple or IR thermometer on the plate top + at the exhaust + ambient cabin) at the post-install thermal commissioning step. Failures (>50 °C) point to:

- Foam plenum too thick → restricting airflow → reduce foam depth on at least one vent.
- Exhaust pass-through restricted (Option B with too-small bulkhead conduit) → switch to Option A.
- Fan not running → check DSP REM tap.
- Fan running but no airflow → check intake foam not collapsed against the fan blade.

## Wago Splice Block

The rear-cubby Wago lever-nut pile (~4-in / 8-out at current count, with future joystick + sensor expansion likely) carries **speaker-signal connections only** (sub-10 A peak per conductor, well below the Wago 32 A rating). Fire risk is essentially zero (V-2 self-extinguishing housings, far below incendiary thresholds). The real concerns are mechanical: vibration over months works lever-clamps loose, exposed splice block is hard to keep service-accessible, no strain relief on the cables.

### Solution: small ABS project box

| Spec | Choice | Reason |
| :--- | :--- | :--- |
| Box | Generic ABS project box, ~120 × 80 × 40 mm, IP54-ish, vented top | Cheap (~€5–10 from Biltema/Verkkokauppa or Hammond 1591 series); same material family as the plate; fire-rated UL94 V-0 typical. |
| Internal backboard | 3 mm plywood / aluminum / cardboard, sized to fit inside the box | Wagos zip-tied to the backboard; backboard screws to the box. Backboard captures the Wagos rigidly so vibration can't shift them. |
| Foam padding | One layer of CTK doorkit foam between backboard and box wall | Vibration damping (its actual design purpose). Doorkit inventory. |
| Cable entries | Rubber grommets through box wall, one grommet per cable bundle | Strain relief at the box wall, not at the Wago lever. |
| Internal anchors | Zip-tie at each grommet's inside face anchoring each bundle to a corner before the Wago | Strain-relief layering; lever-clamp never sees cable tension. |
| Lid | Lift-off (4 screws), vented (4–6 × 5 mm holes) | Service access (every Wago lever visible and reachable from above when lid is off); free convection (defense in depth on heat). |

### Wago lever-engagement quality check

Most-common Wago 221 failure mode (well above any heating concern) is **insufficient conductor insertion** — strip too short, strands not fully captured, or insulation pinched in the clamp. Before sealing the box lid, do a 30-second tug test on each conductor: gentle pull, should not move at all. Any conductor that moves: re-strip 11 mm, re-insert, re-clamp. This single check eliminates 95 % of all real-world Wago issues over the install lifetime.

## Bring-up Sequence

The plate is the **integration vehicle** for two pending engineering tasks (DSP-as-Pi-soundcard, nRF54L15-Pi-wake) plus the plate fabrication itself. Order matters — do the bench-built work first so there are no in-cubby debugging sessions on a hot day with the trim hanging off.

### Stage 1 — Cubby measurement (≤30 min, on the car)

1. Open passenger-side rear cubby trim. Inspect for any factory mount points (none expected, but worth confirming).
2. Tape-measure D1 / D2 / D3 / **D4 (NEW: bulkhead pass-through location)** per Cubby Geometry § above.
3. Photograph the cubby interior with a ruler in frame for later reference.
4. Update this README Cubby Geometry § with the measured values; the working assumption gets replaced. D4 result determines back-zone component placement (nRF93M1 corner) and exhaust location (Option A vs B).

### Stage 2 — nRF54L15 hardware build (workbench, ~4–6 h spread over a weekend)

This is the biggest unbuilt piece. Per `work/cabin_signal_node/README.md`:

- **Stage 6 (always-on power section):** Recom R-78E3.3-0.5 buck + ATO 1 A fuse + Wago `221-413` + reverse-polarity Schottky + TVS. Mount on Veroboard.
- **Stage 6b (12 V high-side MOSFET):** IRF4905 (or IPP80P03P4L) P-channel logic-level FET + gate driver + 470 µF input bulk cap + optional NTC inrush limiter + INA226 current-sense. Sized for 10 A continuous / 15 A peak. **Now in series with the manual hard-kill switch — see Power Topology §.**
- **BLE proximity firmware:** RSSI hysteresis, bonded-phone scanning, **heartbeat over UART (NOT USB-CDC — May 17 decision)**. Same payload codec, different transport.
- **Bench-verify with a 12 V supply + 70 W resistive load** before the plate is ever assembled. Stage 6 success criterion (per cabin_signal_node README): phone-approach turns on the load; phone-leave turns it off after the grace period.

Stage 2 happens **independently of the plate** — pure bench work on the workbench. Output is a functioning Veroboard or DK firmware ready to install onto the plate.

### Stage 3 — Plate fabrication (workbench, ~1 h) ✅ DONE 2026-05-17

1. Cut 4 mm plastic plate to cubby footprint (irregular polygon matching the wheel-well intrusion + cabin-side straight edge). ✅
2. Bond 1 layer of CTK Standard Pro to underside (full coverage). ✅
3. Stack multi-layer CTK shims at the back where the cubby step is lower (level the plate). ✅
4. Bond 1 layer of CTK doorkit foam over the CTK underside (vibration decoupling + dielectric barrier). ✅
5. Cut friction-fit notches in plate edges to engage cubby wall features. ✅

### Stage 4 — Component mounting + power topology hardware (workbench, ~2–3 h)

1. Drill standoff holes in the plate per layout.
2. Install screw-tower standoffs (M3 / M2.5 as appropriate per board).
3. Cut hole + install female cigarette-lighter panel-mount socket.
4. Cut hole + install 50 A rocker hard-kill switch.
5. Cut hole + install ATO fuse box (or surface-mount it via through-bolts).
6. Mount components to standoffs: DSP, Pi5 + NVMe HAT, nRF54L15 DK, nRF93M1 DK, Carlinkit (zip-tied).
7. Wire the Power Topology series chain: +12 V cubby entry → ATO 7.5 A slow-blow → 50 A rocker switch → female lighter socket → 85 W charger USB-C output → Pi USB-C. Verify "ON" position on switch with continuity meter BEFORE final wiring.
8. Build / install the Wago splice block per Wago Splice Block §.
9. Wire bundles per Cable Management § (color-tape the bundles).

### Stage 5 — Pre-install bench test (workbench, ~1 h)

1. Assemble the full plate on the workbench: all components, all bundles.
2. Power up from a bench supply at 12.5 V. Verify:
   - Manual switch OFF → no current draw, all boards dark.
   - Manual switch ON → DSP comes up (Auto Remote OFF + REM-to-+12 V jumper, per May 7 in-car install).
   - Pi5 boots from NVMe.
   - nRF54L15 frames visible on the Pi UART (cabin_signal_node Stage 1 heartbeat — verify with Python decoder reading from `/dev/serial0` or the chosen UART).
   - nRF93M1 enumerates on the Pi USB (RNDIS + AT serial; per `docs/diary/2026-04.md` April 6/7 bring-up).
   - **DSP-as-Pi-soundcard test**: connect Pi USB-A → MEC HD-USB cable, configure PipeWire default sink to `HD-AUDIO USB-INTERFACE FS`, play audio from the Pi, verify it comes out the DSP (see DSP6-as-RPi5-Soundcard § for procedure).
   - **Pi-wake test** (only after cabin node firmware Stage 6b is operational): with phone bonded, walk away → IRF4905 turns off → 85 W charger drops out → Pi loses USB-C power → Pi shuts down. Walk back → MOSFET on → charger up → Pi boots (see nRF54L15 Pi-Wake Control § for procedure).
   - Manual switch OFF mid-operation → instant cut to all small-signal electronics regardless of firmware state (validates the hard-kill function).
   - Fan spins when DSP is on, stops when REM goes low.
3. Run the bench test for 30 min sustained → measure plate ambient temp at three points (top of DSP, between Pi and nRF, at the fan exit) → sanity-check the thermal model.

### Stage 6 — In-car install (1–2 h)

1. Disconnect the DSP from its current direct-floor mounting (4 M4 wood screws into the cubby floor).
2. Mount the DSP onto its standoffs on the plate; reconnect to the existing CCA power + ground + speaker outputs + REM jumper + BE2210 high-level tap.
3. Cut foam plenums + drill side-trim intake hole(s); install the 60 mm fan inline with the intake.
4. Determine exhaust path (Option A or B per D4 measurement); install exhaust foam plenum + bulkhead pass-through ducting if Option B.
5. Friction-fit the plate into the cubby; verify CTK shim levels the plate flush across its footprint.
6. Re-route the bundles per Cable Management §.
7. Power up; smoke-test repeats Stage 5 verifications in-car.

### Stage 7 — Commissioning gate (30+ min sustained run, observe)

Per `work/center_console_refresh/README.md` §6.5b:

- Run the system at sustained moderate load for 30+ min (Pi at typical load, DSP at moderate volume, fan running).
- Measure plate ambient temperature with a thermocouple or IR thermometer at three points (top of DSP, between Pi and nRF, at the exhaust).
- **Pass criterion: ≤50 °C ambient** at any point on the plate.
- **Sub-rattle test (additional, post-install):** play a known bass-heavy track at moderate volume; listen for any resonance from the cubby region. If any buzz: EPDM stick-on bumper pads (3M Bumpon SJ-5302/5303 or generic) on the lid underside near the trim contact edges are the standard fix.
- If >50 °C: investigate ducting / venting / cubby trim airflow per Cooling Architecture § failure-mode table.

### Stage 8 — Trim close + service-access verification (15 min)

1. Reinstall the cubby trim panel (relief notched if D3 measurement requires it).
2. Verify component removability: unscrew 2–4 bolts on any board, lift it off the standoffs onto the cubby floor on its service loop. Confirm everything stays connected and powered.
3. Verify SIM tray accessibility on nRF93M1 with lid open.
4. Final smoke test with the trim closed.

## DSP6 as RPi5 Soundcard (Integration Detail)

This is the audio path enabling CarPlay through the new DSP + speaker system.

### Hardware

- **Cable:** 1 × USB 2.0 A-to-B, ~30 cm (already on hand per `docs/diary/2026-05.md` May 2 evening shopping list, item #6).
- **Routing:** Pi USB-A port → MEC HD-USB module port (full-size USB-B, the "thicker pre-micro-USB connector" — the one that's confirmed correct on the MEC module).
- **Length:** ~10 cm in the cubby is enough; the slack in the 30 cm cable goes into the Pi service loop.

### Software

On the Pi (per `docs/RPi5_Bring-up_Plan.md` Step 7 once it lands):

1. Confirm the MEC HD-USB enumerates: `aplay -l` should show `HD-AUDIO USB-INTERFACE FS` as a card.
2. Set PipeWire default sink:
   ```
   wpctl status              # find the sink ID
   wpctl set-default <id>    # make MEC HD-USB the default
   ```
3. Persist the default-sink choice in `~/.config/wireplumber/main.lua.d/` (a small Lua snippet that picks the MEC by USB device descriptor).
4. Test path: `paplay /usr/share/sounds/alsa/Front_Center.wav` → audible through the speakers connected to the DSP.

### CarPlay path

- iPhone → wireless CarPlay (WiFi Direct) → Carlinkit CPC200-CCPA dongle (USB to Pi) → Pi audio routing → PipeWire → MEC HD-USB → DSP → speakers.
- The Carlinkit dongle presents itself to the Pi as a USB Audio Class **source**; the MEC HD-USB is the **sink**. PipeWire bridges them automatically once both are enumerated.
- Latency is dominated by the WiFi-Direct CarPlay link (~150–250 ms one-way) — well above the audible threshold for video sync, but CarPlay handles its own A/V sync, so the user-perceived latency is fine for music + navigation.

### DSP source priority (already configured)

Per the May 1 bench test and confirmed in-car on May 7: USB primary, BE2210 fallback. When the Pi is powered and streaming, the DSP picks USB; when the Pi is off (cabin domain off, no phone present), the DSP falls back to BE2210. This is exactly the desired behavior.

## nRF54L15 Pi-Wake Control (Integration Detail)

This is the always-on logic that lets the Pi sleep when the owner is away and wake when they approach.

### Hardware

- **nRF54L15 carrier (Veroboard, built in Stage 2 above):** lives on its standoffs on the plate. Always-on, drawing ≤200 µA from the post-AGU CCA rail via the local Wago tap → 1 A fuse → Recom buck (independent of the manual hard-kill switch — the always-on rail is upstream of the switch).
- **IRF4905 high-side MOSFET:** also on the cabin node Veroboard. Source = post-AGU 12 V (Wago tap branch through the manual switch + ATO fuse — see Power Topology §); drain = 12 V input of the 85 W charger (via the female cigarette-lighter socket on the plate); gate driven by an nRF54L15 GPIO through a level-shifter. **In series with the manual hard-kill switch** — either off interrupts power to the charger.
- **85 W charger:** plugs into the lighter socket on the plate. Its USB-C output → Pi USB-C input (directly powers the Pi). Other USB-A outputs (Carlinkit, nRF93M1, nRF54L15-DK 5 V power) hang off the same charger.

### Software

On the nRF54L15 (Zephyr / Nordic SDK firmware in `FW_nrf/`):

1. **BLE proximity scanner**: scans for the bonded phone's BLE advertisement, computes RSSI with hysteresis (e.g. enter at −70 dBm, exit at −85 dBm) to prevent flapping.
2. **GPIO output**: drives the IRF4905 gate. HIGH = MOSFET conducting = charger powered = Pi gets 5 V on USB-C = Pi boots. (Manual hard-kill switch must also be ON; in series.)
3. **UART frame to Pi**: sends a `R129_TYPE_PRESENCE` frame at 1 Hz with the current proximity state over the UART link (Pi GPIO header — see Cable Management § Bundle D2). **Replaces the originally-planned USB-CDC link** (May 17 decision; same payload codec, different transport).
4. **Graceful-shutdown handshake** (Stage 6/7 of cabin_signal_node):
   - Phone leaves range → nRF detects the RSSI exit transition.
   - nRF sends `R129_TYPE_SHUTDOWN_REQUEST` UART frame to Pi.
   - Pi runs `systemctl poweroff` (or a pre-shutdown hook that flushes state, dims display, etc.).
   - Pi acknowledges with `R129_TYPE_SHUTDOWN_ACK` UART frame.
   - nRF starts a 60-second grace-period timer.
   - On grace expiration (or sooner if Pi acknowledges fully off), nRF deasserts MOSFET gate → charger off → Pi loses power.
5. **KL15 override**: if the engine is running (KL15 high), the cabin domain stays on regardless of phone state. KL15 sense is currently jumpered from the BE2210 ACC line in the rear cubby; the permanent KL15 sense moves to the deferred front-half cabin acquisition board when that board exists.

### Hardware Pi-side UART configuration

Enable a Pi GPIO UART (other than the BT-shared default) via Device Tree overlay in `/boot/firmware/config.txt`:

```
enable_uart=1
dtoverlay=uart2     # or uart3 / uart4 / uart5 — Pi5 has 5 UARTs
```

Wiring:

| nRF54L15 DK | Pi5 (40-pin header, depending on chosen UART) | Wire |
| :--- | :--- | :--- |
| Default app-core UART TX (P0.20 on PCA10156) | Pi UART RX | nRF→Pi |
| Default app-core UART RX (P0.22) | Pi UART TX | Pi→nRF |
| GND | any GND pin | common |

Both 3.3 V GPIO; **no level shifter needed**.

### Key safety detail

Until the graceful-shutdown handshake firmware is fully working, the Pi can be killed mid-write by an over-aggressive nRF cutting power. Mitigation:

- Pi root filesystem on NVMe with `commit=1` mount option for ext4 (writes flush every 1 s, not every 5 s default).
- nRF firmware initially uses a generous 5-minute grace timer; tighten to 60 s only after the handshake is proven.
- Pi runs a `pre-shutdown` script that calls `sync` before triggering `systemctl poweroff`.
- **Manual hard-kill switch** is the operator-side bypass: never cuts during a write because the operator only flips it during deliberate service / standby actions.

## Bill of Materials (Plate-Specific)

Items unique to the plate itself. The DSP / Pi / nRF / charger BOMs live in their respective subsystem READMEs.

**Status (May 17 architecture rev):** total drops from ~€85 (May 7 aluminum-extrusion design) to ~€20–30 net new spend, because the new design uses ~€10–15 of inventory (plastic offcut, doorkit CTK + foam) plus ~€10–15 of new items (manual switch, fuse box, ABS project box, fan, lighter socket, grommets).

| # | Component | Spec | Qty | Source | Cost (€) | Status |
| :--- | :--- | :--- | :--- | :--- | ---: | :--- |
| P1 | Plastic plate stock | 4 mm sheet (PP / HDPE / PVC), cut to cubby footprint with corner-intrusion notches and friction-fit edge cuts | 1 | Inventory offcut | (in stock) | ✅ Cut May 17 |
| P2 | CTK Standard Pro damping layer | 2 mm butyl + foil, full underside coverage + multi-layer back-edge shim | ~0.4 m² | Doorkit inventory | (in stock) | ✅ Bonded May 17 |
| P3 | CTK doorkit foam | Profildamp 7.5 mm closed-cell PE with fabric face, full underside | ~0.3 m² | Doorkit inventory | (in stock) | ✅ Bonded May 17 |
| P4 | Acoustic carpet (edge wrap from underside) | Dark-grey, ~0.10 m² for plate edges + ~0.05 m² for sub-cubby lid foam-wedge front edge | ~0.15 m² | Autoviihde, leftover from sub-box wrap (~1.25 m² spare from 2 m² roll) | (in stock) | Pending application |
| P5 | Spray contact adhesive | 3M Super 77 or equivalent | 1 can | Local hardware | ~10 | Pending |
| P6 | Screw-tower standoffs | M2.5 / M3 / M4 mixed, 6–10 mm height, threaded both ends | assorted (~20–30) | Inventory or assortment kit | ~5 | Inventory check |
| P7 | M3 / M4 screws | Various lengths (6 / 10 / 16 mm) for component fastening to standoffs | assorted | Inventory | (in stock) | — |
| P8 | 60 mm 12 V brushless case fan | Arctic F6 12 V or equivalent, ~0.1 A draw, rubber-grommet mount kit | 1 | Local hardware / Verkkokauppa | ~10 | Pending |
| P9 | Female cigarette-lighter panel-mount socket | Standard 12 V auto socket with mounting collar | 1 | Local hardware / Biltema | ~5 | Pending / acquired May 3 |
| P10 | **Manual hard-kill rocker switch** | 2-terminal, 50 A continuous, no integrated illumination | 1 | Local automotive / inventory | ~5 | ✅ Acquired May 17 |
| P11 | **ATO fuse box** | ≥4-slot, panel-mountable, ATO blade fuses | 1 | Local automotive / inventory | ~5 | ✅ Acquired May 17 |
| P12 | ATO blade fuses | 7.5 A slow-blow (charger branch) + 1–2 A fast-blow (spare slots for cabin-node always-on, future joystick) | assorted (~5) | Local automotive | ~3 | Pending |
| P13 | Rubber cable grommets | For cubby trim cutouts (intake, exhaust if Option B) and project-box cable entries | ~6 | Local hardware | ~3 | Pending |
| P14 | **Wago splice-block project box** | ABS, ~120 × 80 × 40 mm, vented top, lift-off lid | 1 | Biltema / Verkkokauppa / Hammond 1591 | ~5–10 | Pending |
| P15 | Internal backboard for project box | 3 mm plywood / aluminum / cardboard, sized to fit box | 1 | Inventory offcut | (in stock) | — |
| P16 | Acoustic foam plenums | 30–50 mm open-cell PU foam, ~100 × 100 mm pieces for intake + exhaust vents | 2 | Local upholstery / inventory | ~5 | Pending |
| P17 | Cable ties + heat shrink + colored tape | Bundle separation per Cable Management § | assorted | Inventory | (in stock) | ✅ |
| P18 | UART jumper wires | 3 × ~30 cm Dupont female-female (Pi GPIO header → nRF54L15 DK GPIO header) | 3 | Inventory | (in stock) | ✅ |
| | **Subtotal (plate-specific, net new)** | | | | **~€50–55** | |

Plus the existing in-flight items (cabin-node Veroboard parts for the eventual production-side IRF4905 + always-on supply, etc.) are accounted for in `work/cabin_signal_node/README.md` BOM and `docs/parts_to_order.md`.

## Open Questions / Decisions Pending

- **D4: bulkhead pass-through location.** Determines (a) which corner the nRF93M1 occupies on the back of the plate — the corner closest to the pass-through wins so the SMA pigtail is short with no sharp connector bend; (b) cooling exhaust location — Option B (trunk-side) preferred if pass-through is dimensionally adequate, Option A (opposite cabin-side wall) is the fallback. 30-second tape measurement at next cubby-trim-open window.
- **"ON" label orientation on rocker switch** (15-second continuity-meter check before final wiring). Cheap rocker switches are sometimes mis-labeled relative to internal contact state.
- **Charger placement strategy:** plug-in via panel-mount lighter socket (current plan, easy swap) vs. hardwired (saves ~5 cm of plate footprint, voids any warranty on the charger). Working assumption: lighter socket.
- **Fan duty cycle / control:** simple on/off via DSP REM (current plan) vs. PWM-controlled by the nRF54L15 based on a thermistor on the plate (more complex, allows quieter idle running). Working assumption: on/off. PWM is a software-only retrofit later.
- **NVMe access during install:** the Pi5 NVMe slot is on the underside of the M.2 HAT+; with the Pi mounted to standoffs, the NVMe is between the Pi PCB and the plate. **Decision: orient the Pi so the NVMe slot is on the cabin-facing side** of the plate so NVMe swap doesn't require removing the Pi from the plate.
- **USB hub:** with the nRF54L15 on UART (May 17), Pi USB-A budget drops from 4-of-4 used to 3-of-4 used. Hub becomes optional, not required. Z-height is reserved for one if a future load (e.g. a USB joystick or a second sensor) needs it.

## Cross-References

- Audio architecture (DSP, MEC HD-USB, sub box): `work/audio_upgrade_blueprint.md`
- Cabin always-on / nRF54L15 / IRF4905 high-side MOSFET / BLE proximity: `work/cabin_signal_node/README.md`
- Pi headless setup, NVMe boot, display integration: `docs/RPi5_Bring-up_Plan.md`
- Center console refresh + cable manifest (the long pulls C16/C17/C18 already done): `work/center_console_refresh/README.md`
- Audio bench test (DSP-as-soundcard validated 2026-05-01): `work/audio_bench_test.md` §9
- Sub box build (driver-side cubby twin): `work/subwoofer_enclosure/README.md`
- Engine-bay node (same nRF SDK / payload format pattern): `docs/nRF5430_Interface_Design.md`

## Work Log

| Date | Stage | Notes |
| :--- | :--- | :--- |
| 2026-05-07 | Doc created (initial design) | Aluminum 20 × 20 mm T-slot extrusion + modular cassette + expansion-clamp friction-fit + 60 mm fan-from-the-start. BOM ~€85. Cubby measurements pending; no fabrication started. (Architecture superseded May 17 — preserved in `docs/diary/2026-05.md` May 7 entry for reference.) |
| 2026-05-17 | Architecture simplified + plate fabricated | Replaced aluminum extrusion + cassettes with 4 mm plastic plate + CTK damping + screw-tower standoffs + zip-tie cable management. Plate cut, CTK bonded, foam underside bonded, friction-fit notches cut. Component layout iterated on the bench (DSP front, Pi front, nRF93M1 + nRF54L15 back). nRF54L15 link moves from USB-CDC to UART (frees Pi USB-A port; same payload codec, different transport). Manual 50 A hard-kill switch + ATO fuse box added in series with charger feed; promoted from interim to permanent design element. Wago splice-block project box plan added. Cooling architecture re-derived from "OEM lid is acoustic insulation, do not cut" constraint: side-trim foam-baffled intake + cross-flow exhaust (cabin or trunk via May 3 fish-string). BOM net-new spend drops to ~€50. Plate ready for power-topology wiring; in-car install pending. |
