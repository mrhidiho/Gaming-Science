import unittest
import random
from gradlab.parallel import *

class ParallelTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(tree_sum([]),0); self.assertEqual(exclusive_scan([]),[])
    def test_single(self): self.assertEqual(exclusive_scan([7]),[0])
    def test_nonpower(self): self.assertEqual(exclusive_scan([3,1,7,0,4]),[0,3,4,11,11])
    def test_random_scan(self):
        rng=random.Random(1)
        for n in range(130):
            a=[rng.randrange(-5,6) for _ in range(n)]
            self.assertEqual(exclusive_scan(a),[sum(a[:i]) for i in range(n)])
            self.assertEqual(tree_sum(a),sum(a))
    def test_stable_compaction(self): self.assertEqual(compact('abcde',[1,0,1,0,1]),list('ace'))
    def test_gemm_ragged_edges(self):
        a=[[i+j for j in range(3)] for i in range(5)]
        b=[[i-j for j in range(7)] for i in range(3)]
        ref=[[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(7)] for i in range(5)]
        self.assertEqual(tiled_gemm(a,b,tile=4),ref)
    def test_gemm_invalid(self):
        with self.assertRaises(ValueError): tiled_gemm([[1]],[[1],[2]])
    def test_scheduling_lower_bound(self):
        for dynamic in (False,True):
            r=scheduling_model([100]+[1]*99,8,dynamic=dynamic)
            self.assertGreaterEqual(r['makespan'],r['lower_bound'])
            self.assertEqual(len(r['trace']),100)
    def test_pipeline_lifetime(self):
        result=pipeline_trace(7,2,5)
        trace=result['trace']
        for i,r in enumerate(trace):
            self.assertGreaterEqual(r['compute_start'],r['ready'])
            if i>=2: self.assertGreaterEqual(r['copy_start'],trace[i-2]['end'])
        self.assertEqual(result['total'],37)
    def test_pipeline_empty(self): self.assertEqual(pipeline_trace(0,2,5)['total'],0)
    def test_roofline_units(self):
        r=roofline(1e9,1e9,10e12,100e9)
        self.assertEqual(r['intensity'],1); self.assertAlmostEqual(r['lower_time_s'],.01)
