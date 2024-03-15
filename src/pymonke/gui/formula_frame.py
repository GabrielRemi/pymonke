from customtkinter import *

from tkinter import StringVar
from typing import Optional, Callable

from ..fit.parse import parse_function, replace_funcs, rename_parameters, RepetitionError
from ..fit.fit import func_type


class FormulaFrame(CTkFrame):
    def __init__(self, **args):
        super().__init__(**args)
        self.text = StringVar(master=self, value="", name="FormulaFrameText")
        self.entry = CTkEntry(master=self, placeholder_text="Enter your formula", textvariable=self.text, width=600)
        self.entry.grid(row=0, column=0, sticky="ew", padx=10)

        self.error_label = CTkLabel(master=self, text="")
        self.error_label.configure(text_color="red")
        self.error_label.grid(row=0, column=1, sticky="e", padx=10)
        self.function: Optional[func_type] = None
        self.param_frames: Optional[list[ParameterFrame]] = None

        self.entry.bind(sequence="<Return>", command=self.on_return)

    def on_return(self, event):
        if self.param_frames is not None:
            for frame in self.param_frames:
                frame.destroy()
        self.param_frames = []
        text = self.entry.get()
        try:
            self.text.set(replace_funcs(text))
            self.no_error()

            self.function, params = parse_function(self.entry.get())
            self.param_frames = []
            for index, param in enumerate(params):
                self.param_frames.append(ParameterFrame(master=self, name=param))
                self.param_frames[index].grid(row=index+1, column=0)
        except Exception as e:
            print(e)
            self.set_error()

    def no_error(self):
        self.error_label.configure(text="")

    def set_error(self):
        self.error_label.configure(text="invalid entry")


class ParameterFrame(CTkFrame):
    def __init__(self, name: str, **args):
        super().__init__(**args)
        self.name_str = name
        self.value = CTkLabel(master=self, text="")
        self.name_var = StringVar(master=self, value=name)
        self.name = CTkEntry(master=self, textvariable=self.name_var)
        self.name.grid(row=0, column=0, padx=10)
        self.name.bind("<Return>", command=self.rename)
        self.value.grid(row=0, column=1, padx=10)

    def rename(self, event):
        new_name = self.name_var.get()
        assert isinstance(self.master, FormulaFrame)  # this Frame only works with FormulaFrame
        formula = self.master.text.get()
        new_formula = rename_parameters(formula, {self.name_str: new_name})
        self.master.text.set(new_formula)
        self.name_str = new_name
