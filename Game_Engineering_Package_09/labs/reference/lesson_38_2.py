"""Lesson 38.2 computational slice.

Summarize raw times only after every output checksum passes. Fields: times_ns, checksums, expected_checksum, warmup (number of leading samples excluded). Positive finite times required; all samples, including warmup, must validate. Report retained n, mean, median and nearest-rank p95; no post-hoc outlier removal.
"""
from __future__ import annotations

import statistics
from labs.common import number, integer, nearest_rank

def solve(case: dict) -> dict:
    times=case['times_ns']; sums=case['checksums']
    if not times or len(times)!=len(sums): raise ValueError('nonempty matching samples required')
    warm=integer(case['warmup'],'warmup',maximum=len(times)-1)
    for t in times: number(t,'time_ns',positive=True)
    if any(s!=case['expected_checksum'] for s in sums): return {'status':'rejected_wrong_output'}
    kept=times[warm:]
    return {'status':'ok','n':len(kept),'mean_ns':statistics.mean(kept),
            'median_ns':statistics.median(kept),'p95_ns':nearest_rank(kept,.95),'excluded_warmup':warm}
