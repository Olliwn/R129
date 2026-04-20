"""R129 diagnostics wire-format decoder, host-side mirror.

Counterpart to `FW_nrf53/payload/r129_payload.{h,c}`. Same frame layout:

    0       SYNC    1       = 0xAE
    1       LEN     1       = N (Data byte count)
    2       TYPE    1       r129_type_t
    3..2+N  DATA    N       type-specific
    3+N     CRC_HI  1       CRC-16/CCITT-FALSE MSB, over SYNC..DATA
    4+N     CRC_LO  1       CRC-16/CCITT-FALSE LSB
    total = 5 + N bytes

Integer fields inside DATA are little-endian. CRC itself is big-endian
on the wire so hex dumps read left-to-right.

Self-contained -- no bleak or other deps, plain stdlib. Unit tests live
next door in `test_r129_payload.py` but match the C-side vectors in
`FW_nrf53/host_test/test_payload.c` so the two ends stay in lockstep.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple

SYNC = 0xAE
HEADER_LEN = 3
CRC_LEN = 2
OVERHEAD = HEADER_LEN + CRC_LEN
MAX_DATA_LEN = 240
MAX_FRAME_LEN = OVERHEAD + MAX_DATA_LEN


class FrameType(IntEnum):
    HEARTBEAT = 0x00
    ANALOG = 0x02
    BLINK = 0x03
    CMD_CLEAR = 0x10


class FrameError(Exception):
    """Raised when a byte string cannot be interpreted as a frame."""


def crc16(data: bytes) -> int:
    """CRC-16/CCITT-FALSE. Poly 0x1021, init 0xFFFF, no reflect, xor-out 0."""
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def encode(frame_type: int, data: bytes = b"") -> bytes:
    """Encode one frame. Returns the raw bytes."""
    if len(data) > MAX_DATA_LEN:
        raise FrameError(f"data too long ({len(data)} > {MAX_DATA_LEN})")
    header = bytes([SYNC, len(data), int(frame_type)])
    body = header + data
    c = crc16(body)
    return body + bytes([(c >> 8) & 0xFF, c & 0xFF])


def decode(buf: bytes) -> Tuple[int, bytes, int]:
    """Decode one frame starting at buf[0].

    Returns (type, data, consumed_bytes). Raises FrameError on malformed input.
    """
    if len(buf) < HEADER_LEN:
        raise FrameError("truncated: need at least 3 bytes for header")
    if buf[0] != SYNC:
        raise FrameError(f"bad sync: 0x{buf[0]:02x} != 0x{SYNC:02x}")
    data_len = buf[1]
    if data_len > MAX_DATA_LEN:
        raise FrameError(f"bad length: {data_len} > {MAX_DATA_LEN}")
    total = OVERHEAD + data_len
    if len(buf) < total:
        raise FrameError(f"truncated: need {total} bytes, got {len(buf)}")
    frame_type = buf[2]
    data = bytes(buf[HEADER_LEN:HEADER_LEN + data_len])
    rx_crc = (buf[HEADER_LEN + data_len] << 8) | buf[HEADER_LEN + data_len + 1]
    want = crc16(buf[:HEADER_LEN + data_len])
    if rx_crc != want:
        raise FrameError(f"bad crc: 0x{rx_crc:04x} != 0x{want:04x}")
    return frame_type, data, total


# Typed payload helpers ------------------------------------------------------

@dataclass
class Heartbeat:
    uptime_ms: int
    counter: int

    _FMT = struct.Struct("<II")  # two le uint32

    @classmethod
    def from_bytes(cls, data: bytes) -> "Heartbeat":
        if len(data) != cls._FMT.size:
            raise FrameError(f"heartbeat expects {cls._FMT.size} bytes, got {len(data)}")
        up, cnt = cls._FMT.unpack(data)
        return cls(uptime_ms=up, counter=cnt)

    def to_bytes(self) -> bytes:
        return self._FMT.pack(self.uptime_ms, self.counter)


def decode_typed(buf: bytes) -> Tuple[FrameType, object, int]:
    """Decode one frame and (when known) return the parsed payload object.

    For an unknown type, the payload is returned as raw bytes.
    """
    raw_type, data, consumed = decode(buf)
    try:
        ft = FrameType(raw_type)
    except ValueError:
        return raw_type, data, consumed  # type: ignore[return-value]
    if ft is FrameType.HEARTBEAT:
        return ft, Heartbeat.from_bytes(data), consumed
    return ft, data, consumed


def pretty_hex(b: bytes) -> str:
    return " ".join(f"{x:02X}" for x in b)


__all__ = [
    "SYNC", "HEADER_LEN", "CRC_LEN", "OVERHEAD",
    "MAX_DATA_LEN", "MAX_FRAME_LEN",
    "FrameType", "FrameError", "Heartbeat",
    "crc16", "encode", "decode", "decode_typed", "pretty_hex",
]
