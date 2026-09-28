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

def lambert(rho, irradiance):
    """Passive diffuse reflection of incident irradiance (cosine already included)."""
    r=finite(rho,'rho'); e=finite(irradiance,'irradiance')
    if not 0<=r<=1 or e<0: raise ValueError('outside passive diffuse domain')
    return r*e/math.pi
