"""Sweep declared analytical parameters; this does not measure hardware.

The functional traces and elapsed cycles are reused from run_capstone.py.
Only setup and the two payload-bandwidth assumptions change. A changed clock,
flow-control design or workload would require an appropriate model rerun.
"""
from __future__ import annotations
import argparse,csv,itertools,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def estimate(case:dict,setup_us:float,host_Bps:float,internal_Bps:float)->dict:
    for name,value in [('setup_us',setup_us),('host_Bps',host_Bps),('internal_Bps',internal_Bps)]:
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError(name+' must be a finite number')
        if value<0 or (name!='setup_us' and value==0): raise ValueError('invalid '+name)
    n=case['n']
    if isinstance(n,bool) or not isinstance(n,int) or n<0: raise ValueError('invalid item count')
    clock=case['assumed_clock_Hz']; cycles=case['elapsed_cycles']
    if clock<=0 or cycles<0: raise ValueError('invalid model timing')
    compute=cycles/clock
    memory=4*n/internal_Bps
    transfer=4*n/host_Bps
    setup=setup_us/1e6 if n else 0.
    sync=5e-6 if n else 0.
    kernel=max(compute,memory)
    return dict(n=n,lanes=case['lanes'],adverse=case['adverse'],
        setup_us=setup_us,host_Bps=host_Bps,internal_Bps=internal_Bps,
        compute_us=compute*1e6,memory_us=memory*1e6,transfer_us=transfer*1e6,
        kernel_us=kernel*1e6,end_to_end_us=(setup+transfer+kernel+sync)*1e6,
        evidence_tier='analytical',timing_scope='conditional payload model, no hardware measurement')

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT/'capstone/results/model_results.json')
    p.add_argument('--output',type=Path,default=ROOT/'capstone/results')
    a=p.parse_args(argv); cases=json.loads(a.input.read_text())
    if not isinstance(cases,list) or not cases: p.error('input must be a nonempty model-results list')
    rows=[estimate(case,s,h,b) for case in cases for s,h,b in
          itertools.product([5.,20.,80.],[25e6,100e6,400e6],[100e6,400e6,1600e6])]
    a.output.mkdir(parents=True,exist_ok=True)
    with (a.output/'sensitivity.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    metadata=dict(kind='analytical parameter sweep',cases=len(rows),
        parameters=dict(setup_us=[5,20,80],host_Bps=[25000000,100000000,400000000],internal_Bps=[100000000,400000000,1600000000]),
        unchanged='Functional traces, elapsed cycles and assumed 100 MHz clock are reused; 5 us completion and four payload bytes/item remain fixed.',
        limitations='No measured accelerator. No change to real transport, memory controller, contention or physical timing is simulated.')
    (a.output/'sensitivity_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    lines=['# Sensitivity of the teaching model','',
        f'{len(rows)} analytical combinations reuse the 36 validated functional traces. Setup, host payload bandwidth and internal payload bandwidth each take three declared values. These are hypothetical assumptions, not measured device properties.','',
        'The table holds setup at 20 us, completion at 5 us and selects N=65,536, four lanes, normal readiness. Only the two bandwidth assumptions change.','',
        '| Host MB/s | Internal MB/s | Conditional end-to-end us |','|---|---|---|']
    for row in rows:
        if row['n']==65536 and row['lanes']==4 and not row['adverse'] and row['setup_us']==20:
            lines.append(f"| {row['host_Bps']/1e6:g} | {row['internal_Bps']/1e6:g} | {row['end_to_end_us']:.3f} |")
    lines+=['','Higher internal bandwidth alone does not remove host transfers. At each bandwidth pair, setup values 5 and 80 us shift a nonempty result by −15 and +60 us relative to this table. An engine decision still needs measured workload frequency and an application critical-path model.','',
        'Reproduce in a new folder with: `python -m capstone.sensitivity --input my_results/model_only/model_results.json --output my_results/model_only`. Changing compute architecture or clock requires a corresponding justified model, not only editing these costs.']
    (a.output/'SENSITIVITY_REPORT.md').write_text('\n'.join(lines)+'\n')
    print(f'Wrote {len(rows)} analytical sensitivity rows to {a.output}')
    return 0
if __name__=='__main__': raise SystemExit(main())
