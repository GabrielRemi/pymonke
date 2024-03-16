from customtkinter import *
from icecream import ic

from typing import Optional

from .misc import browse_files


class BrowseFrame(CTkFrame):
    def __init__(self, file_type: str, **kwargs):
        super().__init__(**kwargs)

        self.type = file_type
        self.file_path = StringVar(master=self, value=None)
        self.entry = CTkEntry(master=self, placeholder_text="Enter the file path", textvariable=self.file_path)
        self.entry.grid(row=0, column=0)

        self.button = CTkButton(master=self, text="Browse", command=self.__browse)
        self.button.grid(row=0, column=1)

    def __browse(self):
        self.file_path.set(browse_files("select Data file", self.type))
