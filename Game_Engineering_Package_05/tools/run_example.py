from pathlib import Path
import argparse
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
NATIVE={f"{module}.{lesson}" for module in [16,18] for lesson in range(1,5)}
PYTHON={f"{module}.{lesson}" for module in [17,19,20] for lesson in range(1,5)}

def find_executable(build,name):
    for path in [build/name,build/(name+".exe"),build/"Debug"/(name+".exe"),build/"Release"/(name+".exe")]:
        if path.is_file():return path.resolve()
    raise FileNotFoundError(f"Build {name} first; no executable in {build}")

def command(lesson,build):
    stem=lesson.replace(".","_")
    if lesson in NATIVE:return [str(find_executable(build,"demo_"+stem))]
    if lesson in PYTHON:return [sys.executable,str(ROOT/"python"/"examples"/("lesson_"+stem+".py"))]
    raise ValueError("unknown lesson")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Run one worked reference example (not a student assessment)")
    parser.add_argument("lesson",choices=sorted(NATIVE|PYTHON))
    parser.add_argument("--build-dir",type=Path,default=ROOT/"build")
    args=parser.parse_args()
    try:raise SystemExit(subprocess.run(command(args.lesson,args.build_dir.resolve()),timeout=15).returncode)
    except (OSError,ValueError,subprocess.TimeoutExpired) as error:parser.exit(2,str(error)+"\n")
