from monke import constants, functions
from monke.functions import ErrorStyle


def test_constants():
    pass


def test_functions():
    errstyle = functions.ErrorStyle.PLUSMINUS
    assert(isinstance(errstyle, functions.ErrorStyle))
    assert(errstyle == functions.ErrorStyle.PLUSMINUS)
    assert(errstyle != functions.ErrorStyle.PARENTHESIS)
    assert(functions.error_round(1.23, 1.13) == ("1.2", "1.2"))
    assert (functions.error_round(1.23, 1.13, error_mode=ErrorStyle.PARENTHESIS) == "1.2(12)")


if __name__ == '__main__':
    test_constants()
    test_functions()