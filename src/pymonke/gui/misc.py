from tkinter import filedialog

import os


class EntryError(Exception):
    def __init__(self, text: str = "Invalid Entry"):
        Exception.__init__(self, text)


def browse_files(text: str, file_type: str) -> str:
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                          filetypes=((text, file_type), ("all files", "*.*")))

    return filename
