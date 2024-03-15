from tkinter import filedialog

import os


def browse_files(text: str, file_type: str) -> str:
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                          filetypes=((text, file_type), ("all files", "*.*")))

    return filename
