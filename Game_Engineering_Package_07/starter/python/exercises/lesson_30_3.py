"""Lesson 30.3: Bounded data-only mod schema.

Input is the mod object itself: exactly version=1, title (1..80 chars), textures (<=16) each exactly name,width,height. Name is unique [A-Za-z0-9_-]{1,64}; integer dimensions 1..2048; RGBA8; total <=16 MiB. Return texture_count,total_bytes. Reject unknown fields, booleans as dimensions, unsupported versions and excessive resources before allocating texture payloads.

Implement this kernel, then complete the full workbook lab and engine transfer.
Do not import the reference solution into your exercise.
"""
from __future__ import annotations

def solve(payload: dict) -> object:
    """Return the documented result; reject invalid inputs with ValueError."""
    raise NotImplementedError("Implement lesson 30.3; see LAB_WORKBOOK.pdf")
