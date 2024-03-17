from customtkinter import *

from typing import Optional


class Slider(CTkFrame):
    def __init__(self, _min: Optional[float] = None, _max: Optional[float] = None, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.min_label = CTkLabel(self, text=str(_min))
        self.min_label.grid(row=0, column=0)

        self.slider = CTkSlider(master=self, command=self.set_value)
        self.slider.grid(row=0, column=1)

        self.max_label = CTkLabel(self, text=str(_max))
        self.max_label.grid(row=0, column=2)

        self.value_label = CTkLabel(self, text="value")
        self.value_label.grid(row=1, column=0, columnspan=3)

        self.set_boundaries(_min, _max)

    def set_boundaries(self, _min: Optional[float] = None, _max: Optional[float] = None):
        if _min is None:
            _min = "min"
        if _max is None:
            _max = "max"

        self.min_label.configure(text=str(_min))
        self.max_label.configure(text=str(_max))

    def set_value(self, value):
        self.value_label.configure(text=str(value))

    def get_value(self) -> float:
        return self.slider.get()
