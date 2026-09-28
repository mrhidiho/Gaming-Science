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

def topo_order(dependencies):
    """Map task->prerequisite names. Return lexicographically stable topological order."""
    if not isinstance(dependencies,dict) or any(not isinstance(k,str) or not k for k in dependencies):
        raise ValueError('task names must be nonempty strings')
    pending={}
    for name,values in dependencies.items():
        if not isinstance(values,(list,tuple,set)) or any(not isinstance(v,str) for v in values):
            raise ValueError('prerequisite lists required')
        pending[name]=set(values)
    if any(d not in pending for deps in pending.values() for d in deps): raise ValueError('unknown dependency')
    result=[]
    while pending:
        ready=sorted(k for k,v in pending.items() if not v)
        if not ready: raise ValueError('dependency cycle')
        name=ready[0]; result.append(name); del pending[name]
        for deps in pending.values(): deps.discard(name)
    return result
