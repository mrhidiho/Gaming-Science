"""Sparse algebra, constrained fitting and run-level uncertainty; standard library only.
The examples expose assumptions and error reports rather than silently returning a value.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import random
from statistics import mean
from typing import Callable, Sequence


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise ValueError("dot: dimensions differ")
    return math.fsum(x*y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


@dataclass(frozen=True)
class CSR:
    """Square CSR with sorted, distinct column indices in each row."""
    n: int
    row: tuple[int, ...]
    col: tuple[int, ...]
    val: tuple[float, ...]

    def __post_init__(self):
        if self.n < 0 or len(self.row) != self.n+1 or self.row[0] != 0:
            raise ValueError("invalid CSR dimensions")
        if self.row[-1] != len(self.val) or len(self.col) != len(self.val):
            raise ValueError("invalid CSR storage lengths")
        if any(a > b for a, b in zip(self.row, self.row[1:])):
            raise ValueError("row offsets are not monotonic")
        if not all(math.isfinite(x) for x in self.val):
            raise ValueError("nonfinite coefficient")
        for i in range(self.n):
            c = self.col[self.row[i]:self.row[i+1]]
            if list(c) != sorted(set(c)) or any(j < 0 or j >= self.n for j in c):
                raise ValueError("invalid/duplicate/unsorted column index")

    @classmethod
    def from_dense(cls, a: Sequence[Sequence[float]]) -> 'CSR':
        n = len(a)
        if any(len(r) != n for r in a):
            raise ValueError("matrix must be square")
        row, col, val = [0], [], []
        for r in a:
            for j, v in enumerate(r):
                if v != 0:
                    col.append(j); val.append(float(v))
            row.append(len(val))
        return cls(n, tuple(row), tuple(col), tuple(val))

    def matvec(self, x: Sequence[float]) -> list[float]:
        if len(x) != self.n:
            raise ValueError("matvec dimensions differ")
        return [math.fsum(self.val[k]*x[self.col[k]]
                          for k in range(self.row[i], self.row[i+1]))
                for i in range(self.n)]

    def diagonal(self) -> list[float]:
        return [math.fsum(self.val[k] for k in range(self.row[i], self.row[i+1])
                          if self.col[k] == i) for i in range(self.n)]


def pcg(a: CSR, b: Sequence[float], *, rtol: float = 1e-10,
        atol: float = 1e-13, maxiter: int = 1000, jacobi: bool = False) -> dict:
    """PCG with zero initial guess and true-residual validation at completion.
    Caller must establish SPD. A positive p^T A p check is a breakdown detector,
    NOT a proof of symmetry or positive definiteness for all input vectors.
    """
    if len(b) != a.n or maxiter < 0 or rtol < 0 or atol < 0:
        raise ValueError("invalid PCG contract")
    if not all(math.isfinite(v) for v in b):
        raise ValueError("nonfinite RHS")
    d = a.diagonal() if jacobi else [1.0]*a.n
    if any(v <= 0 or not math.isfinite(v) for v in d):
        raise ValueError("Jacobi preconditioner must be positive")
    x, r = [0.0]*a.n, list(b)
    tol = max(atol, rtol*norm(b))
    z = [v/w for v, w in zip(r, d)]
    p, rz = z[:], dot(r, z)
    history = [norm(r)]
    steps = 0
    while norm(r) > tol and steps < maxiter:
        ap = a.matvec(p)
        pap = dot(p, ap)
        if pap <= 0 or not math.isfinite(pap):
            raise ArithmeticError("PCG breakdown: nonpositive/nonfinite curvature")
        alpha = rz/pap
        x = [v+alpha*w for v, w in zip(x, p)]
        r = [v-alpha*w for v, w in zip(r, ap)]
        steps += 1
        # Avoid declaring convergence solely on a recursively updated residual.
        if norm(r) <= tol:
            r = [v-w for v, w in zip(b, a.matvec(x))]
            if norm(r) > tol:
                z = [v/w for v, w in zip(r, d)]
                p, rz = z[:], dot(r, z)
                history.append(norm(r))
                continue
        history.append(norm(r))
        if norm(r) <= tol:
            break
        z = [v/w for v, w in zip(r, d)]
        new_rz = dot(r, z)
        beta = new_rz/rz
        p = [v+beta*w for v, w in zip(z, p)]
        rz = new_rz
    true = norm([v-w for v, w in zip(b, a.matvec(x))])
    return dict(x=x, iterations=steps, residual=true, tolerance=tol,
                converged=true <= tol, history=history)


def solve_dense(a: Sequence[Sequence[float]], b: Sequence[float]) -> list[float]:
    """Independent small dense Gaussian-elimination oracle with partial pivoting."""
    n = len(b)
    if len(a) != n or any(len(r) != n for r in a):
        raise ValueError("dense solve dimensions differ")
    m = [list(map(float, r))+[float(v)] for r, v in zip(a, b)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(m[i][k]))
        if m[pivot][k] == 0 or not math.isfinite(m[pivot][k]):
            raise ArithmeticError("singular/nonfinite pivot")
        m[k], m[pivot] = m[pivot], m[k]
        for i in range(k+1, n):
            scale = m[i][k]/m[k][k]
            for j in range(k, n+1):
                m[i][j] -= scale*m[k][j]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = (m[i][-1]-math.fsum(m[i][j]*x[j] for j in range(i+1, n)))/m[i][i]
    return x


def finite_gradient(f: Callable, x: Sequence[float], h: float = 1e-5) -> list[float]:
    if h <= 0 or not math.isfinite(h):
        raise ValueError("positive finite step required")
    out = []
    for i in range(len(x)):
        a, b = list(x), list(x)
        a[i] += h; b[i] -= h
        out.append((f(a)-f(b))/(2*h))
    return out


def constrained_fit(target: Sequence[float], total: float = 1.0) -> list[float]:
    """min 0.5 ||x-target||^2 subject to sum(x)=total; affine constraint only."""
    if not target:
        raise ValueError("empty target")
    lam = (math.fsum(target)-total)/len(target)
    return [v-lam for v in target]


def paired_bootstrap(baseline: Sequence[float], candidate: Sequence[float],
                     *, seed: int = 41, samples: int = 2000) -> dict:
    """Percentile bootstrap of geometric-mean paired run speedups.
    Pairs must be independent at the unit justified by the experiment.
    This routine does not repair correlated frames, tuning leakage or a bad design.
    """
    if len(baseline) != len(candidate) or len(baseline) < 2 or samples < 100:
        raise ValueError("need >=2 pairs and >=100 bootstrap resamples")
    if any(not math.isfinite(v) or v <= 0 for v in [*baseline, *candidate]):
        raise ValueError("positive finite durations required")
    ratios = [math.log(a/b) for a, b in zip(baseline, candidate)]
    rng = random.Random(seed)
    boot = sorted(math.exp(mean(rng.choices(ratios, k=len(ratios))))
                  for _ in range(samples))
    return dict(speedup=math.exp(mean(ratios)),
                lower=boot[int(.025*(samples-1))], upper=boot[int(.975*(samples-1))],
                pairs=len(ratios), method="paired run-level percentile bootstrap")
