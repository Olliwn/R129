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

### Pending
- iPhone pairing (wired first, then wireless auto-reconnect)
- Audio pipeline testing (PipeWire → Match UP 6DSP)

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

## Next Steps
- iPhone pairing flow for the CarPlay dongle.
- Connect and verify Match UP 6DSP + MEC HD-USB audio path.
- Add GPS module for live map tracking.
- Continue higher-level UI and system architecture work in `R129_Driver_UI_System_Design.md`.
