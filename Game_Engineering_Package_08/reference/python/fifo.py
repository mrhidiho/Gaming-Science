"""Single-clock queue oracle; conservative ready, no empty bypass/full replacement."""
from collections import deque
from dataclasses import dataclass
from typing import Optional
@dataclass(frozen=True)
class Cycle:
    in_ready:bool
    out_valid:bool
    out_data:Optional[int]
    push:bool
    pop:bool
    count_after:int

class SyncFIFO:
    def __init__(self,depth:int,width:int=16):
        if not isinstance(depth,int) or depth<1 or not isinstance(width,int) or width<1:
            raise ValueError('positive integer depth/width required')
        self.depth,self.width=depth,width;self.queue=deque()
    def step(self,in_valid:bool=False,in_data:int=0,out_ready:bool=False,reset:bool=False)->Cycle:
        if not isinstance(in_data,int) or not 0<=in_data<(1<<self.width):raise ValueError('data outside width')
        ready=(len(self.queue)<self.depth) and not reset
        valid=bool(self.queue) and not reset
        head=self.queue[0] if valid else None
        push=bool(in_valid and ready);pop=bool(out_ready and valid)
        if reset:self.queue.clear()
        else:
            if pop:self.queue.popleft()
            if push:self.queue.append(in_data)
        return Cycle(ready,valid,head,push,pop,len(self.queue))
