import numpy as np

from typing import Tuple, Any, List
from rounding import roundup_two_significant_digits


def _round_values(x: float, x_error: float) -> Tuple[float, float]:
    """rounds up to 2 significant digits. functions only takes float values as arguments"""
    if not (isinstance(x, float) and isinstance(x_error, float)):
        raise ValueError("both x and x_error must be floating point numbers")
    if x_error <= 0:
        raise ValueError("x_error must be a number bigger than zero")

    x_error = roundup_two_significant_digits(x_error)
    value, exponent = "{:e}".format(x_error).split("e")

    rounding_decimal = - int(exponent)
    if value[2] != "0":
        rounding_decimal += 1

    x = round(x, rounding_decimal)

    return x, x_error


class NumWithError:
    """inputs two numbers and rounds them appropriately, treating __x_error as an uncertainty.
    __x and __x_error could also be array_like objects."""

    def __init__(self, x, x_error):
        if isinstance(x, (float, int)):
            x, x_error = float(x), float(x_error)
            self.__x, self.__x_error = _round_values(x, x_error)
        else:
            x = [float(i) for i in list(x)]
            x_error = [float(i) for i in list(x_error)]
            if len(x) != len(x_error):
                raise ValueError("Length of x and x_error have to be the same")

            self.__x, self.__x_error = [], []
            for num, error in zip(x, x_error):
                num, error = _round_values(num, error)
                self.__x.append(num)
                self.__x_error.append(error)

    @property
    def x(self):
        return self.__x

    @property
    def x_error(self):
        return self.__x_error

    def get_values(self) -> Tuple[float, float] | Tuple[List[float], List[float]]:
        return self.__x, self.__x_error

    def __eq__(self, other):
        return self.__x == other.__x and self.__x_error == other.__x_error

    def __repr__(self):
        return f"NumWithError({self.__x}, {self.__x_error})"
