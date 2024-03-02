import unittest

from src.pymonke.mmath.rounding import roundup_two_significant_digits


class MyTestCase(unittest.TestCase):
    def test_roundup_two_significant_digits(self):
        def f(x):
            return roundup_two_significant_digits(x)

        self.assertEqual(f(0.123), 0.13)  # add assertion here
        self.assertEqual(f(0.1), 0.1)
        self.assertEqual(f(0.100123), 0.11)
        self.assertEqual(f(1234.2345), 1300)
        self.assertEqual(f(2234.2345), 3000)
        self.assertEqual(f(0.9), 0.9)
        self.assertEqual(f(0.8789789), 0.9)
        self.assertEqual(f(0.90234), 1.)


if __name__ == '__main__':
    unittest.main()
