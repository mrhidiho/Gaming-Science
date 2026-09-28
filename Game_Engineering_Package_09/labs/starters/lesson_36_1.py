"""Lesson 36.1 computational slice.

Decode a five-byte educational SPI packet. Fields: mode, expected_mode, elapsed_us, timeout_us, expected_seq, frame. Modes 0..3, bytes 0..255. Packet [0xA5, seq, signed16_hi, signed16_lo, XOR of preceding bytes]. Deadline equality succeeds. The simulator knows endpoint mode metadata; real SPI mode faults are not always self-identifying.
"""
from __future__ import annotations


def solve(case: dict) -> dict:
    """Implement the documented contract; do not import the reference solution."""
    raise NotImplementedError("Implement lesson 36.1")
