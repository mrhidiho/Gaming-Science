import unittest
import math
from gradlab.numerical import *

class NumericalTests(unittest.TestCase):
    def test_csr_product(self):
        self.assertEqual(CSR.from_dense([[2,0],[1,3]]).matvec([4,5]), [8,19])
    def test_csr_bad_column(self):
        with self.assertRaises(ValueError): CSR(1,(0,1),(2,),(1.,))
    def test_csr_duplicate(self):
        with self.assertRaises(ValueError): CSR(1,(0,2),(0,0),(1.,2.))
    def test_cg_known_solution(self):
        a = CSR.from_dense([[4,1],[1,3]])
        result = pcg(a,[6,7])
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['x'][0],1)
        self.assertAlmostEqual(result['x'][1],2)
    def test_cg_zero_rhs(self):
        r=pcg(CSR.from_dense([[1]]),[0])
        self.assertEqual(r['iterations'],0); self.assertTrue(r['converged'])
    def test_cg_nonconvergence_report(self):
        r=pcg(CSR.from_dense([[4,1],[1,3]]),[6,7],maxiter=0)
        self.assertFalse(r['converged'])
    def test_cg_breakdown(self):
        with self.assertRaises(ArithmeticError): pcg(CSR.from_dense([[-1]]),[1])
    def test_preconditioner_scaling(self):
        a=CSR.from_dense([[1,0,0],[0,.001,0],[0,0,.000001]])
        result=pcg(a,[1,.002,.000003],jacobi=True)
        self.assertTrue(result['converged']); self.assertEqual(result['iterations'],1)
        self.assertLess(norm([x-y for x,y in zip(result['x'],[1,2,3])]),1e-10)
    def test_dense_oracle(self):
        x=solve_dense([[0,2],[1,3]],[4,7]); self.assertEqual(x,[1,2])
    def test_gradient(self):
        g=finite_gradient(lambda x:x[0]**2+3*x[1]**2,[2,-1])
        self.assertAlmostEqual(g[0],4,places=7); self.assertAlmostEqual(g[1],-6,places=7)
    def test_constrained_projection(self):
        x=constrained_fit([0,0]); self.assertEqual(x,[.5,.5])
    def test_bootstrap_fixed_ratio(self):
        r=paired_bootstrap([2,4,6],[1,2,3],samples=500)
        self.assertAlmostEqual(r['speedup'],2); self.assertAlmostEqual(r['lower'],2)
    def test_bootstrap_invalid(self):
        with self.assertRaises(ValueError): paired_bootstrap([1,0],[1,1])
