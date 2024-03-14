from typing import Callable, Tuple, List, Iterable, TypeVar, TypeAlias, Union, overload
from mypy_extensions import VarArg
from pandas import Series

class Foo:
    pass
    def __add__(self, other):
        return self

class Bar(Foo):
    pass
# num = TypeVar('num', float, int)
num = TypeVar("num", bound=Foo)



def add(x: num, y: num) -> num:
    return x + y


print(add(Bar(), Foo()))

