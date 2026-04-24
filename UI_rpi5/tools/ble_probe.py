#!/usr/bin/env python3
"""R129 BLE probe.

Stand-alone bring-up tool for the R129-Diag nRF5340 peripheral. Scans for
the advertising name ``R129-Diag``, connects, discovers the custom
service, subscribes to the diagnostics stream notify characteristic,
and pretty-prints every framed payload it receives.

From M1 onwards the notify payload is a framed r129_payload_t (see
``r129_payload.py`` in this folder / ``FW_nrf/payload/r129_payload.h``),
not a raw uint32. Unknown frame types are dumped as hex.

Runs on both the Pi5 (BlueZ) and macOS (CoreBluetooth) via the ``bleak``
library. Not wired into the R129 UI -- this is purely a diagnostic.

Usage:
    pip install bleak
    python3 ble_probe.py                 # scan + connect, decode frames
    python3 ble_probe.py --scan-only     # list advertisements and exit
    python3 ble_probe.py --address XX:XX:XX:XX:XX:XX  # skip scan
    python3 ble_probe.py --raw           # also hex-dump each notification

Firmware side: R129/FW_nrf/app/src/ble_diag.c
"""
from __future__ import annotations

import argparse
import asyncio
import sys
import time
from typing import Optional

try:
    from bleak import BleakClient, BleakScanner
    from bleak.backends.device import BLEDevice
except ImportError:
    sys.exit("bleak not installed. Run: pip install bleak")

from r129_payload import FrameError, FrameType, Heartbeat, decode_typed, pretty_hex


DEVICE_NAME = "R129-Diag"
SERVICE_UUID = "a7290001-5231-3239-a7e1-524531323900"
DIAG_STREAM_UUID = "a7290002-5231-3239-a7e1-524531323900"


async def scan(timeout: float = 5.0) -> Optional[BLEDevice]:
    print(f"scanning for '{DEVICE_NAME}' for {timeout:.1f}s ...")
    # bleak >=3.0: use return_adv so we can read AdvertisementData.rssi
    found = await BleakScanner.discover(timeout=timeout, return_adv=True)
    for address, (dev, adv) in found.items():
        if dev.name == DEVICE_NAME or adv.local_name == DEVICE_NAME:
            print(f"  found {dev.name or adv.local_name} @ {address} rssi={adv.rssi}")
            return dev
    print("  not found")
    return None


async def scan_only(timeout: float = 5.0) -> None:
    print(f"listing all advertisements for {timeout:.1f}s ...")
    found = await BleakScanner.discover(timeout=timeout, return_adv=True)
    for address, (dev, adv) in found.items():
        name = dev.name or adv.local_name
        uuids = ",".join(u[:8] for u in (adv.service_uuids or []))
        marker = ""
        if name == DEVICE_NAME or any(u.startswith("a7290001") for u in (adv.service_uuids or [])):
            marker = "  <-- R129"
        print(f"  {address}  rssi={adv.rssi:>4}  name={name!r:<30} uuids=[{uuids}]{marker}")


async def follow(address: str, raw: bool = False) -> None:
    t0 = time.monotonic()
    received = 0
    bad_frames = 0
    last_counter: Optional[int] = None

    def handler(_sender, data: bytearray) -> None:
        nonlocal received, bad_frames, last_counter
        received += 1
        ts = time.monotonic() - t0
        if raw:
            print(f"[{ts:7.2f}s] raw({len(data)}B): {pretty_hex(bytes(data))}")
        try:
            frame_type, payload, _ = decode_typed(bytes(data))
        except FrameError as e:
            bad_frames += 1
            print(f"[{ts:7.2f}s] bad frame ({e}): {pretty_hex(bytes(data))}")
            return

        if frame_type == FrameType.HEARTBEAT and isinstance(payload, Heartbeat):
            gap = ""
            if last_counter is not None:
                delta = payload.counter - last_counter
                gap = f" (+{delta})" if delta >= 0 else f" ({delta})"
            print(f"[{ts:7.2f}s] HEARTBEAT counter={payload.counter}"
                  f" uptime={payload.uptime_ms/1000:.3f}s{gap}")
            last_counter = payload.counter
        else:
            name = frame_type.name if isinstance(frame_type, FrameType) else f"0x{frame_type:02X}"
            body = pretty_hex(payload) if isinstance(payload, (bytes, bytearray)) else repr(payload)
            print(f"[{ts:7.2f}s] {name}: {body}")

    print(f"connecting to {address} ...")
    async with BleakClient(address) as client:
        print("  connected")
        services = client.services  # triggers discovery on some backends
        svc = services.get_service(SERVICE_UUID)
        if svc is None:
            print("  R129 service not found on peripheral")
            return
        print(f"  service found: {svc.uuid}")
        char = svc.get_characteristic(DIAG_STREAM_UUID)
        if char is None:
            print("  diagnostics stream characteristic not found")
            return
        print(f"  subscribing to {char.uuid} ...")

        await client.start_notify(char, handler)
        print("  subscribed, press Ctrl-C to stop")
        try:
            while client.is_connected:
                await asyncio.sleep(1.0)
        finally:
            await client.stop_notify(char)
            elapsed = time.monotonic() - t0
            print(f"stopped; received {received} notifications"
                  f" ({bad_frames} malformed) over {elapsed:.1f}s")


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--address", help="skip scan, connect directly to this address")
    ap.add_argument("--scan-only", action="store_true", help="list ads and exit")
    ap.add_argument("--timeout", type=float, default=5.0, help="scan timeout")
    ap.add_argument("--raw", action="store_true",
                    help="also hex-dump each received notification")
    args = ap.parse_args()

    if args.scan_only:
        await scan_only(args.timeout)
        return 0

    address = args.address
    if address is None:
        dev = await scan(args.timeout)
        if dev is None:
            return 1
        address = dev.address

    await follow(address, raw=args.raw)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print()
