from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from .plot_canvas import PlotCanvas
from .limits_frame import LimitsFrame


class PlotFrame(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.canvas = PlotCanvas(master=self)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.limits_frame = LimitsFrame(master=self)
        self.limits_frame.min_entry.bind("<Return>", self.min_callback)
        self.limits_frame.max_entry.bind("<Return>", self.max_callback)
        self.limits_frame.grid(row=1, column=0, columnspan=2)

    def min_callback(self, _):
        self.limits_frame.min_callback(_)
        val = self.limits_frame.min.get()
        self.canvas.set_limits(float(val), None)

    def max_callback(self, _):
        self.limits_frame.max_callback(_)
        val = self.limits_frame.max.get()
        self.canvas.set_limits(None, float(val))
