"""Lesson 37.4 computational slice.

Model one serialized request with setup, upload, compute, readback and synchronization. input_bytes/output_bytes count payload; bandwidth_Bps is effective payload bytes/second. For shared=True, use visibility_s instead of explicit copies. compute_s already includes kernel memory service. Only explicit transfer phases are removed; ownership and visibility costs remain.
"""
from __future__ import annotations

from labs.common import number, integer

def solve(case: dict) -> dict:
    inp=integer(case['input_bytes'],'input_bytes'); out=integer(case['output_bytes'],'output_bytes')
    bw=number(case['bandwidth_Bps'],'bandwidth_Bps',positive=True)
    setup=number(case['setup_s'],'setup_s',minimum=0)
    compute=number(case['compute_s'],'compute_s',minimum=0)
    sync=number(case['sync_s'],'sync_s',minimum=0)
    visibility=number(case['visibility_s'],'visibility_s',minimum=0)
    if not isinstance(case['shared'],bool): raise ValueError('shared must be Boolean')
    transfer=visibility if case['shared'] else (inp+out)/bw
    return {'transfer_or_visibility_s':transfer,'latency_s':setup+transfer+compute+sync}
