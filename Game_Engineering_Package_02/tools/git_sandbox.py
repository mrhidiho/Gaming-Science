"""Exercise commits/branch/merge/revert in a new temporary repository only.

Never runs against the learner's existing repository. Uses command-scoped
identity, not global Git configuration. Deletes only its own temporary folder.
"""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

def main():
    git=shutil.which('git')
    if not git:
        print('Git not found. Complete the reading and install through the approved route.')
        return 1
    with tempfile.TemporaryDirectory(prefix='game-course-git-') as temp:
        root=Path(temp)
        def run(*args):
            cmd=[git,'-c','user.name=Course Sandbox','-c',
                 'user.email=course-sandbox@example.invalid',*args]
            result=subprocess.run(cmd,cwd=root,capture_output=True,text=True,
                                  check=True,timeout=15)
            return result.stdout.strip()
        run('init','--initial-branch=main')
        (root/'rules.txt').write_text('damage=3\n',encoding='utf-8')
        run('add','rules.txt'); run('commit','-m','Define starting damage rule')
        run('switch','-c','boundary-fix')
        (root/'rules.txt').write_text('damage=3\nhealth_min=0\n',encoding='utf-8')
        run('add','rules.txt'); run('commit','-m','Specify zero-health boundary')
        run('switch','main'); run('merge','--ff-only','boundary-fix')
        (root/'rules.txt').write_text('damage=30\nhealth_min=0\n',encoding='utf-8')
        run('add','rules.txt'); run('commit','-m','Demonstrate a mistaken damage change')
        run('revert','--no-edit','HEAD')
        final=(root/'rules.txt').read_text(encoding='utf-8')
        assert final=='damage=3\nhealth_min=0\n'
        assert run('status','--porcelain')==''
        print('Temporary repository only; no existing course files changed.')
        print(run('log','--oneline','--all','--graph'))
        print('Restored rules:\n'+final)
        print('PASS: branch, merge, revert and clean working tree.')
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,subprocess.SubprocessError) as exc:
        print('Git exercise failed:',exc)
        raise SystemExit(1)
