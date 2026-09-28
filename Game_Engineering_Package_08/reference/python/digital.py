"""Combinational logic, state transitions and simplified timing worksheets."""
from enum import IntEnum
class State(IntEnum): IDLE=0; RUN=1; DONE=2

def full_adder(a:int,b:int,carry:int)->tuple[int,int]:
    if any(x not in (0,1) for x in (a,b,carry)):raise ValueError('binary inputs required')
    return a^b^carry,(a&b)|(a&carry)|(b&carry)

def ripple_add(a:int,b:int,carry:int=0,width:int=4)->tuple[int,int]:
    if not isinstance(width,int) or width<1 or not 0<=a<(1<<width) or not 0<=b<(1<<width) or carry not in(0,1):
        raise ValueError('unsigned in-range operands and binary carry required')
    result=0
    for bit in range(width):
        s,carry=full_adder((a>>bit)&1,(b>>bit)&1,carry);result|=s<<bit
    return result,carry

def mux(a:int,b:int,select:int)->int:
    if select not in (0,1):raise ValueError('select must be binary')
    return b if select else a

def decoder(value:int,width:int)->int:
    if width<1 or not 0<=value<(1<<width):raise ValueError('invalid decoder input')
    return 1<<value

def next_state(state:int,*,reset:bool=False,abort:bool=False,start:bool=False,
               complete:bool=False,acknowledge:bool=False)->State:
    if reset or abort:return State.IDLE
    if state==State.IDLE:return State.RUN if start else State.IDLE
    if state==State.RUN:return State.DONE if complete else State.RUN
    if state==State.DONE:return State.IDLE if acknowledge else State.DONE
    return State.IDLE

def setup_budget(clock_to_q:float,logic:float,setup:float,uncertainty:float)->float:
    if min(clock_to_q,logic,setup,uncertainty)<0:raise ValueError('nonnegative delays required')
    return clock_to_q+logic+setup+uncertainty

def hold_slack(clock_to_q_min:float,logic_min:float,hold:float,adverse_skew:float)->float:
    return clock_to_q_min+logic_min-hold-adverse_skew
