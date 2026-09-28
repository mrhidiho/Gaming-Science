"""Lesson 36.1 computational slice.

Decode a five-byte educational SPI packet. Fields: mode, expected_mode, elapsed_us, timeout_us, expected_seq, frame. Modes 0..3, bytes 0..255. Packet [0xA5, seq, signed16_hi, signed16_lo, XOR of preceding bytes]. Deadline equality succeeds. The simulator knows endpoint mode metadata; real SPI mode faults are not always self-identifying.
"""
from __future__ import annotations

from labs.common import integer

def solve(case: dict) -> dict:
    mode=integer(case['mode'],'mode',maximum=3)
    expected=integer(case['expected_mode'],'expected_mode',maximum=3)
    elapsed=integer(case['elapsed_us'],'elapsed_us')
    timeout=integer(case['timeout_us'],'timeout_us',minimum=1)
    seq=integer(case['expected_seq'],'expected_seq',maximum=255)
    data=case['frame']
    if not isinstance(data,list): raise ValueError('frame must be a list')
    for b in data: integer(b,'byte',maximum=255)
    if mode != expected: return {'status':'mode_error'}
    if elapsed > timeout: return {'status':'timeout'}
    if len(data)!=5 or data[0]!=0xA5: return {'status':'framing_error'}
    check=0
    for b in data[:-1]: check ^= b
    if check!=data[-1]: return {'status':'checksum_error'}
    if data[1]!=seq: return {'status':'sequence_error'}
    raw=(data[2]<<8)|data[3]
    return {'status':'ok','value':raw if raw<32768 else raw-65536}
