# Rear Passenger Cubby — Electronics Installation Rack

**Status (2026-05-07):** Planning / design phase. UP 6DSP is mounted directly to the cubby floor today (per the May 7 audio install). This doc captures the next-step plan to consolidate **all** rear-cubby electronics — DSP, RPi5, nRF54L15 cabin node, 85 W cigarette-lighter USB charger, and future nRF93M1 cellular modem — onto a shared modular rack, plus the integration of the DSP6 as the Pi's USB Audio Class soundcard (enabling CarPlay) and the nRF54L15 always-on Pi-wake controller.

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
| Match UP 6DSP + MEC HD-USB | ~1.7 L (with 40 mm heatsink ventilation clearance) | ~6 W (Class GD ~85 % eff) | USB-C control port for re-tuning | Already in cubby (May 7) ✅ |
| RPi5 + NVMe HAT | ~1.0 L | ~10–15 W typical, ~25 W peak | NVMe slot, 4× USB-A, 2× HDMI, 40-pin GPIO | Pending in-cubby install |
| nRF54L15 carrier (Veroboard) | ~0.3–0.5 L | <1 W | RESET button, programming pins, vehicle-side pluggable terminals, BLE antenna clearance | Pending hardware build (cabin_signal_node Stage 6/6b) |
| 85 W cigarette-lighter USB charger | ~0.3 L | ~3 W typical (20 W out @ ~85 % eff), peak ~12 W | USB-C + USB-A ports out (to Pi, Qi pad, spare) | Acquired May 3 |
| Female cigarette-lighter socket (panel-mounted on rack) | ~0.1 L | — | Charger plugs into this socket | New — see BOM |
| (Future) nRF93M1 cellular modem | ~0.2 L | ~1–2 W avg, ~5 W TX peak | SIM tray, SMA antenna pigtail | Reserved cassette slot |
| Cabling + service loops + connectors | ~1–2 L | — | Strain relief at every entry/exit, service-loop slack | Designed in §5 below |
| **Total used** | **~5 L of ~17 L** | **~25 W steady, ~50 W peak** | — | — |

**~12 L free** — generous physical headroom. The challenge is mechanical, thermal, and EMI, not volume.

## Design Approach

**Aluminum-profile open-frame skeleton + modular component cassettes + friction-fit clamping mount.**

Rationale (decisions logged 2026-05-07):

- **Aluminum profile (T-slot extrusion, e.g. 20 × 20 mm):** Open structure → natural ventilation. Rigid, vibration-tolerant. T-slot allows infinite component placement flexibility. Reusable across future projects. Same construction language used for 3D-printer frames, lab equipment, and industrial enclosures.
- **Modular cassettes:** Each subsystem (DSP / Pi / nRF / charger / future modem) lives on its own small base plate that bolts to the frame via M5 T-nuts. Removing a cassette = unscrewing 4 bolts; the frame stays in the car. Enables independent service, swap-out, or future upgrades without disturbing the rest of the stack.
- **Friction-fit clamping mount:** Rubber-padded ends on the frame's vertical members + screw-tightened expansion clamps against the cubby walls. **Zero holes drilled in the car.** Fully reversible; the entire rack can be removed and the cubby restored to factory in ~10 minutes. Vibration durability is bounded by the rubber padding's compression set over time — re-torque check at the planned 3-month and 12-month intervals.
- **Fan from the start:** 60 mm 12 V automotive case fan ducted at one face of the frame, wired off the DSP REM line so it only runs when the audio system is on. The cubby's commissioning thermal gate (`work/center_console_refresh/README.md` §6.5b) targets ≤50 °C ambient at sustained load — a fan from the start removes ambiguity and is a €5–10 line item.

**Why not the alternatives** (rejected during 2026-05-07 design discussion):

