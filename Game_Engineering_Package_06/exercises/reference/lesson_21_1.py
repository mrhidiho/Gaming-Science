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

def image_bytes(width, height, channels=4, row_alignment=1):
    """Return (row_stride,total_bytes); alignment may be any positive integer."""
    for n,v in [('width',width),('height',height),('channels',channels),('row_alignment',row_alignment)]:
        integer(v,n,1)
    row=width*channels
    stride=((row+row_alignment-1)//row_alignment)*row_alignment
    return stride,stride*height
