#!/usr/bin/env python3
"""Report tool availability without installing software or accessing devices."""
import argparse,json,platform,shutil,subprocess,sys
from pathlib import Path


def inspect():
    tools={}
    for name,args in {
        'cmake':['--version'],'c++':['--version'],'iverilog':['-V'],
        'vvp':['-V'],'yosys':['-V'],'sby':['--version'],
        'boolector':['--version'],'openroad':['-version'],
    }.items():
        executable=shutil.which(name)
        record=dict(available=bool(executable),path=executable,version=None)
        if executable:
            try:
                done=subprocess.run([executable,*args],capture_output=True,text=True,timeout=8,check=False)
                record['version']=(done.stdout+done.stderr).strip().splitlines()[:4]
                record['version_command_returncode']=done.returncode
            except (OSError,subprocess.TimeoutExpired) as exc:
                record['version_error']=str(exc)
        tools[name]=record
    return dict(python=sys.version,python_executable=sys.executable,platform=platform.platform(),
        architecture=platform.machine(),tools=tools,
        note='Availability is not execution, verification, licensing approval or a completed lab.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args();result=json.dumps(inspect(),indent=2)+'\n'
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(result,encoding='utf-8')
    else:print(result,end='')
