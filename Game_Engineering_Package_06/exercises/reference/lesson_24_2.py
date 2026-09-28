"""Educational contract exercise. Python 3.11+; standard library only."""
import copy
import hashlib
import json
import math

def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)

def handle_valid(index, generation, slots):
    """slots is a sequence of {'alive': bool, 'generation': nonnegative int}."""
    integer(index,'index'); integer(generation,'generation')
    if index>=len(slots): return False
    slot=slots[index]
    if not isinstance(slot,dict) or not isinstance(slot.get('alive'),bool): raise ValueError('bad slot')
    integer(slot.get('generation'),'slot generation')
    return slot['alive'] and slot['generation']==generation
