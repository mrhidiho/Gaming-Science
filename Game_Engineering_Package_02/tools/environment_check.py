"""Read-only environment report. No packages are installed or settings changed."""
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    git=shutil.which('git')
    report={'python':sys.version.split()[0], 'executable':sys.executable,
            'platform':platform.platform(), 'working_directory':str(Path.cwd()),
            'package_root':str(Path(__file__).resolve().parents[1]),
            'python_3_11_or_later':sys.version_info >= (3,11)}
    if git:
        try:
            report['git']=subprocess.run([git,'--version'],check=True,
                capture_output=True,text=True,timeout=10).stdout.strip()
        except (OSError,subprocess.SubprocessError):
            report['git']='found, but version check failed'
    else:
        report['git']='not found; needed at Lesson 04.3, not for first lessons'
    print(json.dumps(report,indent=2))
    return 0 if report['python_3_11_or_later'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
