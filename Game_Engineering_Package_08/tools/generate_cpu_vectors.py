"""Generate G16 reference traces for external HDL comparison; not an RTL run."""
import sys,csv,json,argparse,random
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from reference.python.g16 import Machine,assemble,write_hex,TRACE_FIELDS
from reference.python.cpu_cases import CASES,Case

def generate(output:Path)->int:
    output.mkdir(parents=True,exist_ok=True);cases=list(CASES);rng=random.Random(7344)
    for n in range(20):
        lines=[]
        for _ in range(60):
            dst=rng.randrange(8)
            if rng.randrange(3)==0:lines.append(f'LDI r{dst},{rng.randrange(-256,256)}')
            else:lines.append(f'{rng.choice(["ADD","SUB"])} r{dst},r{rng.randrange(8)},r{rng.randrange(8)}')
        cases.append(Case(f'random_{n:02d}','\n'.join(lines+['HALT'])))
    inventory=[]
    for case in cases:
        folder=output/case.name;folder.mkdir(exist_ok=True)
        (folder/'program.asm').write_text(case.source+'\n');program=assemble(case.source);write_hex(folder/'program.mem',program)
        m=Machine(program);trace=m.run()
        with (folder/'expected.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=TRACE_FIELDS);writer.writeheader();writer.writerows(asdict(t) for t in trace)
        result={'name':case.name,'model':'G16 Python instruction reference','fault':m.fault,'pc':m.pc,'retired':m.retired,
                'registers':m.regs,'memory':m.memory,'seed':7344 if case.name.startswith('random') else None}
        (folder/'expected.json').write_text(json.dumps(result,indent=2)+'\n');inventory.append({'name':case.name,'retired':m.retired,'fault':m.fault})
    (output/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n');return len(cases)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'evidence/cpu_vectors')
    a=p.parse_args();print(f'Generated {generate(a.output)} software-reference cases in {a.output}; HDL not run by this command.')
