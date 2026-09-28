"""Run a lesson demonstration using the Python standard library only."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
ROOT = Path(__file__).resolve().parent
IDS = [f'{m:02}.{i}' for m in range(6,11) for i in range(1,5)]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson',nargs='?',choices=IDS)
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--verify',action='store_true',help='compare text with the recorded test environment')
    args=parser.parse_args()
    if bool(args.lesson)==args.all:parser.error('choose one lesson or --all')
    expected=json.loads((ROOT/'examples/EXPECTED_OUTPUT.json').read_text())
    for lesson in IDS if args.all else [args.lesson]:
        print(f'--- Lesson {lesson} ---',flush=True)
        path=ROOT/'examples'/('lesson_'+lesson.replace('.','_')+'.py')
        # -S omits optional site startup; every example uses only the standard library.
        result=subprocess.run([sys.executable,'-S',str(path)],capture_output=True,text=True,timeout=30)
        print(result.stdout,end='')
        if result.returncode:
            print(result.stderr,file=sys.stderr)
            return result.returncode
        if args.verify and result.stdout!=expected[lesson]:
            print('Recorded text differs. Inspect numeric rounding and environment before concluding the mathematical result is wrong.',file=sys.stderr)
            return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
