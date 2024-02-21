import unittest
from monke.prelude import *
from monke.mmath import error_round, ErrorStyle


class TestErrorRound(unittest.TestCase):
    def test_plusminus(self):
        from monke.mmath import error_round
        monke.math.error_style = ErrorStyle.PLUSMINUS
        self.assertEqual(error_round(2.234, 0.14234), ("2.23", "0.15"))  # add assertion here
        self.assertEqual(error_round(2, 0.14234), ("2.00", "0.15"))
        self.assertEqual(error_round(2, 0.16234), ("2.00", "0.17"))
        self.assertEqual(error_round(2.234123, 0.16234), ("2.23", "0.17"))
        self.assertEqual(error_round(2.234123, 0.19934), ("2.2", "0.2"))
        self.assertEqual(error_round(0.9, 0.99), ("1", "1"))
        self.assertEqual(error_round(10.8567, 0.99), ("11", "1"))
        self.assertEqual(error_round(114.123, 10.89123), ("114", "11"))
        self.assertEqual(error_round(0.8234, 10.914123), ("1", "11"))
        self.assertEqual(error_round(0.08234, 10.914123), ("0", "11"))
        self.assertEqual(error_round(0.8234, 103.814123), ("0", "110"))
        self.assertEqual(error_round(0.8234, 110.0002), ("0", "120"))
        self.assertEqual(error_round(1423.12341287, 103.814123), ("1420", "110"))

    def test_parentheses(self):
        from monke.mmath.statistics import error_round
        monke.math.functions.error_style = ErrorStyle.PARENTHESIS

        self.assertEqual(error_round(2.234, 0.14234), "2.23(15)")  # add assertion here
        # self.assertEqual(error_round(2, 0.14234), ("2.00", "0.15"))
        # self.assertEqual(error_round(2, 0.16234), ("2.00", "0.17"))
        # self.assertEqual(error_round(2.234123, 0.16234), ("2.23", "0.17"))
        # self.assertEqual(error_round(2.234123, 0.19934), ("2.2", "0.2"))
        # self.assertEqual(error_round(0.9, 0.99), ("1", "1"))
        # self.assertEqual(error_round(10.8567, 0.99), ("11", "1"))
        # self.assertEqual(error_round(114.123, 10.89123), ("114", "11"))
        # self.assertEqual(error_round(0.8234, 10.914123), ("1", "11"))
        # self.assertEqual(error_round(0.08234, 10.914123), ("0", "11"))
        # self.assertEqual(error_round(0.8234, 103.814123), ("0", "110"))
        # self.assertEqual(error_round(0.8234, 110.0002), ("0", "120"))
        # self.assertEqual(error_round(1423.12341287, 103.814123), ("1420", "110"))


if __name__ == '__main__':
    unittest.main()
