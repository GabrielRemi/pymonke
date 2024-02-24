import unittest

from monke.mmath import NumWithError


class MyTestCase(unittest.TestCase):
    def test_num_with_error_eq(self):
        self.assertEqual(NumWithError(2.234, 0.123), NumWithError(2.23, 0.13))
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
        self.assertEqual(NumWithError(-2.3, 0.223), NumWithError(-2.3, 0.3))

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

    def test_num_with_error_display_separate(self):
        self.assertEqual(NumWithError(2.234, 0.14234).display_separate(), r"\num{2.23 +- 0.15}")
        self.assertEqual(NumWithError(2, 0.14234).display_separate(), r"\num{2.00 +- 0.15}")
        self.assertEqual(NumWithError(2, 0.16234).display_separate(), r"\num{2.00 +- 0.17}")
        self.assertEqual(NumWithError(2.234123, 0.16234).display_separate(), r"\num{2.23 +- 0.17}")
        self.assertEqual(NumWithError(2.234123, 0.19934).display_separate(), r"\num{2.2 +- 0.2}")
        self.assertEqual(NumWithError(0.9, 0.99).display_separate(), r"\num{1.0 +- 1.0}")
        self.assertEqual(NumWithError(10.8567, 0.99).display_separate(), r"\num{11.0 +- 1.0}")
        self.assertEqual(NumWithError(114.123, 10.89123).display_separate(), r"\num{114.0 +- 11.0}")
        self.assertEqual(NumWithError(0.8234, 10.914123).display_separate(), r"\num{1.0 +- 11.0}")
        self.assertEqual(NumWithError(0.08234, 10.914123).display_separate(), r"\num{0.0 +- 11.0}")
        self.assertEqual(NumWithError(0.8234, 103.814123).display_separate(), r"\num{0.0 +- 110.0}")
        self.assertEqual(NumWithError(0.8234, 110.0002).display_separate(), r"\num{0.0 +- 120.0}")
        self.assertEqual(NumWithError(1423.12341287, 103.814123).display_separate(), r"\num{1420.0 +- 110.0}")
        self.assertEqual(NumWithError(0.000_000_000_712_312, 0.000_000_000_051_512_123).display_separate(),
                         r"\num{0.00000000071 +- 0.00000000006}")

        self.assertEqual(NumWithError(2.23e1, 14e1).display_separate("round-precision=1"),
                         r"\num[round-precision=1]{20.0 +- 140.0}")
        self.assertEqual(NumWithError(2.234, 0.14234).display_table_separate(), r"\tablenum{2.23 +- 0.15}")

    def test_num_with_error_raise(self):
        with self.assertRaises(TypeError):
            NumWithError(23, "not a number")
        with self.assertRaises(TypeError):
            NumWithError("not a number", 23)
        with self.assertRaises(TypeError):
            NumWithError([2.234, 2, "asd"], [0.14234, 0, 123])
        with self.assertRaises(TypeError):
            NumWithError([2, 3, 4], [0.14234, 0])
        with self.assertRaises(ValueError):
            NumWithError(2, 0)
        with self.assertRaises(ValueError):
            NumWithError(2, -0.123)
        with self.assertRaises(ValueError):
            NumWithError(-1.23, 0)
        with self.assertRaises(TypeError):
            NumWithError([2, 3], [-0.14234, 0, 0.123])


if __name__ == '__main__':
    unittest.main()
