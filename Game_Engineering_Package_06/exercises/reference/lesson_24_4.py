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

def validate_scene(document):
    """Validate a candidate, migrate v1 positions, return new v2 object; never mutate input."""
    if not isinstance(document,dict): raise ValueError('scene must be object')
    doc=copy.deepcopy(document); ver=doc.get('version')
    if type(ver) is not int or ver not in (1,2): raise ValueError('unsupported scene version')
    entities=doc.get('entities')
    if not isinstance(entities,list) or len(entities)>100000: raise ValueError('bad entity list')
    ids=set(); out=[]
    for e in entities:
        if not isinstance(e,dict): raise ValueError('entity must be object')
        ident=e.get('id')
        if not isinstance(ident,str) or not ident or len(ident)>128 or ident in ids: raise ValueError('invalid/duplicate id')
        ids.add(ident); p=e.get('position')
        if ver==1:
            if not isinstance(p,dict) or set(p)!=set('xyz'): raise ValueError('v1 position requires x,y,z')
            p=[p[k] for k in 'xyz']
        if not isinstance(p,(list,tuple)) or len(p)!=3: raise ValueError('position requires three values')
        p=[finite(x,'position') for x in p]
        if any(abs(x)>1e6 for x in p): raise ValueError('position exceeds policy bound')
        out.append({'id':ident,'position':p})
    return {'version':2,'entities':out}
