from customtkinter import CTkComboBox

from typing import Callable, Any

from ..misc import get_root, get_meta


class FitComboBox(CTkComboBox):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, values=["Add Fit"], command=self.on_selection)
        self.bind("<Return>", self.add_or_rename)

        self.selection_bindings: list[Callable[[], None]] = []
        self.return_bindings: list[Callable[[], None]] = []

        self.selected: str = "Add Fit"

    def add_or_rename(self, _=None) -> None:
        if (fits := get_meta(self).get("fits")) is None:
            get_meta(self)["fits"] = fits = dict()

        fit_name: str = self.get()
        old: list[str] = self.cget("values")
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
            self.selected = fit_name
        else:  # Rename or delete
            if fit_name == "":
                get_root(self).meta["fits"].pop(self.selected)
                old.remove(self.selected)
                self.set("Add Fit")
                self.selected = "Add Fit"
            else:
                for i, name in enumerate(old):
                    if name == self.selected:
                        old[i] = fit_name
                fits[fit_name] = fits.pop(self.selected)
                self.selected = fit_name
            self.configure(values=old)
        # self.change_meta_of_plotting_arguments()
        for binding in self.return_bindings:
            binding()

    def change_meta_of_plotting_arguments(self):
        # change meta for plotting arguments
        ic(self.selected)
        meta = get_meta(self)["fits"].get(self.selected)
        if meta is not None:
            val = meta.get("plotting_style")
            if val is None:
                meta["plotting_style"] = dict()
            meta = meta["plotting_style"]
        get_root(self).get_fit_frame().plotting_style_arguments.meta = meta
        ic(meta)
        ic(get_meta(self))

    def on_selection(self, event=None):
        self.selected = self.get()
        for binding in self.selection_bindings:
            binding()
        # self.change_meta_of_plotting_arguments()
