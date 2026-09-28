"""Additional property, integration and failure checks for supplied reference code."""
from pathlib import Path
import contextlib
import copy
import io
import json
import math
import random
import runpy
import sys
import types
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import mathkit as m
import check_lab
import run_benchmark

class ReferenceProperties(unittest.TestCase):
    def test_normalize_preserves_direction_and_length(self):
        for v in [(3,4),(-1,3,7),(1e300,1e-300),(1e-300,2e-300)]:
            u=m.normalize(v)
            self.assertAlmostEqual(m.dot(u,u),1.)
            self.assertEqual(len(u),len(v))
    def test_normalize_does_not_mutate(self):
        v=[3,4];old=v.copy();m.normalize(v);self.assertEqual(v,old)
    def test_dot_symmetry(self):
        rng=random.Random(81)
        for _ in range(40):
            a=[rng.randint(-9,9) for _ in range(3)];b=[rng.randint(-9,9) for _ in range(3)]
            self.assertEqual(m.dot(a,b),m.dot(b,a))
    def test_noncommuting_matrices(self):
        r=((0,-1),(1,0));s=((2,0),(0,1));self.assertNotEqual(m.matmul(r,s),m.matmul(s,r))
    def test_solver_residuals(self):
        for a,b in [(((2,1),(1,-1)),(5,1)),(((0,1),(2,1)),(3,7))]:
            x=m.solve2(a,b)
            for row,rhs in zip(a,b):self.assertAlmostEqual(m.dot(row,x),rhs)
    def test_parent_chain(self):
        world=m.matmul(m.matmul(m.translation(10,0,0),m.rotation_z(math.pi/2)),m.translation(2,0,0))
        check_lab.compare(self,m.transform4(world,(0,0,0,1)),(10.,2.,0.,1.))
    def test_rigid_inverse_roundtrip(self):
        a=m.matmul(m.translation(2,3,4),m.rotation_z(.7))
        inv=m.matmul(m.rotation_z(-.7),m.translation(-2,-3,-4))
        check_lab.compare(self,m.transform4(inv,m.transform4(a,(1,5,9,1))),(1.,5.,9.,1.))
    def test_quaternion_sign(self):
        q=(math.sqrt(.5),0,0,math.sqrt(.5))
        check_lab.compare(self,m.quat_rotate(q,(1,0,0)),(0.,1.,0.))
        check_lab.compare(self,m.quat_rotate(tuple(-x for x in q),(1,0,0)),(0.,1.,0.))
    def test_quaternion_nonunit_normalized(self):
        check_lab.compare(self,m.quat_rotate((0,0,0,2),(1,2,3)),(-1.,-2.,3.))
    def test_quaternion_zero_rejected(self):
        with self.assertRaises(ValueError):m.quat_rotate((0,0,0,0),(1,0,0))
    def test_quaternion_dimensions(self):
        with self.assertRaises(ValueError):m.quat_rotate((1,0,0),(1,0,0))
    def test_topological_empty(self):self.assertEqual(m.topological_order({}),[])
    def test_topological_tie_policy(self):self.assertEqual(m.topological_order({'b':['c'],'a':['c'],'c':[]}),['a','b','c'])
    def test_topological_cycle(self):
        with self.assertRaises(ValueError):m.topological_order({'a':['b'],'b':['a']})
    def test_topological_missing_node(self):
        with self.assertRaises(ValueError):m.topological_order({'a':['b']})
    def test_topological_duplicate(self):
        with self.assertRaises(ValueError):m.topological_order({'a':['b','b'],'b':[]})
    def test_topological_self_loop(self):
        with self.assertRaises(ValueError):m.topological_order({'a':['a']})
    def test_line_residual_sum(self):
        xs=(0,1,2,3,4);ys=(1.1,2.9,5.2,6.8,9.0);a,b=m.fit_line(xs,ys)
        self.assertAlmostEqual(sum(y-a*x-b for x,y in zip(xs,ys)),0.)
    def test_derivative_error_order(self):
        e1=abs(m.centered_difference(lambda x:x**3,2,.1)-12)
        e2=abs(m.centered_difference(lambda x:x**3,2,.01)-12)
        self.assertAlmostEqual(e1/e2,100.,places=5)
    def test_quadrature_refinement(self):
        e1=m.integrate(lambda x:x*x,0,1,4)-1/3
        e2=m.integrate(lambda x:x*x,0,1,8)-1/3
        self.assertAlmostEqual(e1/e2,4.)
    def test_explicit_spring_energy_identity(self):
        x,v=1.,0.
        for _ in range(20):x,v=m.spring_step(x,v,1,100,0,.05,'explicit')
        self.assertAlmostEqual((.5*v*v+50*x*x)/50,1.25**20,places=8)
    def test_stable_linear_semi_case(self):
        x,v=1.,0.
        for _ in range(1000):
            x,v=m.spring_step(x,v,1,100,0,.05,'semi')
            self.assertLess(abs(x),2.)
    def test_unstable_linear_semi_case(self):
        x,v=1.,0.
        for _ in range(12):x,v=m.spring_step(x,v,1,100,0,.25,'semi')
        self.assertGreater(abs(x),1000.)
    def test_probability_zero_weight_never_selected(self):
        for u in [0,.1,.25,.5,.999999]:self.assertNotEqual(m.weighted_index([1,0,3],u),1)
    def test_alias_cosine_identity(self):
        for n in range(100):self.assertAlmostEqual(math.cos(2*math.pi*900*n/1000),math.cos(2*math.pi*100*n/1000),places=10)
    def test_alias_sine_sign(self):
        for n in range(100):self.assertAlmostEqual(math.sin(2*math.pi*900*n/1000),-math.sin(2*math.pi*100*n/1000),places=10)
    def test_convolution_commutative(self):
        self.assertEqual(m.convolve([1,2,-1],[2,3]),m.convolve([2,3],[1,2,-1]))
    def test_convolution_linearity(self):
        x=[1,2,3];z=[2,-1,0];h=[1,2]
        left=m.convolve([2*a+3*b for a,b in zip(x,z)],h)
        right=[2*a+3*b for a,b in zip(m.convolve(x,h),m.convolve(z,h))]
        self.assertEqual(left,right)
    def test_convolution_mass(self):
        self.assertAlmostEqual(sum(m.convolve([1,2,3],[.25,.5,.25])),6.)
    def test_quadratic_error_history(self):
        result=m.descent_quadratic(0,.25,8,1e-15)
        for n,x in enumerate(result['history']):self.assertAlmostEqual(x,3-3*(.5**n))
    def test_descent_nonfinite_is_not_success(self):
        with self.assertRaises(ArithmeticError):m.descent_quadratic(1e308,2,10,1e-8)
    def test_benchmark_implementations_agree(self):
        for values,queries in [([],[]),([1,4,7],[1,0,7]),([1,1,2],[1,1,2,3])]:
            expected=sum(any(q==v for v in values) for q in queries)
            self.assertEqual(run_benchmark.scan(values,queries),expected)
            self.assertEqual(run_benchmark.build_set(values,queries),expected)
    def test_prefix_does_not_mutate(self):
        values=[1,0,-1,3];saved=copy.deepcopy(values);m.count_positive_prefix(values,4);self.assertEqual(values,saved)

