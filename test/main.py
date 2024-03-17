import pandas as pd
import numpy as np

from pymonke.misc.file_management import read_data_into_dataframe

data = read_data_into_dataframe("Cu.txt", delimiter="\t")

data.columns = ["channel", "intensity"]
data["intensity error"] = np.sqrt(data["intensity"]) * 10
data.to_csv("Cu.csv", index=False)