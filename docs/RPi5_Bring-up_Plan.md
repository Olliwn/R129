# Raspberry Pi 5 Headless Bring-up Plan

## Objective
Set up the RPi5 for remote SSH operation from the Mac, entirely headless (no keyboard/mouse), and prepare the Git repository for the UI software.

## Step 1: OS Flashing and Headless Configuration
1. **Tool Needed**: Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your Mac.
2. **Select OS**: Choose **Raspberry Pi OS (64-bit)** (Lite is recommended if you only need the background UI app without desktop overhead, but full OS is fine if you plan to use PySide6/X11/Wayland directly).
3. **Advanced Options (The Gear Icon / Ctrl+Shift+X)**:
   - Sets hostname (e.g., `r129-gui`).
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
   ping r129-gui.local
   ```
5. Connect via SSH:
   ```bash
   ssh pi@r129-gui.local
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

## Step 4: GitHub Repository Setup (UI Software)
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
- Continue configuring the NVMe boot to achieve the <15s target to UI application.
- Setup systemd service to auto-start the PySide6 app on boot.
