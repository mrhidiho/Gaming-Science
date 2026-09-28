# Worked demonstration for Lesson 05.4.
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
command = [sys.executable, str(root / "capstone" / "reference" / "play.py"),
           "--demo"]
result = subprocess.run(command, capture_output=True, text=True,
                        timeout=10, check=True)
print(result.stdout.splitlines()[-1])
print("Reference demonstration completed; your own Gate A remains required.")
