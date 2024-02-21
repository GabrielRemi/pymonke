import unittest

from monke.mmath.rounding import roundup_two_significant_digits


class MyTestCase(unittest.TestCase):
    def test_roundup_two_significant_digits(self):
        def f(x):
            return roundup_two_significant_digits(x)

        self.assertEqual(f(0.123), 0.13)  # add assertion here
        self.assertEqual(f(0.1), 0.1)
        self.assertEqual(f(0.100123), 0.11)
        self.assertEqual(f(1234.2345), 1300)
        self.assertEqual(f(2234.2345), 3000)


if __name__ == '__main__':
    unittest.main()
