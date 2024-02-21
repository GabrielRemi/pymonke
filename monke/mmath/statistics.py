import numpy as np
import pandas as pd

from typing import Any

from rounding import *


def varianz_xy(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    return (1/len(x))*((x-x_mean)*(y-y_mean)).sum()


def varianz_x(x):
    x_mean = np.mean(x)
    return (1/len(x))*((x-x_mean)**2).sum()


def mittel_varianzgewichtet(val, val_err):
    return (val/(val_err**2)).sum()/(1/(val_err**2)).sum()
    # --test--
    # sigma = val_err/(val_err.sum())
    # return (sigma*val).sum()


def chisquare(f, x, y, yerr, params: list[float]) -> float:
    """Berechnet das X² pro Freiheitsgrad für eine Funktion f mit parametern <params>
    f: hat die Form f(params, x)
    x: ist ein Array der unabhängigen Variable
    y: ist ein Array der von x abhängigen Variable
    yerr: Fehler von y, kann ein Array oder ein skalarer Wert sein"""

    try:
        iter(x)
        iter(y)
    except TypeError:
        print("x and/ or y not an iterable")
        exit(-1)

    try:
        iter(yerr)
    except:
        yerr = [yerr] * len(x)

    x, y, yerr = np.array(x), np.array(y), np.array(yerr)

    chi_square = np.sum((y - f(params, x))**2 / yerr**2)
    return chi_square / (len(x) - len(params))


