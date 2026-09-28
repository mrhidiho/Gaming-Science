#!/usr/bin/env python3
"""Regenerate deterministic SYNTHETIC teaching outputs. No hardware measurement."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from reference.cache import workloads,cache_hits,serial_cycles
from reference.coherence import MSI
from reference.scheduler import schedule,example_program,Instruction
from reference.models import pareto_front,setup_slack,hold_slack,inverter_chain,dynamic_power,energy_per_item
from reference.protocol import run_mailbox,explore_queue
from reference.ecc import fault_campaign,encode
from reference.analysis import paired_bootstrap
from reference.security import Controller,descriptor_valid


def write_json(path,value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')


def write_csv(path,rows):
    if not rows:
        raise ValueError('cannot infer schema of empty CSV')
    with path.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def generate(out):
    out.mkdir(parents=True,exist_ok=True)
    configs=[('direct',4,1),('two_way',2,2),('fully_associative',1,4)]
    cache_rows=[];sweep=[]
    for name,trace in workloads().items():
        trace_digest=hashlib.sha256(json.dumps(trace,separators=(',',':')).encode()).hexdigest()
        for config,sets,ways in configs:
            hits=cache_hits(trace,sets,ways)
            misses=len(hits)-sum(hits)
            cache_rows.append(dict(workload=name,configuration=config,sets=sets,ways=ways,
                capacity_bytes=sets*ways*64,requests=len(trace),hits=sum(hits),misses=misses,
                serial_model_cycles=serial_cycles(len(trace),misses,2,30),source='synthetic',
                trace_sha256=trace_digest))
            for penalty in (10,30,100):
                sweep.append(dict(workload=name,configuration=config,additional_miss_penalty=penalty,
                    serial_model_cycles=serial_cycles(len(trace),misses,2,penalty),source='synthetic'))
    write_csv(out/'cache_comparison.csv',cache_rows)
    write_csv(out/'cache_penalty_sensitivity.csv',sweep)
    write_json(out/'synthetic_address_traces.json',workloads())
    coherence=MSI();events=[]
    for core,op,data in [(0,'R',0),(1,'R',0),(0,'W',7),(1,'R',0),(1,'W',9),(0,'R',0)]:
        result=coherence.request(core,op,data)
        events.append(dict(core=core,operation=op,data=data,result=result,states=coherence.state.copy(),
                           values=coherence.value.copy(),memory=coherence.memory))
    write_json(out/'atomic_msi_trace.json',dict(model='atomic transitions; no transient messages',events=events))
    fault=example_program();fault[1]=Instruction('B',('A',),3,1,True)
    write_json(out/'scheduler.json',dict(in_order=schedule(example_program(),out_of_order=False),
        out_of_order=schedule(example_program()),precise_fault=schedule(fault)))
    points=[(10,40,20),(8,50,24),(12,45,22),(9,35,25)]
    write_json(out/'analytical_models.json',dict(source='synthetic analytical examples, not physical-design results',
        ppa_candidates=dict(zip('ABCD',points)),objectives=['latency_ms','power_W','area_normalized'],
        frontier=[list('ABCD')[i] for i in pareto_front(points)],
        timing_ns=dict(setup=setup_slack(2,.1,.12,1.5,.15,.08),
            hold=hold_slack(.1,.05,.08,.06,.03),tightened_setup=setup_slack(1.6,.1,.12,1.5,.15,.08)),
        inverter_chains=[inverter_chain(64,i) for i in range(1,5)],
        dynamic_power_W=dynamic_power(.2,10e-12,1,100e6),
        reduced_voltage_power_W=dynamic_power(.2,10e-12,.8,100e6),
        energy_J_per_item=[energy_per_item(.002,1e6),energy_per_item(.003,2e6)]))
    write_json(out/'ecc_fault_campaign.json',fault_campaign())
    mailbox=run_mailbox(list(range(8)),2,3,blocked_ticks=range(30))
    write_json(out/'mailbox_trace.json',mailbox)
    write_json(out/'finite_queue_reachability.json',explore_queue())
    baseline=[10,12,8,20];candidate=[8,9,7,18]
    write_csv(out/'paired_synthetic_times.csv',[dict(pair=i+1,baseline_ms=b,candidate_ms=c,source='synthetic')
        for i,(b,c) in enumerate(zip(baseline,candidate))])
    write_json(out/'paired_analysis.json',dict(source='synthetic four-pair demonstration; not a thesis result',
        **paired_bootstrap(baseline,candidate)))
    controller=Controller();token=controller.submit(0,16,7,0)
    reset_drops=controller.reset();stale=controller.complete(token,0)
    write_json(out/'descriptor_reset.json',dict(source='local pure-Python controller model; no hardware access',
        last_valid=descriptor_valid(4080,16,7,0),overrun=descriptor_valid(4080,32,7,0),
        reset_discarded=reset_drops,stale_completion_accepted=stale,writes=controller.writes))
    write_json(out/'provenance.json',dict(edition='2026-09-28',generator='code/demo.py',
        data_kind='original synthetic fixtures',seed=20260928,
        boundary='No hardware performance, physical timing, analog CDC, RTL proof, or thesis research is claimed.',
        command='python code/demo.py --out examples',ecc_payload_10_hex=f'{encode(10):02X}'))
    return sorted(p.name for p in out.iterdir() if p.is_file())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'examples')
    args=parser.parse_args()
    for name in generate(args.out):
        print(name)
