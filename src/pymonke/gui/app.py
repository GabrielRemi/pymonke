import customtkinter as ctk
from pandas import DataFrame

from typing import Optional, Any

from .formula.formula_frame import FormulaFrame
from .plot.plot_frame import PlotFrame
from .data_init.data_init_frame import DataInitFrame
from .misc import Root, get_meta, get_data


class App(Root, ctk.CTk):
    def __init__(self, rel_height: float = 0.5, rel_width: float = 0.5):
        # Root.__init__(self)
        ctk.CTk.__init__(self)
        Root.__init__(self)

        self.geometry(self.__get_geometry(rel_height, rel_width))
        self.title("PyMonke data fitting")
        self.grid_columnconfigure((0, 1), weight=5)
        self.grid_columnconfigure(2, weight=8)

        # DATA
        self.meta: dict[str, Any] = dict()
        self.data: Optional[DataFrame] = None

        self.plot_frame = PlotFrame(master=self)
        self.plot_frame.grid(row=0, column=1)

        self.data_init = DataInitFrame(master=self)
        self.data_init.load_meta_frame.button.configure(command=self.load_meta)
        self.data_init.browse_data_frame.button.configure(command=self.load_data)
        self.data_init.grid(row=0, column=0)

        self.formula_frame = FormulaFrame(master=self)
        self.formula_frame.grid(row=0, column=2, sticky="nsew", padx=50)

        self.opt = ctk.CTkOptionMenu(master=self, values=["OLS", "ODR"])
        self.opt.set("OLS")
        self.opt.grid(row=1, column=2)

    def __get_geometry(self, rel_height: float, rel_width: float) -> str:
        screen_width = self.winfo_screenwidth() * rel_width
        screen_height = self.winfo_screenheight() * rel_height
        result = f"{int(screen_width)}x{int(screen_height)}"
        return result

    def load_meta(self):
        self.meta = self.data_init.load_meta()
        ic(self.meta)

    def load_data(self):
        self.data = self.data_init.load_data()
        ic(self.data)

