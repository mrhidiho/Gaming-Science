import json,tempfile,unittest
from pathlib import Path
from capstone.pipeline import simulate
from capstone.audit import audit
from labs.reference.lesson_40_2 import solve
class PipelineTests(unittest.TestCase):
    def test_no_stall_cycle_convention(self):
        r=simulate([1,2,3,4],lanes=1,latency=4)
        self.assertEqual(r['elapsed_cycles'],7)
        self.assertEqual(r['tick_count'],8)
    def test_tail_lanes(self):
        r=simulate([1,2,3,4,5],lanes=4,latency=4)
        self.assertEqual(r['accepted_packets'],2)
        self.assertEqual(r['elapsed_cycles'],5)
    def test_independent_packet_arithmetic_full_signed16_domain(self):
        xs=list(range(-32768,32768))
        for gain in [-32768,-1,0,128,384,32767]:
            result=simulate(xs,lanes=64,gain=gain,bias=-3,ready_pattern=[True,False,True])
            expected=solve(dict(bits=16,frac=8,gain=gain,bias=-3,x=xs))['raw']
            self.assertEqual(result['output'],expected)
    def test_empty(self): self.assertEqual(simulate([])['tick_count'],0)
    def test_backpressure_preserves_order(self):
        xs=list(range(-100,100))
        for lanes in [1,2,4,8]:
            r=simulate(xs,lanes=lanes,ready_pattern=[False,True,False,False,True])
            self.assertEqual(r['output'],solve(dict(bits=16,frac=8,gain=384,bias=64,x=xs))['raw'])
            self.assertGreater(r['stalled_ticks'],0)
    def test_permanent_stall_rejected(self):
        with self.assertRaises(ValueError): simulate([1],ready_pattern=[False])
    def test_timeout(self):
        with self.assertRaises(TimeoutError): simulate([1],latency=4,max_ticks=2)
    def test_bad_lanes(self):
        with self.assertRaises(ValueError): simulate([1],lanes=0)
    def test_corrupt_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'data.txt').write_text('changed')
            record=dict(id='a',claim='x',requirement='r',limitations='l',tier='analytical',artifact='data.txt',sha256='0'*64)
            (root/'ledger.json').write_text(json.dumps([record]))
            self.assertIn('a: checksum mismatch',audit(root/'ledger.json'))
    def test_path_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            record=dict(id='a',claim='x',requirement='r',limitations='l',tier='analytical',artifact='../escape',sha256='0'*64)
            (root/'ledger.json').write_text(json.dumps([record]))
            self.assertIn('a: invalid or absent artifact',audit(root/'ledger.json'))
if __name__=='__main__': unittest.main()
