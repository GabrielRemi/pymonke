import nltk
import numpy as np

from typing import Callable, List, Tuple, TypeAlias, Iterable
from mypy_extensions import VarArg

num: TypeAlias = float | int
val: TypeAlias = float | int | Iterable[float | int]


def __gauss(x: num | Iterable, *params) -> num | np.ndarray:
    a = params[0]
    x0 = params[1]
    sigma = params[2]
    return a * np.exp((-(x - x0)**2) / (2 * sigma**2))


__ALPH_OPERATORS = {
    'arccos': 'np.arccos',
    'arccosh': 'np.arccosh',
    'arcsin': 'np.arcsin',
    'arcsinh': 'np.arcsinh',
    'arctan': 'np.arctan',
    'arctanh': 'np.arctanh',
    'cos': 'np.cos',
    'cosh': 'np.cosh',
    'e': 'np.e',
    'exp': 'np.exp',
    'log': 'np.log',
    'pi': 'np.pi',
    'sin': 'np.sin',
    'sinh': 'np.sinh',
    'tan': 'np.tan',
    'tanh': 'np.tanh',
}

__SYMBOL_OPERATORS = {
    '*': '*',
    '+': '+',
    '-': '-',
    '/': '/',
    '^': '**',
}

__FUNCS = {
    "gauss": (__gauss, 3),
}


def parse_function(_formula: str) -> Tuple[Callable[[val, VarArg(float | int)], val], List[str]]:
    """Creates a python function out of a string that represents a mathematical formula.
    x is the variable and all the other arguments are passed as positional arguments to the
    generated callable with the form f(x: float, *params) -> float.
    Returns the callable and a list of all the arguments mentioned in _formula"""
    tokens = nltk.tokenize.wordpunct_tokenize(_formula)
    params: List[str] = []
    for index, token in enumerate(tokens):
        if token in __ALPH_OPERATORS:
            tokens[index] = __ALPH_OPERATORS[token]
        elif token.isalnum() and not token.isnumeric() and token not in params and token != "x":
            params.append(token)

    def function(x: val, *_params: num) -> val:
        if isinstance(x, Iterable):
            return np.array([function(i, *_params) for i in x])
        else:
            try:
                float(x)
            except TypeError:
                raise TypeError(r"Argument x must be a number or an iterable.")
        nonlocal tokens, params
        _tokens = tokens.copy()
        for i, tok in enumerate(_tokens):
            if tok in params:
                param_index = params.index(tok)
                _tokens[i] = str(_params[param_index])
            if tok == "x":
                _tokens[i] = str(x)
        string = " ".join(_tokens)
        for op in __SYMBOL_OPERATORS.keys():
            string = string.replace(op, __SYMBOL_OPERATORS[op])
        return eval(string)

    return function, params
