"""Local descriptor model. No real DMA, IOMMU operation, or hardware access."""
from dataclasses import dataclass,field
from .checks import integer


def descriptor_valid(offset,length,owner,generation,capacity=4096,alignment=16,
                     active_owner=7,active_generation=0):
    try:
        for name,value in [('offset',offset),('length',length),('owner',owner),
                           ('generation',generation),('capacity',capacity),
                           ('alignment',alignment),('active_owner',active_owner),
                           ('active_generation',active_generation)]:
            integer(value,name,1 if name in ('length','capacity','alignment') else 0)
    except ValueError:
        return False
    return (owner==active_owner and generation==active_generation and
            offset%alignment==0 and length%alignment==0 and
            offset<=capacity and length<=capacity-offset)


@dataclass
class Controller:
    capacity: int = 4096
    owner: int = 7
    alignment: int = 16
    generation: int = 0
    queue_limit: int = 4
    pending: list = field(default_factory=list)
    writes: list = field(default_factory=list)
    next_id: int = 0

    def __post_init__(self):
        for name in ('capacity','alignment','queue_limit'):
            integer(getattr(self,name),name,1)
        integer(self.owner,'owner');integer(self.generation,'generation')

    def submit(self,offset,length,owner,generation):
        if len(self.pending)>=self.queue_limit or not descriptor_valid(
            offset,length,owner,generation,self.capacity,self.alignment,self.owner,self.generation):
            return None
        token=self.next_id;self.next_id+=1
        # A private immutable copy prevents a modeled descriptor TOCTOU change.
        self.pending.append((token,self.generation,offset,length))
        return token

    def complete(self,token,generation):
        if generation!=self.generation:
            return False
        for index,row in enumerate(self.pending):
            if row[0]==token and row[1]==generation:
                self.writes.append(row)
                self.pending.pop(index)
                return True
        return False

    def reset(self):
        dropped=len(self.pending)
        self.pending.clear();self.generation+=1
        return dropped