class MutationDetection(unittest.TestCase):
    def check_bad(self,lesson,**changed):
        api=json.loads((ROOT/'source/lab_api.json').read_text())[lesson]
        exports={name:getattr(m,name) for name in api['functions']};exports.update(changed)
        suite=check_lab.make_suite([lesson],True,{lesson:types.SimpleNamespace(**exports)})
        result=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
        self.assertFalse(result.wasSuccessful(),'checker failed to detect known incorrect implementation')
    def test_wrong_distance_operation_detected(self):self.check_bad('06.1',travel_time=lambda d,s:d*s)
    def test_converse_like_logic_detected(self):self.check_bad('06.2',implies=lambda p,q:p==q)
    def test_zero_direction_fallback_detected(self):self.check_bad('07.1',normalize=lambda v:tuple(0 for _ in v))
    def test_wrong_update_order_detected(self):self.check_bad('08.4',spring_step=lambda x,v,mass,stiffness,damping,dt,method:m.spring_step(x,v,mass,stiffness,damping,dt,'explicit'))
    def test_swapped_conditional_detected(self):self.check_bad('09.1',posterior_bug=lambda prior,sensitivity,false_positive:sensitivity)
    def test_wrong_boundary_detected(self):self.check_bad('09.2',weighted_index=lambda weights,u:0)
    def test_truncated_convolution_detected(self):self.check_bad('10.3',convolve=lambda signal,kernel:m.convolve(signal,kernel)[:len(signal)])
    def test_false_convergence_detected(self):self.check_bad('10.4',descent_quadratic=lambda *args:dict(x=3.,converged=True,iterations=0,reason='gradient_tolerance'))

class ExampleChecks(unittest.TestCase):pass
for lesson,expected in json.loads((ROOT/'examples/EXPECTED_OUTPUT.json').read_text()).items():
    def test(self,lesson=lesson,expected=expected):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):runpy.run_path(str(ROOT/'examples'/('lesson_'+lesson.replace('.','_')+'.py')),run_name='__main__')
        self.assertEqual(out.getvalue(),expected)
    setattr(ExampleChecks,'test_example_'+lesson.replace('.','_'),test)
