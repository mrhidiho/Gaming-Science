"""Transactional idempotency, failure injection and fresh-process persistence.

Only synthetic principals are used. Do not deploy this as an account service.
"""
from __future__ import annotations
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile


def initialize(path: Path) -> None:
    with sqlite3.connect(path) as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS rewards
            (id TEXT PRIMARY KEY, player TEXT NOT NULL, points INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS balances
            (player TEXT PRIMARY KEY, points INTEGER NOT NULL);''')


def award(path: Path, principal: str, operation: tuple[str,str,int], failure: str='') -> bool:
    if principal!='match_authority':raise PermissionError('synthetic principal rejected')
    ident,player,points=operation
    if not all(isinstance(v,str) and 1<=len(v)<=64 for v in (ident,player)) or type(points)is not int or not 0<=points<=1000:
        raise ValueError('invalid operation')
    db=sqlite3.connect(path)
    try:
        db.execute('BEGIN IMMEDIATE')
        existing=db.execute('SELECT player, points FROM rewards WHERE id=?',(ident,)).fetchone()
        if existing:
            if existing!=(player,points):raise ValueError('idempotency conflict')
            db.commit();return False
        db.execute('INSERT INTO rewards VALUES (?,?,?)',operation)
        db.execute('INSERT INTO balances VALUES (?,?) ON CONFLICT(player) DO UPDATE SET points=points+excluded.points',(player,points))
        if failure=='before_commit':raise RuntimeError('injected pre-commit failure')
        db.commit()
        if failure=='after_commit':raise RuntimeError('injected lost response after commit')
        return True
    except Exception:
        db.rollback();raise
    finally:db.close()


def read(path: Path) -> dict:
    with sqlite3.connect(path) as db:
        return {'balances':dict(db.execute('SELECT player,points FROM balances ORDER BY player')),
                'rewards':db.execute('SELECT COUNT(*) FROM rewards').fetchone()[0]}


def experiment() -> dict:
    with tempfile.TemporaryDirectory() as folder:
        path=Path(folder)/'results.sqlite';initialize(path)
        for phase in ('before_commit','after_commit'):
            try:award(path,'match_authority',('r17','player1',50),phase)
            except RuntimeError:pass
            else:raise AssertionError('failure injection not reached')
            if phase=='before_commit':assert read(path)=={'balances':{},'rewards':0}
        assert award(path,'match_authority',('r17','player1',50)) is False
        for principal,op,expected in [('player1',('r18','player1',50),PermissionError),('match_authority',('r17','player1',500),ValueError)]:
            try:award(path,principal,op)
            except expected:pass
            else:raise AssertionError('invalid request accepted')
        # Start a fresh interpreter: no in-memory store survives this boundary.
        result=json.loads(subprocess.check_output([sys.executable,__file__,'--read',str(path)],text=True))
        assert result=={'balances':{'player1':50},'rewards':1}
        return {'passed':True,'fresh_process_state':result,'checked':['rollback before commit','reply lost after commit','exact retry','conflicting retry','synthetic ownership','fresh interpreter read'],
                'scope':'SQLite local test; no external identity provider or power-failure test'}

if __name__=='__main__':
    print(json.dumps(read(Path(sys.argv[2])) if len(sys.argv)==3 and sys.argv[1]=='--read' else experiment(),indent=2))
