"""Read-only environment check for the extracted Package 03 folder."""
import sys
from pathlib import Path
import platform

root = Path(__file__).resolve().parent
print("Package 03: Mathematics for Games and Computing")
print("Python:", platform.python_version())
print("Platform:", platform.system(), platform.machine())
if sys.version_info < (3, 11):
    print("Use Python 3.11+ for the selected course baseline.")
    raise SystemExit(1)
required = ["mathkit.py", "run_example.py", "check_lab.py",
            "examples/EXPECTED_OUTPUT.json", "labs/student/lab_06_1.py"]
missing = [p for p in required if not (root / p).is_file()]
if missing:
    print("Missing bundle files:", ", ".join(missing))
    print("Extract the entire ZIP and retain its folder structure.")
    raise SystemExit(1)
print("Required local files found. Core examples need no third-party packages.")
print("Tested by the authoring environment: Python 3.13.5, Linux.")
print("Next: run_example.py 06.1, then work in labs/student/lab_06_1.py.")
