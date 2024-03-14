from typing import Callable, Tuple, List, Iterable
from mypy_extensions import VarArg
from pandas import Series


def func(x: int, *args: int | float) -> int | float:
    return x + sum(args)


f: Callable[[int, VarArg(int | float)], int | float] = func

