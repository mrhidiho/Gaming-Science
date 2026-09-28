"""Start a fixed, bounded child program. No shell or user-supplied source."""
import json
import subprocess
import sys

def run_child(values: list[int], timeout: float = 3.0) -> dict:
    if type(values) is not list or len(values) > 256:
        raise ValueError("values must be a list of at most 256 integers")
    if any(type(x) is not int or not 0 <= x <= 1000 for x in values):
        raise ValueError("each value must be an integer in 0..1000")
    if not 0 < timeout <= 30:
        raise ValueError("timeout must be in (0,30]")
    source = ("import json,os,sys; v=json.loads(sys.stdin.read()); "
              "print(json.dumps({'pid':os.getpid(),'sum':sum(v)}))")
    completed = subprocess.run([sys.executable, "-I", "-c", source],
        input=json.dumps(values), text=True, capture_output=True,
        timeout=timeout, check=True)
    result = json.loads(completed.stdout)
    if type(result.get("pid")) is not int or type(result.get("sum")) is not int:
        raise RuntimeError("invalid result from fixed child program")
    return result
