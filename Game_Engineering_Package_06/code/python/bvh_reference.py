#!/usr/bin/env python3
"""Original educational sphere BVH. Median split; instrumented traversal and brute-force oracle.
Python timings are illustrative local measurements, never GPU or production-engine benchmarks.
"""
from __future__ import annotations
from dataclasses import dataclass
import argparse,json,math,random,time
Vec=tuple[float,float,float]
@dataclass(frozen=True)
class Sphere:
    center:Vec
    radius:float
    ident:int
@dataclass
class Node:
    lo:Vec
    hi:Vec
    ids:list[int]
    left:Node|None=None
    right:Node|None=None

def box_interval(o:Vec,d:Vec,lo:Vec,hi:Vec,tmax:float=math.inf):
    tmin=0.
    for p,v,a,b in zip(o,d,lo,hi):
        if v==0:
            if p<a or p>b:return None
        else:
            x,y=sorted(((a-p)/v,(b-p)/v));tmin=max(tmin,x);tmax=min(tmax,y)
            if tmin>tmax:return None
    return tmin,tmax

def sphere_hit(o:Vec,d:Vec,s:Sphere):
    oc=tuple(o[i]-s.center[i] for i in range(3));a=sum(x*x for x in d)
    if a==0:raise ValueError('zero ray direction')
    half_b=sum(oc[i]*d[i] for i in range(3));c=sum(x*x for x in oc)-s.radius*s.radius
    disc=half_b*half_b-a*c
    if disc<0:return None
    root=math.sqrt(disc)
    for t in ((-half_b-root)/a,(-half_b+root)/a):
        if t>=0:return t
    return None

def build(spheres:list[Sphere],ids:list[int]|None=None)->Node:
    if not spheres:raise ValueError('nonempty sphere set required')
    if ids is None:
        if any(s.radius<=0 or not math.isfinite(s.radius) or any(not math.isfinite(x) for x in s.center) for s in spheres):raise ValueError('invalid sphere')
        if len({s.ident for s in spheres})!=len(spheres):raise ValueError('duplicate sphere identity')
        ids=list(range(len(spheres)))
    lo=tuple(min(spheres[i].center[k]-spheres[i].radius for i in ids) for k in range(3))
    hi=tuple(max(spheres[i].center[k]+spheres[i].radius for i in ids) for k in range(3))
    node=Node(lo,hi,ids)
    if len(ids)>4:
        axis=max(range(3),key=lambda k:hi[k]-lo[k]);order=sorted(ids,key=lambda i:(spheres[i].center[axis],spheres[i].ident));mid=len(order)//2
        node.ids=[];node.left=build(spheres,order[:mid]);node.right=build(spheres,order[mid:])
    return node

def trace(o:Vec,d:Vec,spheres:list[Sphere],root:Node|None,counts:dict)->tuple[float,int]|None:
    if len(o)!=3 or len(d)!=3 or any(not math.isfinite(x) for x in (*o,*d)) or not any(d):raise ValueError('invalid ray')
    best=None
    if root is None:
        leaves=[list(range(len(spheres)))]
    else:
        stack=[root];leaves=[]
        while stack:
            node=stack.pop();counts['boxes']+=1
            if box_interval(o,d,node.lo,node.hi,best[0] if best else math.inf) is None:continue
            if node.left is not None:
                stack.append(node.right);stack.append(node.left)
            else:
                # Intersect during traversal so later bounds can use the current closest hit.
                for i in node.ids:
                    counts['primitives']+=1;t=sphere_hit(o,d,spheres[i])
                    if t is not None and (best is None or (t,spheres[i].ident)<best):best=(t,spheres[i].ident)
        return best
    for ids in leaves:
        for i in ids:
            counts['primitives']+=1;t=sphere_hit(o,d,spheres[i])
            if t is not None and (best is None or (t,spheres[i].ident)<best):best=(t,spheres[i].ident)
    return best

def experiment(count:int=256,rays:int=1000,seed:int=2026)->dict:
    if not 1<=count<=10000 or not 1<=rays<=100000:raise ValueError('experiment bounds exceeded')
    rng=random.Random(seed)
    spheres=[Sphere((rng.uniform(-8,8),rng.uniform(-8,8),rng.uniform(2,20)),rng.uniform(.15,.5),i) for i in range(count)]
    queries=[((0.,0.,-5.),(rng.uniform(-.6,.6),rng.uniform(-.6,.6),1.)) for _ in range(rays)]
    t=time.perf_counter();root=build(spheres);build_ms=(time.perf_counter()-t)*1000
    results=[];stats={}
    for name,node in [('brute',None),('bvh',root)]:
        counters={'boxes':0,'primitives':0};t=time.perf_counter();hits=[trace(o,d,spheres,node,counters) for o,d in queries]
        stats[name]={**counters,'query_ms':(time.perf_counter()-t)*1000};results.append(hits)
    matches=all(a==b or (a is not None and b is not None and a[1]==b[1] and math.isclose(a[0],b[0],rel_tol=1e-12,abs_tol=1e-12)) for a,b in zip(*results))
    if not matches:raise AssertionError('BVH/oracle hit mismatch')
    return {'seed':seed,'spheres':count,'rays':rays,'same_hits':matches,'build_ms':build_ms,**stats,'timing_scope':'Python CPU wall time, one run; not a performance guarantee'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spheres',type=int,default=256);p.add_argument('--rays',type=int,default=1000);p.add_argument('--output');a=p.parse_args()
    report=experiment(a.spheres,a.rays);text=json.dumps(report,indent=2);print(text)
    if a.output:
        from pathlib import Path
        Path(a.output).write_text(text+'\n')
