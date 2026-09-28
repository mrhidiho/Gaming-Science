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

def admit_bytes(budget, resident, existing_temporary, new_staging, new_resident):
    """Combined accounting model: old residency remains during replacement/upload."""
    vals=[integer(v,n) for n,v in [('budget',budget),('resident',resident),('temporary',existing_temporary),('new staging',new_staging),('new resident',new_resident)]]
    b,r,t,s,n=vals
    return r+t+s+n<=b
