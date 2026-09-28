import unittest
import random
import math
from gradlab.rendering import *

class RenderingTests(unittest.TestCase):
    def test_mis_weight(self):
        self.assertEqual(balance(2,6),.25); self.assertEqual(balance(0,0),0)
        self.assertAlmostEqual(balance(2,6,3,1),.5)
    def test_measure(self): self.assertEqual(area_to_solid_angle(.25,4,.5),2)
    def test_integral(self): self.assertLess(abs(integrate_mis(20000)-1/3),.004)
    def test_reservoir_frequency(self):
        counts=[0,0,0]; rng=random.Random(5)
        for _ in range(20000):
            r=Reservoir()
            for i,w in enumerate([1,2,7]): r.update(i,w,rng)
            counts[r.selected]+=1
        for got,w in zip(counts,[.1,.2,.7]): self.assertLess(abs(got/20000-w),.015)
    def test_reservoir_zero(self):
        r=Reservoir(); r.update('x',0,random.Random(1))
        self.assertIsNone(r.selected); self.assertEqual(r.count,1)
    def test_reservoir_negative(self):
        with self.assertRaises(ValueError): Reservoir().update('x',-1,random.Random())
    def test_history_reset(self):
        self.assertEqual(temporal_filter([0,0],[10,10],[False,True],.2),[0,8])
    def test_inverse_albedo(self):
        c=[.2,.5,1]; obs=[.7*x/math.pi for x in c]
        self.assertAlmostEqual(inverse_albedo(c,obs)['albedo'],.7)
    def test_unidentifiable(self):
        with self.assertRaises(ValueError): inverse_albedo([0,0],[0,0])
    def test_bvh_matches_bruteforce(self):
        rng=random.Random(43)
        s=[Sphere((rng.uniform(-3,3),rng.uniform(-3,3),rng.uniform(-3,3)),.4) for _ in range(20)]
        b=BVH.build(s)
        for _ in range(300):
            o=(0.,0.,8.); d=unit((rng.uniform(-1,1),rng.uniform(-1,1),-1.))
            got=b.hit(s,o,d)
            raw=[(hit[0],i) for i,v in enumerate(s) if (hit:=v.intersect(o,d))]
            ref=min(raw) if raw else None
            self.assertEqual(got is None,ref is None)
            if ref: self.assertAlmostEqual(got[0],ref[0]); self.assertEqual(got[3],ref[1])
    def test_refit(self):
        s=[Sphere((float(i),0.,0.),.3) for i in range(5)]
        tree=BVH.build(s); s[0]=Sphere((0.,0.,4.),.3); tree.refit(s)
        hit=tree.hit(s,(0.,0.,8.),(0.,0.,-1.))
        self.assertEqual(hit[3],0); self.assertAlmostEqual(hit[0],3.7)
    def test_axis_parallel_box(self):
        box=BVH((-1.,-1.,-1.),(1.,1.,1.))
        self.assertTrue(box.box_hit((0.,0.,4.),(0.,0.,-1.),10))
        self.assertFalse(box.box_hit((2.,0.,4.),(0.,0.,-1.),10))
    def test_renderer_deterministic(self):
        a=render(6,4,2); b=render(6,4,2)
        self.assertEqual(a,b); self.assertTrue(all(math.isfinite(v) and v>=0 for v in a['pixels']))
    def test_emitter_after_last_scattering_vertex(self):
        class ScriptedTree:
            def __init__(self): self.calls=0
            def hit(self,scene,origin,direction):
                self.calls+=1
                if self.calls==1: return (1.,(0.,0.,0.),(0.,1.,0.),0)
                if self.calls==2: return (2.,(0.,2.,0.),(0.,-1.,0.),1)
                raise AssertionError('path exceeded support')
        scene=[Sphere((0.,-1.,0.),1.,.5),Sphere((0.,3.,0.),1.,0.,2.)]
        tree=ScriptedTree()
        value=path_radiance(scene,tree,(0.,1.,0.),(0.,-1.,0.),random.Random(1),mode='bsdf',max_depth=1)
        self.assertEqual(value,1.)
        self.assertEqual(tree.calls,2)
    def test_no_extra_scatter_past_depth_budget(self):
        class ScriptedTree:
            def __init__(self): self.calls=0
            def hit(self,scene,origin,direction):
                self.calls+=1
                if self.calls>2: raise AssertionError('extra scattering vertex')
                return (1.,(0.,0.,0.),(0.,1.,0.),0)
        tree=ScriptedTree(); scene=[Sphere((0.,-1.,0.),1.,.5)]
        value=path_radiance(scene,tree,(0.,1.,0.),(0.,-1.,0.),random.Random(1),mode='bsdf',max_depth=1)
        self.assertEqual(value,0.)
        self.assertEqual(tree.calls,2)
