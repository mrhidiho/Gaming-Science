"""Student exercise 09.3. Implement these contracts independently.
Run from the bundle root: python check_lab.py 09.3
The provided code checks do not grade proofs, modeling or the full lesson lab.
"""
from __future__ import annotations
import math
from collections.abc import Callable, Sequence

def percentile(values: Sequence[float], p: float) -> float:
    'Nearest-rank empirical percentile; p is a fraction in [0,1].'
    raise NotImplementedError("Complete lesson 09.3 before this check can pass")

def mean_interval(values: Sequence[float], critical: float) -> tuple[float, float, float]:
    'Mean and symmetric interval using caller-supplied critical value.\nInterpretation depends on the sampling model; no automatic coverage promise.'
    raise NotImplementedError("Complete lesson 09.3 before this check can pass")

