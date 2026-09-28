"""Event, timer and software buffer-ownership models, not a device driver."""
from dataclasses import dataclass
from enum import Enum

def set_wins_pending(pending:bool,clear:bool,event:bool)->bool:
    return bool((pending and not clear) or event)

@dataclass
class Timer:
    width:int=16
    count:int=0
    pending:bool=False
    def __post_init__(self):
        if not 1<=self.width<=32 or not 0<=self.count<(1<<self.width):raise ValueError('invalid timer state')
    def tick(self,*,enable:bool,compare:int,clear:bool=False,reset:bool=False,irq_enable:bool=True)->dict:
        if not 0<=compare<(1<<self.width):raise ValueError('compare outside counter width')
        if reset:self.count=0;self.pending=False;event=False
        else:
            if enable:self.count=(self.count+1)&((1<<self.width)-1)
            event=bool(enable and self.count==compare)
            self.pending=set_wins_pending(self.pending,clear,event)
        return {'count':self.count,'event':event,'pending':self.pending,'irq':self.pending and irq_enable}

class Owner(Enum):CPU='cpu';DEVICE='device'
class Buffer:
    def __init__(self):self.owner=Owner.CPU;self.generation=0
    def submit(self)->int:
        if self.owner is not Owner.CPU:raise RuntimeError('device still owns buffer')
        self.owner=Owner.DEVICE;self.generation+=1;return self.generation
    def cpu_write(self)->None:
        if self.owner is not Owner.CPU:raise RuntimeError('CPU cannot mutate an in-flight buffer')
    def complete(self,generation:int)->None:
        if self.owner is not Owner.DEVICE or generation!=self.generation:raise RuntimeError('stale/duplicate completion')
        self.owner=Owner.CPU
