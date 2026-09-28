"""Verify first, then create a new source release from a conservative allowlist."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--inject-failure",action="store_true")
    parser.add_argument("--build-dir",type=Path,help="optional existing build directory; omit for a fresh build")
    args=parser.parse_args();output=args.output.resolve()
    if output.exists():parser.error("output already exists; choose a new release filename")
    command=[sys.executable,str(ROOT/"tools/verify.py")]
    if args.inject_failure:command.append("--inject-failure")
    if args.build_dir:command.extend(["--build-dir",str(args.build_dir.resolve())])
    subprocess.run(command,check=True,timeout=600)
    allowed={"native","python","capstone","tools","templates","data","source","sql","source","sql","source","sql","source","sql"}
    selected=[]
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():continue
        relative=path.relative_to(ROOT)
        if "__pycache__" in relative.parts or path.suffix in {".pyc",".sqlite",".db",".exe",".o"}:continue
        if relative.parts[0] in allowed or relative.as_posix() in {"README.md","environment_check.py","check_lab.py"}:
            selected.append((path,relative.as_posix()))
    manifest={"kind":"verified source release","files":[{"path":name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()} for path,name in selected],
              "note":"Per-file integrity; manifest excludes itself. Source procedure reproducibility is not cross-toolchain binary identity."}
    output.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive creation avoids replacing an existing successful release.
    with zipfile.ZipFile(output,"x",compression=zipfile.ZIP_DEFLATED) as archive:
        for path,name in selected:archive.write(path,"ForgeQueue_Source/"+name)
        archive.writestr("ForgeQueue_Source/RELEASE_MANIFEST.json",json.dumps(manifest,indent=2))
    print(output)

if __name__=="__main__":
    try:main()
    except (OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as error:
        print("Release not completed:",error,file=sys.stderr);raise SystemExit(1)
