import pandas as pd
import numpy as np
from pymonke.misc.file_management import read_data_into_dataframe
from pymonke.fit import Fit, FitResult
import json
from icecream import ic
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import Figure
data = read_data_into_dataframe("Cu.txt", delimiter="\t")

data.columns = ["channel", "intensity"]
data["intensity error"] = np.sqrt(data["intensity"]) * 10
data.to_csv("Cu.csv", index=False)

meta = json.loads(open("data.json").read())

# fit = Fit(data=data, meta_data=meta)
# out = fit.run()
# ic(out)
# fit.plot()
# plt.show()

x = [1, 2, 3, 4, 5]
fig = Figure()
ax = fig.add_subplot(111)
ax.scatter(x, x)
fig.savefig("test.pdf")
