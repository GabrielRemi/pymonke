from customtkinter import *

from typing import Optional

from pymonke.fit.parse import rename_parameters, RepetitionError
from .parameter_frame import ParameterFrame
from pymonke.gui import EntryError


class ParametersScrollableFrame(CTkScrollableFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.param_frames: Optional[dict[str, ParameterFrame]] = None

    def generate_parameter_frames(self, params: list[str]):
        self.delete_parameter_frames()

        for index, param in enumerate(params):
            self.param_frames[param] = ParameterFrame(master=self, name=param)
            self.param_frames[param].grid(row=index, column=0, sticky="ew")

    def delete_parameter_frames(self):
        if self.param_frames is not None:
            for frame in self.param_frames.values():
                frame.destroy()
        self.param_frames = dict()

    def rename_entries(self, formula: str) -> str:
        """Renames the entries if this is possible and outputs the new formula."""
        param_rename = dict()
        for old, frame in zip(self.param_frames.keys(), self.param_frames.values()):
            if old != (new := frame.get_entry()):
                param_rename[old] = new
        try:
            formula = rename_parameters(formula, param_rename)  # could fail
        except (RepetitionError, ValueError) as e:
            for frame in self.param_frames.values():
                frame.reset_entry()
            raise EntryError(e)

        for old in param_rename.keys():
            new = param_rename[old]
            frame = self.param_frames[old]
            frame.set_name(new)
            self.param_frames[new] = self.param_frames.pop(old)
        return formula

    def reset_parameter_entries(self):
        for frame in self.param_frames.values():
            frame.reset_entry()