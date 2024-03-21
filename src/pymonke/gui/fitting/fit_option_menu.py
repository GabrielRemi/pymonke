from customtkinter import *

from ..misc import get_root, get_meta


class FitComboBox(CTkComboBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, values=["Add Fit"], command=self.on_selection)
        self.bind("<Return>", self.add_or_rename)
        self.selected: str = "Add Fit"

    def add_or_rename(self, _):
        if (fits := get_meta(self).get("fits")) is None:
            get_meta(self)["fits"] = fits = dict()

        fit_name = self.get()
        old: list = self.cget("values")
        if fit_name in old:
            return
        if self.selected == "Add Fit":  # Add
            if fit_name == "Add Fit":
                return
            old.insert(-2, fit_name)
            self.configure(values=old)
            self.set(fit_name)
            fits[fit_name] = dict()
            formula_frame = get_root(self).get_fit_frame().formula_frame
            formula_frame.update_formula("")
            formula_frame.update_parameters(None, "")
        else:  # Rename
            for i, name in enumerate(old):
                if name == self.selected:
                    old[i] = fit_name
            self.configure(values=old)
            fits[fit_name] = fits.pop(self.selected)
        self.selected = fit_name
        ic(get_meta(self))

    def on_selection(self, event=None):
        self.selected = self.get()
