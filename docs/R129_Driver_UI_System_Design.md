# R129 Driver UI System Design

## Objective
Define the system design for the Raspberry Pi 5 based driver-facing UI in the `R129`, with emphasis on:

- fast boot to a usable display
- offline-first operation
- reliable local diagnostics display
- optional connectivity that never blocks the core UI

This document begins where the bring-up work ends. Hardware bring-up, NVMe migration, and initial OS setup are tracked separately in `RPi5_Bring-up_Plan.md`.

## System Role
The Raspberry Pi 5 is the in-car presentation and orchestration node. Its primary job is to show useful information from the diagnostics/vehicle interface module to the driver as quickly and reliably as possible after power-on.

The Pi is **not** primarily a network appliance. Network connectivity is optional and secondary.

## Core Design Principles

### 1. UI first
The screen should become useful before the car is driven. Anything not required for local display must not delay the first visible UI state.

### 2. Offline first
The system must boot and operate correctly with no Internet connection, no hotspot, and no external services available.

### 3. Connectivity is opportunistic
Future network paths such as:
- iPhone personal hotspot (opportunistic WiFi tethering)
- **nRF93 Cat-1bis cellular module** via USB (planned, replaces earlier nRF9160 reference)

are useful additions, but they must be treated as background capabilities. Failure or delay in these paths must never prevent the UI from starting.

### 4. Local diagnostics are the main data source
The first meaningful feature is local display of data provided by the diagnostics module. External networking is explicitly lower priority than the local vehicle data path.

### 5. Deterministic startup beats feature richness
For automotive-style use, a simpler and more predictable startup path is better than a richer desktop-like environment that starts slowly or inconsistently.

## Intended Operating Model

### Boot path
1. Pi powers on.
2. OS reaches a minimal ready state.
3. UI application starts automatically.
4. UI shows a useful initial screen immediately, even if live diagnostics data is not yet available.
5. Background services continue initializing after the UI is already visible.

### Runtime path
1. Diagnostics module connects and starts providing local data.
2. UI updates live views from local data.
3. Optional networking comes up later if available.
4. Remote sync, updates, telemetry, or cloud-style features remain non-critical.

## Startup Targets

### Functional target
The driver should see a responsive UI quickly enough that the system feels appliance-like rather than computer-like.

### Engineering target
- Short-term target: reach a visible UI in about `10-15s`
- Long-term target: push below `10s` if practical

### Current baseline
Observed after NVMe boot and package updates:
- `systemd-analyze`: `10.925s`
- kernel: `1.301s`
- userspace: `9.624s`
- `graphical.target`: `9.471s`

This is already a workable baseline, but too much of the path is currently consumed by services that are not required for the driver UI.

## Startup Policy

### Services that must not block UI startup
- waiting for Wi-Fi readiness
- waiting for Internet connectivity
- hotspot discovery
- cellular network setup
- remote update checks
- cloud sync
- Bluetooth accessory discovery unless explicitly required for a user-facing feature

### Services likely worth reducing or disabling
Based on current boot timing, the following deserve review first:
- `NetworkManager-wait-online.service`
- `cloud-init-*`
- `cups-browsed.service`
- `ModemManager.service`
- desktop-oriented background services not needed by the final UI appliance

### Service design rule
If a service is not required to paint the first useful UI screen, it should start after the UI or be disabled entirely.

## Display Strategy

### Current display
Waveshare `5.5"` AMOLED capacitive touchscreen (USB ID `0712:000a`).

- **Native resolution:** `1080x1920` (portrait)
- **Operating resolution:** `1920x1080` (landscape via `transform 90`)
- **Display interface:** HDMI (micro-HDMI on Pi side, full HDMI on display side)
- **Touch interface:** USB HID multitouch (10-point), micro-USB on display to USB-A on Pi
- **Power:** Supplied through the touch USB cable — no separate power cable needed
- **Audio:** 3.5mm headphone jack on display (labeled "HP"), unused
- **EDID:** Reports as `HLT WaveShsare`

### Cabling (2 cables total)
1. **HDMI:** Pi 5 HDMI-0 (micro-HDMI, port closest to USB-C power) → display HDMI input
2. **Touch/Power USB:** Display touch micro-USB → Pi 5 USB-A port

