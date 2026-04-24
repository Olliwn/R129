# FW_nrf — R129 Diagnostics Node Firmware

**Target:** Nordic **nRF54L15 DK** (PCA10156), application core (Cortex-M33, single-core).
**SDK:** nRF Connect SDK **v3.2.0** (Zephyr 4.2.99) at `/opt/nordic/ncs/v3.2.0`.
**BLE controller:** Nordic SoftDevice Controller (`CONFIG_BT_LL_SOFTDEVICE=y`), linked into the single app image.
**Role:** MVP bring-up for the BLE sentry / telemetry node that pairs with the RPi5 dashboard described in `work/nRF5430_interface_board/`.

> **Chip migration note (2026-04-24):** this firmware was originally written for the nRF5340 DK (M0 + M1 were verified on that target on 2026-04-20 — see `docs/diary/2026-04.md`). Re-targeted to nRF54L15 here. The app source is SoC-agnostic Zephyr code and did not change; only `app/sysbuild.conf` (deleted), the build target string, and this README changed. The hardware-design docs under `work/nRF5430_interface_board/` still cite nRF5340 numbers and will be refreshed during the M2 interface-board design pass.

## Current milestone

**M0 — BLE hello-world** ✅ *done 2026-04-20 (on nRF5340 DK) · re-verified on nRF54L15 DK 2026-04-24*
**M1 — framed payload codec** ✅ *done 2026-04-20 (on nRF5340 DK) · re-verified on nRF54L15 DK 2026-04-24*

Firmware advertises as `R129-Diag` and emits a framed `HEARTBEAT` payload every 1 s on both the BLE diagnostics-stream notify characteristic and the USB-CDC / UART0 console. Every future telemetry type (analog sensors, blink codes, commands) is a new `TYPE` value + `DATA` layout on the same wire format — no GATT changes needed. M0/M1 verified end-to-end from CoreBluetooth (Mac) and BlueZ (Pi) with `bleak` on the nRF5340 DK; nothing in the app source changed for the L15 port, so the wire side is expected to behave identically. See `docs/diary/2026-04.md` for the bring-up writeup and the Apr 24 migration entry.

The codec itself is a ~100-line portable C library with zero Zephyr dependencies (lives in `payload/`) and a Python mirror at `../UI_rpi5/tools/r129_payload.py`. Both are exercised against the same test vectors in `host_test/` and `UI_rpi5/tools/test_r129_payload.py`, so firmware and host changes cannot silently drift apart.

## Directory layout

```
FW_nrf/
├── README.md                  # this file
├── .gitignore
├── payload/                   # portable C codec, shared with host_test/ and app/
│   ├── r129_payload.h
│   └── r129_payload.c
├── host_test/                 # host-side unit tests (plain cc, no Zephyr)
│   ├── Makefile
│   └── test_payload.c
├── tools/ncs.sh               # nrfutil toolchain-manager wrapper
└── app/                       # Zephyr "freestanding application"
    ├── CMakeLists.txt
    ├── prj.conf               # Zephyr + BLE Kconfig  (no SoC-specific entries)
    └── src/
        ├── main.c             # app entry, 1 Hz encode + notify + print loop
        ├── ble_diag.c/.h      # custom GATT service, diagnostics-stream notify
        └── uart_log.c/.h      # console heartbeat line + frame hex dump
```

The app is freestanding — it points at the shared NCS workspace at `/opt/nordic/ncs/v3.2.0` rather than carrying its own west manifest. This keeps this directory small (build artifacts aside) and avoids duplicating the ~2 GB SDK tree into the `R129/` git repo.

Note: no `app/sysbuild.conf` — nRF54L15 is single-core so there is no separate network-core image to configure. (On the nRF5340 this file previously enabled the `ipc_radio` netcore BLE controller; that work now happens inside the app image via the SoftDevice Controller.)

## Build + flash

All commands go through `./tools/ncs.sh`, which invokes `nrfutil toolchain-manager launch` for the NCS v3.2.0 bundle and exports `ZEPHYR_BASE` so `west build` resolves its extension commands even though this app is freestanding (lives outside the NCS workspace tree).

