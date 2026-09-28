"""CPU semantic models. Timings from this file are NOT GPU measurements."""
from __future__ import annotations
import heapq
import math
from typing import Sequence


def tree_sum(values: Sequence[int | float]) -> int | float:
    work = list(values)
    if not work:
        return 0
    while len(work) > 1:
        work = [work[i] + (work[i+1] if i+1 < len(work) else 0)
                for i in range(0, len(work), 2)]
    return work[0]


def exclusive_scan(values: Sequence[int]) -> list[int]:
    """Blelloch upsweep/downsweep, padded to next power of two, integer monoid."""
    n = len(values)
    if n == 0:
        return []
    m = 1 << (n-1).bit_length()
    a = list(values)+[0]*(m-n)
    stride = 2
    while stride <= m:
        for j in range(stride-1, m, stride):
            a[j] += a[j-stride//2]
        stride *= 2
    a[-1] = 0
    stride = m
    while stride >= 2:
        for j in range(stride-1, m, stride):
            left = j-stride//2
            t = a[left]
            a[left] = a[j]
            a[j] += t
        stride //= 2
    return a[:n]


def compact(values: Sequence, keep: Sequence[bool]) -> list:
    if len(values) != len(keep):
        raise ValueError("lengths differ")
    flags = [int(bool(k)) for k in keep]
    offsets = exclusive_scan(flags)
    out = [None]*sum(flags)
    for v, flag, offset in zip(values, flags, offsets):
        if flag:
            out[offset] = v
    return out


def tiled_gemm(a: list[list[float]], b: list[list[float]], tile: int = 4) -> list[list[float]]:
    if tile < 1 or not a or not b:
        raise ValueError("nonempty matrices and positive tile required")
    m, k, n = len(a), len(b), len(b[0])
    if n == 0 or any(len(r) != k for r in a) or any(len(r) != n for r in b):
        raise ValueError("incompatible/ragged matrices")
    c = [[0.0]*n for _ in range(m)]
    for i0 in range(0, m, tile):
        for j0 in range(0, n, tile):
            for k0 in range(0, k, tile):
                for i in range(i0, min(i0+tile, m)):
                    for j in range(j0, min(j0+tile, n)):
                        for q in range(k0, min(k0+tile, k)):
                            c[i][j] += a[i][q]*b[q][j]
    return c


def scheduling_model(costs: Sequence[float], workers: int, *, dynamic: bool,
                     overhead: float = 0.0) -> dict:
    """Indivisible jobs, deterministic list scheduling, no arrivals/contention."""
    if workers <= 0 or overhead < 0 or any(x < 0 or not math.isfinite(x) for x in costs):
        raise ValueError("invalid scheduler input")
    trace = []
    if dynamic:
        free = [(0.0, i) for i in range(workers)]
        heapq.heapify(free)
        for job, cost in enumerate(costs):
            start, worker = heapq.heappop(free)
            end = start+cost+overhead
            trace.append((job, worker, start, end))
            heapq.heappush(free, (end, worker))
        loads = [t for t, _ in free]
    else:
        loads = [0.0]*workers
        for job, cost in enumerate(costs):
            worker = job % workers
            start = loads[worker]
            loads[worker] += cost
            trace.append((job, worker, start, loads[worker]))
    return dict(makespan=max(loads, default=0.0), trace=trace,
                lower_bound=max(sum(costs)/workers, max(costs, default=0.0)))


def pipeline_trace(tiles: int, copy: float, compute: float) -> dict:
    """Two buffers, one copy engine, one compute engine, explicit slot lifetime.
    Analytical schedule only: no device API is used here.
    """
    if tiles < 0 or copy < 0 or compute < 0:
        raise ValueError("negative work")
    slot_free = [0.0, 0.0]
    copy_free = compute_free = 0.0
    trace = []
    for i in range(tiles):
        slot = i % 2
        begin = max(copy_free, slot_free[slot])
        ready = begin+copy
        run = max(ready, compute_free)
        end = run+compute
        trace.append(dict(tile=i, slot=slot, copy_start=begin, ready=ready,
                          compute_start=run, end=end))
        copy_free, compute_free, slot_free[slot] = ready, end, end
    return dict(total=compute_free, trace=trace)


def roofline(flops: float, bytes_moved: float, peak_flops_s: float, bandwidth_bytes_s: float) -> dict:
    if min(flops, bytes_moved, peak_flops_s, bandwidth_bytes_s) <= 0:
        raise ValueError("positive model inputs required")
    intensity = flops/bytes_moved
    bound = min(peak_flops_s, intensity*bandwidth_bytes_s)
    return dict(intensity=intensity, bound_flops_s=bound, lower_time_s=flops/bound)
