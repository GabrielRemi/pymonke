from customtkinter import *

from .slider import Slider


class MinMaxSlider(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)

        self.min_slider = Slider(master=self)
        self.min_slider.slider.configure(command=self.set_min_slider)
        self.min_slider.grid(row=1, column=0)

        self.max_slider = Slider(master=self)
        self.max_slider.slider.configure(command=self.set_max_slider)
        self.max_slider.grid(row=1, column=1)

    def set_boundaries(self, _min: float, _max: float) -> None:
        self.min_slider.min_label.configure(text=str(_min))
        self.max_slider.max_label.configure(text=str(_max))

    def set_max_slider(self, value: float):
        """When the max limit slider is moved, change the maximum value of the min slider
        accordingly."""
        self.max_slider.set_value(value)
        self.min_slider.max_label.configure(text=str(value))
        self.min_slider.configure(to=value)

    def set_min_slider(self, value: float):
        """When the min limit slider is moved, change the minimum value of the max slider
        accordingly"""
        self.min_slider.set_value(value)
        self.max_slider.min_label.configure(text=str(value))
        self.max_slider.configure(from_=value)


