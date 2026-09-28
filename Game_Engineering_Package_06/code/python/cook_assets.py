#!/usr/bin/env python3
"""Deterministic, content-addressed teaching cooker. No untrusted-code execution.
Formats documented in ENGINE_REFERENCE.pdf. Atomic rename is not a power-loss durability proof.
"""
from __future__ import annotations
import argparse,hashlib,json,math,os,pathlib,struct,tempfile
TOOL_VERSION='ge-cooker-1'
MAX_SOURCE_BYTES=16*1024*1024

def canonical(value: object)->bytes:
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf8')

def digest(data: bytes)->str:
    return hashlib.sha256(data).hexdigest()

def read_source(path: pathlib.Path)->tuple[bytes,dict]:
    if path.stat().st_size>MAX_SOURCE_BYTES: raise ValueError('source exceeds 16 MiB policy')
    raw=path.read_bytes()
    obj=json.loads(raw,parse_constant=lambda s: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    if not isinstance(obj,dict) or type(obj.get('version')) is not int or obj['version']!=1:
        raise ValueError('expected version-1 object')
    return raw,obj

def finite_number(v: object)->float:
    if isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or abs(v)>10000:
        raise ValueError('component must be finite and within +/-10000')
    return float(v)

def mesh_payload(obj: dict)->bytes:
    vertices=obj.get('vertices')
    if not isinstance(vertices,list) or not vertices or len(vertices)>300000 or len(vertices)%3:
        raise ValueError('mesh requires 1..100000 nonindexed triangles')
    out=bytearray(b'GEM1'+struct.pack('<I',len(vertices)))
    for vertex in vertices:
        if not isinstance(vertex,list) or len(vertex)!=8: raise ValueError('vertex requires x,y,z,u,v,r,g,b')
        values=[finite_number(v) for v in vertex]
        if any(c<0 or c>1 for c in values[5:]): raise ValueError('linear vertex colors must be in [0,1]')
        out.extend(struct.pack('<8f',*values))
    return bytes(out)

def decode_srgb(v: int)->float:
    x=v/255
    return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4

def downsample(pixels:list[tuple[float,float,float]],w:int,h:int)->tuple[list[tuple[float,float,float]],int,int]:
    """Area-weighted box filter; includes the full source extent even for odd sizes."""
    nw,nh=max(1,w//2),max(1,h//2); out=[]
    for y in range(nh):
        y0,y1=y*h/nh,(y+1)*h/nh
        for x in range(nw):
            x0,x1=x*w/nw,(x+1)*w/nw; accum=[0.,0.,0.]
            for iy in range(math.floor(y0),math.ceil(y1)):
                wy=max(0,min(y1,iy+1)-max(y0,iy))
                for ix in range(math.floor(x0),math.ceil(x1)):
                    weight=wy*max(0,min(x1,ix+1)-max(x0,ix))
                    for c in range(3):accum[c]+=pixels[iy*w+ix][c]*weight
            area=(x1-x0)*(y1-y0); out.append(tuple(v/area for v in accum))
    return out,nw,nh

def image_payload(obj:dict)->tuple[bytes,list[dict]]:
    w,h=obj.get('width'),obj.get('height'); values=obj.get('pixels')
    if type(w) is not int or type(h) is not int or not 1<=w<=256 or not 1<=h<=256:
        raise ValueError('teaching image extent must be 1..256')
    if not isinstance(values,list) or len(values)!=w*h*3 or any(type(v) is not int or not 0<=v<=255 for v in values):
        raise ValueError('RGB8 pixel count/range mismatch')
    pixels=[tuple(decode_srgb(values[3*i+c]) for c in range(3)) for i in range(w*h)]
    levels=[]; chunks=[]
    while True:
        levels.append({'width':w,'height':h})
        chunks.append(struct.pack('<II',w,h)+b''.join(struct.pack('<3f',*p) for p in pixels))
        if w==1 and h==1:break
        pixels,w,h=downsample(pixels,w,h)
    header=b'GET1'+struct.pack('<III',obj['width'],obj['height'],len(levels))
    return header+b''.join(chunks),levels

def atomic_write(path:pathlib.Path,data:bytes)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    name=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.tmp-',delete=False) as f:
            name=f.name;f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(name,path);name=None
    finally:
        if name is not None:pathlib.Path(name).unlink(missing_ok=True)

def cook(source:pathlib.Path,out:pathlib.Path,quality:str='box-linear')->dict:
    if quality!='box-linear': raise ValueError('only box-linear policy is implemented')
    mr,mesh=read_source(source/'scene_mesh.json');ir,image=read_source(source/'checker_image.json')
    # Validate/build every payload before touching the output manifest.
    mp=mesh_payload(mesh);ip,levels=image_payload(image)
    settings={'image_filter':quality,'color':'linear-srgb','vertex_format':'8f32-le'}
    ik=digest(canonical({'source':digest(ir),'settings':settings,'tool':TOOL_VERSION,'dependencies':{}}))
    mk=digest(canonical({'source':digest(mr),'settings':settings,'tool':TOOL_VERSION,'dependencies':{'checker':ik}}))
    manifest={'version':1,'tool':TOOL_VERSION,'settings':settings,'assets':{
        'checker':{'key':ik,'path':ik+'.get','payload_sha256':digest(ip),'bytes':len(ip),'mips':levels},
        'scene':{'key':mk,'path':mk+'.gem','payload_sha256':digest(mp),'bytes':len(mp),'dependencies':{'checker':ik}}}}
    atomic_write(out/(ik+'.get'),ip);atomic_write(out/(mk+'.gem'),mp)
    atomic_write(out/'assets_manifest.json',canonical(manifest)+b'\n')
    return manifest

def main()->None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True)
    a=p.parse_args()
    try:
        m=cook(a.source,a.out);print(json.dumps({'manifest':str(a.out/'assets_manifest.json'),'scene':str(a.out/m['assets']['scene']['path'])},indent=2))
    except (ValueError,OSError,KeyError,TypeError,OverflowError) as e:p.exit(1,f'cook error: {e}\n')
if __name__=='__main__':main()
