from customtkinter import *

from ..browse_frame import BrowseFrame


class BrowseSaveFrame(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_button = CTkButton(master=self, text="Save", width=30)
        self.save_button.grid(row=0, column=0)

        self.browse_frame = BrowseFrame(master=self, file_type=".*")
        self.browse_frame.grid(row=0, column=1)
