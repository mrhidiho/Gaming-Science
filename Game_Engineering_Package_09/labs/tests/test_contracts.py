"""Independent declared expected values, plus structural invariants."""
import importlib, unittest
from labs.run import load_cases, check_case
class Contracts(unittest.TestCase): pass

def build_test(identity,case):
    def test(self):
        module=importlib.import_module('labs.reference.lesson_'+identity.replace('.','_'))
        ok,message=check_case(module,case)
        self.assertTrue(ok,message)
    return test
for identity,cases in load_cases().items():
    for index,case in enumerate(cases):
        setattr(Contracts,'test_'+identity.replace('.','_')+'_'+str(index).zfill(2),build_test(identity,case))

class Invariants(unittest.TestCase):
    def test_banks_broadcast(self):
        from labs.reference.lesson_37_2 import bank_conflict
        self.assertEqual(bank_conflict([0]*32),1)
    def test_banks_column(self):
        from labs.reference.lesson_37_2 import bank_conflict
        self.assertEqual(bank_conflict([i*32 for i in range(32)]),32)
    def test_banks_padded(self):
        from labs.reference.lesson_37_2 import bank_conflict
        self.assertEqual(bank_conflict([i*33 for i in range(32)]),1)
    def test_fixedpoint_exhaustive_identity(self):
        from labs.reference.lesson_40_2 import solve
        values=list(range(-128,128))
        self.assertEqual(solve(dict(bits=8,frac=4,gain=16,bias=0,x=values))['raw'],values)
    def test_fixedpoint_odd_symmetry(self):
        from labs.reference.lesson_40_2 import round_even_div
        for x in range(-2048,2049):
            self.assertEqual(round_even_div(x,256),-round_even_div(-x,256))
    def test_reference_count(self): self.assertEqual(len(load_cases()),20)
if __name__=='__main__': unittest.main()
