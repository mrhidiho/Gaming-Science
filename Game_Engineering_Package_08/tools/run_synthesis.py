"""Generic Yosys cell reports; no selected FPGA, place/route, physical timing or Fmax."""
import sys,shutil,subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/synthesis';OUT.mkdir(parents=True,exist_ok=True)
result={'status':'NOT_RUN','layer':'generic synthesis only','target':None,'runs':[]}
if not shutil.which('yosys'):
    result['reason']='yosys is not on PATH';code=2
else:
    code=0;result['version']=subprocess.run(['yosys','-V'],capture_output=True,text=True,timeout=15).stdout.strip()
    try:
        for depth in(3,8):
            netlist=OUT/f'fifo_d{depth}.json'
            script=f'read_verilog -sv -D SYNTHESIS reference/rtl/sync_fifo.sv; chparam -set WIDTH 16 -set DEPTH {depth} sync_fifo; hierarchy -check -top sync_fifo; proc; opt; memory; opt; techmap; opt; check; stat; write_json "{netlist}"'
            p=subprocess.run(['yosys','-p',script],cwd=ROOT,capture_output=True,text=True,timeout=120)
            log=OUT/f'fifo_d{depth}.log';log.write_text(p.stdout+p.stderr)
            result['runs'].append({'depth':depth,'exit_code':p.returncode,'log':log.name})
            if p.returncode:raise RuntimeError(f'Yosys failed: {log}')
        result['status']='PASS'
    except (OSError,subprocess.TimeoutExpired,RuntimeError) as exc:result['status']='FAIL';result['error']=str(exc);code=1
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(code)
