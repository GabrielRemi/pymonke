from customtkinter import *
from icecream import ic

from tkinter import StringVar
from typing import Optional, Callable, Any

from ..fit.parse import parse_function, replace_funcs, rename_parameters, RepetitionError
from ..fit.fit import func_type
from .__init__ import EntryError


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

        self.parameters = ParametersScrollableFrame(master=self, form_frame=self, width=200)
        self.parameters.grid(row=1, column=0, sticky="ns")

        self.entry.bind(sequence="<Return>", command=self.parameters.update_parameters)

    def update_formula(self):
        """Looks for known functions in the formula string and updates it accordingly. Can fail if invalid Entry"""
        try:
            text = self.entry.get()
            self.text.set(replace_funcs(text))
            self.function, params = parse_function(self.entry.get())
            self.reset_error_label()
        except:
            self.set_error_label("Invalid Entry")
            raise EntryError

    def get_func_and_params(self) -> tuple[func_type, list[str]]:
        """Tries to parse the function string into a python function and returns it togeter with its parameters."""
        try:
            self.function, params = parse_function(self.entry.get())
            self.reset_error_label()
            return self.function, params
        except:
            self.set_error_label("Invalid Entry")
            raise EntryError

    def reset_error_label(self):
        self.error_label.configure(text="")

    def set_error_label(self, text: str):
        self.error_label.configure(text=text)


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


class ParametersScrollableFrame(CTkScrollableFrame):
    def __init__(self, form_frame: FormulaFrame, **kwargs):
        super().__init__(**kwargs)

        self.form_frame = form_frame
        self.param_frames: Optional[dict[str, ParameterFrame]] = None

    def update_parameters(self, event) -> None:
        try:
            self.form_frame.update_formula()
            _, params = self.form_frame.get_func_and_params()
        except EntryError:
            self.form_frame.set_error_label("invalid entry")
            return
        try:
            if self.param_frames is not None:
                for frame in self.param_frames.values():
                    frame.destroy()
            self.param_frames = dict()
            self.param_frames = dict()
            for index, param in enumerate(params):
                self.param_frames[param] = ParameterFrame(formula_frame=self.form_frame, master=self, name=param)
                self.param_frames[param].grid(row=index + 1, column=0)
        except:
            self.form_frame.set_error_label("invalid entry")
