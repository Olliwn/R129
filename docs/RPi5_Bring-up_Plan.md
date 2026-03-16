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

## Next Steps
- Measure boot time and remove unnecessary startup overhead.
- Setup systemd service to auto-start the PySide6 app on boot.
- Continue higher-level UI and system architecture work in `R129_Driver_UI_System_Design.md`.
