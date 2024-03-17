from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from .plot_canvas import PlotCanvas
from .slider import Slider


class PlotFrame(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.canvas = PlotCanvas(master=self)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.min_slider = Slider(master=self, _min=199)
        self.min_slider.grid(row=1, column=0)

        self.max_slider = Slider(master=self)
        self.max_slider.grid(row=1, column=1)

