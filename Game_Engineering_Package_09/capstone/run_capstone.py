"""Reproduce a small co-design teaching case, clearly labeling modeled evidence.

Required run uses Python only. --native additionally compiles and measures the
included C++ host baseline using a locally installed g++ or clang++. No packages
are installed, no device drivers are loaded, and no physical hardware is accessed.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,platform,shutil,statistics,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from capstone.pipeline import simulate
from labs.reference.lesson_40_2 import solve as affine


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'capstone/results')
    args=parser.parse_args(argv); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    sizes=[0,1,7,64,1024,65536]
    models=[]; clock=100_000_000; internal_bw=400_000_000; host_bw=100_000_000
    for n in sizes:
        values=[(i*37)%20001-10000 for i in range(n)]
        gold=affine(dict(bits=16,frac=8,gain=384,bias=64,x=values))['raw']
        for lanes in [1,2,4]:
            for adverse in [False,True]:
                pattern=[True] if not adverse else [True,False,False,True]
                run=simulate(values,lanes=lanes,latency=4,ready_pattern=pattern)
                if run['output']!=gold: raise AssertionError('invalid functional result')
                compute=run['elapsed_cycles']/clock
                # One 16-bit input + one 16-bit output per item at the declared level.
                memory=4*n/internal_bw
                # Shared on-chip memory service overlaps arithmetic ideally in this bound.
                kernel=max(compute,memory)
                setup=20e-6 if n else 0.; sync=5e-6 if n else 0.; transfer=4*n/host_bw
                models.append(dict(n=n,lanes=lanes,adverse=adverse,
                    evidence_tier='functional_model_plus_analytical_timing',
                    elapsed_cycles=run['elapsed_cycles'],stalled_ticks=run['stalled_ticks'],
                    assumed_clock_Hz=clock,assumed_internal_Bps=internal_bw,
                    assumed_host_Bps=host_bw,modeled_compute_s=compute,
                    modeled_memory_service_s=memory,modeled_kernel_s=kernel,
                    modeled_end_to_end_s=setup+transfer+kernel+sync,
                    setup_s=setup,transfer_s=transfer,sync_s=sync,
                    multiplier_instances_estimate=lanes,
                    checksum=sum(gold),correct=True))
    (out/'model_results.json').write_text(json.dumps(models,indent=2))
    trace=simulate([1,3,-1,-3,32767,-32768,0],lanes=2,latency=4,ready_pattern=[True,False,True])
    (out/'example_pipeline_trace.json').write_text(json.dumps(trace,indent=2))
    native=[]; metadata={'python':sys.version,'platform':platform.platform(),
        'implementation':platform.python_implementation(),'native_executed':False,
        'model_limitations':['assumed latency and clock, not synthesized','no routing, CDC, power or memory-controller simulation',
        'global pipeline stalls model one selected protocol','payload bandwidth assumptions; not vendor specifications',
        'toy workload, not a measured production game frame']}
    if args.native:
        compiler=shutil.which('g++') or shutil.which('clang++')
        if not compiler: parser.error('--native requires an existing C++17 compiler; omit it for Python-only run')
        exe=out/('native_baseline.exe' if sys.platform=='win32' else 'native_baseline')
        flags=['-std=c++17','-O3','-Wall','-Wextra','-Wpedantic']
        command=[compiler,*flags,str(ROOT/'capstone/native_baseline.cpp'),'-o',str(exe)]
        build=subprocess.run(command,text=True,capture_output=True,timeout=60,check=False)
        (out/'native_build.log').write_text(build.stdout+build.stderr)
        if build.returncode: raise RuntimeError('native compilation failed; see native_build.log')
        metadata.update(native_executed=True,compiler=subprocess.check_output([compiler,'--version'],text=True).splitlines()[0],compile_flags=flags,
            measurement_boundary='C++ host function only; allocation, validation and checksum outside timing',
            sampling='five warmup invocations per variant, 30 paired samples; alternating variant order; no outlier removal',
            caveats='No CPU pinning, frequency control or thermal instruments. Nanosecond timer unit is not timer accuracy. Small cases may be timer dominated.')
        for n in sizes:
            run=subprocess.run([str(exe),str(n),'30'],text=True,capture_output=True,timeout=30,check=True)
            (out/f'native_n{n}.csv').write_text(run.stdout)
            rows=list(csv.DictReader(io.StringIO(run.stdout)))
            expected=sum(affine(dict(bits=16,frac=8,gain=384,bias=64,x=[(i*37)%20001-10000 for i in range(n)]))['raw'])
            for row in rows:
                if row['correct']!='true' or int(row['checksum'])!=expected:
                    raise AssertionError('independent Python checksum rejected native output')
            for variant in ['contiguous','blocked']:
                times=[int(r['elapsed_ns']) for r in rows if r['variant']==variant and r['phase']=='sample']
                native.append(dict(n=n,variant=variant,n_samples=len(times),evidence_tier='host_measurement',
                    median_ns=statistics.median(times),p95_nearest_rank_ns=sorted(times)[math.ceil(.95*len(times))-1],
                    min_ns=min(times),max_ns=max(times),checksum=expected))
        (out/'native_summary.json').write_text(json.dumps(native,indent=2))
        # Platform-specific binaries are intentionally not retained in the curriculum.
        exe.unlink()
    (out/'environment.json').write_text(json.dumps(metadata,indent=2))
    lines=['# Demonstration result, not a completed learner Gate H','',
        'The reference case is a bounded fixed-point affine transform. It is a teaching example, not a production engine workload.',
        '', '## Modeled alternatives','',
        '36 cases compare 1-, 2- and 4-lane alternatives at six sizes with normal and backpressured output. Every value was checked against the integer oracle. Timing assumes a 100 MHz clock; the clock and resource counts are NOT synthesis results.',
        '', 'The analytical end-to-end model includes 20 microseconds setup, 5 microseconds completion, 100 MB/s host payload transfer and 400 MB/s internal payload service. Units are decimal. Zero-size calls are skipped. These constants are educational assumptions, not hardware specifications.',
        '', '| N | Lanes | Adverse | Modeled kernel us | Modeled end-to-end us |',
        '|---|---|---|---|---|']
    for row in models:
        if row['n'] in [1,64,65536]:
            lines.append(f"| {row['n']} | {row['lanes']} | {row['adverse']} | {row['modeled_kernel_s']*1e6:.3f} | {row['modeled_end_to_end_s']*1e6:.3f} |")
    lines+=['','Four lanes do not automatically beat one. At the declared internal bandwidth, 4 bytes per item imposes 10 ns per item, already matching the one-lane asymptotic compute interval at 100 MHz. More lanes mainly shorten startup/drain effects or mitigate selected stalls; changing memory bandwidth can change that result.',
        '', '## Host measurements','']
    if native:
        lines+=['These are real timings of the provided C++ programs on the build host, not FPGA/GPU timings and not a measurement of the learner\'s machine. The contiguous loop is optimized by the compiler; the blocked loop is a second software candidate, not a promised improvement. No Python-to-hardware speedup claim is made.','',
            '| N | Variant | Median ns | p95 ns | Samples |','|---|---|---|---|---|']
        for row in native: lines.append(f"| {row['n']} | {row['variant']} | {row['median_ns']} | {row['p95_nearest_rank_ns']} | {row['n_samples']} |")
    else: lines+=['Native measurements were not requested. Run with --native when a C++17 compiler is available; otherwise all numerical timing results remain modeled.']
    lines+=['','## What the learner still must do','',
        'Choose and measure an actual engine workload; set application-specific quality and latency tolerances; reproduce a competent baseline; adapt at least two architecture alternatives; sweep setup, transfer and internal bandwidth; retain small, large and adverse cases; and defend an independently reproduced conclusion. A software-only winning design is a valid outcome.',
        '', 'The supplied pipeline is an educational behavioral register model. It is not a tested board, synthesizable RTL, an ASIC estimate, an electrical design approval or evidence of console SDK access.']
    (out/'REFERENCE_REPORT.md').write_text('\n'.join(lines)+'\n')
    ledger=[]
    for identity,path,tier,claim,limit in [
        ('DEMO-C1','model_results.json','functional_model','All reference pipeline cases matched the integer oracle.','Only supplied patterns and bounded arithmetic are tested.'),
        ('DEMO-C2','model_results.json','analytical','Compare end-to-end timing under explicitly assumed clock and bandwidth.','No synthesis, placement, routing or hardware timing validation.'),
        ('DEMO-C3','environment.json','host_measurement' if native else 'analytical','Record the execution environment and native-run status.','Metadata is not proof of portability.')]:
        ledger.append(dict(id=identity,tier=tier,artifact=path,sha256=hashlib.sha256((out/path).read_bytes()).hexdigest(),requirement='DEMO-REQ',claim=claim,limitations=limit))
    (out/'evidence_ledger.json').write_text(json.dumps(ledger,indent=2))
    print(f'Wrote {len(models)} model cases and {len(native)} native summaries to {out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
