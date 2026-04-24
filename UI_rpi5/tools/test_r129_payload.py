#!/usr/bin/env python3
"""Unit tests for r129_payload.py, matching FW_nrf/host_test/test_payload.c.

Keep these two files in lock-step: every test vector in the C suite has
a Python twin here, so a change on one side that breaks the other is
caught immediately. Run with::

    python3 -m unittest test_r129_payload.py
"""
from __future__ import annotations

import struct
import unittest

from r129_payload import (
    FrameError,
    FrameType,
    Heartbeat,
    MAX_DATA_LEN,
    MAX_FRAME_LEN,
    OVERHEAD,
    SYNC,
    crc16,
    decode,
    decode_typed,
    encode,
)


class TestCrc16(unittest.TestCase):
    def test_known_check_value(self):
        self.assertEqual(crc16(b"123456789"), 0x29B1)

    def test_empty(self):
        self.assertEqual(crc16(b""), 0xFFFF)

    def test_single_bit_sensitivity(self):
        self.assertNotEqual(crc16(b"\x00"), crc16(b"\x01"))


class TestRoundTrip(unittest.TestCase):
    def test_heartbeat(self):
        hb = Heartbeat(uptime_ms=0x12345678, counter=0xDEADBEEF)
        frame = encode(FrameType.HEARTBEAT, hb.to_bytes())
        self.assertEqual(len(frame), OVERHEAD + 8)
        self.assertEqual(frame[0], SYNC)
        self.assertEqual(frame[1], 8)
        self.assertEqual(frame[2], FrameType.HEARTBEAT)
        self.assertEqual(frame[3], 0x78)   # uptime LSB
        self.assertEqual(frame[6], 0x12)   # uptime MSB
        self.assertEqual(frame[7], 0xEF)   # counter LSB
        self.assertEqual(frame[10], 0xDE)  # counter MSB

        ft, data, consumed = decode(frame)
        self.assertEqual(consumed, len(frame))
        self.assertEqual(ft, FrameType.HEARTBEAT)
        hb2 = Heartbeat.from_bytes(data)
        self.assertEqual(hb2, hb)

    def test_zero_length(self):
        frame = encode(FrameType.CMD_CLEAR, b"")
        self.assertEqual(len(frame), OVERHEAD)
        ft, data, consumed = decode(frame)
        self.assertEqual(ft, FrameType.CMD_CLEAR)
        self.assertEqual(data, b"")
        self.assertEqual(consumed, OVERHEAD)

    def test_max_length(self):
        payload = bytes((i * 31 + 7) & 0xFF for i in range(MAX_DATA_LEN))
        frame = encode(FrameType.ANALOG, payload)
        self.assertEqual(len(frame), MAX_FRAME_LEN)
        ft, data, consumed = decode(frame)
        self.assertEqual(ft, FrameType.ANALOG)
        self.assertEqual(data, payload)
        self.assertEqual(consumed, MAX_FRAME_LEN)

    def test_over_max_length(self):
        with self.assertRaises(FrameError):
            encode(FrameType.ANALOG, b"\x00" * (MAX_DATA_LEN + 1))


class TestDecodeErrors(unittest.TestCase):
    def _good(self):
        return encode(FrameType.HEARTBEAT, b"ab")

    def test_bad_sync(self):
        f = bytearray(self._good())
        f[0] = 0x00
        with self.assertRaises(FrameError):
            decode(bytes(f))

    def test_bad_crc(self):
        f = bytearray(self._good())
        f[3] ^= 0x01
        with self.assertRaises(FrameError):
            decode(bytes(f))

    def test_truncated(self):
        f = self._good()
        with self.assertRaises(FrameError):
            decode(f[:1])
        with self.assertRaises(FrameError):
            decode(f[:-1])
        # full length: succeeds
        decode(f)

    def test_bad_length_byte(self):
        bogus = bytes([SYNC, MAX_DATA_LEN + 1, 0])
        with self.assertRaises(FrameError):
            decode(bogus)


class TestBackToBack(unittest.TestCase):
    """RPi5 consumer: two frames concatenated in one buffer."""

    def test_stream(self):
        f1 = encode(FrameType.HEARTBEAT, Heartbeat(1000, 1).to_bytes())
        f2 = encode(FrameType.HEARTBEAT, Heartbeat(2000, 2).to_bytes())
        stream = f1 + f2

        pos = 0
        ft, hb_bytes, consumed = decode(stream[pos:])
        self.assertEqual(ft, FrameType.HEARTBEAT)
        self.assertEqual(Heartbeat.from_bytes(hb_bytes).counter, 1)
        pos += consumed

        ft, hb_bytes, consumed = decode(stream[pos:])
        self.assertEqual(Heartbeat.from_bytes(hb_bytes).counter, 2)
        pos += consumed

        self.assertEqual(pos, len(stream))


class TestTypedDecode(unittest.TestCase):
    def test_heartbeat_typed(self):
        hb = Heartbeat(uptime_ms=42_000, counter=7)
        frame = encode(FrameType.HEARTBEAT, hb.to_bytes())
        ft, obj, consumed = decode_typed(frame)
        self.assertEqual(ft, FrameType.HEARTBEAT)
        self.assertIsInstance(obj, Heartbeat)
        self.assertEqual(obj, hb)
        self.assertEqual(consumed, len(frame))


class TestCrossImplVector(unittest.TestCase):
    """Byte-for-byte vector that also appears in test_payload.c."""

    def test_heartbeat_deadbeef(self):
        hb = Heartbeat(uptime_ms=0x12345678, counter=0xDEADBEEF)
        frame = encode(FrameType.HEARTBEAT, hb.to_bytes())
        # SYNC LEN TYPE  uptime(le)   counter(le)   CRC
        # AE   08  00    78 56 34 12  EF BE AD DE   ?? ??
        expected_prefix = bytes.fromhex("AE 08 00 78 56 34 12 EF BE AD DE".replace(" ", ""))
        self.assertEqual(frame[:11], expected_prefix)
        # CRC is deterministic; compute and cross-check
        expected_crc = crc16(expected_prefix)
        self.assertEqual(frame[11], (expected_crc >> 8) & 0xFF)
        self.assertEqual(frame[12], expected_crc & 0xFF)
        # Full frame round-trips
        self.assertEqual(len(frame), 13)
        _, data, _ = decode(frame)
        self.assertEqual(struct.unpack("<II", data), (hb.uptime_ms, hb.counter))


if __name__ == "__main__":
    unittest.main()
