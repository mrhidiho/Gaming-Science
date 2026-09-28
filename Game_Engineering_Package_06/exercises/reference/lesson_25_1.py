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
    if not isinstance(source_bytes,bytes) or not isinstance(settings,dict) or not isinstance(dependencies,dict):
        raise ValueError('invalid key inputs')
    if not isinstance(tool_version,str) or not tool_version: raise ValueError('tool version required')
    if any(not isinstance(k,str) or not isinstance(v,str) for k,v in dependencies.items()): raise ValueError('invalid dependencies')
    try:
        payload=json.dumps({'source_sha256':hashlib.sha256(source_bytes).hexdigest(),'settings':settings,
            'dependencies':dependencies,'tool_version':tool_version},sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    except (TypeError,ValueError) as exc: raise ValueError('settings must be canonical JSON') from exc
    return hashlib.sha256(payload).hexdigest()
