import unittest
import random
from gradlab.compiler import *

class CompilerTests(unittest.TestCase):
    def test_liveness_loop(self):
        b={'entry':dict(use=[],defs=['i'],succ=['loop']),
           'loop':dict(use=['i','n'],defs=['i'],succ=['loop','exit']),
           'exit':dict(use=['i'],defs=[],succ=[])}
        r=live_variables(b)
        self.assertEqual(r['live_in']['loop'],['i','n'])
        self.assertIn('n',r['live_in']['entry']); self.assertGreater(r['iterations'],1)
    def test_cfg_phi(self):
        b={'entry':{'term':['br','cond','yes','no']},
           'yes':{'code':[['a','copy',[1]]],'term':['jmp','merge']},
           'no':{'code':[['b','copy',[2]]],'term':['jmp','merge']},
           'merge':{'phi':{'x':{'yes':'a','no':'b'}},'term':['ret','x']}}
        self.assertEqual(run_cfg(b,{'cond':1}),1); self.assertEqual(run_cfg(b,{'cond':0}),2)
    def test_cfg_fuel(self):
        with self.assertRaises(RuntimeError): run_cfg({'entry':{'term':['jmp','entry']}},{},fuel=5)
    def test_dsl_wrap(self): self.assertEqual(interpret(('add',('const',MASK),('const',1)),{}),0)
    def test_fold_equivalence(self):
        expr=('mul',('add',('var','x'),('const',0)),('add',('const',2),('const',3)))
        out=fold(expr,{'x'}); rng=random.Random(45)
        for _ in range(256):
            env={'x':rng.randrange(1<<32)}
            self.assertEqual(interpret(expr,env),interpret(out,env))
        self.assertEqual(out,('mul',('var','x'),('const',5)))
    def test_reject_effect(self):
        with self.assertRaises(ValueError): interpret(('open','file'),{})
    def test_reject_unknown(self):
        with self.assertRaises(ValueError): interpret(('var','x'),{})
    def test_reject_depth(self):
        expr=('const',1)
        for _ in range(40): expr=('add',expr,('const',1))
        with self.assertRaises(ValueError): interpret(expr,{})
    def test_reject_huge_integer(self):
        with self.assertRaises(ValueError): interpret(('const',1<<50),{})
    def test_cache_key(self):
        args=dict(tree=('const',1),target='cpu',compiler_version='1',flags='strict')
        a=cache_key(**args); args['flags']='fast'
        self.assertNotEqual(a,cache_key(**args))
    def test_alias_ranges(self):
        self.assertTrue(ranges_overlap(0,16,8,8)); self.assertFalse(ranges_overlap(0,8,8,8))
        self.assertFalse(ranges_overlap(0,0,0,8))
    def test_emission(self):
        out=generate_cpp(('add',('var','x'),('const',1)),{'x'})
        self.assertIn('arg_0',out); self.assertIn('uint32_t',out)
