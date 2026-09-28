#!/usr/bin/env python3
"""Check visible warm-up cases. Pending starters are expected, not passing work."""
from __future__ import annotations
import argparse, importlib.util, json, math
from pathlib import Path


def same(a,b):
    if type(b) is bool: return type(a) is bool and a==b
    if isinstance(b,(int,float)):
        return not isinstance(a,bool) and isinstance(a,(int,float)) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10)
    if isinstance(b,list): return isinstance(a,(list,tuple)) and len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lesson',default='all')
    args=p.parse_args()
    base=Path(__file__).parent/'exercises'
    cases=json.loads((base/'cases.json').read_text())
    if args.lesson!='all' and args.lesson not in cases: p.error('unknown lesson ID')
    selected=cases if args.lesson=='all' else {args.lesson:cases[args.lesson]}
    pending=failed=passed=0
    for id,c in selected.items():
        spec=importlib.util.spec_from_file_location('exercise_'+id.replace('.','_'),base/f"lesson_{id.replace('.','_')}.py")
        module=importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            value=module.solve(c['input'])
            if not same(value,c['expected']):
                failed+=1;print(id,'FAIL',repr(value),'expected',repr(c['expected']))
            else: passed+=1;print(id,'PASS (visible warm-up only)')
        except NotImplementedError:
            pending+=1; print(id,'PENDING: learner implementation required')
        except Exception as exc:
            failed+=1;print(id,'ERROR',type(exc).__name__,str(exc))
    print(f'{passed} passed; {pending} pending; {failed} failed')
    return 1 if failed else 2 if pending else 0

if __name__=='__main__': raise SystemExit(main())