```bash
cd ~/R129/R129/FW_nrf

# clean build from scratch
./tools/ncs.sh west build -b nrf54l15dk/nrf54l15/cpuapp app -d build -p always

# incremental rebuild
./tools/ncs.sh west build -d build

# flash to the DK over USB (uses the nrfutil runner on nRF54L15, not legacy nrfjprog)
./tools/ncs.sh west flash -d build

# open a sub-shell with the toolchain on PATH (west, ninja, arm-zephyr-eabi-gcc...)
./tools/ncs.sh bash
```

Build products:
- `build/merged.hex` — single hex with application + Zephyr + Bluetooth host + SoftDevice Controller. Single-image because nRF54L15 has no separate network core (contrast with the nRF5340 dual-hex build that produced `merged.hex` + `merged_CPUNET.hex`).

Smoke-build footprint (2026-04-24, first build on nRF54L15, M1 payload stack):

```
FLASH: 146 444 B / 1 428 KB (10.01 %)
RAM:    32 724 B /   188 KB (17.00 %)
```

FLASH grew vs the nRF5340 app-core number (105 700 B) because the SoftDevice Controller is now linked into the single image — but the net device footprint dropped, since the 5340 also carried a separate ~130 KB network-core image that no longer exists. RAM is slightly smaller (one fewer IPC transport to maintain).

### DK switch settings for bench development

As observed on 2026-04-24 with a PCA10156 L15 DK out of the box (serial `001057774115`), no switch changes were needed — plugging the debug USB (single IMCU USB-C port on this board) into the Mac was sufficient for `west flash` + UART + BLE to all work. The L15 DK does not have the nRF5340 DK's "nRF ONLY / DEFAULT" power-split slider (SW6 on the 5340); instead a single IMCU supply path powers the nRF when the debug USB is plugged in.

Document the actual switch / jumper positions here once a bench config other than "out-of-box + USB power" is needed (e.g. when the DK starts drawing power from the R129 interface board 3 V3 rail at M2).

### UART console over USB

Despite nRF54L15 being single-core, the DK's IMCU still enumerates **two** `tty.usbmodem*` VCOMs on macOS (observed; the nRF Connect SDK 3.2.0 shipping image does this on the L15 DK just like on the 5340). The **higher-suffix** one is the app-core UART0 — same heuristic as on the 5340 DK. Example observed:

```
/dev/tty.usbmodem0010577741151   # silent (auxiliary / Nordic Cloud-backhaul port, unused by our firmware)
/dev/tty.usbmodem0010577741153   # app UART0 — use this
```

```bash
screen /dev/tty.usbmodem0010577741153 115200
# expect, once per second:
#   R129-CTR <n> uptime=<ms> ms
#   R129-FRM AE 08 00 <uptime LE 4B> <counter LE 4B> <CRC HI> <CRC LO>
# exit: Ctrl-A  K  y
```

Or the Python snippet from the `.venv` (more robust under re-enumeration; `screen` sometimes fights with the Cursor terminal for port ownership):

```bash
~/R129/R129/UI_rpi5/tools/.venv/bin/python3 -c "
import serial, time, sys
s = serial.Serial('/dev/tty.usbmodem0010577741153', 115200, timeout=1)
for _ in range(5):
    line = s.readline()
    if line: sys.stdout.write(line.decode('utf-8', errors='replace'))
    sys.stdout.flush()
"
```

### Payload codec host tests

Runs on a plain system `cc` (Apple clang / gcc). No Zephyr, no NCS bundle needed. Nothing changed between nRF5340 and nRF54L15 — the codec is portable C99.

```bash
cd ~/R129/R129/FW_nrf/host_test
make          # compiles ../payload/r129_payload.c + test_payload.c, runs all tests
```

A matching Python suite lives next to the probe:

```bash
cd ~/R129/R129/UI_rpi5/tools
python3 -m unittest test_r129_payload.py
```

The two test files intentionally share vectors (e.g. the `{uptime=0x12345678, counter=0xDEADBEEF}` heartbeat round-trip) so firmware-side and host-side codec changes stay in lockstep.

