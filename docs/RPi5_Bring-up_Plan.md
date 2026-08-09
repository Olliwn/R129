# Raspberry Pi 5 Headless Bring-up Plan

## Objective
Set up the RPi5 for remote SSH operation from the Mac, entirely headless (no keyboard/mouse), and prepare the Git repository for the UI software.

## Current Verified State
- Hostname is `r129` and the Pi responds at `r129.local`.
- SSH access is working for `pi@r129.local`.
- The Pi now boots successfully from the NVMe M.2 drive with the USB stick removed.
- The attached NVMe M.2 drive is detected as `nvme0n1` (`931.5G`).
- The NVMe has now been partitioned, formatted, and cloned from the clean USB system.
- The cloned NVMe target has updated `fstab` and `cmdline.txt` pointing to the NVMe partition `PARTUUID`s.
- Verified root filesystem is `/dev/nvme0n1p2` and `/boot/firmware` is `/dev/nvme0n1p1`.
- Immediate next goal: measure and optimize boot time toward the `<15s` UI target.

## Step 1: OS Flashing and Headless Configuration
1. **Tool Needed**: Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your Mac.
2. **Select OS**: Choose **Raspberry Pi OS (64-bit)** (Lite is recommended if you only need the background UI app without desktop overhead, but full OS is fine if you plan to use PySide6/X11/Wayland directly).
3. **Advanced Options (The Gear Icon / Ctrl+Shift+X)**:
   - Sets hostname (e.g., `r129`).
   - Enable **SSH** (Use password authentication or provide your Mac's `~/.ssh/id_rsa.pub` key).
   - Configure **Wireless LAN**: Enter your local Wi-Fi SSID and password (make sure it's a 2.4GHz/5GHz network your Mac is also on).
   - Set username and password (e.g., `pi` / `mercedes`).
   - Set locale settings (Timezone: Europe/Helsinki, Keyboard: fi).
4. **Flash**: Write the image to the microSD card (or NVMe drive if you have the adapter ready).

## Step 2: First Boot and SSH Connection
1. Insert the flashed MicroSD/NVMe into the RPi5.
2. Apply USB-C power to the Pi.
3. Wait 1-2 minutes for the initial boot and Wi-Fi connection.
4. On your Mac terminal, ping the Pi to find it:
   ```bash
   ping r129.local
   ```
5. Connect via SSH:
   ```bash
   ssh pi@r129.local
   ```
   (Accept the ECDSA key prompt).

## Step 3: Initial Pi Configuration
Once logged in via SSH:
1. Update system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
2. Install necessary dependencies for UI development (PySide6, Git, etc.):
   ```bash
   sudo apt install git python3-pip python3-venv -y
   ```

## Step 4: Move Boot to the NVMe M.2 Drive
**Goal:** stop booting from the temporary USB stick and migrate to the internal NVMe drive for faster and more permanent operation.

### Preferred Path
Use a fresh Raspberry Pi OS 64-bit install on the NVMe with the same headless settings already proven to work:
- Hostname: `r129`
- SSH enabled
- Same Wi-Fi credentials
- Same username/password or SSH key setup

This keeps the system clean and avoids carrying over any temporary bring-up artifacts from the USB boot media.

### Verification Before Migration
From the running Pi:
```bash
lsblk -f
sudo fdisk -l /dev/nvme0n1
```

Expected current state: `nvme0n1` is visible but has no partitions or filesystems yet.

### Verification After Migration
After flashing or cloning to NVMe and rebooting:
```bash
lsblk -f
findmnt -n -o SOURCE /
```

Success criteria:
- root filesystem (`/`) is no longer on `/dev/sda2`
- root filesystem is on the NVMe device
- the Pi still answers at `r129.local`
- `ssh pi@r129.local` still works normally

### Notes
- Keep the USB stick unchanged until NVMe boot is confirmed working.
- This migration is the key prerequisite for the `<15s` boot target to the UI application.
- Current status: standalone NVMe boot has been verified successfully.

## Step 5: GitHub Repository Setup (UI Software)
1. On your Mac, go to GitHub and create a new repository (e.g., `R129-Pi-UI`).
2. Clone it to your Mac:
   ```bash
   cd ~/PROJ/R129
   git clone https://github.com/YOUR_USERNAME/R129-Pi-UI.git UI_rpi5_src
   ```
3. Generate an SSH key on the Pi for GitHub deployment (if you want to pull directly on the Pi):
   ```bash
   ssh-keygen -t ed25519 -C "rpi5-r129"
   cat ~/.ssh/id_ed25519.pub
   ```
   *Add this key to your GitHub account as a Deploy Key or standard SSH key.*
4. On the Pi, clone the new repository:
   ```bash
   git clone git@github.com:YOUR_USERNAME/R129-Pi-UI.git
   ```

## Step 6: Display Integration (DONE — 2026-04-03)

### Hardware
- **Display:** Waveshare 5.5" AMOLED capacitive touchscreen (USB ID `0712:000a`)
- **Resolution:** 1080x1920 native (portrait), rotated to 1920x1080 (landscape) via kanshi `transform 90`
- **Cabling:** 2 cables total:
  1. HDMI: Pi 5 HDMI-0 (micro-HDMI) → display HDMI input
  2. Touch/Power USB: display touch micro-USB → Pi 5 USB-A
- **Touch:** 10-point multitouch, auto-mapped to rotated display by `autotouch` package
- **Power:** Display powered through the touch USB cable — no separate power needed

### Configuration files
- `~/.config/kanshi/config` — persistent display rotation
- `autotouch` package handles touch-to-display coordinate mapping

### Gotchas discovered
- Display ships with two protective films. The inner film is non-conductive and blocks capacitive touch.
- First two USB cables tried were charge-only (no data lines). Third cable worked.
- The panel has **two micro-USB ports**: *touch + power*, and *power-only*. A cable in the power-only port gives a lit panel with completely dead touch.

### Touchscreen dead — triage

Run this before assuming a software fault. The whole question is whether the kernel sees a touch device at all:

```bash
sudo dmesg | grep -i 0712              # Waveshare touch controller = 0712:000a
cat /proc/bus/input/devices            # is there a touch device listed?
lsusb                                  # is 0712:000a on the bus?
```

**If `0712` never appears, it is a hardware/cabling fault — no software change will help.** Software-side sanity checks (`dpkg -l | grep autotouch`, `~/.config/kanshi/config`) are worth one line each to rule out, but a missing kernel input device is never caused by a userspace package.

Physical checks, in order:

1. Cable is in the panel's **touch** micro-USB port, not the **power-only** one.
2. Re-seat both ends including any 180° adapter. Micro-USB backing out a fraction of a millimetre keeps the outer power pins in contact while breaking the inner data pins — which presents as *lit panel, dead touch*.
3. Move the Pi end to a different USB-A port.
4. Swap in a known-good **data-capable** cable (see the charge-only gotcha above).

Watch for it live while re-seating:

```bash
sudo dmesg -w | grep --line-buffered -iE "0712|input: "
```

Success looks like a `New USB device found, idVendor=0712` line followed by a new `input:` registration.

**Caveat:** `grim` screenshots capture the *compositor framebuffer*, not the physical panel. A clean screenshot proves the Pi is rendering — it tells you nothing about whether the panel is lit or the digitiser is alive. Confirm the panel state with human eyes.

**Note on input redundancy:** with the touchscreen down and the rotary encoder not yet installed, the head unit has *no* usable input at all. Installing the Alps rotary/joystick (already supported by `input_manager.py` on GPIO 17/27/22/23/24/25/5) would provide a fallback path for exactly this failure.

## Step 7: CarPlay Integration (DONE — 2026-04-16)

### Hardware
- **Dongle:** Carlinkit CPC200-CCPA (USB ID `1314:1520`)
- **Connection:** Pi 5 USB-A port (USB 2.0), self-powered
- **Capabilities:** Wired + Wireless CarPlay (WiFi Direct 5 GHz), Android Auto

### Software
- **LIVI v5.9.3** — Electron-based CarPlay host (AppImage)
- **Location:** `/home/pi/LIVI/LIVI.AppImage`
- **Config:** `~/.config/LIVI/config.json` — 1792×1080 viewport (leaves room for the 128 px R129 sidebar), 60 fps, night mode, `kiosk: false`
- **udev:** `/etc/udev/rules.d/52-carplay.rules` — automatic dongle permissions

### UI integration (PyQt5)
- `CarPlayView` (`UI_rpi5/src/carplay_view.py`) occupies the 6th sidebar slot ("CARPLAY" icon).
- Tap or PRESS launches LIVI as a detached subprocess (`start_new_session=True`, `--no-sandbox`). Dongle presence is polled from `/sys/bus/usb/devices/3-1/idVendor` (fallback `lsusb`) at 5 s intervals; repaint only on state change.
- Navigating away calls `wlrctl window minimize app_id:livi` — **the LIVI process stays alive so the phone connection is preserved**. Returning calls `wlrctl window focus app_id:livi`.
- On UI shutdown (`closeEvent`), `os.killpg(pgid, SIGTERM)` cleans up the whole Electron process group.
- `ViewManager` grew `on_hidden()` / `on_shown()` lifecycle hooks used for this.

### labwc window rules (`~/.config/labwc/rc.xml`)
Positions the LIVI window beside the sidebar so the R129 icons stay touchable:
```xml
<windowRule identifier="livi" serverDecoration="no" fixedPosition="yes">
    <action name="MoveTo" x="128" y="0" />
    <action name="ResizeTo" width="1792" height="1080" />
</windowRule>
```

### Verified
- Dongle enumerates and is recognized by LIVI on startup
- LIVI renders in the 1792×1080 area beside the R129 sidebar (no overlap)
- Minimize / restore on view switch works with zero reconnection cost
- Telemetry socket on port 4000

### iPhone pairing (2026-05-27)

**Pair to `LIVI`, not `r129`.** There are two Bluetooth devices the iPhone will see for this car:
- **`r129`** — the Pi's own BT radio. Used for A2DP music streaming only. Has *nothing* to do with CarPlay; pairing here does not enable CarPlay.
- **`LIVI`** — the Carlinkit dongle's internal BT radio. Branded by the LIVI host app at first-pair time (same name as the dongle's Wi-Fi-Direct SSID). **This is the one CarPlay needs.**

Pairing to both is fine and recommended — they use independent radios on the iPhone (BT classic for `r129` A2DP, Wi-Fi for the `LIVI` dongle) and do not contend. iOS picks the right route automatically: CarPlay when the dongle is active, A2DP otherwise.

First-time pair procedure (canonical):
1. On the iPhone: Settings → Bluetooth → tap the `LIVI` entry → accept pairing prompt.
2. iOS shows "Use CarPlay with this car?" → Yes.
3. Settings → General → CarPlay → confirm `LIVI` is in "My Car".
4. Within a few seconds the dongle's USB reset loop stops (see "Signal" below), LIVI's blinking-square screen transitions to live CarPlay content.

**Recovery procedure** for "LIVI shows a slowly-blinking small square, won't connect to phone":
1. Long-press the CarPlay sidebar slot (≥600 ms) until the icon turns red, release. LIVI subprocess exits.
2. On the iPhone: reboot the phone. Forces iOS to drop stale BT / Wi-Fi-Direct associations — this is the single most reliable fix for the stuck-handshake state. (Toggling `Use CarPlay with this car` off/on without a reboot sometimes works, often doesn't.)
3. After the iPhone boots, Settings → Bluetooth → tap `LIVI` to reconnect.
4. Short-tap the CarPlay sidebar slot to re-launch LIVI. Handshake should complete within ~5 seconds.

**Don't read the iPhone BT menu as a CarPlay status indicator.** Bluetooth is only the matchmaker — used once at session start to negotiate the Wi-Fi-Direct association between iPhone and dongle. The actual CarPlay session (video + audio + iAP2) runs entirely over Wi-Fi-Direct. iOS routinely tears down the BT link after the Wi-Fi-Direct association is established to save phone battery, so `LIVI — Not Connected` in the iPhone BT menu *while CarPlay is actively rendering on screen* is **expected and normal**, not a fault.

**Pi-side signal — "is CarPlay actually up?"**: the CCPA muxes video + audio + iAP2 control through its single vendor-specific bulk endpoint (`3-2:1.0`). It does *not* expose UVC/UAC sub-interfaces and does *not* create a new PipeWire sink when the link comes up — LIVI demuxes all of that internally. So the cleanest external signal is the **dongle's USB disconnect/reconnect cycle stopping**:
- Cycle rate **every ~12-50 sec** = dongle is in "no phone paired with my Wi-Fi-Direct radio" reset loop.
- **Cycle stops** (no `usb 3-2: USB disconnect` lines in `dmesg` for >1 min) = Wi-Fi-Direct session up, CarPlay link is healthy.

Verify with: `sudo dmesg | grep "usb 3-2" | tail -10` — compare timestamps to current uptime (`awk '{print int($1)}' /proc/uptime`).

### Exit gesture (2026-05-27)

The CarPlay sidebar slot supports two gestures:
- **Short tap** (release < 600 ms) — navigates to CarPlay view, ensures LIVI is running.
- **Long press** (hold ≥ 600 ms) — emits `Sidebar.carplay_stop_requested` → `MainWindow._stop_carplay()` → `CarPlayView._stop_livi()` → kills the LIVI Electron process group via `os.killpg(SIGTERM)`. Works from any page. Visual feedback during hold: slot dims to warm orange (0-600 ms), then flips to `theme.NEEDLE_RED` once the long-press threshold is crossed ("release now to stop").

Use the long press whenever LIVI gets stuck on the blinking-square screen, or to fully tear down the CarPlay subprocess before doing a clean re-pair.

### Sidebar polarity (2026-05-27)

For daylight visibility, all sidebar slots now render with filled `theme.AMBER` (`QColor(255, 191, 0)` — canonical VDO brightness yellow) background and dark icon dots. Selection is marked by a small red pip in the top-right corner of the slot (8 px diameter, 12 px inset, `theme.NEEDLE_RED`). The pip is suppressed during a CarPlay long-press hold so the hold's colour change communicates the gesture progress without the pip mudding the signal.

### Pending
- Audio pipeline testing (PipeWire → Match UP 6DSP)
- Runtime-adjustable amber brightness (Qt-level scalar wrapping `theme.AMBER`) for night dim + OLED burn-in mitigation
- `carplay_view.py` dongle-detection fast-path: currently hardcoded to `/sys/bus/usb/devices/3-1`, should scan for `1314:1520` across `/sys/bus/usb/devices/*` since the dongle re-enumerates to other ports after unbind/rebind

## Step 8: Exit-to-Desktop & Fallback Desktop Usability (DONE — 2026-04-16)

### Exit slot
- Last sidebar slot is **EXIT** (`exit_view.py`, power-symbol icon).
- Tap or PRESS calls `QApplication.quit()` → systemd user service exits cleanly → Linux desktop is revealed.
- The desktop is a rare-use fallback, not a primary feature. Restart via a desktop launcher icon (`~/Desktop/r129-ui.desktop`) that runs `systemctl --user start r129-ui.service`.

### Dynamic compositor output scaling
The driver UI is hand-tuned for 1920×1080 @ 1.0× scale. The Pi desktop at that scale is unreadable on a 5.5" panel. Solution: flip the Wayland compositor's output scale only while the UI is not running.

Implemented via systemd hooks in `r129-ui.service`:
```ini
ExecStartPre=/usr/bin/wlr-randr --output HDMI-A-1 --scale 1
ExecStopPost=/usr/bin/wlr-randr --output HDMI-A-1 --scale 1.5
```

- On UI start: scale snaps to **1×** → R129 and LIVI render at their designed sizes.
- On UI exit (clean, crash, or manual stop): scale snaps to **1.5×** → desktop, taskbar, file manager, squeekboard OSK all become readable.
- Brief (~few frames) flicker during the transition — acceptable for a fallback path.

### Other desktop usability tweaks
- `~/.config/labwc/environment`: `GDK_SCALE=2` for non-layer-shell GTK apps (harmless fallback — layer-shell clients honour the compositor scale instead).
- `~/.config/lxterminal/lxterminal.conf`: `fontname=Monospace 16` — VTE ignores `GDK_SCALE`, so the terminal grid font is bumped explicitly.

### Why this separation works
| Launch path | Env scope | Compositor scale at paint time |
| :--- | :--- | :--- |
| R129 UI (systemd user svc) | systemd-user env — no `GDK_SCALE` | 1× (set by `ExecStartPre`) |
| LIVI (child of R129 UI) | Inherits from R129 UI | 1× (LIVI is Chromium/Electron, follows compositor) |
| Desktop apps (pcmanfm, wf-panel-pi, lxterminal…) | labwc session env — `GDK_SCALE=2` visible | 1.5× when UI is off |

## Step 9: Desktop Popup Suppression (DONE — 2026-08-09)

Desktop notification daemons float windows *above* the R129 Qt surface and take Wayland focus, so they can intercept touch. Worth eliminating on a head unit.

> **Don't stop at the popup.** On 2026-08-09 popups and an unresponsive screen appeared together and the popups were assumed to be the cause. They weren't — the touchscreen was physically disconnected. If the screen is still dead after clearing the popups, go to "Touchscreen dead — triage" under Step 6.

### blueman-applet
Observed 2026-08-09: two stacked `blueman-applet: iPhone` ("Disconnected") windows over the centre of the display. Bluetooth pairing on this Pi is already handled headlessly by `bt-agent.service` (`--capability=NoInputNoOutput`), so the applet is redundant.

Disabled with a user-level autostart override that shadows `/etc/xdg/autostart/blueman.desktop`:

```ini
# ~/.config/autostart/blueman.desktop
[Desktop Entry]
Type=Application
Name=blueman-applet
Exec=/usr/bin/blueman-applet
Hidden=true
```

`Hidden=true` in `~/.config/autostart/` suppresses the system-wide entry without editing `/etc`, so an OS package update can't silently re-enable it.

**If a popup blocks the UI again**, identify it first rather than rebooting:

```bash
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 wlrctl window list
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 grim /tmp/screen.png
```

`grim` is installed — screenshotting over SSH is the fastest way to see what the car display is actually showing.

### Gotcha: `pgrep -f` / `pkill -f` self-match kills the SSH session

`pgrep -f` and `pkill -f` match against full command lines, including the command line of the `bash -c` wrapper SSH spawns — which contains the pattern string itself. The pattern matches its own shell and the session dies. Hit twice now (2026-05-27 with `pkill -f /tmp/.mount_LIVI`, 2026-08-09 with `pgrep -f "blueman-applet|blueman-tray"`).

Wrap one character of the pattern in a single-character class:

```bash
pgrep -af "blueman-[a]pplet"     # matches blueman-applet, not this command line
pgrep -af "python3.*main[.]py"
```

The regex still matches the target; the literal command line does not match the regex.

## Deploying UI changes to the Pi

The UI source lives at `/home/pi/R129_UI/src` on the Pi (no git checkout there — deploy is an rsync push from the repo's `UI_rpi5/src`).

```bash
# 1. Dry run — confirm the file list is what you expect
rsync -avzn --exclude=__pycache__ UI_rpi5/src/ pi@r129.local:/home/pi/R129_UI/src/

# 2. Real transfer
rsync -avz --exclude=__pycache__ UI_rpi5/src/ pi@r129.local:/home/pi/R129_UI/src/

# 3. Syntax check BEFORE restarting — the old UI is still running at this point
ssh pi@r129.local 'cd /home/pi/R129_UI/src && python3 -m py_compile *.py'

# 4. Restart
ssh pi@r129.local 'XDG_RUNTIME_DIR=/run/user/1000 systemctl --user restart r129-ui.service'
```

Step 3 matters: a syntax error caught after the restart leaves a dead head unit in a car that may be parked out of Wi-Fi range.

### Driving the UI remotely for verification

`wtype` is installed and can exercise the UI over SSH for smoke-testing after a deploy:

```bash
export WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000
wlrctl window focus title:"R129 Driver UI"
wtype -k Down; wtype -k Return      # navigate sidebar → activate page
```

**Never send `Escape` or `Q`** — `MainWindow.keyPressEvent` maps both to `close()`, which quits the UI. Arrows and `Return` only.

Note this exercises the *keyboard/rotary* input path and the paint path, not the touch handlers (`mousePressEvent`). Touch targets still need a finger at the car.

## Next Steps
- Connect and verify Match UP 6DSP + MEC HD-USB audio path.
- Add GPS module for live map tracking.
- Finger-test the touch-operable menu layer (Settings taps, slider drag, Exit hold-to-quit).
- Continue higher-level UI and system architecture work in `R129_Driver_UI_System_Design.md`.
