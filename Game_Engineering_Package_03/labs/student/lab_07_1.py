"""Student exercise 07.1. Implement these contracts independently.
Run from the bundle root: python check_lab.py 07.1
The provided code checks do not grade proofs, modeling or the full lesson lab.
"""
from __future__ import annotations
import math
from collections.abc import Callable, Sequence

def dot(a: Sequence[float], b: Sequence[float]) -> float:
    'Implement dot; see LAB_WORKBOOK and the reference contract.'
    raise NotImplementedError("Complete lesson 07.1 before this check can pass")

def normalize(v: Sequence[float]) -> tuple[float, ...]:
    'Scale first to avoid overflow/underflow in a direct sum of squares.'
    raise NotImplementedError("Complete lesson 07.1 before this check can pass")

