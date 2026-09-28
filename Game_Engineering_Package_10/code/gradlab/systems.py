"""Deterministic engine-system models with explicit, deliberately small contracts."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import hashlib
import json
from .numerical import solve_dense


def xpbd_scalar(predicted: float, rest: float, inverse_mass: float,
                compliance: float, dt: float, multiplier: float = 0.0):
    if dt <= 0 or inverse_mass < 0 or compliance < 0:
        raise ValueError("invalid XPBD parameters")
    scaled = compliance/(dt*dt)
    denominator = inverse_mass+scaled
    if denominator == 0:
        return predicted, multiplier  # Pinned hard constraint cannot move.
    dl = (-(predicted-rest)-scaled*multiplier)/denominator
    return predicted+inverse_mass*dl, multiplier+dl


def bar_step(u, v, *, dt, compliance, iterations=8, method="xpbd", gravity=-9.81):
    """Unit masses; 1D displacements, first particle pinned, adjacent springs.
    XPBD uses linear constraints, resets multipliers once per timestep, then
    accumulates across iterations. 'implicit' is an independent dense solve.
    This is not 3D cloth, collision response or nonlinear finite elements.
    """
    if len(u) != len(v) or len(u) < 2 or dt <= 0 or compliance <= 0 or iterations < 1:
        raise ValueError("invalid elastic bar")
    if method not in ("xpbd", "implicit"):
        raise ValueError("unknown method")
    n = len(u)
    y = [0.0]+[u[i]+dt*v[i]+dt*dt*gravity for i in range(1, n)]
    if method == "implicit":
        stiffness = dt*dt/compliance
        a = [[0.0]*(n-1) for _ in range(n-1)]
        for i in range(n-1):
            a[i][i] = 1+stiffness*(1 if i == n-2 else 2)
            if i: a[i][i-1] = -stiffness
            if i+1 < n-1: a[i][i+1] = -stiffness
        x = [0.0]+solve_dense(a, y[1:])
    else:
        x, lam = y[:], [0.0]*(n-1)
        scaled = compliance/(dt*dt)
        for _ in range(iterations):
            for i in range(n-1):
                wi, wj = (0.0 if i == 0 else 1.0), 1.0
                c = x[i+1]-x[i]
                dl = (-c-scaled*lam[i])/(wi+wj+scaled)
                x[i] -= wi*dl
                x[i+1] += wj*dl
                lam[i] += dl
    velocity = [0.0]+[(x[i]-u[i])/dt for i in range(1, n)]
    return x, velocity


def simulate_bar(n=6, dt=1/60, duration=.5, compliance=.001, iterations=8, method="xpbd"):
    steps = round(duration/dt)
    if n < 2 or steps < 1 or abs(steps*dt-duration) > 1e-9:
        raise ValueError("duration must be a positive integral number of timesteps")
    u, v = [0.0]*n, [0.0]*n
    trajectory = []
    for _ in range(steps):
        u, v = bar_step(u, v, dt=dt, compliance=compliance, iterations=iterations, method=method)
        trajectory.append(u[:])
    return dict(u=u, v=v, trajectory=trajectory, duration=steps*dt)


@dataclass(frozen=True)
class Request:
    asset: str
    size: int
    deadline: int
    epoch: int


class StreamModel:
    """One load per tick, bounded admission and residency, load-order eviction.
    Models metadata/data ownership, NOT real asynchronous I/O or device fences.
    """
    def __init__(self, budget: int, capacity: int):
        if budget <= 0 or capacity <= 0: raise ValueError("positive limits required")
        self.budget, self.capacity, self.epoch = budget, capacity, 0
        self.queue, self.resident, self.trace = [], {}, []
        self.peak = 0

    def request(self, r: Request) -> str:
        if r.size <= 0: raise ValueError("invalid asset size")
        if r.epoch != self.epoch: return "stale"
        if r.size > self.budget: return "oversize"
        if r.asset in self.resident or any(q.asset == r.asset for q in self.queue): return "duplicate"
        if len(self.queue) >= self.capacity: return "backpressure"
        self.queue.append(r)
        return "accepted"

    def teleport(self):
        self.epoch += 1
        self.queue.clear()
        # Old residents are placeholders until evicted; their bytes still count.
        self.trace.append(dict(event="teleport", epoch=self.epoch))

    def tick(self):
        if not self.queue: return None
        self.queue.sort(key=lambda r: (r.deadline, r.asset))
        r = self.queue.pop(0)
        while sum(self.resident.values())+r.size > self.budget:
            oldest = next(iter(self.resident))
            del self.resident[oldest]
            self.trace.append(dict(event="evict", asset=oldest))
        self.resident[r.asset] = r.size
        size = sum(self.resident.values())
        self.peak = max(self.peak, size)
        self.trace.append(dict(event="load", asset=r.asset, resident_bytes=size, epoch=self.epoch))
        return r.asset


class FencedStore:
    """Single atomic sink, persistent state assumed; NOT a consensus protocol.
    A monotonically increasing token is checked at the irreversible-effect sink.
    Deduplication is bounded and refuses new effects when full; no unsafe eviction.
    """
    def __init__(self, capacity=128):
        if capacity <= 0: raise ValueError("positive capacity required")
        self.epoch, self.owner, self.effects, self.capacity = 0, "A", {}, capacity

    def grant(self, owner: str, epoch: int):
        if epoch <= self.epoch: raise ValueError("epoch must increase")
        self.owner, self.epoch = owner, epoch

    def commit(self, owner: str, epoch: int, request_id: str, amount: int):
        if owner != self.owner or epoch != self.epoch: return "stale"
        if request_id in self.effects:
            return "duplicate" if self.effects[request_id] == amount else "conflict"
        if len(self.effects) >= self.capacity: return "backpressure"
        self.effects[request_id] = amount
        return "committed"


def lifecycle_check(bug=False):
    """Exhaustive BFS of a finite one-request lifecycle; returns shortest violation.
    State = (alive, issued, pending, callback_after_release). Safety only.
    No liveness proof is produced by this finite-state reachability checker.
    """
    initial = (True, False, False, False)
    queue = deque([(initial, [])]); seen = {initial}
    while queue:
        state, path = queue.popleft()
        alive, issued, pending, bad = state
        if bad: return dict(safe=False, visited=len(seen), counterexample=path)
        edges = []
        if alive and not issued:
            edges.append(("request", (alive, True, True, False)))
        if alive:
            edges.append(("release", (False, issued, pending, False)))
        if pending:
            # Correct callback dispatch guards owner lifetime; otherwise discards.
            edges.append(("complete", (alive, issued, False, not alive if bug else False)))
            edges.append(("cancel", (alive, issued, False, False)))
        for action, nxt in edges:
            if nxt not in seen:
                seen.add(nxt); queue.append((nxt, path+[action]))
    return dict(safe=True, visited=len(seen), counterexample=None)


def replay_hash(events):
    return hashlib.sha256(json.dumps(events, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()
