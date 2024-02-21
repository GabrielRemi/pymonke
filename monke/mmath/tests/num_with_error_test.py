import unittest

from monke.mmath import NumWithError


class MyTestCase(unittest.TestCase):
    def test_num_with_error_eq(self):
        self.assertEqual(NumWithError(2.234, 0.123), NumWithError(2.23, 1.3))  # add assertion here
        self.assertEqual(NumWithError(2.234, 0.14234), NumWithError(2.23, 0.15))
        self.assertEqual(NumWithError(2, 0.14234), NumWithError(2.00, 0.15))
        self.assertEqual(NumWithError(2, 0.16234), NumWithError(2.00, 0.17))
        self.assertEqual(NumWithError(2.234123, 0.16234), NumWithError(2.23, 0.17))
        self.assertEqual(NumWithError(2.234123, 0.19934), NumWithError(2.2, 0.2))
        self.assertEqual(NumWithError(0.9, 0.99), NumWithError(1, 1))
        self.assertEqual(NumWithError(10.8567, 0.99), NumWithError(11, 1))
        self.assertEqual(NumWithError(114.123, 10.89123), NumWithError(114, 11))
        self.assertEqual(NumWithError(0.8234, 10.914123), NumWithError(1, 11))
        self.assertEqual(NumWithError(0.08234, 10.914123), NumWithError(0, 11))
        self.assertEqual(NumWithError(0.8234, 103.814123), NumWithError(0, 110))
        self.assertEqual(NumWithError(0.8234, 110.0002), NumWithError(0, 120))
        self.assertEqual(NumWithError(1423.12341287, 103.814123), NumWithError(1420, 110))

    def test_num_with_error_values(self):
        self.assertEqual(NumWithError(2.234, 0.14234).get_values(), (2.23, 0.15))
        self.assertEqual(NumWithError(2, 0.14234).get_values(), (2.00, 0.15))
        self.assertEqual(NumWithError(2, 0.16234).get_values(), (2.00, 0.17))
        self.assertEqual(NumWithError(2.234123, 0.16234).get_values(), (2.23, 0.17))
        self.assertEqual(NumWithError(2.234123, 0.19934).get_values(), (2.2, 0.2))
        self.assertEqual(NumWithError(0.9, 0.99).get_values(), (1, 1))
        self.assertEqual(NumWithError(10.8567, 0.99).get_values(), (11, 1))
        self.assertEqual(NumWithError(114.123, 10.89123).get_values(), (114, 11))
        self.assertEqual(NumWithError(0.8234, 10.914123).get_values(), (1, 11))
        self.assertEqual(NumWithError(0.08234, 10.914123).get_values(), (0, 11))
        self.assertEqual(NumWithError(0.8234, 103.814123).get_values(), (0, 110))
        self.assertEqual(NumWithError(0.8234, 110.0002).get_values(), (0, 120))
        self.assertEqual(NumWithError(1423.12341287, 103.814123).get_values(), (1420, 110))

    def test_num_with_error_arrays(self):
        self.assertEqual(
            NumWithError([2.234, 2, 2], [0.14234, 0.14234, 0.16234]).get_values(),
            ([2.23, 2.00, 2.00], [0.15, 0.15, 0.17]))


if __name__ == '__main__':
    unittest.main()
