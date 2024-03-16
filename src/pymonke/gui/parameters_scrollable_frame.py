from customtkinter import *

from typing import Optional

from .formula_frame import FormulaFrame
from .parameter_frame import ParameterFrame
from .__init__ import EntryError


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
