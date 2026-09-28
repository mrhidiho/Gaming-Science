"""Lesson 40.3 computational slice.

Simulate one registered 4-byte-word buffer with explicit ownership. capacity is bytes. Events submit(offset,count), timeout, complete(epoch), reset. Submission validates alignment and subtraction-based bounds; zero count is rejected. A timeout quarantines the buffer and completion cannot release a quarantined buffer. reset models acknowledged device quiescence, advances epoch, and reclaims the buffer. No actual DMA occurs.
"""
from __future__ import annotations

from labs.common import integer

def solve(case: dict) -> dict:
    capacity=integer(case['capacity'],'capacity',1)
    owner='HOST'; epoch=0; pending=False; quarantined=False; statuses=[]
    for event in case['events']:
        op=event['op']
        if op=='submit':
            offset=event['offset']; count=event['count']
            valid=(type(offset) is int and type(count) is int and 0<=offset<=capacity and
                   offset%4==0 and count>0 and count<=(capacity-offset)//4)
            if owner!='HOST': statuses.append('busy')
            elif not valid: statuses.append('invalid_descriptor')
            else: owner='DEVICE'; pending=True; statuses.append('submitted')
        elif op=='timeout':
            if not pending: statuses.append('no_request')
            else: quarantined=True; statuses.append('quarantined')
        elif op=='complete':
            incoming=integer(event['epoch'],'epoch')
            if incoming!=epoch: statuses.append('stale_completion')
            elif not pending: statuses.append('no_request')
            elif quarantined: statuses.append('completion_ignored_quarantined')
            else: owner='HOST'; pending=False; statuses.append('completed')
        elif op=='reset':
            # Educational reset is an acknowledged quiescence operation, not just a write.
            epoch+=1; owner='HOST'; pending=False; quarantined=False; statuses.append('reset_quiesced')
        else: raise ValueError('unsupported operation')
    return {'statuses':statuses,'owner':owner,'epoch':epoch,'pending':pending,'quarantined':quarantined}
