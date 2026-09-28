# Worked demonstration for Lesson 01.2.
from pathlib import Path
import sys

print("python:", sys.version.split()[0])
print("script name:", Path(__file__).name)
print("working directory name:", Path.cwd().name)
print("script exists:", Path(__file__).is_file())
