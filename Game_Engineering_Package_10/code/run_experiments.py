#!/usr/bin/env python3
"""Rebuild diagnostic evidence. Small synthetic workloads; no hardware claims."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import platform
import random
import subprocess
import sys
import time
from pathlib import Path
from gradlab import numerical as nu, parallel as pa, rendering as re, systems as sy, compiler as co


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf8')


def save_csv(path, rows):
    if not rows: return
    with path.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def run_numerical(out):
    rows=[]
    for exponent in (0,2,4,6):
        n=12; d=[10**(-exponent*i/(n-1)) for i in range(n)]
        a=nu.CSR.from_dense([[d[i] if i==j else 0 for j in range(n)] for i in range(n)])
        truth=[1+i/n for i in range(n)]; b=a.matvec(truth)
        for pre in (False,True):
            result=nu.pcg(a,b,jacobi=pre,rtol=1e-12,maxiter=200)
            rows.append(dict(condition_number=10**exponent,jacobi=pre,
                             iterations=result['iterations'],converged=result['converged'],
                             residual=result['residual'],forward_error=nu.norm([a-b for a,b in zip(result['x'],truth)])))
    save_csv(out/'numerical.csv',rows)


def run_parallel(out):
    rows=[]
    rng=random.Random(42)
    for n in (0,1,3,1023,1024,1025):
        values=[rng.randrange(10) for _ in range(n)]
        actual=pa.exclusive_scan(values)
        reference=[]; total=0
        for v in values: reference.append(total); total+=v
        rows.append(dict(n=n,equal=actual==reference,sum=total))
    save_csv(out/'scan_cases.csv',rows)
    save_json(out/'pipeline_model.json',pa.pipeline_trace(8,2,5))
    save_json(out/'schedule_model.json',dict(static=pa.scheduling_model([100]+[1]*99,8,dynamic=False),
                                           dynamic=pa.scheduling_model([100]+[1]*99,8,dynamic=True,overhead=.1)))


def run_bar(out):
    rows=[]
    for n in (4,8):
        for dt in (1/30,1/60,1/120):
            reference=sy.simulate_bar(n=n,dt=dt,duration=.2,method='implicit')
            for iterations in (1,4,16,64):
                start=time.perf_counter_ns()
                result=sy.simulate_bar(n=n,dt=dt,duration=.2,iterations=iterations)
                elapsed=time.perf_counter_ns()-start
                maximum=max(abs(a-b) for ua,ub in zip(result['trajectory'],reference['trajectory']) for a,b in zip(ua,ub))
                rows.append(dict(particles=n,dt_s=dt,iterations=iterations,duration_s=.2,
                                 max_displacement_error_m=maximum,elapsed_ns=elapsed,
                                 evidence='one CPU run; linear 1D synthetic bar'))
    save_csv(out/'bar_sensitivity.csv',rows)


def run_render(out):
    results=[]
    for mode in ('bsdf','mis'):
        start=time.perf_counter_ns(); image=re.render(width=24,height=18,spp=8,mode=mode)
        elapsed=time.perf_counter_ns()-start
        save_json(out/f'render_{mode}_linear.json',image)
        re.write_ppm(image,out/f'render_{mode}.ppm')
        results.append(dict(mode=mode,width=24,height=18,spp=8,elapsed_ns=elapsed,
                            mean_linear_radiance=sum(image['pixels'])/len(image['pixels'])))
    save_csv(out/'render_diagnostics.csv',results)
    # Independent seeded estimator trials; not an image-quality or equal-cost study.
    rows=[dict(seed=s,estimate=re.integrate_mis(2000,seed=s),truth=1/3) for s in range(20)]
    save_csv(out/'mis_integral_trials.csv',rows)


def run_systems(out):
    stream=sy.StreamModel(1024,4)
    statuses=[stream.request(sy.Request(f'asset-{i}',300,i,0)) for i in range(6)]
    stream.tick(); stream.tick(); stream.teleport()
    stream.request(sy.Request('teleport-target',700,0,1)); stream.tick()
    save_json(out/'stream_trace.json',dict(statuses=statuses,peak_bytes=stream.peak,trace=stream.trace))
    save_json(out/'lifecycle.json',dict(correct=sy.lifecycle_check(),deliberate_bug=sy.lifecycle_check(True)))


def run_compiler(out):
    expr=('mul',('add',('var','x'),('const',0)),('add',('const',2),('const',3)))
    folded=co.fold(expr,{'x'})
    (out/'generated_kernel.cpp').write_text(co.generate_cpp(folded,{'x'}),encoding='utf8')
    rng=random.Random(45)
    mismatches=0
    for _ in range(1000):
        env={'x':rng.randrange(1<<32)}
        mismatches += co.interpret(expr,env)!=co.interpret(folded,env)
    save_json(out/'compiler_semantics.json',dict(original=expr,folded=folded,cases=1000,mismatches=mismatches,
              cache_key=co.cache_key(folded,target='portable-u32',compiler_version='teaching-v1',flags='wrap')))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('experiment',choices=['all','numerical','parallel','bar','render','systems','compiler'])
    p.add_argument('--out',type=Path,default=Path('out'))
    args=p.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    selected=['numerical','parallel','bar','render','systems','compiler'] if args.experiment=='all' else [args.experiment]
    for name in selected:
        globals()['run_'+name](args.out)
        print('completed:',name)
    source_hashes={str(f.relative_to(Path(__file__).parent)):hashlib.sha256(f.read_bytes()).hexdigest()
                   for f in sorted((Path(__file__).parent/'gradlab').glob('*.py'))}
    save_json(args.out/'run_environment.json',dict(python=sys.version,platform=platform.platform(),
              machine=platform.machine(),command=sys.argv,source_sha256=source_hashes,
              evidence='CPU diagnostic run; no GPU or external reproduction certification'))

if __name__=='__main__': main()
