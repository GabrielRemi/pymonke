from customtkinter import *

from ..misc import get_meta


class LimitsFrame(CTkFrame):
    def __init__(self, label: str = "", **kwargs):
        CTkFrame.__init__(self, **kwargs)
        if label != "":
            self.label = CTkLabel(master=self, text=label)
            self.label.grid(row=0, column=0)

        self.min = StringVar(value="min")
        self.max = StringVar(value="max")
        self.lower_bound: float = 0
        self.upper_bound: float = 1
        self.set_bounds(0, 1)

        self.entry_bindings = []

        self.min_entry = CTkEntry(self, textvariable=self.min)
        self.min_entry.bind("<Return>", command=self.min_callback)
        self.max_entry = CTkEntry(self, textvariable=self.max)
        self.max_entry.bind("<Return>", command=self.max_callback)

        # for binding in self.entry_bindings:
        #     self.min_entry.bind("<Return>", command=binding)
        #     self.max_entry.bind("<Return>", command=binding)

        self.min_entry.grid(row=1, column=0)
        self.max_entry.grid(row=1, column=1)

    def set_bounds(self, _min: float, _max: float) -> None:
        self.lower_bound = _min
        self.upper_bound = _max
        self.min.set(str(_min))
        self.max.set(str(_max))

    def set_min(self, value: float):
        if value >= (max := float(self.max.get())):
            value = max
            value -= (max - self.lower_bound) / max * 0.001
        self.min.set(str(value))
        # get_meta(self)["x_min_limit"] = value

    def set_max(self, value: float):
        if value <= (_min := float(self.min.get())):
            value = _min
            value += (self.upper_bound - _min) / _min * 0.001
        self.max.set(str(value))
        # get_meta(self)["x_max_limit"] = value

    def min_callback(self, _):
        self.set_min(float(self.min.get()))
        for binding in self.entry_bindings:
            binding()

    def max_callback(self, _):
        self.set_max(float(self.max.get()))
        for binding in self.entry_bindings:
            binding()

