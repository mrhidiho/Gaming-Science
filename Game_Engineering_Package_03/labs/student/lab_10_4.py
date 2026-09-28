"""Student exercise 10.4. Implement these contracts independently.
Run from the bundle root: python check_lab.py 10.4
The provided code checks do not grade proofs, modeling or the full lesson lab.
"""
from __future__ import annotations
import math
from collections.abc import Callable, Sequence

def descent_quadratic(x0: float, alpha: float, max_steps: int=100, tol: float=1e-08) -> dict:
    'Minimize (x-3)^2 by fixed-step gradient descent, returning explicit status.\nOnly finite, moderate-scale trajectories are supported. Nonfinite evaluation\nraises ArithmeticError, rather than serializing a misleading successful run.'
    raise NotImplementedError("Complete lesson 10.4 before this check can pass")

