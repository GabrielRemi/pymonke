import numpy as np
from typing import Any, List

from error_style import ErrorStyle


def roundup(x, r=2):
    """rounds up a number to the decimal place r"""
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
    """rounds the given number up to 2 significant digits"""
    scientific: List[str] = "{:e}".format(x).split("e")
    value, exponent = float(scientific[0]), int(scientific[1])
    if value < 2:
        value = roundup(value, 1)
    else:
        value = roundup(value, 0)

    return float(f"{value}e{exponent}")


def error_round(x, xerr, error_mode: ErrorStyle = ErrorStyle.PLUSMINUS, get_float=False) -> Any:
    """rounds xerr to at most 2 significant numbers and rounds __x to the same position. Outputs the
    numbers as strings. The return type is determined by error_mode."""

    if isinstance(x, (int, float)):
        x = [x]
    if isinstance(xerr, (int, float)):
        xerr = [xerr]

    if len(x) != len(xerr):
        print('error_round: beide arrays benötigen dieselbe Länge')
        return

    xerr_sci = [0]*len(x)
    new_xerr = [0]*len(x)
    xerr_str = ['']*len(x)         # gerundete werte als string
    new_x = [0]*len(x)
    x_str = ['']*len(x)

    for i, j in enumerate(xerr):
        xerr_sci[i] = np.format_float_scientific(j)
        this = xerr_sci[i]
        K = ''               # gibt Rundungsstellen an
        last = len(this) - 1  # letzer index
        K = this[last-2:]
        K = -int(K)
        if this[0] == '1':
            K += 1

        new_xerr[i] = roundup(xerr[i], K)
        xerr_str[i] = np.format_float_positional(new_xerr[i])
        if new_xerr[i] == int(new_xerr[i]):
            # transformier ganzzahlige floats in ints
            new_xerr[i] = int(new_xerr[i])
            xerr_str[i] = str(new_xerr[i])

        # definiere neues K bei gerundeten Fehlern
        xerr_sci[i] = np.format_float_scientific(new_xerr[i])
        this = xerr_sci[i]
        K = ''               # gibt Rundungsstellen an
        last = len(this) - 1  # letzer index
        K = this[last-2:]
        K = -int(K)
        if this[0] == '1' and (this[2] != 'e'):
            K += 1

        # Runde Messwerte
        new_x[i] = round(x[i], K)
        if K >= 0:
            numformat = '{:.'+str(K)+'f}'
            x_str[i] = numformat.format(new_x[i])
        else:
            x_str[i] = str(int(new_x[i]))

        # entfernt bei -0.0 das minuszeichen
        if x_str[i][0] == '-' and new_x[i] == 0:
            new_x[i] = -new_x[i]
            x_str[i] = x_str[i][1:]

    if error_mode == ErrorStyle.PLUSMINUS:
        if get_float == False:
            if len(x) != 1:
                return x_str, xerr_str
            else:
                return x_str[0], xerr_str[0]
        else:
            if len(x) != 1:
                return [float(i) for i in x_str], [float(i) for i in xerr_str]
            else:
                return float(x_str[0]), float(xerr_str[0])
    elif error_mode == ErrorStyle.PARENTHESIS:
        result = []
        for j, i in enumerate(xerr_str):

            error = i.replace('.', '')
            while error[0] == '0':
                error = error[1:]
            result.append(f'{x_str[j]}({error})')
        if len(x) != 1:
            return result
        else:
            return result[0]

    elif error_mode == ErrorStyle.SCIENTIFIC:
        res = []
        e_list = []   # Liste aller Potenzen
        for i, j in enumerate(x_str):
            value = float(x_str[i])
            error = xerr_str[i]
            val_str = x_str[i]  # wert als string

            e = 0                       # die Potenz
            result = None              # Der Endwert, der ausgegeben wird

            first = 0                                   # erste Stelle, die eine Zahl ist
            minus = ''   # fügt ein minus hinzu, falls negativ
            if value < 0:
                first = 1
                minus = '-'

            if value != 0:
                # macht aus dem Wert eine Zahl der Form #1.01234#
                while val_str[first] == '0' or val_str[first] == '.':
                    first += 1
            else:
                pass
            # print(val_str, len(val_str), first)
            result = f'{minus}{val_str[first]}.'

            for number in val_str[first+1:]:
                if number != '.':
                    result += number
            if result[-1] == '.':
                result = result[:-1]
            # print(result)

            # bestimmt die Potenz
            if abs(value) < 10 and value != 0:
                while abs(value) < 1:
                    e -= 1
                    value = value * 1e1
                    # error = error * 1e1
            elif abs(value) >= 10:
                while abs(value) >= 10:
                    e += 1
                    value = value * 1e-1

            e_list.append(e)

            # mache aus dem Fehler einen integer
            error = error.replace('.', '')
            while error[0] == '0':
                error = error[1:]

            if e != 0:
                res.append(f'{result}({error})e{e}')
            else:
                res.append(f'{result}({error})')
        if len(x) != 1:
            return res, e_list
        else:
            return res[0], e_list[0]


def round_align(list):
    n = 0    # die Anzahl der Arrays
    num = 0  # Anzahl der Elemente pro Array
    try:
        num = np.shape(list)[1]
        n = np.shape(list)[0]
    except:
        n = 1
        num = np.shape(list)[0]
        list = [list]

    list_sci = [0]*n
    for i in range(n):
        dummy = [0]*num
        last = 100                  # Anzahl der wenigsten nachkommastellen im Array
        for j in range(num):
            dummy[j] = np.format_float_positional(list[i][j])
            this = dummy[j]
            k = len(this)
            decimals = 0

            while this[k-1] != '.':
                decimals += 1
                k -= 1

            if last > decimals:
                last = decimals
        numformat = '{:.'+str(last)+'f}'

        for j in range(num):
            dummy[j] = numformat.format(list[i][j])
        list_sci[i] = dummy

    if n == 1:
        return list_sci[0]
    else:
        return list_sci
