"""Run the three supplied ideal/toy SPICE decks and retain logs."""
import sys,subprocess,shutil,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/spice';OUT.mkdir(parents=True,exist_ok=True)
result={'status':'NOT_RUN','layer':'SPICE ideal/toy circuit models, not hardware measurements','runs':[]};code=2
if not shutil.which('ngspice'):result['reason']='ngspice is not on PATH'
else:
    code=0;result['status']='PASS'
    try:
        for deck in sorted((ROOT/'reference/spice').glob('*.cir')):
            p=subprocess.run(['ngspice','-b',str(deck)],cwd=OUT,capture_output=True,text=True,timeout=60)
            (OUT/(deck.stem+'.log')).write_text(p.stdout+p.stderr);result['runs'].append({'deck':deck.name,'exit_code':p.returncode})
            if p.returncode:raise RuntimeError(f'failed deck {deck.name}')
    except (OSError,subprocess.TimeoutExpired,RuntimeError) as exc:result['status']='FAIL';result['error']=str(exc);code=1
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(code)