- 3D-printed PETG modular trays: viable but PETG glass-transition is ~70 °C; in a car cubby in Finnish summer with 25 W of heat, the safety margin is too thin. Aluminum has no thermal limit at relevant temperatures.
- Aluminum sheet base plate + standoffs: less flexible than profile-and-cassette; harder to fabricate without proper metalworking tools.
- Plywood / MDF: flammable in a confined space with heat sources, and adds ~1 kg of mass that doesn't help anything.
- Single tray (everything bolted to one plate): no separation between subsystems → service access requires removing the whole stack.

## Cubby Geometry (TO MEASURE)

Three open dimensions remain pending from the April 27 evening diary entry — must be tape-measured at the next car visit before the rack frame can be cut:

| # | Dimension | Why |
| :--- | :--- | :--- |
| D1 | Cubby interior W × D × H above the trim panel | Sets the maximum frame envelope. |
| D2 | Bottom welded-stud → cubby-edge distance (passenger-side ground stud) | Sets the cable-entry side of the frame and where the DSP power-and-ground bundle exits. |
| D3 | Trim panel underside profile (does it sit clear of the frame top, or does it need a relief notch?) | Sets the maximum frame height; determines whether the trim panel can close over the rack or needs a relief cut. |

**Working assumption** (to be confirmed): cubby is approximately 350 mm W × 300 mm D × 160 mm H (≈17 L), tapered following the wheel-well on the outboard side. Frame target: 320 W × 270 D × 140 H mm (a few cm of clearance on each side for friction-fit pads and trim closure).

## Frame Design

### Profile selection

| Spec | Choice | Rationale |
| :--- | :--- | :--- |
| Profile | **20 × 20 mm T-slot aluminum extrusion** | Adequate stiffness for ~5 kg of load + vibration. M5 T-nut interface, widely available (Ali Express, 3D printer suppliers, Misumi). Smaller and lighter than 30 × 30 mm. |
| Total length needed | ~2.5 m (4 verticals + 4 long-edge horizontals + 4 short-edge horizontals with margin) | Order one 3 m stick + spare for cassette mounting rails. |
| Corner brackets | M5 90° corner brackets, 8 pieces | Connects 12 frame edges (cube needs 8 corners; 2 brackets per corner is overkill, 1 per corner with proper T-nut tightening is fine). |
| T-slot nuts | M5, ~30 pieces | 4 per cassette × 5 cassettes = 20, plus 8 for corner brackets, plus margin. |

### Friction-fit clamping interface

The frame is held in the cubby by **expansion clamps at the ends of the vertical profiles**, not by holes drilled into the cubby:

```
   ┌──────────────────────────────┐  ← cubby ceiling (trim panel underside)
   │                              │
   │ ╔══════════════════════════╗ │  ← frame top horizontal (with rubber pad on top)
   │ ║                          ║ │
   │ ║ [DSP cassette]           ║ │
   │ ║                          ║ │
   │ ║ [Pi cassette]            ║ │
   │ ║                          ║ │
   │ ║ [nRF cassette]           ║ │
   │ ║                          ║ │
   │ ║ [charger cassette]       ║ │
   │ ║                          ║ │
   │ ╚══════════════════════════╝ │  ← frame bottom (with rubber pad below)
   │                              │
   └──────────────────────────────┘  ← cubby floor
```

Mechanism:
- Each vertical profile has a **rubber pad** at top and bottom (high-density EPDM or neoprene foam, ~5 mm compressed thickness when loaded).
- An **adjustment bolt** at the top end of each vertical pushes against an expansion plate, which forces the rubber pad firmly into the cubby ceiling and floor.
- Tightening the bolt → frame is locked vertically by friction; loosening → frame lifts out cleanly.
- Same principle as a tension rod / shower curtain rod, scaled up.

A cheaper alternative if the expansion-bolt design proves fiddly: **threaded leveling feet** with rubber pads on the bottom of the verticals, screwed up against the cubby ceiling. Same concept, simpler hardware.

### Fan integration

