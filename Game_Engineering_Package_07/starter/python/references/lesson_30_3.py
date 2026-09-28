"""Reference kernel for 30.3. Not a complete engine subsystem."""
from __future__ import annotations
import math

def finite(value: object, name: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, not a boolean")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def integer(value: object, name: str = "value", minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value

def solve(payload: dict) -> dict:
    import re
    if not isinstance(payload,dict) or set(payload)!={'version','title','textures'}:raise ValueError('mod fields')
    if type(payload['version'])is not int or payload['version']!=1:raise ValueError('unsupported version')
    if not isinstance(payload['title'],str) or not 1<=len(payload['title'])<=80:raise ValueError('title')
    textures=payload['textures']
    if not isinstance(textures,list) or len(textures)>16:raise ValueError('texture count')
    names=set(); total=0
    for item in textures:
        if not isinstance(item,dict) or set(item)!={'name','width','height'}:raise ValueError('texture schema')
        name=item['name']
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',name) or name in names:raise ValueError('texture name')
        names.add(name); w=integer(item['width'],minimum=1); h=integer(item['height'],minimum=1)
        if max(w,h)>2048:raise ValueError('dimension cap')
        total+=w*h*4
        if total>16*1024*1024:raise ValueError('total resource cap')
    return {'texture_count':len(textures),'total_bytes':total}
