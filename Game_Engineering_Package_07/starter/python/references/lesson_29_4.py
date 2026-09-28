"""Reference kernel for 29.4. Not a complete engine subsystem."""
from __future__ import annotations
import math

def finite(value: object, name: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, not a boolean")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def integer(value: object, name: str = "value", minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

def solve(payload: dict) -> dict:
    import copy
    if payload.get('principal')!='match_authority':raise ValueError('unauthorized principal')
    def operation(op):
        if not isinstance(op,dict) or set(op)!={'id','player','points'}:raise ValueError('operation schema')
        if any(not isinstance(op[k],str) or not 1<=len(op[k])<=64 for k in ('id','player')):raise ValueError('operation names')
        points=integer(op['points'])
        if points>1000:raise ValueError('reward bound')
        return dict(op)
    op=operation(payload['operation']); ledger=payload['ledger']; balances=payload['balances']
    if not isinstance(ledger,list) or len(ledger)>4096 or not isinstance(balances,dict) or len(balances)>4096:raise ValueError('store cap')
    ledger=[operation(x) for x in ledger]; balances=copy.deepcopy(balances)
    for name,value in balances.items():
        if not isinstance(name,str) or not 1<=len(name)<=64:raise ValueError('balance principal')
        integer(value)
    ids=set(); prior=None
    for old in ledger:
        if old['id'] in ids:raise ValueError('invalid duplicate stored id')
        ids.add(old['id'])
        if old['id']==op['id']:
            if old!=op:raise ValueError('idempotency conflict')
            prior=old
    if prior is not None:
        return {'ledger':ledger,'balances':balances,'applied':False}
    if len(ledger)>=4096:raise ValueError('store cap')
    ledger.append(op); balances[op['player']]=balances.get(op['player'],0)+op['points']
    return {'ledger':ledger,'balances':balances,'applied':True}