- 60 mm 12 V brushless case fan (e.g. Noctua NF-A6x25 5V if 5 V better suits a 12 V → 5 V buck branch from the DSP REM line, or a generic Arctic F6 12 V if direct 12 V).
- Mounted to the **rear face of the frame** (the face that points away from the cabin opening), drawing air OUT of the rack envelope. Air enters from the cabin-facing face naturally through the open frame structure.
- Wired to **DSP REM line** (terminal-block tap), so it only runs when the DSP is on. Avoids permanent fan whine / parasitic drain.
- Optional ducting: a small piece of foam or 3D-printed PETG ducting from the fan to a small vent slot in the cubby trim panel. If the cubby is fully sealed, the fan stagnates the air rather than evacuating it; if there's any natural exit path (gaps in the trim, a rear vent), the fan works as designed.

## Cassette Design

Each cassette is a small flat base plate with the subsystem mounted to it via standoffs. Cassettes have a uniform mounting interface to the frame: **4 corner holes for M5 T-nut bolts**, slot-loaded into the frame's T-slots and tightened.

| Cassette | Base plate | Component mounting | Notes |
| :--- | :--- | :--- | :--- |
| **DSP** | 3 mm aluminum sheet, 180 × 80 mm | 4 × M4 wood screws into existing DSP base-plate provisions OR rubber-isolated grommets through the DSP's mounting flanges | Already partially mounted today — re-mount onto cassette during rack install |
| **Pi5** | 3 mm aluminum sheet OR 8 mm plywood, 100 × 80 mm | 4 × M2.5 brass standoffs to Pi mounting holes; NVMe HAT stacks above | Cassette is the heat path for Pi if aluminum — bonus passive cooling. Leave 25 mm clearance above Pi for HAT + 40-pin GPIO header access. |
| **nRF54L15** | 8 mm plywood OR 3 mm acrylic, 100 × 60 mm | Veroboard mounted via M3 nylon standoffs (electrically isolated from the cassette) | Pluggable screw terminals on one edge for vehicle-side wiring. BLE antenna requires ~15 mm clear space — orient cassette so antenna faces an aluminum-profile-free direction (toward the cubby opening). |
| **85 W charger** | 8 mm plywood, 80 × 60 mm | Female cigarette-lighter panel-mount socket through the cassette (charger plugs into it normally; charger removable for swap) | The lighter socket is the friend: it lets the charger be swapped without rewiring. Socket positive → IRF4905 high-side MOSFET drain (always-on rail, gated). |
| **Future nRF93M1** | TBD | TBD | Reserved frame slot, ~100 × 60 mm. SMA pigtail to antenna routes through cubby trim or via the rear-bulkhead fish-string (per `work/center_console_refresh/README.md` §5.7c). |

**Each cassette is independently removable**: unscrew 4 M5 bolts, slide out, redo the wiring at the connector level. No part of the rack is co-dependent on another cassette being present.

## Cable Management

Cabling is the secret killer of any rack install. Approach: **separate bundles by signal class**, **service loops at every cassette**, **strain relief at every entry/exit**.

### Bundles (color-coded with tape or cable ties)

