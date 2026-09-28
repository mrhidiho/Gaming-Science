"""Read-only environment report; installs nothing and changes no settings."""
import json
import platform
import shutil
import sqlite3
import subprocess
import sys

def version(command):
    executable=shutil.which(command)
    if not executable:return {"available":False}
    try:
        run=subprocess.run([executable,"--version"],capture_output=True,text=True,timeout=5)
        return {"available":True,"first_line":(run.stdout or run.stderr).splitlines()[0]}
    except (OSError,subprocess.TimeoutExpired,IndexError) as error:
        return {"available":True,"probe_error":type(error).__name__}

def report():
    return {"python":sys.version,"python_executable":sys.executable,
            "platform":platform.platform(),"machine":platform.machine(),
            "sqlite_runtime":sqlite3.sqlite_version,
            "tools":{name:version(name) for name in ["cmake","g++","clang++","git"]},
            "note":"No compiler probe here establishes complete C++20 library support. Build the supplied targets."}

if __name__=="__main__":print(json.dumps(report(),indent=2))
