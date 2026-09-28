"""Additional checks for the independent analytical sensitivity extension."""
import unittest
from capstone.sensitivity import estimate
class SensitivityTests(unittest.TestCase):
    def setUp(self):
        self.case=dict(n=100,lanes=4,adverse=False,assumed_clock_Hz=100_000_000,elapsed_cycles=28)
    def test_declared_traffic_and_overhead(self):
        r=estimate(self.case,20,100e6,400e6)
        self.assertAlmostEqual(r['kernel_us'],1.0)
        self.assertAlmostEqual(r['transfer_us'],4.0)
        self.assertAlmostEqual(r['end_to_end_us'],30.0)
    def test_higher_internal_bandwidth_cannot_remove_host_transfer(self):
        r=estimate(self.case,20,100e6,1600e6)
        self.assertAlmostEqual(r['kernel_us'],.28)
        self.assertAlmostEqual(r['end_to_end_us'],29.28)
    def test_empty_skipped_operation(self):
        c=dict(self.case,n=0,elapsed_cycles=0)
        self.assertEqual(estimate(c,20,100e6,400e6)['end_to_end_us'],0)
    def test_reject_nonfinite_or_zero_rates(self):
        for values in [(20,0,1),(20,1,float('inf')),(-1,1,1),(True,1,1)]:
            with self.assertRaises(ValueError): estimate(self.case,*values)
