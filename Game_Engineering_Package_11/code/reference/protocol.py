"""Digital one-entry CDC handshake and a finite abstract queue explorer.

No metastability model or MTBF claim. Coordinated reset discards in-flight work.
"""
from dataclasses import dataclass
from collections import deque
from .checks import integer


@dataclass
class Mailbox:
    req: int = 0
    ack: int = 0
    req1: int = 0
    req2: int = 0
    ack1: int = 0
    ack2: int = 0
    payload: object = None
    epoch: int = 0

    @property
    def source_ready(self):
        return self.req == self.ack2

    def reset(self, source=True, destination=True):
        if not (source and destination):
            raise ValueError('this model requires coordinated reset')
        outstanding=self.req != self.ack  # Undelivered, not just awaiting ack return.
        self.req=self.ack=self.req1=self.req2=self.ack1=self.ack2=0
        self.payload=None
        self.epoch+=1
        return int(outstanding)

    def step(self, source_edge, destination_edge, offered=None, destination_ready=True):
        if offered is not None and not source_edge:
            raise ValueError('offer requires a source edge')
        old=self.__dict__.copy()
        accepted=bool(source_edge and offered is not None and old['req']==old['ack2'])
        delivered=None
        if source_edge:
            self.ack1, self.ack2=old['ack'],old['ack1']
            if accepted:
                self.payload=offered
                self.req=old['req']^1
        if destination_edge:
            self.req1,self.req2=old['req'],old['req1']
            if destination_ready and old['req2'] != old['ack']:
                delivered=old['payload']
                self.ack=old['req2']
        return accepted,delivered


def run_mailbox(values, source_period=2, destination_period=3, source_phase=0,
                destination_phase=0, blocked_ticks=()):
    integer(source_period,'source_period',1); integer(destination_period,'destination_period',1)
    integer(source_phase,'source_phase'); integer(destination_phase,'destination_phase')
    if source_phase>=source_period or destination_phase>=destination_period:
        raise ValueError('phase must be within its clock period')
    if any(v is None for v in values):
        raise ValueError('None is reserved for no offered transaction')
    box=Mailbox(); accepted=[]; delivered=[]; trace=[]; cursor=0
    blocked=set(blocked_ticks)
    budget=max(blocked,default=0)+20*(len(values)+1)*max(source_period,destination_period)
    for t in range(budget):
        se=t%source_period==source_phase; de=t%destination_period==destination_phase
        offer=values[cursor] if se and cursor<len(values) else None
        yes,out=box.step(se,de,offer,t not in blocked)
        if yes:
            accepted.append(offer);cursor+=1
        if out is not None:
            delivered.append(out)
        if se or de:
            trace.append(dict(tick=t,source_edge=se,destination_edge=de,
                              accepted=offer if yes else None,delivered=out,
                              req=box.req,ack=box.ack,ready=box.source_ready))
        if cursor==len(values) and len(delivered)==len(values) and box.source_ready:
            return dict(accepted=accepted,delivered=delivered,trace=trace,epoch=box.epoch)
    raise RuntimeError('handshake did not drain within the declared test budget')


def queue_step(state, push=None, pop=False, capacity=2):
    integer(capacity,'capacity',1)
    if len(state)>capacity:
        raise ValueError('invalid pre-state')
    apush=push is not None and len(state)<capacity
    apop=bool(pop and state)
    out=state[0] if apop else None
    result=state[1:] if apop else state
    if apush:
        result=result+(push,)
    assert len(result)==len(state)+int(apush)-int(apop)
    assert 0<=len(result)<=capacity
    return result,out,apush,apop


def explore_queue(capacity=2, alphabet=(0,1)):
    integer(capacity,'capacity',1)
    if not alphabet or None in alphabet:
        raise ValueError('nonempty alphabet without None required')
    visited={()}; pending=deque([()]); transitions=0
    while pending:
        state=pending.popleft()
        for value in (None,)+tuple(alphabet):
            for pop in (False,True):
                nxt,*_=queue_step(state,value,pop,capacity)
                transitions+=1
                if nxt not in visited:
                    visited.add(nxt);pending.append(nxt)
    return dict(states=len(visited),transitions=transitions,fixed_point=True,
                scope='abstract ordered sequence queue; not parameterized RTL proof')
