"""Cooker/BVH integration and failure-path tests; standard library only."""
import hashlib,importlib.util,json,math,pathlib,shutil,struct,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'code/python'))
import cook_assets as c
import bvh_reference as b
class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.home=pathlib.Path(self.temp.name)
        self.src=self.home/'src';shutil.copytree(ROOT/'assets/source',self.src)
    def tearDown(self):self.temp.cleanup()
    def test_mesh_format(self):
        _,obj=c.read_source(self.src/'scene_mesh.json');blob=c.mesh_payload(obj)
        self.assertEqual(blob[:4],b'GEM1');self.assertEqual(struct.unpack('<I',blob[4:8])[0],12);self.assertEqual(len(blob),8+12*32)
    def test_deterministic_fresh_build(self):
        a=c.cook(self.src,self.home/'a');z=c.cook(self.src,self.home/'z');self.assertEqual(a,z)
        for p in (self.home/'a').iterdir():self.assertEqual(p.read_bytes(),(self.home/'z'/p.name).read_bytes())
    def test_payload_hashes(self):
        m=c.cook(self.src,self.home/'out')
        for a in m['assets'].values():self.assertEqual(c.digest((self.home/'out'/a['path']).read_bytes()),a['payload_sha256'])
    def test_image_format_mips(self):
        _,obj=c.read_source(self.src/'checker_image.json');blob,levels=c.image_payload(obj)
        self.assertEqual(blob[:4],b'GET1');self.assertEqual(levels,[{'width':8,'height':8},{'width':4,'height':4},{'width':2,'height':2},{'width':1,'height':1}])
        self.assertEqual(len(blob),16+4*8+85*12)
        self.assertAlmostEqual(struct.unpack('<3f',blob[-12:])[0],.5)
    def test_odd_area_filter(self):
        pixels=[(float(i),)*3 for i in range(15)];out,w,h=c.downsample(pixels,3,5)
        self.assertEqual((w,h),(1,2));self.assertAlmostEqual(sum(v[0] for v in out)/2,7)
    def test_dependency_invalidation(self):
        a=c.cook(self.src,self.home/'a');obj=json.loads((self.src/'checker_image.json').read_text());obj['pixels'][0]=40
        (self.src/'checker_image.json').write_text(json.dumps(obj));z=c.cook(self.src,self.home/'z')
        self.assertNotEqual(a['assets']['checker']['key'],z['assets']['checker']['key']);self.assertNotEqual(a['assets']['scene']['key'],z['assets']['scene']['key'])
    def test_bad_source_preserves_manifest(self):
        out=self.home/'out';c.cook(self.src,out);before=(out/'assets_manifest.json').read_bytes()
        (self.src/'scene_mesh.json').write_text('{"version":1,"vertices":[[0]]}')
        with self.assertRaises(ValueError):c.cook(self.src,out)
        self.assertEqual((out/'assets_manifest.json').read_bytes(),before)
    def test_mesh_nan_rejected(self):
        with self.assertRaises(ValueError):c.mesh_payload({'vertices':[[math.nan]*8]*3})
    def test_mesh_bad_color(self):
        with self.assertRaises(ValueError):c.mesh_payload({'vertices':[[0,0,0,0,0,2,0,0]]*3})
    def test_pixel_count(self):
        with self.assertRaises(ValueError):c.image_payload({'width':2,'height':2,'pixels':[]})
    def test_unknown_filter(self):
        with self.assertRaises(ValueError):c.cook(self.src,self.home/'out','unknown')
    def test_constant_json(self):
        (self.src/'bad.json').write_text('{"version":1,"x":NaN}')
        with self.assertRaises(ValueError):c.read_source(self.src/'bad.json')
    def test_sphere_nonunit_ray(self):self.assertEqual(b.sphere_hit((0,0,-3),(0,0,2),b.Sphere((0,0,0),1,0)),1)
    def test_sphere_inside(self):self.assertEqual(b.sphere_hit((0,0,0),(1,0,0),b.Sphere((0,0,0),1,0)),1)
    def test_sphere_behind(self):self.assertIsNone(b.sphere_hit((0,0,-3),(0,0,-1),b.Sphere((0,0,0),1,0)))
    def test_box_parallel_miss(self):self.assertIsNone(b.box_interval((2,0,0),(0,1,0),(-1,-1,-1),(1,1,1)))
    def test_bvh_matches(self):self.assertTrue(b.experiment(32,100)['same_hits'])
    def test_identical_centroids(self):
        spheres=[b.Sphere((0,0,2),1,i) for i in range(20)];root=b.build(spheres)
        self.assertEqual(b.trace((0,0,0),(0,0,1),spheres,root,{'boxes':0,'primitives':0}),(1,0))
    def test_bvh_empty_rejected(self):
        with self.assertRaises(ValueError):b.build([])
    def test_zero_ray_rejected(self):
        with self.assertRaises(ValueError):b.trace((0,0,0),(0,0,0),[],None,{'boxes':0,'primitives':0})
if __name__=='__main__':unittest.main(verbosity=2)
