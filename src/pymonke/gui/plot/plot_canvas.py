from customtkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from typing import Optional

from ..misc import get_data, get_meta, get_root


class PlotCanvas(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0)

    def set_limits(self, _min: Optional[float], _max: Optional[float]) -> None:
        x1, x2 = self.ax.get_xlim()
        if _min is not None:
            x1 = _min
        if _max is not None:
            x2 = _max

        self.ax.set_xlim((x1, x2))
        self.canvas.draw()

    def plot_data(self) -> None:
        fit = get_root(self).do_fit()
        self.ax.clear()
        fit.plot_ax(self.ax)
        self.canvas.draw()

