"""Measured local membership workload; includes set construction in method B.

Not a GPU/game-engine benchmark or a device buying recommendation. Outputs go to
one NEW directory. Existing files are never overwritten by this script.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import json
import platform
import random
import statistics
import time
import mathkit

def scan(values,queries):
    return sum(q in values for q in queries)

def build_set(values,queries):
    lookup=set(values)
    return sum(q in lookup for q in queries)

def run(out:Path,pairs:int=30):
    if out.exists():raise ValueError('output directory already exists; choose a new --out path')
    if pairs not in (10,20,30):raise ValueError('supported pair counts: 10,20,30')
    critical={10:2.262157163,20:2.093024054,30:2.045229642}[pairs]
    rng=random.Random(260903)
    rows=[]; summaries=[]
    for size in (32,512,4096):
        values=[3*i+1 for i in range(size)]
        for query_count in (1,32):
            queries=[rng.randrange(-3,3*size+4) for _ in range(query_count)]
            oracle=sum(1 for q in queries if q>=1 and (q-1)%3==0 and (q-1)//3<size)
            methods={'A_scan':scan,'B_build_set':build_set}
            for _ in range(3):
                for method in methods.values():
                    if method(values,queries)!=oracle:raise AssertionError('warmup correctness failure')
            a_times=[];b_times=[];differences=[]
            for pair in range(pairs):
                order=list(methods)
                rng.shuffle(order)
                measured={}
                for position,name in enumerate(order):
                    start=time.perf_counter_ns()
                    answer=methods[name](values,queries)
                    elapsed=(time.perf_counter_ns()-start)/1e6
                    if answer!=oracle:raise AssertionError('measured result differs from analytic membership oracle')
                    measured[name]=elapsed
                    rows.append(dict(size=size,query_count=query_count,pair=pair,order=position,algorithm=name,
                                     elapsed_ms=elapsed,result=answer,correct=True))
                a_times.append(measured['A_scan']);b_times.append(measured['B_build_set'])
                differences.append(measured['B_build_set']-measured['A_scan'])
            mean,low,high=mathkit.mean_interval(differences,critical)
            summaries.append(dict(size=size,query_count=query_count,pairs=pairs,mean_B_minus_A_ms=mean,
                                  conditional_t95_low_ms=low,conditional_t95_high_ms=high,
                                  median_A_ms=statistics.median(a_times),median_B_ms=statistics.median(b_times),
                                  nearest_rank_p95_A_ms=mathkit.percentile(a_times,.95),
                                  nearest_rank_p95_B_ms=mathkit.percentile(b_times,.95)))
    out.mkdir(parents=True,exist_ok=False)
    with (out/'raw_trials.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    with (out/'summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summaries[0]));writer.writeheader();writer.writerows(summaries)
    metadata=dict(data_kind='measured_local_python_microbenchmark',utc=datetime.now(timezone.utc).isoformat(),
                  python=platform.python_version(),implementation=platform.python_implementation(),
                  operating_system=platform.system(),machine=platform.machine(),seed=260903,pairs_per_workload=pairs,
                  workloads=6,warmups_per_method_per_workload=3,rows=len(rows),clock='perf_counter_ns',
                  includes='A: list membership queries; B: set construction and membership queries',
                  excludes='input construction, output validation, CSV writing, process startup, graphics and game-engine integration',
                  percentile='nearest rank, p95 fraction 0.95',difference_sign='B minus A; negative means B took less time',
                  interval_assumptions='Student t interval on paired differences, conditional on independent approximately normal pair differences. Ordering is randomized; independence/normality are not established automatically.',
                  inference_limit='Local short Python workload only. No native engine, GPU, universal device, causal player-experience or population-tail claim.')
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2,allow_nan=False))
    print(f'Wrote {len(rows)} measured rows and {len(summaries)} workload summaries to {out}')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True,help='new directory for raw data, summaries and metadata')
    parser.add_argument('--pairs',type=int,choices=(10,20,30),default=30)
    args=parser.parse_args()
    try:run(args.out,args.pairs)
    except (ValueError,OSError) as error:parser.exit(2,f'Benchmark stopped: {error}\n')
if __name__=='__main__':main()
