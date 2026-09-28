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

def asset_key(source_bytes, settings, dependencies, tool_version):
    """Content key for a teaching cooker; dependency map is logical-id->content digest."""
    raise NotImplementedError('Complete exercise 25.1; see LAB_WORKBOOK.pdf')