| Bundle | Carries | Color tag | Routing |
| :--- | :--- | :--- | :--- |
| **A** Power high-current | 8 mm² CCA red (battery +12 V from AGU), 8 mm² CCA black (ground to factory stud), DSP REM jumper (currently +12 V) | **RED tape** | Enters cubby from outboard side, terminates at DSP +12 V terminal block. Wago `221-413` tap on the DSP +12 V terminal branches to: (a) cabin-node always-on buck, (b) IRF4905 MOSFET source, (c) lighter socket positive. |
| **B** Power low-current branches | 1.5 mm² red branches from the Wago tap to charger / nRF buck / aux 12 V outlet | **YELLOW tape** | Internal to the rack; strain-relief at the Wago and at each cassette terminal. |
| **C** Audio signal | BE2210 high-level CAT6 (already in cubby), DSP speaker outputs (4 × 2.5 mm² to fronts/sub) | **WHITE tape** | Enters cubby from inboard side (separate entry from Bundle A to avoid power-induced noise). DSP speaker outputs route through cassette-to-cassette spaces directly to vehicle-side. |
| **D** USB / data | Pi → MEC HD-USB (audio sink), Pi → nRF54L15 (USB-CDC), Pi → Carlinkit dongle, Pi → display USB-A | **BLUE tape** | Internal to the rack between Pi cassette and DSP / nRF cassettes. The Pi → DSP USB cable is the ~10 cm in-cubby pull that the May 1 bench test proved out. |
| **E** Antenna / RF | nRF54L15 BLE antenna (PCB-trace antenna on the carrier, no cable), future nRF93M1 SMA cellular antenna pigtail | **GREEN tape** | nRF BLE: clear-space requirement only, no cable. Future cellular: SMA pigtail from cassette to cubby exit, then to antenna location TBD. |
| **F** Display + HDMI (front-cubby pulls already done) | C16 HDMI to display, C17 USB to display touch | **PURPLE tape** | Already pulled May 4; terminates at Pi cassette in the rear cubby. |

### Service loops

Each cassette gets ~10 cm of slack on every cable entering it — enough to remove the cassette from the frame and lay it on the cubby floor for service without disconnecting wires. This costs ~1 L of cable volume in aggregate but pays for itself the first time something needs to be reseated.

### Strain relief

- **At cubby entry:** rubber grommet through the trim panel cutout (cabin-side and outboard-side entries have separate grommets to keep Bundle A separated from Bundle C).
- **At each cassette terminal:** zip-tie or 3D-printed cable clamp anchoring the bundle to the cassette before the conductors land in the screw terminal. Stops vibration from working the terminal joint loose over years.
- **At the Wago `221-413` tap:** the 8 mm² CCA enters the Wago straight; the 1.5 mm² branches exit the Wago at 90° and are strain-relieved against an aluminum profile cross-piece.

## Bring-up Sequence

The rack is the **integration vehicle** for two pending engineering tasks (DSP-as-Pi-soundcard, nRF54L15-Pi-wake) plus the rack itself. Order matters — do the bench-built work first so there are no in-cubby debugging sessions on a hot day with the door trim hanging off.

### Stage 1 — Cubby measurement (≤30 min, on the car)

1. Open passenger-side rear cubby trim. Inspect for any factory mount points (none expected, but worth confirming).
2. Tape-measure D1 / D2 / D3 per §"Cubby Geometry" above.
3. Photograph the cubby interior with a ruler in frame for later reference.
4. Update this README §"Cubby Geometry" with the measured values; the working assumption above gets replaced.

### Stage 2 — nRF54L15 hardware build (workbench, ~4–6 h spread over a weekend)

This is the biggest unbuilt piece. Per `work/cabin_signal_node/README.md`:

- **Stage 6 (always-on power section):** Recom R-78E3.3-0.5 buck + ATO 1 A fuse + Wago `221-413` + reverse-polarity Schottky + TVS. Mount on Veroboard.
- **Stage 6b (12 V high-side MOSFET):** IRF4905 (or IPP80P03P4L) P-channel logic-level FET + gate driver + 470 µF input bulk cap + optional NTC inrush limiter + INA226 current-sense. Sized for 10 A continuous / 15 A peak.
- **BLE proximity firmware:** RSSI hysteresis, bonded-phone scanning, heartbeat over USB-CDC. Reuses engine-bay node firmware skeleton.
- **Bench-verify with a 12 V supply + 70 W resistive load** before the rack is ever assembled. Stage 6 success criterion (per cabin_signal_node README): phone-approach turns on the load; phone-leave turns it off after the grace period.

Stage 2 happens **independently of the rack** — pure bench work on the workbench. Output is a functioning Veroboard ready to be bolted to its cassette.

### Stage 3 — Frame fabrication (workbench, ~3 h)

