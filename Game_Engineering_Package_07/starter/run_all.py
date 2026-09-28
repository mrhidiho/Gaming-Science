"""Run the supplied references/demos/companions; these are not student assessment.

python starter/run_all.py
python starter/run_all.py --native  # additionally requires CMake and a C++17 compiler
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def run(command,timeout=60):
    result=subprocess.run(command,text=True,capture_output=True,timeout=timeout)
    if result.returncode:
        print(result.stdout);print(result.stderr,file=sys.stderr)
        raise RuntimeError('Command failed: '+' '.join(map(str,command)))
    print('PASS:', ' '.join(str(x) for x in command))
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--native',action='store_true');args=parser.parse_args()
    try:
        run([sys.executable,ROOT/'python'/'run_tests.py','--target','references'])
        run([sys.executable,ROOT/'python'/'test_properties.py'])
        for path in sorted((ROOT/'python'/'demos').glob('lesson_*.py')):run([sys.executable,path])
        for path in sorted((ROOT/'integration').glob('*_lab.py')):run([sys.executable,path])
        if args.native:
            if not shutil.which('cmake') or not shutil.which('ctest'):raise RuntimeError('CMake/CTest not found')
            with tempfile.TemporaryDirectory(prefix='volume06-native-') as folder:
                run(['cmake','-S',ROOT/'cpp','-B',folder,'-DCMAKE_BUILD_TYPE=Release'])
                run(['cmake','--build',folder,'--config','Release'])
                run(['ctest','--test-dir',folder,'-C','Release','--output-on-failure'])
        print('All selected package reference checks passed. Full labs and capstone evidence remain learner work.')
        return 0
    except (OSError,subprocess.TimeoutExpired,RuntimeError) as exc:
        print('FAILED:',exc,file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
