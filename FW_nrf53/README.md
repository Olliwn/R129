# FW_nrf53 — R129 Diagnostics Node Firmware

**Target:** Nordic nRF5340 DK (PCA10095), application core.
**SDK:** nRF Connect SDK **v3.2.0** (Zephyr 4.2.99) at `/opt/nordic/ncs/v3.2.0`.
**Role:** MVP bring-up for the BLE sentry / telemetry node that pairs with the RPi5 dashboard described in `work/nRF5430_interface_board/`.

## Current milestone

**M0 — BLE hello-world** ✅ *done 2026-04-20*
**M1 — framed payload codec** ✅ *done 2026-04-20*

Firmware advertises as `R129-Diag` and emits a framed `HEARTBEAT` payload every 1 s on both the BLE diagnostics-stream notify characteristic and the USB-CDC / UART0 console. Every future telemetry type (analog sensors, blink codes, commands) is a new `TYPE` value + `DATA` layout on the same wire format — no GATT changes needed. Verified end-to-end from CoreBluetooth (Mac) and BlueZ (Pi) with `bleak`. See `docs/diary/2026-04.md` for the bring-up writeup.

The codec itself is a ~100-line portable C library with zero Zephyr dependencies (lives in `payload/`) and a Python mirror at `../UI_rpi5/tools/r129_payload.py`. Both are exercised against the same test vectors in `host_test/` and `UI_rpi5/tools/test_r129_payload.py`, so firmware and host changes cannot silently drift apart.

## Directory layout

```
FW_nrf53/
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
    ├── prj.conf               # Zephyr + BLE Kconfig
    ├── sysbuild.conf          # sysbuild hints (netcore image)
    └── src/
        ├── main.c             # app entry, 1 Hz encode + notify + print loop
        ├── ble_diag.c/.h      # custom GATT service, diagnostics-stream notify
        └── uart_log.c/.h      # console heartbeat line + frame hex dump
```

The app is freestanding — it points at the shared NCS workspace at `/opt/nordic/ncs/v3.2.0` rather than carrying its own west manifest. This keeps this directory small (build artifacts aside) and avoids duplicating the ~2 GB SDK tree into the `R129/` git repo.

## Build + flash

All commands go through `./tools/ncs.sh`, which invokes `nrfutil toolchain-manager launch` for the NCS v3.2.0 bundle and exports `ZEPHYR_BASE` so `west build` resolves its extension commands even though this app is freestanding (lives outside the NCS workspace tree).

```bash
cd ~/R129/R129/FW_nrf53

# clean build from scratch
./tools/ncs.sh west build -b nrf5340dk/nrf5340/cpuapp app -d build -p always

# incremental rebuild
./tools/ncs.sh west build -d build

# flash to the DK over USB (uses nrfjprog via J-Link OB)
./tools/ncs.sh west flash -d build

# open a sub-shell with the toolchain on PATH (west, ninja, arm-zephyr-eabi-gcc...)
./tools/ncs.sh bash
```

Build products:
- `build/merged.hex`  — app core (nRF5340 cpuapp) image, contains our application + Zephyr + BT host
- `build/merged_CPUNET.hex`  — network core image (stock `ipc_radio` BT controller, auto-built by sysbuild)

`west flash` programs both cores in one shot.

### DK switch settings for bench development

| Switch | Position | Why |
|---|---|---|
| **SW8 (POWER)** | **ON** | Obvious, but easy to miss. LD5 (green) lights when on. |
| **SW6 (nRF ONLY / DEFAULT)** | **DEFAULT** | Must be DEFAULT for the J-Link interface MCU to enumerate on USB. `nRF ONLY` (used in the car to save 5 mA) disables J-Link and then `west flash` / UART both vanish. |
| **SW9 (VEXT → nRF)** | VDD (center) | Default. |
| Cable to | **J2** (short edge, "USB DEBUG") | J3 is wired to the nRF5340's own USB peripheral — unused by our firmware. |

### UART console over USB

The DK exposes two VCOMs. On macOS they show up as a pair of `tty.usbmodem*` ports with adjacent suffixes. **The higher-suffix one is UART0 on the app core** (where our `printk` output goes). Example observed on this Mac:

```
/dev/tty.usbmodem0010500648591   # silent (net core)
/dev/tty.usbmodem0010500648593   # app core UART0 — use this
```

```bash
screen /dev/tty.usbmodem0010500648593 115200
# expect, once per second:
#   R129-CTR <n> uptime=<ms> ms
#   R129-FRM AE 08 00 <uptime LE 4B> <counter LE 4B> <CRC HI> <CRC LO>
# exit: Ctrl-A  K  y
```

### Payload codec host tests

Runs on a plain system `cc` (Apple clang / gcc). No Zephyr, no NCS bundle needed.

```bash
cd ~/R129/R129/FW_nrf53/host_test
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
| `0x10` | `CMD_CLEAR` | reserved for M4 (RPi5 → nRF5340 clear-code request) | — |

Future types are additive — the stream characteristic never changes UUID.

## Roadmap

| Milestone | Content | Depends on |
|---|---|---|
| **M0** | BLE counter, UART log | Toolchain ✅ |
| **M1** | Framed payload library (encode / decode / CRC) | M0 ✅ |
| M2 | Stage-1 power board soldered; DK powered from board 5 V | Stage 1 hardware |
| M3 | ADS1115 I²C driver, real 4-channel analog telemetry (`0x02`) | M1, M2 |
| M4 | Blink-code RX + code-clear TX optocoupler path (`0x03` / `0x10`) | Stages 2–3 hardware |
| M5 | Full 9-channel X11 read, duty-cycle capture on KE pin 3 | Stages 6–7 hardware |
| M6 | Sleep / wake manager mode — PM + GPIO drive for Pi power | M5 |

## Hardware notes

See `work/nRF5430_interface_board/Breadboard_Build_Instructions.md` for the full hardware design. For M0–M1 the DK runs standalone on USB power with no interface board attached.
