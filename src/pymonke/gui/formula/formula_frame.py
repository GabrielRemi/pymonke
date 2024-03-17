from customtkinter import *

from tkinter import StringVar
from typing import Optional

from pymonke.fit.parse import parse_function, replace_funcs
from pymonke.fit.fit import func_type
from pymonke.gui import EntryError
from ..misc import get_meta
from .parameters_scrollable_frame import ParametersScrollableFrame


class FormulaFrame(CTkFrame):
    def __init__(self, **args):
        super().__init__(**args)
        self.text = StringVar(master=self, value="", name="FormulaFrameText")
        self.function: Optional[func_type] = None

        self.configure(height=5000, width=1000)
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_rowconfigure(1, weight=20)
        self.grid_columnconfigure(0, weight=1)

        self.entry = CTkEntry(master=self, placeholder_text="Enter your formula", textvariable=self.text,
                              width=self.master["width"])
        self.entry.grid(row=0, column=0, sticky="ew", padx=10)

        self.error_label = CTkLabel(master=self, text="")
        self.error_label.configure(text_color="red")
        self.error_label.grid(row=2, column=0, sticky="we", padx=10)

        self.parameters = ParametersScrollableFrame(master=self, width=200)
        self.parameters.grid(row=1, column=0, sticky="ns")

        self.entry.bind(sequence="<Return>", command=self.update_parameters)
        # self.entry.bind(sequence="<Leave>", command=self.update_parameters)

    def update_formula(self):
        """Looks for known functions in the formula string and updates it accordingly. Can fail if invalid Entry"""
        try:
            text = self.entry.get()
            self.text.set(replace_funcs(text))
            self.function, params = parse_function(self.entry.get())
        except:
            raise EntryError

    def get_func_and_params(self) -> tuple[func_type, list[str]]:
        """Tries to parse the function string into a python function and returns it together with its parameters."""
        try:
            self.function, params = parse_function(self.entry.get())
            self.reset_error_label()
            return self.function, params
        except:
            raise EntryError

    def update_parameters(self, _):
        try:
            self.update_formula()
            _, params = self.get_func_and_params()
            self.parameters.generate_parameter_frames(params)
            self.reset_error_label()
        except EntryError:
            self.set_error_label("Invalid Entry")

    def rename(self):
        formula: str = self.text.get()
        try:
            new = self.parameters.rename_entries(formula)
            self.text.set(new)
            self.reset_error_label()
        except EntryError as e:
            self.set_error_label(str(e))
        except Exception as e:
            print(e, file=sys.stderr)
            exit(-1)

    def reset_error_label(self):
        self.error_label.configure(text="")

    def set_error_label(self, text: str):
        self.error_label.configure(text=text)
