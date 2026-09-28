"""Lesson 39.3 computational slice.

Compute an educational stereo pose in meters with +Y up and -Z forward. Head yaw is right-handed about +Y. Constant linear velocity predicts head translation between sample_s and target_s (0..0.1 seconds ahead). Eye offsets +/-ipd_m/2 are rotated into world coordinates. tracking_valid=False returns no invented pose. This is not an OpenXR runtime implementation.
"""
from __future__ import annotations

import math
from labs.common import number

def solve(case: dict) -> dict:
    if not isinstance(case['tracking_valid'],bool): raise ValueError('tracking flag required')
    if not case['tracking_valid']: return {'render':'tracking_lost'}
    p=case['position_m']; v=case['velocity_mps']
    if len(p)!=3 or len(v)!=3: raise ValueError('three coordinates required')
    for x in p+v: number(x,'coordinate')
    ipd=number(case['ipd_m'],'ipd_m',positive=True)
    if ipd>.2: raise ValueError('outside educational IPD range')
    sample=number(case['sample_s'],'sample_s',minimum=0); target=number(case['target_s'],'target_s',minimum=0)
    dt=target-sample
    if not 0<=dt<=.1+1e-12: raise ValueError('prediction horizon outside contract')
    angle=math.radians(number(case['yaw_deg'],'yaw_deg')); cs=math.cos(angle); sn=math.sin(angle)
    center=[p[i]+v[i]*dt for i in range(3)]
    def eye(offset): return [round(center[0]+cs*offset,12),round(center[1],12),round(center[2]-sn*offset,12)]
    return {'render':'stereo_model','left_m':eye(-ipd/2),'right_m':eye(ipd/2),'prediction_s':dt}
