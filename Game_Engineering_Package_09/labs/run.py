"""Demos and per-lesson contract checks; Python standard library only."""
from __future__ import annotations
import argparse, importlib, json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))

def load_cases(): return json.loads((ROOT/'data/LAB_CASES.json').read_text())

def equivalent(actual,expected):
    if type(expected) is dict:
        return type(actual) is dict and set(actual)==set(expected) and all(equivalent(actual[k],v) for k,v in expected.items())
    if type(expected) is list:
        return type(actual) is list and len(actual)==len(expected) and all(equivalent(a,b) for a,b in zip(actual,expected))
    if isinstance(expected,(int,float)) and not isinstance(expected,bool):
        return isinstance(actual,(int,float)) and not isinstance(actual,bool) and math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-10)
    return type(actual) is type(expected) and actual==expected

def check_case(module,case):
    try: result=module.solve(case['input'])
    except Exception as exc:
        if type(exc).__name__==case.get('raises'): return True,''
        return False,f'unexpected {type(exc).__name__}: {exc}'
    if 'raises' in case: return False,'expected '+case['raises']
    return equivalent(result,case['expected']),f'expected {case["expected"]}, got {result}'

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['list','demo','check','all'])
    parser.add_argument('lesson',nargs='?')
    parser.add_argument('--student',action='store_true',help='check starter/student implementations')
    args=parser.parse_args(argv); cases=load_cases()
    if args.command=='list':
        print('\n'.join(cases)); return 0
    if args.command!='all' and args.lesson not in cases:
        parser.error('provide an available lesson ID, for example 36.1')
    route='starters' if args.student else 'reference'; failed=0; count=0
    ids=list(cases) if args.command=='all' else [args.lesson]
    for identity in ids:
        module=importlib.import_module('labs.'+route+'.lesson_'+identity.replace('.','_'))
        if args.command=='demo':
            for case in [x for x in cases[identity] if 'expected' in x][:3]:
                print(json.dumps({'lesson':identity,'case':case['name'],'input':case['input'],'result':module.solve(case['input'])},indent=2))
        else:
            for case in cases[identity]:
                ok,message=check_case(module,case); count+=1
                if not ok: failed+=1; print(f'FAIL {identity}: {case["name"]}: {message}')
            print(f'{identity}: checked {len(cases[identity])} cases ({route})')
    if args.command!='demo': print(f'{count-failed}/{count} passed; {failed} failed')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