The display's dedicated "power" micro-USB port is not needed — the touch USB carries enough current for the AMOLED panel.

### In-car installation cabling
The display ships with 180° U-turn adapter connectors for both HDMI and micro-USB. These redirect the cables straight behind the display instead of exiting sideways, minimizing depth for flush panel mounting. Combined with flat FPC cables (micro-HDMI to HDMI flat ribbon + flat micro-USB), the entire assembly can be very thin:

- **Display-side:** 180° adapters on HDMI and touch micro-USB → cables exit rearward
- **Cables:** Flat FPC HDMI (micro-HDMI Type D → HDMI Type A) + flat micro-USB
- **Pi-side:** Standard micro-HDMI and USB-A ports

### Display rotation (persistent)
Rotation is handled by `kanshi` (auto-started by labwc on RPi OS):

`~/.config/kanshi/config`:
```
profile {
    output HDMI-A-1 mode 1080x1920 position 0,0 transform 90
}
```

Touch coordinate mapping is handled automatically by the `autotouch` package (pre-installed on RPi OS with labwc).

### Hardware notes
- The display ships with **two** protective films. The inner film is non-conductive and blocks capacitive touch — it must be removed for touch to work.
- The display can also accept separate power via a second micro-USB port, but this is redundant when the touch USB is connected to the Pi.

## Data Flow

### Primary paths (two local sources)
The Pi has **two independent local data sources** plus the trunk monitor:

1. **Engine-bay node over BLE** — under-hood-only signals (`X11` blink codes, `EHA` current, airflow potentiometer, lambda integrator, engine-side `ECT`). See `docs/nRF5430_Interface_Design.md` and `docs/PH2_2_architecture.md`.
2. **Cabin signal node over USB-CDC** — cabin-side signals (cluster gauge senders, `VSS`, `TD` at cluster, brake / kickdown / reverse / hand-brake, `KL15`/`KL30`/`KL58`, console rocker switches, door / hood / trunk ajar, cabin ambient sensors `BME280` / IMU / `TSL2591`). See `docs/cabin_signal_survey.md` and `work/cabin_signal_node/README.md`.
3. **Trunk battery monitor** — `INA226` + `DS18B20` directly on the Pi I²C / 1-Wire buses (`work/battery_monitor/README.md`).

`Diagnostics modules (BLE + USB) -> Pi local interfaces -> acquisition layer -> vehicle_state.py -> UI`

Both BLE and USB-CDC frames use the same `FW_nrf/payload/r129_payload.h` wire format (`SYNC + LEN + TYPE + DATA + CRC16`). The cabin node uses a new `R129_TYPE_CABIN = 0x04` payload type alongside the existing engine-node types.

### Secondary path
`Optional network interface -> background services -> non-critical features`

### Design consequence
The UI should degrade gracefully:
- if either diagnostics source is unavailable, show "connecting" or last known state for the affected signal group; the other source continues to feed its signals to the UI
- if networking is unavailable, show no error that blocks normal use
- the cabin USB-CDC source must tolerate Pi reboots cleanly (re-enumerate on boot, no firmware corruption on power cycle)

## Tech Stack (Decided 2026-04-03)

**Python 3.13 + PyQt5 (Qt 5.15.15)** on Raspberry Pi OS with labwc (Wayland).

### Why PyQt5
Benchmarked on the actual RPi5 hardware (2026-04-03):
- **PyQt5 first frame: 136ms** (fastest of all tested options)
- pygame first frame: 371ms
- PySide6: not available in system packages
- Electron/Chromium: estimated 3-8s (disqualified on boot time)
- C++ Qt/QML: estimated ~80-120ms (marginal gain, much harder to develop)

PyQt5 combines the fastest startup with full widget toolkit (QPainter for custom gauge rendering, QWidgets for settings/menus, signals/slots for data binding).

### CarPlay integration path
Apple CarPlay requires MFi hardware authentication (cannot be implemented in software alone). The planned approach uses a **Carlinkit CPC200-CCPA** USB dongle that handles MFi auth and outputs an H.264 video stream and PCM audio over USB. Touch events are forwarded back to the dongle over USB.

