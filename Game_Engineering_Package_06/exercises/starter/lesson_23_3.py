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

def attachment_bytes(width, height, bytes_per_pixel, samples=1):
    """Uncompressed attachment payload only; excludes driver tiling/metadata/padding."""
    raise NotImplementedError('Complete exercise 23.3; see LAB_WORKBOOK.pdf')
