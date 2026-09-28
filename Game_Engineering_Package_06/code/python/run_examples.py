"""Run one checked reference expression per lesson; not a replacement for the labs."""
import importlib.util,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
cases=json.loads((ROOT/'tests/exercise_cases.json').read_text())
for lid,pairs in cases.items():
    spec=importlib.util.spec_from_file_location('lesson',ROOT/'exercises/reference'/('lesson_'+lid.replace('.','_')+'.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    expression=pairs[0][0]
    print(f'{lid}: {expression} -> {eval(expression,mod.__dict__)}')
