"""A bounded reference-game microbenchmark, not a hardware ranking or FPS claim."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import platform
import statistics
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'capstone/reference'))
from yard.model import State,step

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--updates',type=int,default=10000)
parser.add_argument('--trials',type=int,default=7)
args=parser.parse_args()
if not 1<=args.updates<=1000000 or not 3<=args.trials<=100:
    parser.error('updates must be 1..1000000; trials must be 3..100')
# Mix accepted moves and restarts, so timing is not mostly terminal-state no-ops.
commands=('d','a','wait','r')
def run():
    state=State()
    for i in range(args.updates):
        state,_=step(state,commands[i % len(commands)])
    return state
run()  # untimed warm-up
seconds=[]
final=None
for _ in range(args.trials):
    started=time.perf_counter()
    result=run()
    elapsed=time.perf_counter()-started
    if final is not None and result!=final:
        raise RuntimeError('benchmark result changed between trials')
    final=result
    seconds.append(elapsed)
print(json.dumps({'python':sys.version.split()[0],'platform':platform.platform(),
    'updates_per_trial':args.updates,'trial_count':args.trials,
    'command_cycle':commands,'seconds_per_trial':seconds,
    'median_seconds':statistics.median(seconds),
    'median_microseconds_per_update':statistics.median(seconds)*1e6/args.updates,
    'final_state':asdict(final),'timed_region':'Python loop, validation, rule update and message selection; no drawing or file I/O',
    'claim_limit':'This is not full-game FPS, CPU-vs-CPU evidence, or a portability guarantee.'},indent=2))
