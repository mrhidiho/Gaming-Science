"""Bounded JSON parsing and replace-on-success saves for an educational game.

A same-directory temporary file prevents an ordinary failed write from replacing
the previous save. This is not a cross-platform power-loss durability guarantee,
a concurrent-writer transaction system, or an untrusted-directory security design.
"""
from dataclasses import asdict
import json
import os
from pathlib import Path
import tempfile
from .model import RULES_ID,State,normalise,validate

MAX_BYTES=65536
MAX_COMMANDS=1000

def _unique_pairs(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field')
        result[key]=value
    return result

def _reject_constant(value):
    raise ValueError('non-finite JSON constant: '+value)

def parse(text):
    if type(text) is not str or len(text.encode('utf-8'))>MAX_BYTES:
        raise ValueError('file exceeds the 64 KiB limit')
    try:
        return json.loads(text,object_pairs_hook=_unique_pairs,
                          parse_constant=_reject_constant)
    except (json.JSONDecodeError,RecursionError) as exc:
        raise ValueError('invalid JSON') from exc

def pack_state(state):
    validate(state)
    return {'version':1,'rules':RULES_ID,'state':asdict(state)}

def unpack_state(payload):
    if type(payload) is not dict or set(payload)!={'version','rules','state'}:
        raise ValueError('invalid save envelope')
    if type(payload['version']) is not int or payload['version']!=1:
        raise ValueError('unsupported save version')
    if payload['rules']!=RULES_ID:
        raise ValueError('incompatible map/rules ID')
    data=payload['state']
    if type(data) is not dict or set(data)!={'x','y','energy','turns','status'}:
        raise ValueError('invalid state fields')
    return validate(State(**data))

def _read(path):
    with Path(path).open('rb') as stream:
        raw=stream.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:
        raise ValueError('file exceeds the 64 KiB limit')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError('file must be UTF-8') from exc

def load(path):
    return unpack_state(parse(_read(path)))

def _atomic_json(path,payload):
    path=Path(path)
    text=json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if len(text.encode('utf-8'))>MAX_BYTES:
        raise ValueError('encoded file exceeds the 64 KiB limit')
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',newline='\n',
                dir=path.parent,prefix='.'+path.name+'.',suffix='.tmp',delete=False) as stream:
            temporary=Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary,path)
        temporary=None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

def save(path,state):
    _atomic_json(path,pack_state(state))

def write_replay(path,initial,commands):
    if type(commands) is not list or len(commands)>MAX_COMMANDS:
        raise ValueError('replay requires at most 1000 commands')
    for command in commands:
        normalise(command)
    _atomic_json(path,{'version':1,'rules':RULES_ID,
                      'initial':pack_state(initial),'commands':commands})

def read_replay(path):
    data=parse(_read(path))
    if type(data) is not dict or set(data)!={'version','rules','initial','commands'}:
        raise ValueError('invalid replay envelope')
    if type(data['version']) is not int or data['version']!=1 or data['rules']!=RULES_ID:
        raise ValueError('unsupported replay version/rules')
    commands=data['commands']
    if type(commands) is not list or len(commands)>MAX_COMMANDS:
        raise ValueError('replay requires at most 1000 commands')
    for command in commands:
        normalise(command)
    return unpack_state(data['initial']),list(commands)
