"""Read-only local tool report. Does not install or change system settings."""
import sys,shutil,subprocess,json,platform,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def inspect()->dict:
    result={'python':sys.version,'platform':platform.platform(),'python_compatible':sys.version_info>=(3,10),'tools':{}}
    for name,args in {'iverilog':['-V'],'vvp':['-V'],'verilator':['--version'],'yosys':['-V'],'ngspice':['--version'],'sby':['--version'],'boolector':['--version']}.items():
        path=shutil.which(name);entry={'available':bool(path),'path':path}
        if path:
            try:
                p=subprocess.run([path,*args],capture_output=True,text=True,timeout=15)
                entry.update({'exit_code':p.returncode,'version_output':(p.stdout+p.stderr).strip()[:2000]})
            except (OSError,subprocess.TimeoutExpired) as exc:entry['error']=str(exc)
        result['tools'][name]=entry
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'evidence/preflight.json');a=p.parse_args()
    result=inspect();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));sys.exit(0 if result['python_compatible'] else 2)
