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

def temporal_sample(current, history, weight, history_valid):
    """Scalar blend; caller supplies validity from reprojection/disocclusion tests."""
    c=finite(current,'current'); w=finite(weight,'history weight')
    if not 0<=w<=1 or not isinstance(history_valid,bool): raise ValueError('invalid policy')
    if not history_valid: return c
    h=finite(history,'history')
    return (1-w)*c+w*h
