"""Run tests against the completed REFERENCE game, not the learner's scaffold."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
result=subprocess.run([sys.executable,'-m','unittest','discover','-s',
    str(ROOT/'capstone/reference/tests'),'-v'])
raise SystemExit(result.returncode)
