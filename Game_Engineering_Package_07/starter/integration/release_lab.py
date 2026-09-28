"""Local staged release pointer and recoverable JSON save demonstration.

Process interruption is injected with exceptions. This does not establish
power-loss durability, signed update authenticity, or every filesystem behavior.
"""
import hashlib
import json
import os
from pathlib import Path
import tempfile


def atomic_json(path,data,fail_before_replace=False):
    raw=json.dumps(data,sort_keys=True,allow_nan=False).encode()
    if len(raw)>1024*1024:raise ValueError('save size cap')
    temporary=path.with_suffix(path.suffix+'.pending')
    with temporary.open('wb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
    if fail_before_replace:raise RuntimeError('injected interruption before activation')
    os.replace(temporary,path)
    # A production durability contract may require directory sync and platform
    # handling. This sample deliberately makes no crash-durability guarantee.


def experiment():
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);save=root/'save.json';pointer=root/'current.json'
        atomic_json(save,{'version':1,'score':10})
        try:atomic_json(save,{'version':1,'score':99},True)
        except RuntimeError:pass
        assert json.loads(save.read_text())['score']==10
        (root/'v1').mkdir();(root/'v1'/'game.txt').write_text('release one')
        atomic_json(pointer,{'release':'v1'})
        stage=root/'v2';stage.mkdir();content=b'release two';(stage/'game.txt').write_bytes(content)
        expected=hashlib.sha256(content).hexdigest()
        assert hashlib.sha256((stage/'game.txt').read_bytes()).hexdigest()==expected
        try:atomic_json(pointer,{'release':'v2'},True)
        except RuntimeError:pass
        assert json.loads(pointer.read_text())['release']=='v1'
        atomic_json(pointer,{'release':'v2'})
        assert (root/json.loads(pointer.read_text())['release']/'game.txt').read_bytes()==content
        return {'passed':True,'save_old_value_survived':True,'old_release_until_activation':True,'new_release_after_activation':True,
                'limits':'Local exception injection; hash is integrity check only; no signed updates or power-loss certification.'}

if __name__=='__main__':print(json.dumps(experiment(),indent=2))
