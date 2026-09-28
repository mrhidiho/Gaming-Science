"""Student exercise 08.2. Implement these contracts independently.
Run from the bundle root: python check_lab.py 08.2
The provided code checks do not grade proofs, modeling or the full lesson lab.
"""
from __future__ import annotations
import math
from collections.abc import Callable, Sequence

def integrate(f: Callable[[float], float], a: float, b: float, n: int, method: str='trapezoid') -> float:
    'Signed quadrature using n panels; method is left or trapezoid.'
    raise NotImplementedError("Complete lesson 08.2 before this check can pass")

