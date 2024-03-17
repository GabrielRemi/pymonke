from customtkinter import *
import pandas as pd

import json

from .browse_save_frame import BrowseSaveFrame
from ..browse_frame import BrowseFrame
from ..entry_label_frame import EntryLabelFrame
from ..info_label import InfoLabel
from ..misc import get_data, get_meta

from pymonke.misc.file_management import read_data_into_dataframe
from pymonke.misc.dataframe import get_error_column_name


class DataInitFrame(CTkFrame):
    def __init__(self, **kwargs):
        CTkFrame.__init__(self, **kwargs)

        self.browse_data_frame = BrowseFrame(file_type="*.csv; *.txt", master=self, placeholder="Enter the data file")
        self.browse_data_frame.grid(row=0, column=0, columnspan=2)

        self.load_meta_frame = BrowseFrame(file_type=".json", master=self, browse_text="load",
                                           placeholder="Enter the meta data for plotting")
        self.load_meta_frame.grid(row=1, column=0, columnspan=2)

        self.x_data_frame = EntryLabelFrame(master=self, label="X")
        self.x_data_frame.entry.bind("<Return>", self.save_x_name)
        self.x_data_frame.grid(row=2, column=0)
        self.y_data_frame = EntryLabelFrame(master=self, label="Y")
        self.y_data_frame.entry.bind("<Return>", self.save_y_name)
        self.y_data_frame.grid(row=2, column=1)

        self.info_label = InfoLabel(master=self, text="Errors displayed here", text_color="red")
        self.info_label.grid(row=3, column=0, columnspan=2)

        self.save_meta_frame = BrowseSaveFrame(master=self)
        self.save_meta_frame.grid(row=4, column=0, columnspan=2)

    def load_data(self) -> pd.DataFrame:
        try:
            self.browse_data_frame.browse()
            file_path = self.browse_data_frame.file_path.get()
            data = read_data_into_dataframe(file_path)
            get_meta(self)["file"] = file_path
            ic(get_meta(self))
            self.info_label.show_info(text="data loaded successfully")
            return data
        except Exception as e:
            self.info_label.show_error(str(e))

    def load_meta(self) -> dict | None:
        try:
            self.load_meta_frame.browse()
            file_path = self.load_meta_frame.file_path.get()
            data = json.loads(open(file_path).read())
            self.info_label.show_info("Meta Data loaded successfully")
            return data
        except Exception as e:
            self.info_label.show_error(str(e))
            return None

    def check_xy_input(self, x_or_y: str, ):
        if x_or_y == "x":
            if (text := self.x_data_frame.text.get()) is not None and self.entry_in_dataframe(text):
                self.info_label.show_info("X column found")
            else:
                self.info_label.show_error("X column not found")
        elif x_or_y == "y":
            if (text := self.y_data_frame.text.get()) is not None and self.entry_in_dataframe(text):
                if get_error_column_name(get_data(self), text) is None:
                    self.info_label.show_error("Y Error not found")
                else:
                    self.info_label.show_info("Y column found")
            else:
                self.info_label.show_error("Y column not found")

    def entry_in_dataframe(self, name: str) -> bool:
        if (data := get_data(self)) is not None:
            return name in data
        else:
            return False

    def save_x_name(self, _=None):
        x_name = self.x_data_frame.text.get()
        get_meta(self)["x"] = x_name
        self.check_xy_input("x")
        ic(get_meta(self))

    def save_y_name(self, _=None):
        y_name = self.y_data_frame.text.get()
        get_meta(self)["y"] = y_name
        self.check_xy_input("y")
        ic(get_meta(self))

    def load_from_meta(self) -> None:
        """Function that initializes values in this frame if metadata is loaded."""
