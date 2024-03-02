import numpy as np
from typing import List


def roundup(x: float | int, r=2) -> float:
    """Rounds up a number to the decimal place r"""
    a = x*10**r
    a = np.ceil(a)
    a = a*10**(-r)

    if type(x) == float or type(x) == int or type(x) == np.float64:
        if a == 0:
            a = 10**(-r)
    else:
        try:                                           # rundet mehrdimensionale arrays
            for i, j in enumerate(a):
                for k, l in enumerate(j):
                    if i == 0:
                        i = 10**(-r)
        except:                                        # rundet eindimensionale arrays
            for i, j in enumerate(a):
                if i == 0:
                    i = 10**(-r)

    return np.around(a, r)


def roundup_two_significant_digits(x: float) -> float:
    """Rounds the given number up to 2 significant digits"""
    scientific: List[str] = "{:e}".format(x).split("e")
    value, exponent = float(scientific[0]), int(scientific[1])
    if value < 2:
        value = roundup(value, 1)
    else:
        value = roundup(value, 0)

    return float(f"{value}e{exponent}")