#### Software: LIVI (Linux In-Vehicle Infotainment)
**[LIVI](https://github.com/f-io/LIVI)** (formerly `pi-carplay`) is the chosen CarPlay host software. It explicitly supports the CPC200-CCPA dongle on RPi5 with Pi OS Trixie.

Key capabilities:
- Hardware-accelerated video pipeline (H.264 decode)
- GStreamer audio backend (integrates with PipeWire → MEC HD-USB → Match UP 6DSP)
- Touchscreen and multi-touch support
- Audio metadata and playback state integration (feeds the Music view)
- iAP2 turn-by-turn navigation data (can overlay directions on the gauge view)
- Microphone input for Siri and phone calls
- Distributed as an AppImage with an automated RPi install script
- Actively maintained (v5.6.0+)

Alternative projects evaluated:
- `react-carplay` (Electron/React, 816 stars) — more community but rougher edges, heavier runtime
- `FastCarPlay` (C++, 87 stars) — lightest weight but fewest features, no wireless CarPlay confirmed

#### Wireless CarPlay (primary mode)
The CPC200-CCPA dongle supports both wired and wireless CarPlay. Wireless is the intended mode:
- The dongle creates a WiFi Direct link to the iPhone — CarPlay connects automatically when the driver is in the car
- The dongle stays permanently connected to the Pi via USB, hidden behind the dash
- No user-facing USB port or cable needed in the cabin
- First-time pairing may require a temporary wired connection; after that, reconnection is automatic

#### Physical installation
```
Behind dash (hidden):  Carlinkit dongle ──USB──→ RPi5 USB-A port
In driver's pocket:    iPhone ~~WiFi Direct~~→ Carlinkit dongle (automatic)
```

#### CarPlay display layout
CarPlay negotiates its viewport size with the host. The dongle output resolution is configurable. Two layout modes are planned:

**Full-screen mode:** CarPlay takes the entire 1920x1080 display. The gauge view is not visible. Activated by user gesture (e.g. swipe or touch target).

**Split-screen mode (preferred):** CarPlay runs in a sub-viewport while a persistent status bar shows critical vehicle data:
```
┌──────────────────────────────────────────────────────────┐
│  RPM: 2400  ·  85 km/h  ·  90°C  ·  ADS: COMFORT       │  ← PyQt5 status bar
├──────────────────────────────────────────────────────────┤
│                                                          │
│                   Apple CarPlay                          │  ← LIVI CarPlay viewport
│                 (navigation map)                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```
The CarPlay viewport resolution is set to match the available area (e.g. 1920x960 or similar). Touch events within the CarPlay region are mapped to the CarPlay coordinate space and forwarded to the dongle; touches on the status bar are handled by PyQt5.

### Source location
`UI_rpi5/src/` — deployed to `/home/pi/R129_UI/src/` on the Pi.

### Application files
- `main.py` — entry point, dotenv loader, platform-aware launch (fullscreen on RPi, windowed on desktop)
- `main_window.py` — fullscreen `QMainWindow`: sidebar + status bar + `QStackedWidget` with 8 pages
- `input_actions.py` — `InputAction` enum (UP, DOWN, LEFT, RIGHT, CW, CCW, PRESS, LONG_PRESS)
- `input_manager.py` — unified input from GPIO joystick/encoder (RPi5) and keyboard (desktop dev)
- `vehicle_state.py` — central `QObject` data model with `pyqtSignal` for live updates
- `sim_provider.py` — simulated data generator for development
- `view_manager.py` — 4-state navigation model (SIDEBAR → PAGE → MENU → PARAM_EDIT)
- `sidebar.py` — vertical sidebar with 9×9 dot-matrix pixel-art icons
- `status_bar.py` — compact top bar (clock, page name, warnings)
- `theme.py` — centralized colors, fonts, scaling, retro FX settings, map constants
- `dot_matrix.py` — 5×7 dot-matrix text renderer with glow bleed and flicker effects
- `home_view.py` — wireframe 3D car (Bresenham rasterized dot-matrix), touch pitch/yaw, vehicle info
- `r129_wireframe.py` — 3D vertex/edge data for the R129 wireframe model
- `classic_cluster_view.py` — R129 VDO-style instrument cluster reproduction
- `gauge_view.py` — modern 3-gauge + bars cluster with tapered needles and bezel rings
- `split_pane_view.py` — reusable 25/75 split-pane base class for menu views
- `settings_view.py` — settings page (display style, brightness, retro FX toggle)
- `diag_view.py` — diagnostics page (system fault codes, sensor readings)
- `map_view.py` — slippy-tile map renderer using CartoDB/OSM tiles (see Map section)
- `placeholder_view.py` — placeholder for unimplemented pages

### Map view (implemented 2026-04-06)
Interactive slippy-tile map renderer. **QWebEngineView was rejected** — Chromium's GPU compositor corrupts the Wayland surface on RPi5 + AMOLED (horizontal pixel stride mismatch, persists across page switches, not fixable with software rendering flags).

**Solution:** Custom tile renderer fetching 512×512 @2x PNG tiles from CartoDB dark basemap via `urllib` in background threads. LRU tile cache (256 tiles), 1-tile pre-fetch margin for smooth panning.

- **Tile layers:** Dark (CartoDB dark_all), Light (CartoDB light_all), OSM (openstreetmap.org). PRESS cycles layers.
- **Controls:** Joystick arrows pan, CW/CCW zoom (range 2–18). Touch drag-to-pan, scroll/wheel zoom. Recenter button (crosshair icon, bottom-right) appears when panned away from home.
- **GPS-ready:** `set_home(lat, lng)` method for future GPS integration. Default: Helsinki (60.17°N, 24.94°E).
- **No API key required** for CartoDB/OSM tiles.

## Software Architecture

### Logical layers

#### 1. Acquisition layer
Responsible for talking to **both** local diagnostics sources and normalizing incoming data into a single stream of Qt signals to the UI:

- **BLE** from the engine-bay node (`nRF54L15` / `nRF5340`) — under-hood-only signals.
- **USB-CDC** from the always-on cabin signal node (`nRF54L15`) — cabin-side signals + cabin ambient sensors + lock state, BLE proximity, and Pi power state.
- **I²C / 1-Wire** from the trunk battery monitor (`INA226` + `DS18B20`).

All three sources are independent — failure or disconnect of any one must not block the others. The BLE and USB sources share the `FW_nrf/payload/r129_payload.h` framing so a single decoder handles both.

#### 2. State/cache layer
Maintains the current local vehicle/application state so the UI can render quickly and survive transient disconnects.

#### 3. UI layer
Fullscreen PyQt5 application with stacked views:
- **Gauge view** — primary driving display (QPainter custom rendering)
- **Music view** — now-playing display with AVRCP metadata and touch controls, amber VDO style (future)
- **Diagnostics view** — fault codes, sensor readings (future)
- **Settings view** — configuration (future)
- **CarPlay view** — embedded H.264 video from CarPlay dongle (future)

#### 4. Background integration layer
Handles optional networking, sync, logging upload, or future remote capabilities.

## Audio Architecture

### Overview
The audio system combines the original Becker BE2210 head unit (cassette/radio) with a modern digital streaming path through the Match UP 6DSP. The BE2210 stays installed and functional for period-correct use; high-quality streaming audio is handled entirely by the RPi5 → DSP path.

### Audio paths

#### Path 1 — Bluetooth streaming (primary, best quality)
```
iPhone → Bluetooth A2DP (AAC) → RPi5 PipeWire → USB (UAC digital, lossless) → Match UP 6DSP → Speakers
```
- iPhone streams from any music service (YouTube Music, Apple Music, Spotify, podcasts, etc.)
- RPi5 acts as a Bluetooth A2DP audio sink
- PipeWire routes audio to the Match UP 6DSP via USB Audio Class (UAC) — fully digital, lossless
- DSP handles crossovers, time alignment, EQ, and amplification
- AVRCP metadata (track title, artist, album, position) sent alongside audio; displayed on the Pi in the Music view
- AVRCP controls (play/pause/skip/volume) sent from Pi touchscreen back to iPhone

#### Path 2 — CarPlay audio (wireless)
```
iPhone ~~WiFi Direct~~→ Carlinkit dongle → USB (PCM audio) → RPi5 PipeWire → USB (UAC) → Match UP 6DSP → Speakers
```
- Wireless CarPlay: iPhone connects to the dongle via WiFi Direct (automatic, no cable)
- When CarPlay is active, the iPhone stops sending Bluetooth A2DP audio and routes everything through CarPlay instead
- The CarPlay dongle delivers both H.264 video and PCM audio over USB to the Pi
- LIVI decodes both: video to its display surface, audio → GStreamer → PipeWire source
- PipeWire routes CarPlay audio to the same output sink (Match UP 6DSP)
- CarPlay audio includes music, navigation voice prompts, phone calls, and Siri
- The output side (Pi → USB → Match DSP) is identical to Path 1 — only the input source changes

#### Audio source switching
The iPhone controls which path is active. Bluetooth A2DP and CarPlay audio are mutually exclusive:
- **CarPlay disconnected/inactive:** iPhone → Bluetooth A2DP → Pi (Path 1)
- **CarPlay active:** iPhone → CarPlay dongle → Pi USB (Path 2)

PipeWire handles both sources and routes whichever is active to the Match UP 6DSP output sink. No manual switching needed.

#### Path 3 — Legacy (cassette/radio)
```
Becker BE2210 → car speaker wiring → speakers
```
- Cassette and FM/AM radio through the original head unit
- Independent of the Pi audio system — plays through the BE2210's own amplification
- The BE2210 has an aftermarket AUX input, usable as a backup analog path from the Pi (Waveshare 3.5mm HP jack → BE2210 AUX)

#### Path 4 — Backup analog (if needed)
```
RPi5 → HDMI audio → Waveshare 3.5mm HP jack → cable → BE2210 AUX input → speakers
```
- Analog fallback if the Match USB module is unavailable
- Lower quality than the USB-to-DSP path but functional

### Audio backend
- **PipeWire** + **WirePlumber** (running, verified 2026-04-03)
- No PulseAudio — PipeWire handles ALSA, Bluetooth, and USB audio natively
- When the Match UP 6DSP USB module is connected, it will appear as a standard ALSA/PipeWire audio sink
- Default sink priority: Match USB > HDMI-0 (Waveshare HP jack)
- PipeWire automatically routes whichever audio source is active (BT A2DP or CarPlay USB) to the default output sink

### Music view (planned)
A PyQt5 view in the stacked UI styled as a period-correct amber-on-black VDO display:
- Track title, artist, album from AVRCP metadata (read via D-Bus `org.bluez.MediaPlayer1`)
- Playback position bar
- Touch controls: previous / play-pause / next / volume (sent via AVRCP D-Bus commands)
- No web browser, no streaming service APIs, no authentication — works with any music app on the iPhone

### Match UP 6DSP USB integration
- The MEC HD-USB module (part M142045, €149) plugs into the UP 6DSP's MEC expansion slot
- Registers as a USB Audio Class (UAC1/UAC2) device — Linux kernel ALSA driver handles it natively, no proprietary drivers
- PipeWire automatically discovers and routes to the USB sink
- Full Speed mode (up to 96 kHz / 24-bit) works driverless on all platforms — more than sufficient for car audio
- Expected on `lsusb` as an Audiotec Fischer device; verify with `aplay -l` after connecting
- The UP 6DSP provides 6 amplified channels (4 × 65W @ 4Ω + 2 × 160W @ 2Ω) — exact fit for fully active 2-way front + DVC2 subwoofer with zero unused channels

## Boot Configuration

### Measured boot time (2026-04-03)
After disabling `NetworkManager-wait-online` and `cloud-init-*`:
- **Total: 5.3s** (1.6s kernel + 3.7s userspace)
- `graphical.target` reached at 3.7s
- UI service starts immediately after → **first frame at ~5.5s from power-on**

### Auto-start
The UI runs as a `systemd` user service (`r129-ui.service`) with `After=graphical.target`. User linger is enabled so the service starts at boot without requiring a login session.

Service file: `UI_rpi5/r129-ui.service` → deployed to `~/.config/systemd/user/r129-ui.service`

### Disabled services
- `NetworkManager-wait-online.service` (saved 6s)
- `cloud-init-main.service`, `cloud-init-local.service`, `cloud-init-network.service` (saved ~1s)

## Networking Policy

### Mandatory requirement
Networking must be optional at boot.

### Hotspot policy
If an iPhone hotspot is used later:
- it should connect when available
- it must never delay UI startup
- failure to connect must remain silent or low-priority

### Cellular policy — nRF93 Cat-1bis
The planned cellular module is a Nordic **nRF93 Cat-1bis** connected via USB. It replaces the earlier nRF9160 reference and is a better fit for this project:
- Connects as a standard USB network adapter (CDC-ECM/RNDIS) — no driver work on the Pi, NetworkManager picks it up natively
- Cat-1bis provides up to ~10 Mbps — more than enough for OTA updates, telemetry, and remote access
- Higher power consumption than nRF9160 is acceptable in a car environment (12V supply, not battery-constrained)
- Stays within the Nordic ecosystem alongside the nRF5340 diagnostics node
- Requires an external LTE antenna — antenna selection and routing must be resolved before committing to installation

**Planned use cases (all non-blocking, background-only):**
- OTA software updates without WiFi — push new UI builds to the car remotely
- Telemetry upload — continuous vehicle data logging (ADS, temperatures, fault codes) to a server
- Remote SSH — debug the Pi without physical access to the car
- Always-on remote channel — the cabin signal node (which owns BLE keyless lock/unlock and Pi wake) can also relay status over cellular for alert reporting independent of the owner's phone

**Design rules:**
- Cellular startup must be independent from the driver UI path
- Failure to connect must never block or delay any local functionality
- Use for enrichment, upload, and remote access only — core features work fully offline
- SIM card with a small data plan (~200-500 MB/month) is sufficient

**Status:** Planned. Antenna solution must be determined before hardware integration.

## Immediate Design Priorities
1. ~~Remove or defer startup services.~~ **DONE (2026-04-03).** 12.2s → 5.3s boot.
2. ~~Decide the final UI launch method under `systemd`.~~ **DONE (2026-04-03).** User service with linger.
3. ~~Integrate display.~~ **DONE (2026-04-03).** Waveshare 5.5" AMOLED via HDMI + USB.
4. Define the local interface contract between the diagnostics module (nRF5340 BLE) and the Pi UI.
5. ~~Establish the first minimal UI screen set.~~ **DONE (2026-04-03).** Gauge view with simulated data running.
6. ~~Build full 8-page application with input infrastructure.~~ **DONE (2026-04-06).** Joystick + touch, sidebar navigation, retro dot-matrix aesthetics, interactive map.

## Open Questions
- What exact BLE service/characteristic UUIDs will the engine-bay Nordic node expose?
- Cabin signal node USB-CDC: confirm `/dev/ttyACM*` enumeration is stable across Pi reboots, and that the cabin MCU survives Pi power cycles cleanly. See `work/cabin_signal_node/README.md` Stage 1 exit criteria.
- How should the Waveshare 5.5" AMOLED be mounted mechanically in the car?
- Should the desktop session (labwc) be kept or replaced with a minimal Wayland compositor for the kiosk path?
- nRF93 Cat-1bis antenna: internal PCB antenna vs. external antenna routed to the roof/rear window? Needs RF evaluation in the intended mounting location.

## Next Steps
- Define BLE data contract (engine-bay Nordic → Pi)
- Define USB-CDC data contract for the cabin signal node — recommended approach is to reuse `FW_nrf/payload/r129_payload.h` framing and add a `R129_TYPE_CABIN = 0x04` payload type, so a single decoder handles both transports. See `docs/cabin_signal_survey.md` §"Wire format" and `work/cabin_signal_node/README.md` §"Wire Format".
- Replace simulated gauge values with live BLE + USB-CDC data
- Configure Bluetooth A2DP sink and pair iPhone for music streaming
- Build Music view (AVRCP metadata display + touch controls)
- Populate diagnostics view with live data from X11 blink codes
- Order and integrate CarPlay USB dongle for navigation (Carlinkit CPC200-CCPA ordered 2026-04-03)
- Connect and verify Match UP 6DSP + MEC HD-USB (M142045) audio path
- Add GPS module for live map tracking (`set_home()` already wired in map view)
- Mechanical mounting design for in-car installation
