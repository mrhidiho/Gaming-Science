"""Print only local tool information. No network access or system changes."""
import platform
import sys

print("Python:", platform.python_version())
print("Implementation:", platform.python_implementation())
print("Operating system:", platform.system())
print("Architecture:", platform.machine())
print("Python executable:", sys.executable)
print("Keep the interpreter version and exact command in your private lab journal.")