1. Order 3 m × 20 × 20 mm aluminum extrusion + corner brackets + T-nuts + rubber pads + leveling feet (BOM below, ~€50 for everything).
2. Cut to the lengths derived from the Stage-1 measurements.
3. Assemble the frame on the workbench. Test fit cassette base plates (mocked up in cardboard if the actual cassettes aren't built yet).
4. Test-fit the empty frame in the cubby — adjust rubber pads / leveling feet until the frame is rigid in the cubby with no rattle.

### Stage 4 — Cassette fabrication (workbench, ~2 h)

1. Cut cassette base plates to size (table saw or jigsaw for plywood; tin snips or dremel for aluminum).
2. Drill standoff mounting holes per cassette spec table above.
3. Mount components to cassettes: DSP, Pi5 + NVMe HAT, nRF54L15 Veroboard, charger socket.
4. Cable each cassette internally — every cassette has its own pigtail to a labeled connector at the cassette edge.

### Stage 5 — Pre-install bench test (workbench, ~1 h)

1. Assemble the full rack on the workbench: frame + all cassettes + all bundles.
2. Power up from a bench supply at 12.5 V. Verify:
   - DSP comes up (Auto Remote OFF + REM-to-+12 V jumper, per the May 7 in-car install).
   - Pi5 boots from NVMe.
   - nRF54L15 enumerates as USB-CDC on the Pi (cabin_signal_node Stage 1 heartbeat visible in `dmesg` and the Python decoder).
   - **DSP-as-Pi-soundcard test**: connect Pi USB-A → MEC HD-USB cable, configure PipeWire default sink to `HD-AUDIO USB-INTERFACE FS`, play audio from the Pi, verify it comes out the DSP. (See §"DSP6-as-RPi5-Soundcard" below for full procedure.)
   - **Pi-wake test**: with phone bonded, walk away → IRF4905 turns off → 85 W charger drops out → Pi loses USB-C power → Pi shuts down. Walk back → MOSFET on → charger up → Pi boots. (See §"nRF54L15 Pi-Wake Control" below for full procedure.)
   - Fan spins when the DSP is on, stops when REM goes low.
3. Run the bench test for 30 min sustained → measure rack ambient temp at three points (top of DSP, between Pi and charger, at the fan exit) → sanity-check the thermal model.

### Stage 6 — In-car install (1–2 h)

1. Disconnect the DSP from its current direct-floor mounting (4 M4 wood screws into the cubby floor).
2. Mount the DSP onto its cassette; reconnect to the existing CCA power + ground + speaker outputs + REM jumper + BE2210 high-level tap.
3. Friction-fit the frame into the cubby per Stage-1 measured geometry. Tighten leveling feet / expansion bolts until the frame is locked solid.
4. Slide the remaining cassettes into the frame (Pi, nRF, charger).
5. Re-route the bundles per §"Cable Management" above — Bundle A (power) on one side, Bundle C (audio signal) on the other, Bundle D (USB) inside the rack envelope.
6. Power up; smoke-test repeats Stage 5 verifications in-car.

### Stage 7 — Commissioning gate (30+ min sustained run, observe)

Per `work/center_console_refresh/README.md` §6.5b:

- Run the system at sustained moderate load for 30+ min (Pi at typical load, DSP at moderate volume, fan running).
- Measure rack ambient temperature with a thermocouple or IR thermometer.
- **Pass criterion: ≤50 °C ambient** at any point in the rack envelope.
- If >50 °C: investigate ducting / venting / cubby trim airflow. Worst-case mitigation is a vent slot in the cubby trim panel + a passive cabin-air intake — straightforward to retrofit.

### Stage 8 — Trim close + service-loop verification (15 min)

1. Reinstall the cubby trim panel (relief notched if D3 measurement requires it).
2. Verify cassette removability: unscrew 4 bolts on any cassette, slide it out, lay it on the cubby floor on its service loop. Confirm everything stays connected and powered.
3. Final smoke test with the trim closed.

## DSP6 as RPi5 Soundcard (Integration Detail)

This is the audio path enabling CarPlay through the new DSP + speaker system.

### Hardware

- **Cable:** 1 × USB 2.0 A-to-B, ~30 cm (already on hand per `docs/diary/2026-05.md` May 2 evening shopping list, item #6).
- **Routing:** Pi USB-A port → MEC HD-USB module port (full-size USB-B, the "thicker pre-micro-USB connector" — the one that's confirmed correct on the MEC module).
- **Length:** ~10 cm in the cubby is enough; the slack in the 30 cm cable goes into the Pi cassette service loop.

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

- **nRF54L15 carrier (Veroboard, built in Stage 2 above):** lives on its cassette. Always-on, drawing ≤200 µA from the post-AGU CCA rail via the local Wago tap → 1 A fuse → Recom buck.
- **IRF4905 high-side MOSFET:** also on the cabin node Veroboard. Source = post-AGU 12 V (Wago tap branch); drain = 12 V input of the 85 W charger (via the female cigarette-lighter socket on the charger cassette); gate driven by an nRF54L15 GPIO through a level-shifter.
- **85 W charger:** plugs into the lighter socket on its cassette. Its USB-C output → Pi USB-C input (directly powers the Pi). Other outputs (Qi pad, spare USB) are TBD by the user's eventual cabin-charger placement decision.

### Software

On the nRF54L15 (Zephyr / Nordic SDK firmware in `FW_nrf/`):

1. **BLE proximity scanner**: scans for the bonded phone's BLE advertisement, computes RSSI with hysteresis (e.g. enter at −70 dBm, exit at −85 dBm) to prevent flapping.
2. **GPIO output**: drives the IRF4905 gate. HIGH = MOSFET conducting = charger powered = Pi gets 5 V on USB-C = Pi boots.
3. **USB-CDC frame to Pi**: sends a `R129_TYPE_PRESENCE` frame at 1 Hz with the current proximity state, so the Pi can react in software (e.g. preload UI screens, start key services).
4. **Graceful-shutdown handshake** (Stage 6/7 of cabin_signal_node):
   - Phone leaves range → nRF detects the RSSI exit transition.
   - nRF sends `R129_TYPE_SHUTDOWN_REQUEST` USB-CDC frame to Pi.
   - Pi runs `systemctl poweroff` (or a pre-shutdown hook that flushes state, dims display, etc.).
   - Pi acknowledges with `R129_TYPE_SHUTDOWN_ACK` USB-CDC frame.
   - nRF starts a 60-second grace-period timer.
   - On grace expiration (or sooner if Pi acknowledges fully off), nRF deasserts MOSFET gate → charger off → Pi loses power.
5. **KL15 override**: if the engine is running (KL15 high), the cabin domain stays on regardless of phone state. KL15 sense is currently jumpered from the BE2210 ACC line in the rear cubby; the permanent KL15 sense moves to the deferred front-half cabin acquisition board when that board exists.

### Key safety detail

Until the graceful-shutdown handshake firmware is fully working, the Pi can be killed mid-write by an over-aggressive nRF cutting power. Mitigation:

- Pi root filesystem on NVMe with `commit=1` mount option for ext4 (writes flush every 1 s, not every 5 s default).
- nRF firmware initially uses a generous 5-minute grace timer; tighten to 60 s only after the handshake is proven.
- Pi runs a `pre-shutdown` script that calls `sync` before triggering `systemctl poweroff`.

## Bill of Materials (Rack-Specific)

Items unique to the rack itself. The DSP / Pi / nRF / charger BOMs live in their respective subsystem READMEs.

| # | Component | Spec | Qty | Source | Cost (€) | Status |
| :--- | :--- | :--- | :--- | :--- | ---: | :--- |
| R1 | Aluminum T-slot extrusion | 20 × 20 mm, M5 T-slot | 3 m + 1 m spare | Ali Express / 3DJake / Misumi | ~15 | Pending order |
| R2 | M5 90° corner brackets | For 20 × 20 mm extrusion, with screws | 8 | Same | ~8 | Pending order |
| R3 | M5 T-slot nuts | For 20 × 20 mm extrusion | ~30 | Same | ~6 | Pending order |
| R4 | M5 socket-head bolts | 12 mm length | ~30 | Local hardware (Motonet/Biltema) | ~5 | Pending |
| R5 | Rubber pad / EPDM foam | 5 mm thick, ~20 × 20 mm pieces | 8 | Local hardware | ~5 | Pending |
| R6 | Adjustable leveling feet OR expansion bolts | M6 thread, ~25 mm length, with rubber tip | 4 | Local hardware | ~10 | Pending |
| R7 | 60 mm 12 V brushless case fan | Arctic F6 12V or equivalent, ~0.1 A draw | 1 | Local hardware / Verkkokauppa | ~10 | Pending |
| R8 | Cassette base plates | 3 mm aluminum sheet (for DSP, Pi) + 8 mm plywood (for nRF, charger), cut to size | 5 | Bauhaus offcut bin / inventory | ~10 | Pending |
| R9 | M2.5 / M3 / M4 brass standoffs + screws | Mixed lengths (8/12/16 mm) | assorted | Inventory or assortment kit | ~5 | Inventory check |
| R10 | Female cigarette-lighter panel-mount socket | Standard 12 V auto socket, with mounting collar | 1 | Local hardware / Biltema | ~5 | Pending |
| R11 | Cable ties + heat shrink + colored tape | Bundle separation | assorted | Inventory | ~3 | Inventory check |
| R12 | Rubber cable grommets | For cubby trim cutouts | 2 | Local hardware | ~3 | Pending |
| | **Subtotal (rack-specific)** | | | | **~85** | |

Plus the existing in-flight items (cabin-node Veroboard parts, fuse holders, Wago lever-nuts, etc.) are already accounted for in `work/cabin_signal_node/README.md` BOM and `docs/parts_to_order.md`.

## Open Questions / Decisions Pending

- **Profile size 20 × 20 vs 30 × 30:** 20 × 20 is the working spec. If the cubby measurements come back tighter than expected, may need to step down to 15 × 15 (less stiff but available). If volume is generous and stiffness of 20 × 20 feels marginal, step up to 30 × 30 (heavier, more expensive).
- **Charger placement strategy:** plug-in via panel-mount lighter socket (current plan, easy swap) vs. hardwired (saves ~5 cm of cassette depth, voids any warranty on the charger). Working assumption: lighter socket. Revisit if cassette depth becomes a constraint.
- **Fan duty cycle / control:** simple on/off via DSP REM (current plan) vs. PWM-controlled by the nRF54L15 based on temperature (more complex, allows quieter idle running). Working assumption: on/off. PWM is a software-only retrofit later if fan whine bothers anyone.
- **Future nRF93M1 cassette location:** reserved slot in the rack, but the antenna-pigtail run is non-trivial. The fish-string from the rear cubby through the rear bulkhead into the trunk (per `work/center_console_refresh/README.md` §5.7c, pulled May 3) is the irreversible step that buys optionality. Decide cassette / antenna location when the modem actually arrives.
- **NVMe access during install:** the Pi5 NVMe slot is on the underside of the Pi board; with the Pi mounted to a cassette via standoffs, the NVMe is captive between the Pi PCB and the cassette plate. **Decision: route the cassette plate so the NVMe slot is accessible from the cabin-facing side** — that way an NVMe swap doesn't require removing the cassette from the rack. (Alternative: put the Pi in a HAT-style enclosure that has an NVMe access window.)

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
| 2026-05-07 | Doc created | This file. Captures aluminum-profile / modular-cassette / friction-fit-mount / fan-from-the-start decisions made on 2026-05-07 evening. Cubby measurements pending; no fabrication has started. |
