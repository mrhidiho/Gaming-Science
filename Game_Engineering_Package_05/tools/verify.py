"""Local reference verification. No downloads, installation or public services."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from environment_check import report
from tools.run_example import command,find_executable,NATIVE,PYTHON

def run(cmd,**kwargs):
    print("+", " ".join(map(str,cmd)),flush=True)
    subprocess.run(list(map(str,cmd)),check=True,timeout=180,**kwargs)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir",type=Path)
    parser.add_argument("--inject-failure",action="store_true")
    args=parser.parse_args()
    if args.inject_failure:
        code="import unittest\nclass Gate(unittest.TestCase):\n def test_injected(self): self.fail('Intentional pipeline test failure')\nunittest.main()\n"
        run([sys.executable,"-c",code])
    if args.build_dir:
        build=args.build_dir.resolve()
    else:
        parent=ROOT/".build";parent.mkdir(exist_ok=True)
        build=Path(tempfile.mkdtemp(prefix="verify-",dir=parent))
    run(["cmake","-S",ROOT/"native","-B",build,"-DCMAKE_BUILD_TYPE=Debug","-DSTUDENT_EXERCISES=OFF"])
    run(["cmake","--build",build,"--config","Debug","--parallel","2"])
    run(["ctest","--test-dir",build,"-C","Debug","--output-on-failure"])
    native=find_executable(build,"native_worker")
    env=os.environ.copy();env["COURSE_IMPL"]="reference";env["NATIVE_WORKER"]=str(native)
    run([sys.executable,"-m","unittest","discover","-s","python/tests","-v"],cwd=ROOT,env=env)
    expected=json.loads((ROOT/"data/expected_examples.json").read_text())
    for lesson in sorted(NATIVE|PYTHON):
        completed=subprocess.run(command(lesson,build),capture_output=True,text=True,check=True,timeout=15)
        if completed.stdout.strip()!=expected[lesson].strip():
            raise RuntimeError("worked-example output mismatch: "+lesson)
        print("PASS example",lesson)
    run([sys.executable,ROOT/"capstone/reference/run_demo.py","--native",native],cwd=ROOT)
    (build/"environment.json").write_text(json.dumps(report(),indent=2)+"\n")
    print("Reference verification completed. Build directory:",build)
    print("This does not certify student work, hardware performance or all concurrent executions.")

if __name__=="__main__":
    try:main()
    except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired,RuntimeError) as error:
        print("VERIFICATION FAILED:",error,file=sys.stderr);raise SystemExit(1)
