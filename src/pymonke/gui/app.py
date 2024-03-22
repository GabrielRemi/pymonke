from typing import Optional, Any

import customtkinter as ctk
from pandas import DataFrame, Series

from .data_init.data_init_frame import DataInitFrame
from .dict_frame import DictFrame
from .fitting.fit_frame import FitFrame
from .misc import Root
from .plot.plot_frame import PlotFrame
from ..fit import Fit, FitResult
from ..misc.dataframe import get_error_column_name


class App(Root, ctk.CTk):
    def __init__(self, rel_height: float = 0.6, rel_width: float = 0.8):
        ctk.CTk.__init__(self)

        self.geometry(self.__get_geometry(rel_height, rel_width))
        self.title("PyMonke data fitting")
        self.grid_columnconfigure((0, 1), weight=5)
        self.grid_columnconfigure(2, weight=8)

        # DATA
        self.meta: dict[str, Any] = dict()
        self.data: Optional[DataFrame] = None
        self.fit_result: Optional[dict[str, FitResult]] = None

        self.plot_frame = PlotFrame(master=self)
        self.plot_frame.grid(row=0, column=1)

        self.data_init = DataInitFrame(master=self)
        self.data_init.load_meta_frame.button.configure(command=self.load_meta)
        self.data_init.browse_data_frame.button.configure(command=self.load_data)
        self.data_init.grid(row=0, column=0)

        # self.read_data_arguments_frame = DictFrame(master=self, text="Additional Arguments for data reading")
        # self.read_data_arguments_frame.return_bindings = [self.update_read_data_args]
        #
        # self.read_data_arguments_frame.grid(row=1, column=0)

        self.fit_frame = FitFrame(master=self)
        self.fit_frame.grid(row=0, column=2, sticky="nsew", padx=50, rowspan=2)

        # self.plotting_style_arguments = DictFrame(master=self, text="Plotting Style Arguments")
        # self.plotting_style_arguments.return_bindings = [self.fit_frame.update_plotting_style]
        # self.plotting_style_arguments.grid(row=1, column=1, pady=20)

        # self.formula_frame.after(10000, self.plot_frame.plot_data)

    def __get_geometry(self, rel_height: float, rel_width: float) -> str:
        screen_width = self.winfo_screenwidth() * rel_width
        screen_height = self.winfo_screenheight() * rel_height
        result = f"{int(screen_width)}x{int(screen_height)}"
        return result

    def get_fit_frame(self) -> FitFrame:
        return self.fit_frame

    def get_fit_meta(self) -> Optional[dict[str, Any]]:
        fit = self.get_fit_frame().get_fit_name()
        if fit is None:
            return None
        return self.meta["fits"][fit]

    def load_meta(self):
        if (val := self.data_init.load_meta()) is not None:
            self.meta = val
        self.load_from_meta()
        ic(self.meta)

    def load_data(self):
        self.data = self.data_init.load_data()
        ic(self.data)

    def load_from_meta(self) -> None:
        # self.read_data_arguments_frame.load_parameters(self.meta)
        self.data_init.load_from_meta()
        self.plot_frame.load_from_meta()
        self.fit_frame.load_from_meta()
        # self.load_plotting_style_arguments_from_fit_meta()
        ic(self.data)

    def get_plot_frame(self) -> Any:
        return self.plot_frame

    def get_x(self) -> Optional[Series]:
        if (x := self.meta.get("x")) is not None and self.data is not None:
            return self.data[x]
        return None

    def do_fit(self) -> Fit:
        fit: Fit = Fit(meta_data=self.meta, data=self.data)
        self.fit_result = fit.run()
        return fit

    def get_y(self) -> Optional[Series]:
        if (y := self.meta.get("y")) is not None and self.data is not None:
            return self.data[y]
        return None

    def get_sy(self) -> Optional[Series]:
        if (y := self.meta.get("y")) is not None and self.data is not None:
            return self.data[get_error_column_name(self.data, y)]
        return None

    def get_sx(self) -> Optional[Series]:
        if (x := self.meta.get("x")) is not None and self.data is not None:
            return self.data.get(get_error_column_name(self.data, x))
        return None
