"""Lesson 40.2 computational slice.

Apply a signed fixed-point affine transform with explicit rounding and saturation. x and gain are signed encoded integers with bits (2..32) and frac (0..bits-1) fractional bits. Compute nearest-even(x*gain / 2**frac) + bias, then saturate to bits. bias is an encoded signed integer in the same format. Return raw integer outputs; Python arbitrary-precision intermediates avoid overflow.
"""
from __future__ import annotations


def solve(case: dict) -> dict:
    """Implement the documented contract; do not import the reference solution."""
    raise NotImplementedError("Implement lesson 40.2")
