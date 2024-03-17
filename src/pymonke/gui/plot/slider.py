from customtkinter import *

from typing import Optional


class Slider(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)
        self.min_label = CTkLabel(self)
        self.min_label.grid(row=0, column=0)

        self.slider = CTkSlider(master=self, command=self.set_value)
        self.slider.grid(row=0, column=1)

        self.max_label = CTkLabel(self)
        self.max_label.grid(row=0, column=2)

        self.value_label = CTkLabel(self, text="value")
        self.value_label.grid(row=1, column=0, columnspan=3)

    def set_value(self, value):
        self.value_label.configure(text=str(value))

    def get_value(self) -> float:
        return self.slider.get()
