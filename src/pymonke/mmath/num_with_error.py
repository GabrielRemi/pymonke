from json import JSONEncoder
import json
from typing import Tuple
from typing_extensions import Self

from .rounding import roundup_two_significant_digits


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


class NumWithError(dict):
    """inputs two numbers and rounds them appropriately, treating x_error as an uncertainty."""

    def __init__(self, x: float | int, x_error: float | int) -> None:
        if isinstance(x, (float, int)) and isinstance(x_error, (float, int)):
            x, x_error = float(x), float(x_error)
            self.__x, self.__x_error, self.__exponent = _round_values(x, x_error)
        else:
            raise TypeError("x and x_error must be numbers")
        dict.__init__(self, value=self.__x, error=self.__x_error)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def x_error(self) -> float:
        return self.__x_error

    def get_values(self) -> Tuple[float, float]:
        return self.__x, self.__x_error

    def display_table_separate(self, option: str | None = None) -> str:
        r"""Creates a string of the form \tablenum{x +- x_error}"""
        if option is None:
            option = ''
        else:
            option = f"[{option}]"

        format_str = "{:}"
        if self.__exponent < 0:
            precision = str(-self.__exponent + 1)
            if "{:e}".format(self.__x_error)[2] == "0":
                precision = str(-self.__exponent)
            format_str = f"{{:.{precision}f}}"
        return f"\\tablenum{option}{{{format_str.format(self.x)} +- {format_str.format(self.x_error)}}}"

    def display_separate(self, option: str | None = None) -> str:
        r"""Same as display_table_separate but with \num instead of \tablenum."""
        output = self.display_table_separate(option)
        output = output.replace(r"\tablenum", r"\num")
        return output

    def __eq__(self, other: object) -> bool:
        if hasattr(other, "__x") and hasattr(other, "__x_error"):
            if isinstance(other.__x, float) and isinstance(other.__x_error, float):
                return self.__x == other.__x and self.__x_error == other.__x_error
        return False

    def __repr__(self) -> str:
        return f"NumWithError({self.__x}, {self.__x_error})"

    def __str__(self) -> str:
        return f"{self.__x} +- {self.__x_error}"
