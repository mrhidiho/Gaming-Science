"""G16 v1: an original 16-bit educational ISA, NOT a RISC-V implementation.
See source/G16_ISA_SPEC.md for exact encoding, retirement and fault rules.
"""
from dataclasses import dataclass,asdict
from pathlib import Path
import re
MASK=0xffff
TRACE_FIELDS=('index','pc','instr','next_pc','reg_we','rd','reg_value','mem_we','mem_addr','mem_value','halt')
class AssemblyError(ValueError):pass
class ExecutionLimit(RuntimeError):pass

def sext(value:int,bits:int)->int:
    value &= (1<<bits)-1
    return value-(1<<bits) if value&(1<<(bits-1)) else value

@dataclass(frozen=True)
class Trace:
    index:int;pc:int;instr:int;next_pc:int;reg_we:int;rd:int;reg_value:int
    mem_we:int;mem_addr:int;mem_value:int;halt:int

class Machine:
    def __init__(self,program:list[int]):
        if len(program)>256 or any(not isinstance(x,int) or not 0<=x<=MASK for x in program):
            raise ValueError('code requires <=256 unsigned 16-bit words')
        self.code=list(program)+[0]*(256-len(program));self.memory=[0]*256;self.regs=[0]*8
        self.pc=0;self.stopped=False;self.fault=None;self.retired=0
    def step(self)->Trace|None:
        if self.stopped:return None
        if not 0<=self.pc<256:
            self.stopped=True;self.fault='fetch_address';return None
        pc=self.pc;word=self.code[pc];op=word>>12;rd=(word>>9)&7;ra=(word>>6)&7;rb=(word>>3)&7
        nxt=(pc+1)&MASK;write=False;value=0;store=False;address=0;data=0;halt=False;error=None
        if op==0:
            if word!=0:error='illegal_instruction'
        elif op==1:write=True;value=sext(word&511,9)&MASK
        elif op in (2,3):
            if word&7:error='illegal_instruction'
            else:write=True;value=(self.regs[ra]+self.regs[rb] if op==2 else self.regs[ra]-self.regs[rb])&MASK
        elif op in(4,5):
            address=(self.regs[ra]+sext(word&63,6))&MASK
            if address>=256:error='data_address'
            elif op==4:write=True;value=self.memory[address]
            else:store=True;data=self.regs[rd]
        elif op==6:
            if self.regs[rd]==0:nxt=(pc+1+sext(word&511,9))&MASK
        elif op==7:
            if word&0xf00:error='illegal_instruction'
            else:nxt=word&255
        elif op==15:
            if word!=0xf000:error='illegal_instruction'
            else:halt=True
        else:error='illegal_instruction'
        if error:
            self.stopped=True;self.fault=error;return None
        real_write=write and rd!=0
        if real_write:self.regs[rd]=value
        if store:self.memory[address]=data
        result=Trace(self.retired,pc,word,nxt,int(real_write),rd if real_write else 0,value if real_write else 0,
                     int(store),address if store else 0,data if store else 0,int(halt))
        self.pc=nxt;self.retired+=1;self.stopped=halt;return result
    def run(self,budget:int=10000)->list[Trace]:
        if budget<1:raise ValueError('positive execution budget required')
        trace=[]
        for _ in range(budget):
            item=self.step()
            if item is not None:trace.append(item)
            if self.stopped:return trace
        raise ExecutionLimit(f'no halt/fault after {budget} steps at PC {self.pc}')

def _register(token:str)->int:
    m=re.fullmatch(r'r([0-7])',token.lower())
    if not m:raise AssemblyError(f'invalid register {token!r}')
    return int(m.group(1))

def _integer(token:str)->int:
    try:return int(token,0)
    except ValueError as exc:raise AssemblyError(f'invalid integer {token!r}') from exc

def _signed(value:int,bits:int)->int:
    if not -(1<<(bits-1))<=value<(1<<(bits-1)):raise AssemblyError(f'{value} outside signed {bits}-bit range')
    return value&((1<<bits)-1)

def assemble(source:str)->list[int]:
    """Two-pass labels. LD/ST syntax: LD rd, base, signed_offset. BZ reg,label|offset.
    .word accepts an unsigned 16-bit literal for directed illegal-instruction tests.
    """
    labels={};statements=[];pc=0
    for lineno,raw in enumerate(source.splitlines(),1):
        line=raw.split(';',1)[0].split('#',1)[0].strip()
        if not line:continue
        if ':' in line:
            label,line=line.split(':',1);label=label.strip()
            if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',label) or label in labels:
                raise AssemblyError(f'line {lineno}: invalid/duplicate label')
            labels[label]=pc;line=line.strip()
        if line:statements.append((lineno,pc,line));pc+=1
    if pc>256:raise AssemblyError('code exceeds 256 words')
    output=[]
    for lineno,pc,line in statements:
        tokens=line.replace(',',' ').split();op=tokens[0].upper();a=tokens[1:]
        count={'NOP':0,'HALT':0,'LDI':2,'ADD':3,'SUB':3,'LD':3,'ST':3,'BZ':2,'JMP':1,'.WORD':1}
        if op not in count or len(a)!=count[op]:raise AssemblyError(f'line {lineno}: bad operation/operand count')
        try:
            if op=='NOP':word=0
            elif op=='HALT':word=0xf000
            elif op=='LDI':word=0x1000|(_register(a[0])<<9)|_signed(_integer(a[1]),9)
            elif op in ('ADD','SUB'):
                word=((2 if op=='ADD' else 3)<<12)|(_register(a[0])<<9)|(_register(a[1])<<6)|(_register(a[2])<<3)
            elif op in('LD','ST'):
                word=((4 if op=='LD' else 5)<<12)|(_register(a[0])<<9)|(_register(a[1])<<6)|_signed(_integer(a[2]),6)
            elif op=='BZ':
                displacement=labels[a[1]]-(pc+1) if a[1] in labels else _integer(a[1])
                word=0x6000|(_register(a[0])<<9)|_signed(displacement,9)
            elif op=='JMP':
                target=labels[a[0]] if a[0] in labels else _integer(a[0])
                if not 0<=target<=255:raise AssemblyError('jump target outside 0..255')
                word=0x7000|target
            else:
                word=_integer(a[0])
                if not 0<=word<=MASK:raise AssemblyError('.word outside 16-bit range')
        except AssemblyError as exc:raise AssemblyError(f'line {lineno}: {exc}') from exc
        output.append(word)
    return output

def write_hex(path:Path,program:list[int],pad:bool=True)->None:
    if len(program)>256 or any(not 0<=w<=MASK for w in program):raise ValueError('invalid image')
    words=program+[0]*(256-len(program)) if pad else program
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(f'{w:04x}\n' for w in words))
