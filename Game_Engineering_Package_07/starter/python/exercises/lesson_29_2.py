"""Lesson 29.2: Timestamped snapshot interpolation.

Input nonempty snapshots [server_time,position], time render target. Maximum 4096 samples. Sort timestamps, deduplicate identical values, reject conflicting duplicate times and non-finite values. Linear interpolation inside bracket; hold nearest endpoint outside. Return position only; full lab must track hold/delay/recovery telemetry.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 29.2; see LAB_WORKBOOK.pdf")
