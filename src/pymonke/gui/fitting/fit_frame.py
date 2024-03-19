from customtkinter import *

from ..formula.formula_frame import FormulaFrame
from .fit_option_menu import FitComboBox
from ..misc import get_meta


class FitFrame(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.formula_frame = FormulaFrame(master=self, width=6000)
        self.formula_frame.grid(row=0, column=0, sticky="nsew")
        self.formula_frame.entry.bind("<Return>", self.update_to_meta)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.fit_combo_box = FitComboBox(master=self)
        self.fit_combo_box.configure(command=self._fit_combo_on_selection)
        self.fit_combo_box.bind("<Return>", self.update_from_fit_meta)
        self.fit_combo_box.grid(row=1, column=0)

        self.fit_type_option = CTkOptionMenu(master=self, values=["OLS", "ODR"], command=self.update_to_meta)
        self.fit_type_option.set("OLS")
        self.fit_type_option.grid(row=1, column=1)

    def get_fit_type(self):
        if self.fit_type_option.get() == "OLS":
            return "optimize.curve_fit"
        if self.fit_type_option.get() == "ODR":
            return "odr"

    def set_fit_type(self, _type: str):
        if _type == "optimize.curve_fit":
            self.fit_type_option.set("OLS")
        elif _type == "odr":
            self.fit_type_option.set("ODR")

    def update_to_meta(self, _=None):
        """update meta from all child objects"""
        if (fits := get_meta(self).get("fits")) is None or self.fit_combo_box.get() == "Add Fit":
            return
        fit = fits[self.fit_combo_box.selected]
        fit["fit_type"] = self.get_fit_type()
        fit["function"] = self.formula_frame.text.get()
        ic(get_meta(self))

    def update_from_fit_meta(self, _=None):
        """if Values exist in meta[fit_name]. load them in."""
        if (fits := get_meta(self).get("fits")) is None or self.fit_combo_box.get() == "Add Fit":
            return
        fit = fits[self.fit_combo_box.selected]
        if (func := fit.get("function")) is not None:
            self.formula_frame.text.set(func)
        else:
            self.formula_frame.text.set("")
        if (fit_type := fit.get("fit_type")) is not None:
            self.set_fit_type(fit_type)
        else:
            self.set_fit_type("OLS")

    def _fit_combo_on_selection(self, _=None):
        self.fit_combo_box.selected = self.fit_combo_box.get()
        self.update_from_to_meta()

    def _fit_combo_add_or_rename(self, _=None):
        self.fit_combo_box.add_or_rename()
        self.update_from_fit_meta()

    def update_from_to_meta(self, _=None) -> None:
        self.update_from_fit_meta()
        self.update_to_meta()

    def load_from_meta(self, _=None) -> None:
        meta = get_meta(self)
        if (fits := meta.get("fits")) is not None:
            if len(fits) >= 1:
                self.fit_combo_box.configure(values=[*(keys := fits.keys()), "Add Fit"])
                self.fit_combo_box.set(keys[0])
                self.update_from_fit_meta()

