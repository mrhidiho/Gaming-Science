"""Educational reference mathematics for Package 03. Python standard library only.

These routines expose small, testable contracts, not a production numerical library.
Inputs are finite built-in int/float values (booleans are rejected). Functions raise
ValueError for invalid domains/dimensions. Nonfinite arithmetic fails explicitly;
ArithmeticError/OverflowError or a standard-library ValueError may be raised for
unsupported extreme intermediates. These are not arbitrary-range solvers.
"""
from __future__ import annotations
import math
from collections import deque
from collections.abc import Callable, Sequence


def real(x: float, name: str = 'value') -> float:
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(f'{name} must be a finite int or float, not bool')
    try:
        y = float(x)
    except OverflowError as exc:
        raise ValueError(f'{name} is outside the supported float range') from exc
    if not math.isfinite(y):
        raise ValueError(f'{name} must be finite')
    return y


def integer(n: int, name: str = 'count', minimum: int = 0) -> int:
    if type(n) is not int or n < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')
    return n


def finite_result(x: float) -> float:
    if not math.isfinite(x):
        raise ArithmeticError('nonfinite intermediate/result; rescale the problem')
    return x


def vector(v: Sequence[float], name: str = 'vector') -> tuple[float, ...]:
    if not isinstance(v, (list, tuple)) or not v:
        raise ValueError(f'{name} must be a nonempty list/tuple')
    return tuple(real(x, name) for x in v)


def travel_time(distance: float, speed: float) -> float:
    """Nonnegative distance / strictly positive speed, with consistent units."""
    d, s = real(distance, 'distance'), real(speed, 'speed')
    if d < 0 or s <= 0:
        raise ValueError('distance >= 0 and speed > 0 are required')
    return finite_result(d / s)


def implies(p: bool, q: bool) -> bool:
    """Material implication, for actual Boolean operands."""
    if type(p) is not bool or type(q) is not bool:
        raise ValueError('p and q must be bool')
    return (not p) or q


def count_positive_prefix(values: Sequence[float], k: int) -> int:
    """Count values > 0 in values[:k]; input values must all be finite."""
    if not isinstance(values, (list, tuple)):
        raise ValueError('values must be a list/tuple')
    checked = [real(x) for x in values]
    integer(k, 'k')
    if k > len(checked):
        raise ValueError('k exceeds the input length')
    count = 0
    for i in range(k):
        if checked[i] > 0:
            count += 1
    return count


def halving_steps(n: int) -> int:
    """Repeated floor division by 2 until n <= 1; n must be positive."""
    integer(n, 'n', 1)
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


def topological_order(graph: dict[str, list[str]]) -> list[str]:
    """Edges mean prerequisite -> dependent. Stable lexicographic tie policy.
    Every node must have a key, duplicate edges are rejected, cycles raise ValueError.
    """
    if not isinstance(graph, dict) or any(not isinstance(k, str) for k in graph):
        raise ValueError('graph must be a dictionary with string nodes')
    indegree = {k: 0 for k in graph}
    for edges in graph.values():
        if not isinstance(edges, (list, tuple)) or any(not isinstance(v, str) for v in edges):
            raise ValueError('neighbors must be lists/tuples of string nodes')
        if len(edges) != len(set(edges)) or any(v not in graph for v in edges):
            raise ValueError('duplicate edge or missing node key')
        for v in edges:
            indegree[v] += 1
    ready = sorted(v for v, d in indegree.items() if d == 0)
    order: list[str] = []
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
                ready.sort()
    if len(order) != len(graph):
        raise ValueError('dependency cycle')
    return order


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    a, b = vector(a), vector(b)
    if len(a) != len(b):
        raise ValueError('vector dimensions differ')
    return finite_result(math.fsum(x * y for x, y in zip(a, b)))


