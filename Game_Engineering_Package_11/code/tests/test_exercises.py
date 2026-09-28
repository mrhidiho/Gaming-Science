import importlib,math,os,unittest
from itertools import combinations
api=importlib.import_module(os.environ.get('V10_IMPLEMENTATION','reference')+'.exercises')


class ExerciseContracts(unittest.TestCase):
    def test_cache_worked(self):
        self.assertEqual(api.cache_hits([0,64,0,128,0,64],2,1),[False,False,True,False,False,True])
    def test_cache_two_way(self):
        self.assertEqual(api.cache_hits([0,64,0,128,0,64],2,2),[False,False,True,False,True,True])
    def test_cache_lru_promotion(self):
        self.assertEqual(api.cache_hits([0,64,0,128,0,64],1,2),[False,False,True,False,True,False])
    def test_cache_same_line(self):
        self.assertEqual(api.cache_hits([0,1,63,64],1,1),[False,True,True,False])
    def test_cache_empty(self):
        self.assertEqual(api.cache_hits([],1,1),[])
    def test_cache_bad_geometry(self):
        for s,w,b in [(0,1,64),(3,1,64),(1,0,64),(1,1,3),(True,1,64)]:
            with self.subTest(s=s,w=w,b=b),self.assertRaises(ValueError):api.cache_hits([],s,w,b)
    def test_cache_bad_address(self):
        for a in [-1,1.2,True]:
            with self.subTest(a=a),self.assertRaises(ValueError):api.cache_hits([a],1,1)
    def test_frontier_example(self):
        self.assertEqual(api.pareto_front([(10,40,20),(8,50,24),(12,45,22),(9,35,25)]),[0,1,3])
    def test_frontier_duplicates(self):
        self.assertEqual(api.pareto_front([(1,2),(1,2),(2,3)]),[0,1])
    def test_frontier_tradeoff(self):
        self.assertEqual(api.pareto_front([(1,3),(2,2),(3,1)]),[0,1,2])
    def test_frontier_empty(self):self.assertEqual(api.pareto_front([]),[])
    def test_frontier_invalid(self):
        for rows in [[()],[(1,),(2,3)],[(math.nan,1)],[(math.inf,2)]]:
            with self.subTest(rows=rows),self.assertRaises(ValueError):api.pareto_front(rows)
    def test_setup_worked(self):self.assertAlmostEqual(api.setup_slack(2,.1,.12,1.5,.15,.08),.25)
    def test_setup_tightened(self):self.assertAlmostEqual(api.setup_slack(1.6,.1,.12,1.5,.15,.08),-.15)
    def test_hold_worked(self):self.assertAlmostEqual(api.hold_slack(.1,.05,.08,.06,.03),-.06)
    def test_skew_sign(self):
        self.assertGreater(api.setup_slack(2,.2,.1,1,.1,.1),api.setup_slack(2,0,.1,1,.1,.1))
        self.assertLess(api.hold_slack(.2,.1,.1,.1,0),api.hold_slack(0,.1,.1,.1,0))
    def test_timing_bad_input(self):
        with self.assertRaises(ValueError):api.setup_slack(2,0,-1,1,.1,0)
        with self.assertRaises(ValueError):api.hold_slack(math.nan,.1,.1,.1,0)
    def test_ecc_worked(self):self.assertEqual(api.ecc_encode(10),0xD2)
    def test_ecc_clean(self):
        for p in range(16):
            with self.subTest(p=p):self.assertEqual(api.ecc_decode(api.ecc_encode(p))['payload'],p)
    def test_ecc_all_single(self):
        for p in range(16):
            for bit in range(8):
                with self.subTest(p=p,bit=bit):
                    result=api.ecc_decode(api.ecc_encode(p)^(1<<bit))
                    self.assertEqual(result['payload'],p)
                    self.assertEqual(result['corrected_word'],api.ecc_encode(p))
    def test_ecc_all_double(self):
        for p in range(16):
            for a,b in combinations(range(8),2):
                with self.subTest(p=p,a=a,b=b):
                    result=api.ecc_decode(api.ecc_encode(p)^(1<<a)^(1<<b))
                    self.assertEqual(result['status'],'detected_double');self.assertIsNone(result['payload'])
    def test_ecc_triple_limit(self):self.assertNotEqual(api.ecc_decode(api.ecc_encode(0)^7)['payload'],0)
    def test_ecc_bad_input(self):
        for p in [-1,16,True,1.5]:
            with self.subTest(p=p),self.assertRaises(ValueError):api.ecc_encode(p)
        for w in [-1,256,True]:
            with self.subTest(w=w),self.assertRaises(ValueError):api.ecc_decode(w)
    def test_ratio_identical(self):self.assertAlmostEqual(api.paired_gmean([1,2],[1,2]),1)
    def test_ratio_constant(self):self.assertAlmostEqual(api.paired_gmean([10,20],[8,16]),1.25)
    def test_ratio_reciprocal(self):self.assertAlmostEqual(api.paired_gmean([2,1],[1,2]),1)
    def test_ratio_bad(self):
        for b,c in [([],[]),([1],[]),([0],[1]),([1],[math.nan]),([1],[-1])]:
            with self.subTest(b=b,c=c),self.assertRaises(ValueError):api.paired_gmean(b,c)
    def test_descriptor_boundary(self):self.assertTrue(api.descriptor_valid(4080,16,7,0))
    def test_descriptor_overrun(self):self.assertFalse(api.descriptor_valid(4080,32,7,0))
    def test_descriptor_authorization(self):
        self.assertFalse(api.descriptor_valid(0,16,8,0));self.assertFalse(api.descriptor_valid(0,16,7,1))
    def test_descriptor_invalid(self):
        for args in [(-16,16,7,0),(0,0,7,0),(1,16,7,0),(0,17,7,0),(True,16,7,0),(0,'16',7,0)]:
            with self.subTest(args=args):self.assertFalse(api.descriptor_valid(*args))
    def test_descriptor_large(self):self.assertFalse(api.descriptor_valid(2**64-16,32,7,0))
