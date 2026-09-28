import math
import unittest
from simulation import advance


class MotionTests(unittest.TestCase):
    def test_positive_motion(self):
        self.assertEqual(advance(2, 8, 0.25), 4.0)

    def test_zero_time(self):
        self.assertEqual(advance(2, 8, 0), 2.0)

    def test_zero_velocity(self):
        self.assertEqual(advance(-2, 0, 0.25), -2.0)

    def test_negative_velocity(self):
        self.assertEqual(advance(2, -8, 0.25), 0.0)

    def test_five_ticks(self):
        position = 0.0
        for _ in range(5):
            position = advance(position, 6, 0.25)
        self.assertEqual(position, 7.5)

    def test_negative_time_rejected(self):
        with self.assertRaises(ValueError):
            advance(0, 1, -0.1)

    def test_nonfinite_each_argument(self):
        for value in (math.nan, math.inf, -math.inf):
            for index in range(3):
                values = [0.0, 1.0, 0.1]
                values[index] = value
                with self.subTest(value=value, index=index):
                    with self.assertRaises(ValueError):
                        advance(*values)

    def test_type_errors(self):
        for value in (True, "1", None, []):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    advance(0, 1, value)

    def test_result_overflow(self):
        with self.assertRaises(ValueError):
            advance(1e308, 1e308, 1e308)

    def test_unrepresentable_integer(self):
        with self.assertRaises(ValueError):
            advance(10**10000, 1, 1)

    def test_decimal_tolerance(self):
        self.assertAlmostEqual(advance(0.1, 0.2, 0.3), 0.16)


if __name__ == "__main__":
    unittest.main()
