"""Fixed-latency DAG issue model with in-order retirement and precise faults.

Cycle order: complete, retire one, issue up to width. Latency L issued at t
finishes at t+L. No branches, physical registers, cache, LSQ, or ISA emulation.
"""
from dataclasses import dataclass
from .checks import integer


@dataclass(frozen=True)
class Instruction:
    name: str
    dependencies: tuple = ()
    immediate: int = 0
    latency: int = 1
    fault: bool = False


def schedule(program, width=1, window=4, out_of_order=True):
    integer(width, 'width', 1); integer(window, 'window', 1)
    seen = set()
    for ins in program:
        if not isinstance(ins.name,str) or not ins.name or ins.name in seen:
            raise ValueError('instruction names must be nonempty and unique')
        if any(dep not in seen for dep in ins.dependencies):
            raise ValueError('dependencies must name earlier instructions')
        integer(ins.latency, 'latency', 1)
        if isinstance(ins.immediate,bool) or not isinstance(ins.immediate,int):
            raise ValueError('immediate must be an integer')
        seen.add(ins.name)
    if not program:
        return dict(last_retirement_cycle=0, committed={}, events={}, fault=None)
    events, computed, committed = {}, {}, {}
    next_retire = 0
    # A conservative termination bound for this acyclic fixed-latency model.
    bound = sum(i.latency for i in program) + 3*len(program) + 1
    for t in range(bound):
        for ins in program:
            event = events.get(ins.name)
            if event and event['finish'] == t:
                computed[ins.name] = event['result']
        if next_retire < len(program):
            ins = program[next_retire]
            if ins.name in computed:
                if ins.fault:
                    return dict(last_retirement_cycle=t, committed=committed,
                                events=events, fault=ins.name)
                committed[ins.name] = computed[ins.name]
                events[ins.name]['retire'] = t
                next_retire += 1
                if next_retire == len(program):
                    return dict(last_retirement_cycle=t, committed=committed,
                                events=events, fault=None)
        issued = 0
        for ins in program[next_retire:next_retire+window]:
            if ins.name in events:
                continue
            ready = all(dep in computed for dep in ins.dependencies)
            if not ready:
                if not out_of_order:
                    break
                continue
            events[ins.name] = dict(issue=t, finish=t+ins.latency,
                                   result=ins.immediate+sum(computed[d] for d in ins.dependencies))
            issued += 1
            if issued == width:
                break
    raise RuntimeError('internal scheduler progress failure')


def example_program():
    return [Instruction('A', (), 2, 4), Instruction('B', ('A',), 3),
            Instruction('C', (), 5), Instruction('D', ('C',), 7)]
