import customtkinter as ctk


from .formula.formula_frame import FormulaFrame
from .plot.plot_frame import PlotFrame
from .browse_frame import BrowseFrame

class App(ctk.CTk):
    def __init__(self, fig_num: int = 1, rel_height: float = 0.5, rel_width: float = 0.5):
        super().__init__()
        self.geometry(self.__get_geometry(rel_height, rel_width))
        self.title("PyMonke data fitting")
        self.grid_columnconfigure((0, 1), weight=5)
        self.grid_columnconfigure(2, weight=8)

        self.browse_data_frame = BrowseFrame(file_type=".*", master=self)
        self.browse_data_frame.grid(row=0, column=0)

        self.plot_frame = PlotFrame(master=self)
        self.plot_frame.grid(row=0, column=1)

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



