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
- iPhone personal hotspot
- a cellular node based on `nRF9160`

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

### Current display plan
Use the original official `7"` Raspberry Pi Touch Display as the local driver display.

### Important hardware note
The original official Touch Display supports:
- `DSI` for display/touch data
- either `GPIO` power from the Raspberry Pi or separate `micro USB` power to the display controller board

This matters because the `M.2 HAT+` makes GPIO/header access more awkward. For this hardware combination, separate `micro USB` power to the display may be the cleanest integration path.

### Current design assumption
- Treat the original display's documented `micro USB` power option as a valid baseline design choice.
- If `micro USB` power is used, do not also connect display power over GPIO.
- In that mode, the only connection between Pi and display should be the `DSI` ribbon.
- Prefer separate display power over awkward GPIO power wiring if it simplifies the `Pi 5 + M.2 HAT+` mechanical stack.

### Integration consequence
Display integration should be treated as a dedicated hardware/software step after the core boot and UI startup path is stable.

### Safety and integration note
If the display is powered by `micro USB`:
- do not connect the display's GPIO power wires to the Pi at the same time
- keep the Pi and the display on their intended power inputs
- use the `DSI` cable only for the Pi-to-display connection

## Data Flow

### Primary path
`Diagnostics module -> Pi local interface -> local service/process -> UI`

### Secondary path
`Optional network interface -> background services -> non-critical features`

### Design consequence
The UI should degrade gracefully:
- if diagnostics are unavailable, show "connecting" or last known state
- if networking is unavailable, show no error that blocks normal use

## Software Architecture Direction

### Recommended logical layers

#### 1. Acquisition layer
Responsible for talking to the diagnostics module and normalizing incoming data.

#### 2. State/cache layer
Maintains the current local vehicle/application state so the UI can render quickly and survive transient disconnects.

#### 3. UI layer
The full-screen driver-facing application. This should be able to launch independently of optional services.

#### 4. Background integration layer
Handles optional networking, sync, logging upload, or future remote capabilities.

## Boot Mode Direction

### Near-term
Keep using Raspberry Pi OS as installed, but reduce unnecessary startup overhead and auto-launch the UI.

### Medium-term
Consider whether the final system should:
- keep a lightweight desktop session and launch a full-screen app, or
- run an even more direct kiosk/appliance path with fewer desktop dependencies

The correct choice should be driven by:
- display/touch support quality
- boot time
- reliability
- PySide6/graphics behavior on the target screen

## Networking Policy

### Mandatory requirement
Networking must be optional at boot.

### Hotspot policy
If an iPhone hotspot is used later:
- it should connect when available
- it must never delay UI startup
- failure to connect must remain silent or low-priority

### Cellular policy
If an `nRF9160` is added later:
- treat it as a secondary communications module
- keep its startup independent from the driver UI path
- use it for enrichment, upload, remote diagnostics, or telemetry only after core local functionality is stable

## Immediate Design Priorities
1. Remove or defer startup services that do not contribute to the initial driver UI.
2. Decide the final UI launch method under `systemd`.
3. Integrate the original `7"` Touch Display cleanly with the Pi 5 and `M.2 HAT+`, likely using separate `micro USB` display power and `DSI` only between boards.
4. Define the local interface contract between the diagnostics module and the Pi UI.
5. Establish the first minimal UI screen set.

## Open Questions
- What exact transport will the diagnostics module use to talk to the Pi?
- Is the first production UI portrait or landscape on the `7"` display?
- Will the first UI run on top of a desktop session or as a more direct kiosk target?
- Which services from the stock Raspberry Pi OS image can be removed safely for this project?
- How should the original `7"` display and its separate power lead be mounted mechanically together with the `M.2 HAT+`?

## Next Document Candidates
- UI boot optimization plan
- original Touch Display integration notes
- diagnostics-to-UI interface contract
- driver screen information architecture
