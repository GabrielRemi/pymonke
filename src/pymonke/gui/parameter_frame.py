from customtkinter import *

from typing import Any

from .formula_frame import FormulaFrame
from ..fit.parse import rename_parameters


class ParameterFrame(CTkFrame):
    def __init__(self, formula_frame: FormulaFrame, name: str, **args):
        super().__init__(**args)
        self.formula_frame = formula_frame
        self.name_str = name
        self.value = CTkLabel(master=self, text="", width=120)
        self.name_var = StringVar(master=self, value=name)
        self.name = CTkEntry(master=self, textvariable=self.name_var, width=50)
        self.name.grid(row=0, column=0, padx=10)
        self.name.bind("<Return>", command=self.rename)
        self.value.grid(row=0, column=1, sticky="w")

    def rename(self, event):
        new_name = self.name_var.get()
        old_name = self.name_str
        formula = self.formula_frame.text.get()
        try:
            new_formula = rename_parameters(formula, {old_name: new_name})
            self.formula_frame.text.set(new_formula)
            self.formula_frame.parameters.param_frames[new_name] = self.formula_frame.parameters.param_frames.pop(
                old_name)
            self.name_str = new_name
            self.formula_frame.reset_error_label()
        except Exception as e:
            self.name_var.set(old_name)
            self.formula_frame.set_error_label(str(e))

    def set_value(self, value: Any):
        self.value.configure(text=str(value))