## BLE verification from the host

The Pi5-side `bleak` probe lives at `../UI_rpi5/tools/ble_probe.py` and also works on macOS. Homebrew Python 3 blocks system-wide `pip install` under PEP 668, so use a venv:

```bash
python3 -m venv ~/R129/R129/UI_rpi5/tools/.venv
source ~/R129/R129/UI_rpi5/tools/.venv/bin/activate
pip install bleak
python3 ~/R129/R129/UI_rpi5/tools/ble_probe.py
```

First run will prompt for Bluetooth permission for the Terminal / Cursor app — grant it.

BLE device name (`R129-Diag`), service UUID, characteristic UUID, and wire format are all unchanged between the nRF5340 and nRF54L15 builds — the probe does not know or care which SoC is on the other side of the link.

## Custom GATT service UUIDs

Base UUID scheme: `a729xxxx-5231-3239-a7e1-524531323900`
- `5231 3239` = ASCII `R1 29`
- `a729`, `a7e1` = project prefix

| Characteristic | UUID | Properties | Payload |
|---|---|---|---|
| R129 Diagnostics Service | `a7290001-5231-3239-a7e1-524531323900` | — | — |
| Diagnostics stream | `a7290002-5231-3239-a7e1-524531323900` | Notify + Read | Framed `r129_payload_t` (see below) |

### Wire format (see `payload/r129_payload.h` for the authoritative spec)

```
offset  field   bytes   notes
0       SYNC    1       = 0xAE
1       LEN     1       = N (Data byte count; 0..240)
2       TYPE    1       r129_type_t (HEARTBEAT=0x00, ANALOG=0x02, BLINK=0x03, CMD_CLEAR=0x10, ...)
3..2+N  DATA    N       type-specific payload
3+N     CRC_HI  1       CRC-16/CCITT-FALSE MSB, over SYNC..DATA
4+N     CRC_LO  1       CRC-16/CCITT-FALSE LSB
total = 5 + N bytes
```

Integer fields inside DATA are little-endian. The CRC itself is big-endian so a raw hex dump reads left-to-right.

Current types:

| Type | Name | Data layout | Cadence |
|---|---|---|---|
| `0x00` | `HEARTBEAT` | `uint32_t uptime_ms; uint32_t counter;` (8 B, LE) | 1 Hz always-on |
| `0x02` | `ANALOG` | reserved for M3 (ADS1115 channels) | — |
| `0x03` | `BLINK` | reserved for M4 (blink-code frames from KE pin X11) | — |
| `0x10` | `CMD_CLEAR` | reserved for M4 (host → nRF54L15 clear-code request) | — |

Future types are additive — the stream characteristic never changes UUID.

## Roadmap

| Milestone | Content | Depends on |
|---|---|---|
| **M0** | BLE counter, UART log | Toolchain ✅ |
| **M1** | Framed payload library (encode / decode / CRC) | M0 ✅ |
| **L15 port** | Rebuild + rerun M0/M1 on nRF54L15 DK | nRF54L15 DK in hand |
| M2 | Stage-1 power board soldered; DK powered from board 3 V3 / 5 V | Stage 1 hardware |
| M3 | ADS1115 I²C driver, real 4-channel analog telemetry (`0x02`) | M1, M2 |
| M4 | Blink-code RX + code-clear TX optocoupler path (`0x03` / `0x10`) | Stages 2–3 hardware |
| M5 | Full 9-channel X11 read, duty-cycle capture on KE pin 3 | Stages 6–7 hardware |
| M6 | Sleep / wake manager mode — PM + GPIO drive for Pi power | M5 |

## Hardware notes

See `work/nRF5430_interface_board/Breadboard_Build_Instructions.md` for the full hardware design. **Those docs still cite nRF5340 pinouts, current draw, and package footprint and will be refreshed as part of the M2 design pass** (see the stale-ref notice at the top of that README). For M0–M1 the DK runs standalone on USB power with no interface board attached, so the mismatch does not affect current bring-up work.
