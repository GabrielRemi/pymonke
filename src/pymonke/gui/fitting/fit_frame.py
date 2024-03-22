from customtkinter import *

from typing import Any

from ..formula.formula_frame import FormulaFrame
from ..formula.parameter_frame import ParameterFrame
from .fit_option_menu import FitComboBox
from ..list_frame import ListFrame
from ..misc import get_meta, get_root
from ..plot.limits_frame import LimitsFrame
from ..dict_frame import DictFrame


class FitFrame(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.formula_frame = FormulaFrame(master=self, width=6000)
        self.formula_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.formula_frame.entry.bind("<Return>", self.update_to_meta)
        self.formula_frame.entry_bindings = [self.update_parameter_entries_from_formula_frame]
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.fit_combo_box = FitComboBox(master=self)
        self.fit_combo_box.configure(command=self._fit_combo_on_selection)
        self.fit_combo_box.bind("<Return>", self.update_from_fit_meta)
        self.fit_combo_box.grid(row=1, column=0)

        self.fit_type_option = CTkOptionMenu(master=self, values=["OLS", "ODR"], command=self.update_to_meta)
        self.fit_type_option.set("OLS")
        self.fit_type_option.grid(row=1, column=1)

        self.start_parameter_frame = ListFrame(text="Start Parameters", has_add_button=False, master=self)
        self.start_parameter_frame.entry_bindings = [self.update_start_parameters]
        self.start_parameter_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.limits_frame = LimitsFrame(master=self, label="Fitting Limits")
        self.limits_frame.entry_bindings = [self.load_limits_to_meta]
        self.limits_frame.grid(row=3, column=0, columnspan=2)

        self.plotting_style_arguments = DictFrame(master=self, text="Plotting Style Arguments")
        self.plotting_style_arguments.return_bindings = [self.update_plotting_style]
        self.plotting_style_arguments.grid(row=4, column=0, pady=20, columnspan=2)

    def update_parameter_entries_from_formula_frame(self):
        params = self.formula_frame.parameters.get_params()
        if params is None:
            self.start_parameter_frame.delete_all()
        else:
            # search for already set parameters in meta
            if (fit := self.get_fit_name()) is None:
                self.start_parameter_frame.set_parameters([0] * len(params))
            else:
                meta_params = get_meta(self)["fits"][fit].get("start_parameters")
                if meta_params is None or len(meta_params) != len(params):
                    self.start_parameter_frame.set_parameters([0] * len(params))
                else:
                    self.start_parameter_frame.set_parameters(meta_params)
        ic(get_meta(self))

    def set_param_values(self, values: dict[str, Any]):
        self.formula_frame.parameters.set_param_values(values)

    def set_params_values_from_results(self):
        fit_name = get_root(self).get_fit_frame().get_fit_name()
        if fit_name is not None:
            fit_result = get_root(self).fit_result
            if fit_result is not None:
                result = fit_result.get(fit_name)
                if result is not None:
                    get_root(self).get_fit_frame().set_param_values(result.as_dict())

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
        if (fits := get_meta(self).get("fits")) is None or self.fit_combo_box.selected == "Add Fit":
            return
        fit = fits[self.fit_combo_box.selected]
        fit["fit_type"] = self.get_fit_type()
        fit["function"] = self.formula_frame.text.get()
        ic()
        ic(get_meta(self))

    def get_fit_name(self) -> str | None:
        if (val := self.fit_combo_box.selected) == "Add Fit":
            return None
        else:
            return val

    def get_start_parameters(self) -> list[float]:
        p0 = []
        for param in self.start_parameter_frame.get_list():
            if param == "":
                p0.append(0)
            else:
                p0.append(float(param))

        return p0

    def update_start_parameters(self, _=None):
        p0 = self.get_start_parameters()
        if (val := self.get_fit_name()) is None:
            return
        get_meta(self)["fits"][val]["start_parameters"] = p0
        ic(get_meta(self))

    # -----PLOTTING-STYLE-----------------------------------------------------------
    def get_plotting_style_arguments(self) -> dict:
        return self.plotting_style_arguments.get_args()
    #

    def load_plotting_style_arguments_from_fit_meta(self):
        if (fit_name := self.get_fit_name()) is None:
            return
        fit_meta = get_meta(self)["fits"][fit_name]
        if (plotting_style := fit_meta.get("plotting_style")) is not None:
            self.plotting_style_arguments.load_parameters(plotting_style)

    def update_plotting_style(self):
        ic.enable()
        if (val := self.get_fit_name()) is None:
            return
        ic(val)
        args = self.get_plotting_style_arguments()
        if get_meta(self)["fits"][val].get("plotting_style") is None:
            get_meta(self)["fits"][val]["plotting_style"] = args
        else:
            get_meta(self)["fits"][val]["plotting_style"].update(args)
        ic(get_meta(self))
        ic.disable()

    # -----PLOTTING-STYLE-----------------------------------------------------------

    def load_limits_to_meta(self):
        if (val := self.get_fit_name()) is None:
            return
        d = get_meta(self)["fits"][val]
        d["x_min_limit"] = float(self.limits_frame.min.get())
        d["x_max_limit"] = float(self.limits_frame.max.get())
        ic(get_meta(self))

    def load_limits_from_fit_meta(self):
        if (val := self.get_fit_name()) is None:
            return
        d = get_meta(self)["fits"][val]
        if (val := d.get("x_min_limit")) is not None:
            self.limits_frame.min.set(val)
        if (val := d.get("x_max_limit")) is not None:
            self.limits_frame.max.set(val)
        self.set_params_values_from_results()

    def update_from_fit_meta(self, _=None):
        """if Values exist in meta[fit_name]. load them in."""
        if (fits := get_meta(self).get("fits")) is None or self.fit_combo_box.selected == "Add Fit":
            return
        fit = fits[self.fit_combo_box.selected]
        if (func := fit.get("function")) is not None:
            self.formula_frame.update_parameters(None, func)
        else:
            self.formula_frame.update_parameters("")
        if (fit_type := fit.get("fit_type")) is not None:
            self.set_fit_type(fit_type)
        else:
            self.set_fit_type("OLS")
        self.load_limits_from_fit_meta()
        self.load_plotting_style_arguments_from_fit_meta()

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
        ic()
        meta = get_meta(self)
        if (fits := meta.get("fits")) is not None:
            if len(fits) >= 1:
                self.fit_combo_box.configure(values=[*(keys := list(fits.keys())), "Add Fit"])
                self.fit_combo_box.set(keys[0])
                self.fit_combo_box.selected = keys[0]
                self.update_from_fit_meta()
