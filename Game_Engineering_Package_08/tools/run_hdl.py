"""Compile/run reference HDL with Icarus and compare G16 and raster results.
Missing tools produce NOT_RUN and exit 2; they never become a passing result.
This runner is included but was not executable in the package-authoring environment.
"""
import sys,shutil,subprocess,json,csv,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.generate_cpu_vectors import generate
from reference.python.video import rgb

def checked(command:list[str],log:Path)->None:
    p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120)
    log.write_text('$ '+' '.join(command)+'\n'+p.stdout+p.stderr)
    if p.returncode:raise RuntimeError(f'command failed ({p.returncode}): see {log}')

def rows(path:Path)->list[dict]:
    with path.open(newline='') as f:return [{k:int(v) for k,v in row.items()} for row in csv.DictReader(f)]

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=['all','fifo','semantics','sat_add','scanout','g16'],default='all');a=parser.parse_args()
    out=ROOT/'evidence/hdl';out.mkdir(parents=True,exist_ok=True)
    missing=[n for n in ('iverilog','vvp') if not shutil.which(n)]
    result={'status':'NOT_RUN','layer':'RTL digital simulation, not analog/physical proof','selection':a.only,'missing_tools':missing,'checks':[]}
    if missing:
        result['reason']='Required simulator executables are not on PATH.'
        (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return 2
    try:
        result['iverilog_version']=subprocess.run(['iverilog','-V'],capture_output=True,text=True,timeout=15).stdout[:2000]
        entries=[('semantics','semantics_demo.sv','tb_semantics',None),
                 *[('fifo','sync_fifo.sv','tb_fifo',depth) for depth in (1,3,8)],
                 ('sat_add','sat_add_stream.sv','tb_sat_add',None),('scanout','scanout.sv','tb_scanout',None)]
        for name,source,top,depth in entries:
            if a.only not in ('all',name):continue
            tag=top+(f'_d{depth}' if depth is not None else '')
            executable=out/(tag+'.vvp');command=['iverilog','-g2012','-s',top,'-o',str(executable)]
            if depth is not None:command+=['-P',f'{top}.DEPTH={depth}']
            command +=[str(ROOT/'reference/rtl'/source),str(ROOT/'tests'/f'{top}.sv')]
            checked(command,out/f'{tag}_compile.log')
            run=['vvp',str(executable)]
            if name=='scanout':run +=[f'+CAPTURE={out / "scanout.csv"}']
            checked(run,out/f'{tag}_run.log')
            if name=='scanout':
                pixels=rows(out/'scanout.csv')
                if len(pixels)!=3072:raise AssertionError('scanout active pixel count')
                for idx,pixel in enumerate(pixels):
                    x,y=idx%64,idx//64
                    if (pixel['x'],pixel['y'])!=(x,y):raise AssertionError(f'scanout ordering at {idx}')
                    r,g,b=rgb(x,y)
                    if pixel['rgb']!=((r<<16)|(g<<8)|b):raise AssertionError(f'scanout color at {(x,y)}')
            result['checks'].append({'name':tag,'status':'PASS'})
        if a.only in ('all','g16'):
            vectors=out/'cpu_vectors';generate(vectors);executable=out/'tb_g16.vvp'
            checked(['iverilog','-g2012','-s','tb_g16','-o',str(executable),str(ROOT/'reference/rtl/g16_core.sv'),str(ROOT/'tests/tb_g16.sv')],out/'g16_compile.log')
            code={None:0,'fetch_address':1,'illegal_instruction':2,'data_address':3}
            for folder in sorted(p for p in vectors.iterdir() if p.is_dir()):
                observed=folder/'observed.csv';terminal=folder/'observed_terminal.txt'
                checked(['vvp',str(executable),f'+PROG={folder / "program.mem"}',f'+TRACE={observed}',f'+TERMINAL={terminal}'],folder/'run.log')
                expected=rows(folder/'expected.csv');actual=rows(observed)
                if expected!=actual:
                    mismatch=next((i for i,(x,y) in enumerate(zip(expected,actual)) if x!=y),min(len(expected),len(actual)))
                    raise AssertionError(f'{folder.name}: retirement mismatch at {mismatch}; expected length {len(expected)}, observed {len(actual)}')
                meta=json.loads((folder/'expected.json').read_text());lines=terminal.read_text().splitlines()
                fault,fc,pc=map(int,lines[0].split(','));regs=list(map(int,lines[1:9]));memory=list(map(int,lines[9:]))
                if (fault,fc,pc)!=(int(meta['fault'] is not None),code[meta['fault']],meta['pc']) or regs!=meta['registers'] or memory!=meta['memory']:
                    raise AssertionError(f'{folder.name}: terminal architectural state mismatch')
                result['checks'].append({'name':folder.name,'status':'PASS','retirements':len(actual)})
        result['status']='PASS';exitcode=0
    except (OSError,subprocess.TimeoutExpired,RuntimeError,AssertionError,ValueError) as exc:
        result['status']='FAIL';result['error']=str(exc);exitcode=1
    (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return exitcode
if __name__=='__main__':sys.exit(main())
