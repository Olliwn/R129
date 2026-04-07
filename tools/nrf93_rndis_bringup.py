#!/usr/bin/env python3
"""
nRF93M1 RNDIS bring-up script.
Sends AT commands to activate the cellular data connection and enable
RNDIS networking. Triggered by udev/systemd on DK plug-in or power cycle.

Usage:
    python3 nrf93_rndis_bringup.py [--port /dev/ttyACM0] [--teardown]
"""

import argparse
import glob
import subprocess
import sys
import time

try:
    import serial
except ImportError:
    sys.exit("pyserial not installed: sudo apt install -y python3-serial")

BAUD = 115200
TIMEOUT = 3
MAX_REG_WAIT = 60
MAX_PORT_RETRIES = 5


def find_at_port():
    """Probe ttyACM ports, retrying if port is temporarily busy."""
    for attempt in range(MAX_PORT_RETRIES):
        for port in sorted(glob.glob("/dev/ttyACM*")):
            try:
                s = serial.Serial(port, BAUD, timeout=1)
                s.reset_input_buffer()
                s.write(b"AT\r\n")
                time.sleep(0.5)
                resp = s.read(s.in_waiting or 64).decode(errors="replace")
                s.close()
                if "OK" in resp:
                    return port
            except Exception:
                continue
        if attempt < MAX_PORT_RETRIES - 1:
            print(f"[nrf93] No AT port found, retry {attempt+1}/{MAX_PORT_RETRIES}...")
            time.sleep(2)
    return None


def at(ser, cmd, timeout=3.0):
    ser.reset_input_buffer()
    ser.write((cmd + "\r\n").encode())
    lines = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        raw = ser.readline()
        if not raw:
            continue
        line = raw.decode(errors="replace").strip()
        if not line:
            continue
        lines.append(line)
        if line in ("OK", "ERROR") or line.startswith("+CME ERROR"):
            break
    resp = "\n".join(lines)
    print(f"  > {cmd}\n    {resp}")
    return resp


def bringup(port):
    print(f"[nrf93] Opening {port}")
    ser = serial.Serial(port, BAUD, timeout=TIMEOUT)

    resp = at(ser, "AT")
    if "OK" not in resp:
        ser.close()
        sys.exit(f"[nrf93] No AT response on {port}")

    at(ser, "AT+CFUN=1", timeout=4.0)

    time.sleep(1)
    resp = at(ser, "AT+CPIN?")
    if "READY" not in resp:
        ser.close()
        sys.exit("[nrf93] SIM not ready")

    print("[nrf93] Waiting for network registration...")
    t0 = time.monotonic()
    while time.monotonic() - t0 < MAX_REG_WAIT:
        resp = at(ser, "AT+CEREG?")
        if any(f"0,{s}" in resp for s in ("1", "5")):
            print("[nrf93] Registered" + (" (roaming)" if ",5" in resp else ""))
            break
        time.sleep(3)
    else:
        ser.close()
        sys.exit("[nrf93] Registration timeout")

    resp = at(ser, "AT+CGPADDR")
    if "CGPADDR" in resp and "ERROR" not in resp:
        print("[nrf93] Modem IP assigned")
    else:
        print("[nrf93] No PDP address, activating...")
        at(ser, 'AT+CGDCONT=1,"IP","internet"')
        at(ser, "AT+CGACT=1,1", timeout=5.0)
        resp = at(ser, "AT+CGPADDR")
        if "ERROR" in resp:
            ser.close()
            sys.exit("[nrf93] PDP activation failed")

    resp = at(ser, "AT%NETDEVCTL=3,1,1", timeout=5.0)
    if "OK" not in resp:
        ser.close()
        sys.exit("[nrf93] NETDEVCTL failed")

    print("[nrf93] RNDIS enabled, requesting DHCP lease on eth1...")
    ser.close()

    try:
        subprocess.run(["dhcpcd", "-w", "eth1"], timeout=30, check=True,
                       capture_output=True, text=True)
        print("[nrf93] DHCP lease acquired on eth1")
    except FileNotFoundError:
        try:
            subprocess.run(["dhclient", "-v", "eth1"], timeout=30, check=True,
                           capture_output=True, text=True)
            print("[nrf93] DHCP lease acquired on eth1 (dhclient)")
        except Exception as e:
            print(f"[nrf93] WARNING: DHCP failed ({e}), eth1 may need manual IP")
    except subprocess.TimeoutExpired:
        print("[nrf93] WARNING: DHCP timed out on eth1")
    except subprocess.CalledProcessError as e:
        print(f"[nrf93] WARNING: DHCP error: {e.stderr.strip()}")

    result = subprocess.run(["ip", "addr", "show", "eth1"], capture_output=True, text=True)
    if "inet " in result.stdout:
        ip_line = [l.strip() for l in result.stdout.splitlines() if "inet " in l][0]
        print(f"[nrf93] eth1 address: {ip_line}")
    else:
        print("[nrf93] WARNING: eth1 has no IPv4 address")

    # Make LTE the preferred default route (metric 100 < WiFi's 600)
    gw = subprocess.run(["ip", "route", "show", "default", "dev", "eth1"],
                        capture_output=True, text=True)
    if gw.stdout.strip():
        subprocess.run(["ip", "route", "del", "default", "dev", "eth1"], check=False,
                       capture_output=True)
        gw_addr = gw.stdout.strip().split("via")[1].split()[0] if "via" in gw.stdout else ""
        if gw_addr:
            subprocess.run(["ip", "route", "add", "default", "via", gw_addr,
                            "dev", "eth1", "metric", "100"],
                           check=False, capture_output=True)
            print(f"[nrf93] LTE default route set (metric 100, via {gw_addr})")

    print("[nrf93] Cellular internet should now be available")
    return 0


def teardown(port):
    print(f"[nrf93] Teardown on {port}")
    ser = serial.Serial(port, BAUD, timeout=TIMEOUT)
    at(ser, "AT%NETDEVCTL=0,1")
    ser.close()
    print("[nrf93] RNDIS disabled")
    return 0


def main():
    parser = argparse.ArgumentParser(description="nRF93M1 RNDIS bring-up")
    parser.add_argument("--port", default=None, help="AT serial port (auto-detected if omitted)")
    parser.add_argument("--teardown", action="store_true", help="Disable RNDIS and exit")
    args = parser.parse_args()

    port = args.port
    if port is None:
        print("[nrf93] Auto-detecting AT port...")
        port = find_at_port()
        if port is None:
            sys.exit("[nrf93] No AT-capable ttyACM port found")
        print(f"[nrf93] Found AT port: {port}")

    if args.teardown:
        return teardown(port)
    return bringup(port)


if __name__ == "__main__":
    sys.exit(main() or 0)
