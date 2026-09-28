"""Two simulated clients, one authoritative server, seeded faulty transport.

This is an in-process protocol simulator, not a socket server or authentication
system. The full workbook lab requires learners to add a process/socket adapter.
The last 80 ticks use reliable transport solely to drain and check convergence.
"""
from __future__ import annotations
import hashlib
import heapq
import json
import random


def experiment(seed: int = 2901) -> dict:
    rng=random.Random(seed); events=[]; serial=0
    stats={'sent':0,'dropped':0,'duplicates':0,'stale_snapshots':0,'rejected_owner':0}
    server={i:{'position':0,'ack':0,'buffer':{}} for i in (0,1)}
    clients={i:{'position':0,'ack':0,'pending':{},'snapshot':-1} for i in (0,1)}
    epoch=7
    def step(x,delta):return min(100,max(-100,x+delta))
    def send(tick,kind,recipient,payload):
        nonlocal serial
        stats['sent']+=1
        reliable=tick>=280
        if not reliable and rng.random()<.2:
            stats['dropped']+=1;return
        copies=1+(not reliable and rng.random()<.1)
        if copies==2:stats['duplicates']+=1
        for _ in range(copies):
            serial+=1
            heapq.heappush(events,(tick+(1 if reliable else rng.randrange(1,7)),serial,kind,recipient,payload.copy()))
    def accept_input(sender,p):
        if p.get('epoch')!=epoch or p.get('owner')!=sender:
            stats['rejected_owner']+=1;return
        s=server[sender];seq=p['seq'];delta=p['delta']
        if type(seq)is not int or type(delta)is not int or delta not in (-1,0,1) or not 1<=seq<=120:return
        if seq<=s['ack']:return
        if seq in s['buffer'] and s['buffer'][seq]!=delta:raise AssertionError('conflicting duplicate')
        s['buffer'][seq]=delta
        while s['ack']+1 in s['buffer']:
            s['ack']+=1;s['position']=step(s['position'],s['buffer'].pop(s['ack']))
    # Synthetic envelope ownership test, not cryptographic identity verification.
    accept_input(0,{'epoch':epoch,'owner':1,'seq':1,'delta':1})
    for tick in range(360):
        while events and events[0][0]<=tick:
            _,_,kind,recipient,p=heapq.heappop(events)
            if kind=='input':accept_input(recipient,p)
            else:
                c=clients[recipient]
                if p['epoch']!=epoch or p['snapshot']<=c['snapshot']:
                    stats['stale_snapshots']+=1;continue
                c['snapshot']=p['snapshot'];c['ack']=p['ack']
                c['pending']={q:d for q,d in c['pending'].items() if q>p['ack']}
                x=p['position']
                for q,d in sorted(c['pending'].items()):x=step(x,d)
                c['position']=x
        if tick<120:
            for i,c in clients.items():
                # A repeatable player input tape, independent of transport RNG.
                delta=(1 if (tick//20+i)%2==0 else -1)
                c['pending'][tick+1]=delta;c['position']=step(c['position'],delta)
        for i,c in clients.items():
            if tick%3==0:
                for seq,delta in sorted(c['pending'].items()):
                    send(tick,'input',i,{'epoch':epoch,'owner':i,'seq':seq,'delta':delta})
            if tick%2==0:
                s=server[i]
                send(tick,'snapshot',i,{'epoch':epoch,'snapshot':tick,'ack':s['ack'],'position':s['position']})
    assert stats['dropped']>0 and stats['duplicates']>0 and stats['rejected_owner']==1
    for i,s in server.items():
        assert s['ack']==120 and not s['buffer']
        assert not clients[i]['pending'] and clients[i]['position']==s['position']
    positions={str(i):s['position'] for i,s in server.items()}
    return {'seed':seed,'clients':2,'commands_per_client':120,'unreliable_ticks':280,
            'reliable_drain_ticks':80,'final_positions':positions,'statistics':stats,
            'state_sha256':hashlib.sha256(json.dumps(positions,sort_keys=True).encode()).hexdigest(),
            'scope':'in-process scalar simulation; no sockets or production authentication'}

if __name__=='__main__':
    a=experiment();b=experiment();assert a==b
    print(json.dumps({'repeat_identical':True,'result':a},indent=2,sort_keys=True))
