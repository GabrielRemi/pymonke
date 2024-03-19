from customtkinter import *
import pandas as pd

from dataclasses import dataclass, field
import os
from tkinter import filedialog
from typing import Any, Optional


class EntryError(Exception):
    """Error that occurs when trying to enter a text into an entry that is not supposed to be entered
    by the user."""
    def __init__(self, text: str = "Invalid Entry"):
        Exception.__init__(self, text)


def browse_files(text: str, file_type: str) -> str:
    """Search for a file in the file explorer."""
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                          filetypes=((text, file_type), ("all files", "*.*")))

    return filename


@dataclass
class Root:
    meta: dict = field(default_factory=dict)
    data: Optional[pd.DataFrame] = None
    fit_result: Optional[dict] = None

    def load_from_meta(self) -> None:
        """Update everything based on the meta dictionary."""
        ...

    def get_x(self) -> Optional[pd.Series]: ...

    def get_y(self) -> Optional[pd.Series]: ...

    def get_sx(self) -> Optional[pd.Series]: ...

    def get_sy(self) -> Optional[pd.Series]: ...

    def get_plot_frame(self) -> Any: ...

    def do_fit(self) -> Any: ...

    def __lt__(self, other):
        return len(self.data) < len(other.data)

    def __hash__(self):
        return hash(1)


class Update:
    """Virtual Typing class for every class that should be updated if Root.meta is changed."""
    def update(self):
        ...

    def __lt__(self, other):
        return len(self.__name__) < len(other.__name__)

    def __hash__(self):
        return hash(1)


def get_meta(obj: CTkBaseClass) -> dict[str, Any]:
    """Get the metadata for data fitting by looking for a master object that has the meta attribute
    and is a subclass of Root."""
    master = obj.master
    while not isinstance(master, Root):
        master = master.master

    assert isinstance(master, Root)
    return master.meta


def get_data(obj: CTkBaseClass) -> Optional[pd.DataFrame]:
    """Get the metadata for data fitting by looking for a master object that has the meta attribute
    and is a subclass of Root."""
    master = obj.master
    while not isinstance(master, Root):
        master = master.master

    assert isinstance(master, Root)
    return master.data


def get_root(obj: CTkBaseClass) -> Root:
    """Get the Root object."""
    master = obj.master
    while not isinstance(master, Root):
        master = master.master

    return master