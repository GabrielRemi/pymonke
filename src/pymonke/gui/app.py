import customtkinter as ctk
from customtkinter import CTk
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import filedialog

import os

from .misc import browse_files
from .formula_frame import FormulaFrame


class App(ctk.CTk):
    def __init__(self, fig_num: int = 1, rel_height: float = 0.5, rel_width: float = 0.5):
        super().__init__()
        self.geometry(self.__get_geometry(rel_height, rel_width))
        self.title("PyMonke data fitting")

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
        file_name: str

        def f():
            nonlocal file_name
            file_name = browse_files("select Data file", ".csv, .txt")
            print(file_name)

        self.grid_columnconfigure(1, weight=10)
        self.formula_frame = FormulaFrame(master=self)
        self.formula_frame.grid(row=0, column=1, sticky="nsew")

        self.button = ctk.CTkButton(self, text="browse files", command=f)
        self.button.grid(row=1, column=1)


        self.opt = ctk.CTkOptionMenu(master=self, values=["OLS", "ODR"])
        self.opt.set("OLS")
        self.opt.grid(row=1, column=2)

    def __get_geometry(self, rel_height: float, rel_width: float) -> str:
        screen_width = self.winfo_screenwidth() * rel_width
        screen_height = self.winfo_screenheight() * rel_height
        result = f"{int(screen_width)}x{int(screen_height)}"
        return result



