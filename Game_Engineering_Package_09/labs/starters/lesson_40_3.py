"""Lesson 40.3 computational slice.

Simulate one registered 4-byte-word buffer with explicit ownership. capacity is bytes. Events submit(offset,count), timeout, complete(epoch), reset. Submission validates alignment and subtraction-based bounds; zero count is rejected. A timeout quarantines the buffer and completion cannot release a quarantined buffer. reset models acknowledged device quiescence, advances epoch, and reclaims the buffer. No actual DMA occurs.
"""
from __future__ import annotations


def solve(case: dict) -> dict:
    """Implement the documented contract; do not import the reference solution."""
    raise NotImplementedError("Implement lesson 40.3")
