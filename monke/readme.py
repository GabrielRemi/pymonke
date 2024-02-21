from monke.mmath import ErrorStyle, error_round
import monke.mmath as math

def func(a: int = 1, l: list = []):

    print(error_round(0.000234245234, 0.123e-6, ErrorStyle.PLUSMINUS, True))


func()
