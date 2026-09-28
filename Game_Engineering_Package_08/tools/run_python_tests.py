"""Execute all supplied Python reference tests and retain auditable output."""
import sys,subprocess,json,platform,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
start=time.time();p=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,capture_output=True,text=True)
log=p.stdout+p.stderr;(OUT/'python_tests.txt').write_text(log)
result={'status':'PASS' if p.returncode==0 else 'FAIL','layer':'Python reference tests only',
        'python':sys.version,'platform':platform.platform(),'command':[sys.executable,'-m','unittest','discover','-s','tests','-v'],
        'exit_code':p.returncode,'elapsed_seconds':round(time.time()-start,4),'log':'python_tests.txt'}
(OUT/'python_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(log);sys.exit(p.returncode)
