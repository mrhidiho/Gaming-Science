"""Check one exercise. Defaults to unfinished student code, not reference code."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
NATIVE={f"{m}.{i}" for m in [16,18] for i in range(1,5)}
PYTHON={f"{m}.{i}" for m in [17,19] for i in range(1,5)}

def run(command,**kwargs):
    print("+", " ".join(map(str,command)),flush=True)
    subprocess.run(list(map(str,command)),check=True,timeout=180,**kwargs)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("lesson",choices=sorted(NATIVE|PYTHON))
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--reference",action="store_true")
    group.add_argument("--student",action="store_true")
    parser.add_argument("--build-dir",type=Path)
    args=parser.parse_args()
    implementation="reference" if args.reference else "student"
    if args.lesson in NATIVE:
        build=(args.build_dir or ROOT/".build"/("check-"+implementation)).resolve()
        run(["cmake","-S",ROOT/"native","-B",build,"-DCMAKE_BUILD_TYPE=Debug",
             "-DSTUDENT_EXERCISES="+("OFF" if args.reference else "ON")])
        run(["cmake","--build",build,"--target","contract_tests","--config","Debug","--parallel","2"])
        run(["ctest","--test-dir",build,"-C","Debug","--output-on-failure","-R","^lab_"+re.escape(args.lesson)+"$"])
    else:
        env=os.environ.copy();env["COURSE_IMPL"]=implementation
        name="Test"+args.lesson.replace(".","")
        run([sys.executable,"-m","unittest","python.tests.test_labs."+name,"-v"],cwd=ROOT,env=env)
    print(implementation,"checks passed; written reasoning and practical evidence remain required.")

if __name__=="__main__":
    try:main()
    except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as error:
        print("Check failed:",error,file=sys.stderr);raise SystemExit(1)