def normalize(v: Sequence[float]) -> tuple[float, ...]:
    """Scale first to avoid overflow/underflow in a direct sum of squares."""
    v = vector(v)
    scale = max(abs(x) for x in v)
    if scale == 0:
        raise ValueError('zero vector has no unique direction')
    scaled = tuple(x / scale for x in v)
    length = math.hypot(*scaled)
    return tuple(x / length for x in scaled)


def matrix(a: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    if not isinstance(a, (list, tuple)) or not a:
        raise ValueError('matrix must have at least one row')
    rows = tuple(vector(r, 'matrix row') for r in a)
    if any(len(r) != len(rows[0]) for r in rows):
        raise ValueError('ragged matrix')
    return rows


def matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    a, b = matrix(a), matrix(b)
    if len(a[0]) != len(b):
        raise ValueError('inner matrix dimensions differ')
    return tuple(tuple(finite_result(math.fsum(a[i][k] * b[k][j] for k in range(len(b))))
                       for j in range(len(b[0]))) for i in range(len(a)))


def solve2(a: Sequence[Sequence[float]], b: Sequence[float], rtol: float = 1e-12) -> tuple[float, float]:
    """Scaled elimination with partial pivoting. Reject relatively small pivots.
    This is a two-by-two teaching solver, not a general conditioning certificate.
    """
    a, b = matrix(a), vector(b)
    tol = real(rtol, 'rtol')
    if len(a) != 2 or len(a[0]) != 2 or len(b) != 2 or not 0 <= tol < 1:
        raise ValueError('two-by-two system and 0 <= rtol < 1 required')
    scale = max(abs(x) for row in a for x in row)
    if scale == 0:
        raise ValueError('singular system')
    rows = [[finite_result(x / scale) for x in row] + [finite_result(y / scale)]
            for row, y in zip(a, b)]
    if abs(rows[1][0]) > abs(rows[0][0]):
        rows.reverse()
    if abs(rows[0][0]) <= tol:
        raise ValueError('singular or numerically small first pivot')
    multiplier = rows[1][0] / rows[0][0]
    rows[1][1] -= multiplier * rows[0][1]
    rows[1][2] -= multiplier * rows[0][2]
    if abs(rows[1][1]) <= tol:
        raise ValueError('singular or numerically small second pivot')
    y = finite_result(rows[1][2] / rows[1][1])
    x = finite_result((rows[0][2] - rows[0][1] * y) / rows[0][0])
    return x, y


def transform4(m: Sequence[Sequence[float]], v: Sequence[float]) -> tuple[float, ...]:
    """Column-vector homogeneous multiply, without perspective division."""
    m, v = matrix(m), vector(v)
    if len(m) != 4 or len(m[0]) != 4 or len(v) != 4:
        raise ValueError('4x4 matrix and four-component vector required')
    return tuple(dot(row, v) for row in m)


def translation(x: float, y: float, z: float) -> tuple[tuple[float, ...], ...]:
    x, y, z = real(x), real(y), real(z)
    return ((1., 0., 0., x), (0., 1., 0., y), (0., 0., 1., z), (0., 0., 0., 1.))


def rotation_z(theta: float) -> tuple[tuple[float, ...], ...]:
    theta = real(theta, 'radian angle')
    c, s = math.cos(theta), math.sin(theta)
    return ((c, -s, 0., 0.), (s, c, 0., 0.), (0., 0., 1., 0.), (0., 0., 0., 1.))


def quat_rotate(q: Sequence[float], v: Sequence[float]) -> tuple[float, float, float]:
    """Normalize scalar-first q=(w,x,y,z); active right-handed rotation."""
    q, v = vector(q), vector(v)
    if len(q) != 4 or len(v) != 3:
        raise ValueError('quaternion length 4 and vector length 3 required')
    w, x, y, z = normalize(q)
    vx, vy, vz = v
    # t = 2 * cross(q.xyz, v); v' = v + w*t + cross(q.xyz, t)
    tx, ty, tz = 2*(y*vz-z*vy), 2*(z*vx-x*vz), 2*(x*vy-y*vx)
    return tuple(finite_result(a) for a in (vx+w*tx+y*tz-z*ty,
                                         vy+w*ty+z*tx-x*tz,
                                         vz+w*tz+x*ty-y*tx))


def fit_line(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float]:
    """Return slope, intercept for unweighted ordinary least squares with intercept."""
    xs, ys = vector(xs), vector(ys)
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError('at least two paired observations required')
    mx, my = math.fsum(xs)/len(xs), math.fsum(ys)/len(ys)
    xx = finite_result(math.fsum((x-mx)**2 for x in xs))
    if xx == 0:
        raise ValueError('predictor has no resolvable variation')
    xy = finite_result(math.fsum((x-mx)*(y-my) for x, y in zip(xs, ys)))
    slope = finite_result(xy / xx)
    return slope, finite_result(my - slope*mx)


def centered_difference(f: Callable[[float], float], x: float, h: float) -> float:
    x, h = real(x), real(h, 'h')
    if h <= 0 or x+h == x or x-h == x:
        raise ValueError('positive resolvable h required')
    return finite_result((real(f(x+h), 'f(x+h)') - real(f(x-h), 'f(x-h)'))/(2*h))


def integrate(f: Callable[[float], float], a: float, b: float, n: int, method: str = 'trapezoid') -> float:
    """Signed quadrature using n panels; method is left or trapezoid."""
    a, b = real(a), real(b)
    integer(n, 'n', 1)
    if method not in ('left', 'trapezoid'):
        raise ValueError('method must be left or trapezoid')
    if a == b:
        return 0.
    h = finite_result((b-a)/n)
    if a+h == a:
        raise ValueError('panel width is not resolvable at this scale')
    if method == 'left':
        total = math.fsum(real(f(a+i*h), 'function value') for i in range(n))
    else:
        total = 0.5*(real(f(a), 'f(a)')+real(f(b), 'f(b)'))
        total += math.fsum(real(f(a+i*h), 'function value') for i in range(1, n))
    return finite_result(h * total)


def constant_acceleration(x0: float, v0: float, a: float, t: float) -> tuple[float, float]:
    x0, v0, a, t = real(x0), real(v0), real(a), real(t)
    if t < 0:
        raise ValueError('t must be nonnegative')
    return finite_result(x0+v0*t+0.5*a*t*t), finite_result(v0+a*t)


def spring_step(x: float, v: float, mass: float, stiffness: float, damping: float,
                dt: float, method: str = 'semi') -> tuple[float, float]:
    x, v, m, k, c, dt = (real(z) for z in (x, v, mass, stiffness, damping, dt))
    if m <= 0 or k < 0 or c < 0 or dt < 0 or method not in ('explicit', 'semi'):
        raise ValueError('m>0, k>=0, c>=0, dt>=0 and a valid method are required')
    a = finite_result((-k*x-c*v)/m)
    vn = finite_result(v+a*dt)
    xn = finite_result(x+(v if method == 'explicit' else vn)*dt)
    return xn, vn


def posterior_bug(prior: float, sensitivity: float, false_positive: float) -> float:
    p, s, f = (real(z) for z in (prior, sensitivity, false_positive))
    if any(not 0 <= z <= 1 for z in (p, s, f)):
        raise ValueError('probabilities must lie in [0,1]')
    denominator = p*s+(1-p)*f
    if denominator == 0:
        raise ValueError('conditioning event has probability zero')
    return p*s/denominator


def weighted_index(weights: Sequence[float], u: float) -> int:
    """u in [0,1); weights finite/nonnegative with finite positive sum."""
    weights, u = vector(weights), real(u)
    if any(w < 0 for w in weights) or not 0 <= u < 1:
        raise ValueError('negative weight or u outside [0,1)')
    total = finite_result(math.fsum(weights))
    if total <= 0:
        raise ValueError('total weight must be positive')
    # Compare against normalized cumulative boundaries; skip zero-width bins.
    running = 0.
    last_positive = 0
    for i, w in enumerate(weights):
        running += w/total
        if w > 0:
            last_positive = i
            if u < running:
                return i
    return last_positive  # handles rounding of the last cumulative boundary


def percentile(values: Sequence[float], p: float) -> float:
    """Nearest-rank empirical percentile; p is a fraction in [0,1]."""
    values, p = vector(values), real(p)
    if not 0 <= p <= 1:
        raise ValueError('p outside [0,1]')
    ordered = sorted(values)
    return ordered[max(0, math.ceil(p*len(ordered))-1)]


def mean_interval(values: Sequence[float], critical: float) -> tuple[float, float, float]:
    """Mean and symmetric interval using caller-supplied critical value.
    Interpretation depends on the sampling model; no automatic coverage promise.
    """
    values, critical = vector(values), real(critical)
    if len(values) < 2 or critical <= 0:
        raise ValueError('two values and a positive critical value required')
    n = len(values)
    mean = math.fsum(values)/n
    variance = finite_result(math.fsum((x-mean)**2 for x in values)/(n-1))
    half = critical * math.sqrt(variance/n)
    return mean, finite_result(mean-half), finite_result(mean+half)


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    actual, predicted = vector(actual), vector(predicted)
    if len(actual) != len(predicted):
        raise ValueError('paired lengths differ')
    return finite_result(math.sqrt(math.fsum((a-b)**2 for a,b in zip(actual,predicted))/len(actual)))


def gradient(f: Callable[[tuple[float, ...]], float], point: Sequence[float], h: float) -> tuple[float, ...]:
    point, h = vector(point), real(h)
    if h <= 0:
        raise ValueError('h must be positive')
    result = []
    for i, x in enumerate(point):
        if x+h == x or x-h == x:
            raise ValueError('h is not resolvable at this coordinate scale')
        plus, minus = list(point), list(point)
        plus[i] += h
        minus[i] -= h
        result.append(finite_result((real(f(tuple(plus)))-real(f(tuple(minus))))/(2*h)))
    return tuple(result)


def alias_frequency(frequency: float, sample_rate: float) -> float:
    """Baseband alias magnitude in [0, fs/2]; does not encode phase/sign."""
    f, fs = real(frequency), real(sample_rate)
    if fs <= 0 or f < 0:
        raise ValueError('frequency >= 0 and sample_rate > 0 required')
    r = f % fs
    return min(r, fs-r)


def convolve(signal: Sequence[float], kernel: Sequence[float]) -> list[float]:
    """Full zero-extended convolution; output length N+K-1, or [] for N=0."""
    if not isinstance(signal, (list, tuple)):
        raise ValueError('signal must be a list/tuple')
    h = vector(kernel, 'kernel')
    if not signal:
        return []
    x = vector(signal, 'signal')
    return [finite_result(math.fsum(h[k]*x[n-k] for k in range(len(h)) if 0 <= n-k < len(x)))
            for n in range(len(x)+len(h)-1)]


def descent_quadratic(x0: float, alpha: float, max_steps: int = 100, tol: float = 1e-8) -> dict:
    """Minimize (x-3)^2 by fixed-step gradient descent, returning explicit status.
    Only finite, moderate-scale trajectories are supported. Nonfinite evaluation
    raises ArithmeticError, rather than serializing a misleading successful run.
    """
    x, alpha, tol = real(x0), real(alpha), real(tol)
    integer(max_steps, 'max_steps')
    if alpha <= 0 or tol <= 0:
        raise ValueError('alpha and tol must be positive')
    history = [x]
    for step in range(max_steps+1):
        g = finite_result(2*(x-3))
        if abs(g) <= tol or step == max_steps:
            try:
                value = finite_result((x-3)**2)
            except OverflowError as exc:
                raise ArithmeticError('quadratic overflow') from exc
            converged = abs(g) <= tol
            return dict(x=x, value=value, gradient=g, iterations=step,
                        converged=converged, reason='gradient_tolerance' if converged else 'iteration_limit',
                        history=history)
        x = finite_result(x-alpha*g)
        history.append(x)
    raise AssertionError('unreachable')
