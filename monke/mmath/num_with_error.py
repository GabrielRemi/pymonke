import numpy as np

from typing import Tuple, Any, List
from rounding import roundup_two_significant_digits


def _round_values(x: float, x_error: float) -> Tuple[float, float, float]:
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

    return x, x_error, int(exponent)


class NumWithError:
    """inputs two numbers and rounds them appropriately, treating __x_error as an uncertainty."""
    def __init__(self, x: float | int,  x_error: float | int) -> None:
        if isinstance(x, (float, int)) and isinstance(x_error, (float, int)):
            x, x_error = float(x), float(x_error)
            self.__x, self.__x_error, self.__exponent = _round_values(x, x_error)
        else:
            raise TypeError("x and x_error must be numbers")

    @property
    def x(self):
        return self.__x

    @property
    def x_error(self):
        return self.__x_error

    def get_values(self) -> Tuple[float, float]:
        return self.__x, self.__x_error

    def display_table_separate(self, option: str = None) -> str:
        """outputs a string with the number and uncertainty separated by '+-' in a <num> block.
        This functionality is meant to be used for work with tabular in latex with the siunitx package.
        Can add an optional string, which will be added the following way: \tablenum[option]{number1 +- number2}."""
        if option is None:
            option = ''
        else:
            option = f"[{option}]"

        precision = ''
        format_str = "{:}"
        if self.__exponent < 0:
            precision = str(-self.__exponent + 1)
            format_str = f"{{:.{precision}f}}"
        return f"\\tablenum{option}{{{format_str.format(self.x)} +- {format_str.format(self.x_error)}}}"

    def display_separate(self, option: str = None) -> str:
        """Same as display_table_separate but with \num instead of \tablenum."""
        output = self.display_table_separate(option)
        output = output.replace(r"\tablenum", r"\num")
        return output

    def __eq__(self, other):
        return self.__x == other.__x and self.__x_error == other.__x_error

    def __repr__(self):
        return f"NumWithError({self.__x}, {self.__x_error})"
