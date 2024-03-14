from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import scipy.odr as odr

import os
from pprint import pprint
os.chdir(r"C:\Users\GaboM\PycharmProjects\Monke2\tests")



def gauss_func(x, *params):
    return params[0] * np.exp(-(params[1] - x) ** 2 / (2 * params[2] ** 2))


# %% Wolfram
raw_data = np.loadtxt("W.txt", skiprows=1)
data = pd.DataFrame(raw_data, columns=["channel", "intensity"])
data.query("channel > 80 and channel < 170", inplace=True)

# %% Molybdän
raw_data = np.loadtxt("Mo.txt", skiprows=1)
data = pd.DataFrame(raw_data, columns=["channel", "intensity"])
data.query("channel > 200 and channel < 280", inplace=True)
p0 = [1000, 230, 3]


def func(x, *params):
    return gauss_func(x, *params)

# %% Kupfer
raw_data = np.loadtxt("Cu.txt", skiprows=1)
data = pd.DataFrame(raw_data, columns=["channel", "intensity"])
data.query("channel > 90 and channel < 130", inplace=True)
p0 = [8000, 108, 3, 1000, 117, 3]


def func(x, *params):
    return gauss_func(x, *params[0:3]) + gauss_func(x, *params[3:6])


# %% fitting with optimize.curve_fit
data["intensity error"] = [np.sqrt(i) * 1.5 if i > 1 else 1 for i in data["intensity"]]

out: tuple = curve_fit(func, xdata=data["channel"], ydata=data["intensity"],
                sigma=data["intensity error"], p0=p0,
                check_finite=True, absolute_sigma=False)
popt, pcov = out
pprint(popt)
pprint(pcov)

#%% fitting with ODR


def odr_func(params, x):
    return func(x, *params)


data["channel error"] = [abs(np.sin(i * np.pi / 180)) * 1.5 if i > 1 else 1 for i in data["intensity"]]

x, y = data["channel"], data["intensity"]
sx, sy = data["channel error"], data["intensity error"]

odr_data = odr.RealData(x=x, y=y, sy=sy, sx=sx)
odr_model = odr.Model(odr_func)
odr_odr = odr.ODR(odr_data, odr_model, p0)
odr_out: odr.Output = odr_odr.run()
popt = odr_out.beta
odr_out.pprint()



#%% plotting
x = np.linspace(min(data["channel"]), max(data["channel"]), 300)
plt.figure()
plt.errorbar(data["channel"], data["intensity"], yerr=data["intensity error"], xerr=data.get("channel error"),
             linestyle="", ms=5, marker="o")
plt.plot(x, func(x, *popt))
plt.show()
