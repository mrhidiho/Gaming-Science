#!/usr/bin/env python3
"""Check inventoried release files and curriculum counts; no network or writes."""
from pathlib import Path
import hashlib,json,sys


def validate(root):
    root=root.resolve()
    manifest=json.loads((root/'FILE_MANIFEST.json').read_text(encoding='utf-8'))
    issues=[];seen=set()
    for item in manifest['files']:
        name=item['path']
        if name in seen:
            issues.append('duplicate manifest path: '+name);continue
        seen.add(name)
        relative=Path(name)
        target=(root/relative).resolve()
        if relative.is_absolute() or '..' in relative.parts or not target.is_relative_to(root):
            issues.append('unsafe manifest path: '+name);continue
        if not target.is_file():issues.append('missing file: '+name);continue
        payload=target.read_bytes()
        if len(payload)!=item['bytes']:issues.append('size differs: '+name)
        if hashlib.sha256(payload).hexdigest()!=item['sha256']:issues.append('hash differs: '+name)
    course=json.loads((root/'curriculum.json').read_text(encoding='utf-8'))
    expected=[f'{m}.{i}' for m in range(46,51) for i in range(1,5)]
    if [x['id'] for x in course['lessons']]!=expected:issues.append('lesson IDs differ')
    for lesson in course['lessons']:
        if len(lesson['quiz'])!=3 or len(lesson['answers'])!=3:issues.append('quiz/answer count: '+lesson['id'])
    if course['package']!=11 or course['volume']!=10:issues.append('package/volume mismatch')
    if len(course['modules'])!=5:issues.append('module count differs')
    return issues,len(manifest['files'])


if __name__=='__main__':
    try:
        errors,count=validate(Path(__file__).parent)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print('VALIDATION ERROR:',exc,file=sys.stderr);sys.exit(2)
    if errors:
        print('\n'.join(errors),file=sys.stderr);sys.exit(1)
    print(f'PASS: {count} inventoried files match; 20 lesson IDs and 60 question/answer pairs checked.')
    print('The manifest does not hash itself. Extra learner files are ignored. Integrity is not authenticity or correctness.')
