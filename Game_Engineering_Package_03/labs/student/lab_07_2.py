"""Student exercise 07.2. Implement these contracts independently.
Run from the bundle root: python check_lab.py 07.2
The provided code checks do not grade proofs, modeling or the full lesson lab.
"""
from __future__ import annotations
import math
from collections.abc import Callable, Sequence

def matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    'Implement matmul; see LAB_WORKBOOK and the reference contract.'
    raise NotImplementedError("Complete lesson 07.2 before this check can pass")

def solve2(a: Sequence[Sequence[float]], b: Sequence[float], rtol: float=1e-12) -> tuple[float, float]:
    'Scaled elimination with partial pivoting. Reject relatively small pivots.\nThis is a two-by-two teaching solver, not a general conditioning certificate.'
    raise NotImplementedError("Complete lesson 07.2 before this check can pass")

