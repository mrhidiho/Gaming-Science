"""Lesson 26.4: Canonical replay and first divergence.

Input left and right lists of JSON-compatible state dictionaries. Return the zero-based first differing state index, or null when equal. Different lengths diverge at the first missing state. Canonicalize with sorted string keys and compact JSON, reject non-finite floats, cap trace length at 10000. This is a Python-environment encoding, not a cross-language wire specification.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 26.4; see LAB_WORKBOOK.pdf")
