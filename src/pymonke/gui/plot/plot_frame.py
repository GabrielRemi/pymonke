from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from typing import Optional

from .plot_canvas import PlotCanvas
from .limits_frame import LimitsFrame
from ..misc import get_meta, get_root


class PlotFrame(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.canvas = PlotCanvas(master=self)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.limits_frame = LimitsFrame(master=self, label="Plotting limits")
        self.limits_frame.min_entry.bind("<Return>", self.min_callback)
        self.limits_frame.max_entry.bind("<Return>", self.max_callback)
        self.limits_frame.grid(row=1, column=0, columnspan=2)

        self.button = CTkButton(self, text="Fit Data", command=self.plot_data)
        self.button.grid(row=2, column=0, columnspan=2)

    def min_callback(self, _):
        self.limits_frame.min_callback(_)
        val = self.limits_frame.min.get()
        self.canvas.set_limits(float(val), None)
        self.load_limits_to_meta()

    def max_callback(self, _):
        self.limits_frame.max_callback(_)
        val = self.limits_frame.max.get()
        self.canvas.set_limits(None, float(val))
        self.load_limits_to_meta()

    def plot_data(self) -> None:
        self.canvas.plot_data()
        _min, _max = self.canvas.ax.get_xlim()
        self.limits_frame.set_bounds(_min, _max)

        ic()
        # show parameter values after the fit
        fit_name = get_root(self).get_fit_frame().get_fit_name()
        if fit_name is not None:
            fit_result = get_root(self).fit_result
            if fit_result is not None:
                result = get_root(self).fit_result.get(fit_name)
                if result is not None:
                    get_root(self).get_fit_frame().set_param_values(result.as_dict())
                ic(result)

    def load_from_meta(self) -> None:
        self.plot_data()
        meta = get_meta(self)
        _min, _max = meta.get("x_min_limit"), meta.get("x_max_limit")
        ic(_min, _max)
        if _min is not None:
            self.limits_frame.set_min(_min)
        if _max is not None:
            self.limits_frame.set_max(_max)
        self.canvas.set_limits(_min, _max)

    def load_limits_to_meta(self, _=None):
        _min = float(self.limits_frame.min.get())
        _max = float(self.limits_frame.max.get())
        get_meta(self)["x_min_limit"] = _min
        get_meta(self)["x_max_limit"] = _max
        ic(get_meta(self))
