# Worked demonstration for Lesson 04.3.
from pathlib import Path
import runpy

package_root = Path(__file__).resolve().parents[1]
print("Running the isolated Git demonstration.")
runpy.run_path(str(package_root / "tools" / "git_sandbox.py"),
               run_name="__main__")
