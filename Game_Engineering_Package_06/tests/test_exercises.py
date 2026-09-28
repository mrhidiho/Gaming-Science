"""Run from the package root: python tests/test_exercises.py --track reference.
The starter track deliberately fails until the learner implements its contracts.
"""
import argparse, importlib.util, json, math, pathlib, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('--track',choices=['reference','starter'],default='reference'); p.add_argument('--lesson')
a=p.parse_args()
cases=json.loads((ROOT/'tests/exercise_cases.json').read_text())
if a.lesson and a.lesson not in cases: p.error('unknown lesson')
class ContractTests(unittest.TestCase): pass
loaded={}
for lid, pairs in cases.items():
    if a.lesson and a.lesson!=lid: continue
    spec=importlib.util.spec_from_file_location('ex_'+lid.replace('.','_'), ROOT/'exercises'/a.track/('lesson_'+lid.replace('.','_')+'.py'))
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); loaded[lid]=module
    for ix,(expr,expect) in enumerate(pairs):
        def run(self,expr=expr,expect=expect,module=module):
            if expect=='ValueError':
                with self.assertRaises(ValueError): eval(expr,module.__dict__)
            else:
                actual=eval(expr,module.__dict__); expected=eval(expect,{'math':math})
                if isinstance(expected,float): self.assertAlmostEqual(actual,expected,places=10)
                else: self.assertEqual(actual,expected)
        setattr(ContractTests,'test_'+lid.replace('.','_')+'_'+str(ix+1),run)
# Additional state-preservation and history tests run only when their lesson is selected.
if '24.4' in loaded:
    def no_mutation(self):
        m=loaded['24.4']; source={'version':1,'entities':[{'id':'a','position':{'x':1,'y':2,'z':3}}]}
        before=json.dumps(source); result=m.validate_scene(source); result['entities'][0]['position'][0]=99
        self.assertEqual(json.dumps(source),before)
    ContractTests.test_24_4_no_mutation=no_mutation
if '25.3' in loaded:
    def invalid_no_mutation(self):
        m=loaded['25.3']; state={'a':[0,0,0]}; undo=[]; redo=[{'old':True}]
        with self.assertRaises(ValueError): m.apply_edit(state,undo,redo,'a',[float('nan'),0,0])
        self.assertEqual((state,undo,redo),({'a':[0,0,0]},[],[{'old':True}]))
    def records(self):
        m=loaded['25.3']; state={'a':[0,0,0]}; undo=[]; redo=[{'old':True}]
        m.apply_edit(state,undo,redo,'a',[1,2,3]); self.assertEqual(redo,[])
        self.assertEqual(undo[0],{'id':'a','before':[0,0,0],'after':[1.0,2.0,3.0]})
        self.assertEqual(state['a'],[1.0,2.0,3.0])
    ContractTests.test_25_3_invalid_preserves_state=invalid_no_mutation
    ContractTests.test_25_3_records_history=records
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests))
sys.exit(not result.wasSuccessful())
