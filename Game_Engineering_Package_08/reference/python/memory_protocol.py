"""Single-outstanding ready/valid memory. Accepted writes commit once immediately.

Response latency >=1 edges. During response wait/hold no new request is accepted.
Reset cancels an outstanding response; it DOES NOT undo an accepted write. A host
must invalidate the transaction epoch; blindly retrying a side-effectful write is unsafe.
"""
from dataclasses import dataclass
from typing import Optional
@dataclass(frozen=True)
class Request:
    write:bool
    address:int
    data:int=0
@dataclass(frozen=True)
class Response:
    data:int
    error:bool
@dataclass(frozen=True)
class Event:
    request_ready:bool
    response_valid:bool
    response:Optional[Response]
    accepted_request:bool
    accepted_response:bool

class Memory:
    def __init__(self,words:int=256):
        if words<1:raise ValueError('positive memory size required')
        self.words=[0]*words;self.response=None;self.remaining=0;self.write_count=0
    def step(self,request:Optional[Request]=None,response_ready:bool=True,latency:int=1,reset:bool=False)->Event:
        if not isinstance(latency,int) or latency<1:raise ValueError('positive integer latency required')
        if reset:
            self.response=None;self.remaining=0
            return Event(False,False,None,False,False)
        ready=self.response is None
        valid=self.response is not None and self.remaining==0
        visible=self.response if valid else None
        accept=request is not None and ready;take=valid and response_ready
        if take:self.response=None
        elif self.response is not None and self.remaining>0:self.remaining-=1
        if accept:
            error=not 0<=request.address<len(self.words) or not 0<=request.data<=65535
            data=0
            if not error:
                if request.write:self.words[request.address]=request.data;self.write_count+=1
                else:data=self.words[request.address]
            self.response=Response(data,error);self.remaining=latency-1
        return Event(ready,valid,visible,accept,take)
