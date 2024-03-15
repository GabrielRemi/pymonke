import customtkinter as tk
from customtkinter import CTk
from icecream import ic
import matplotlib.pyplot as plt

from .app import App


def run():
    app = App()
    app.mainloop()

