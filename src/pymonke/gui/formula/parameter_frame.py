from customtkinter import *

from typing import Any, Callable


class ParameterFrame(CTkFrame):
    def __init__(self, name: str, **args):
        super().__init__(**args)
        self.name = name
        self.value = CTkLabel(master=self, text="", width=120)
        self.name_var = StringVar(master=self, value=name)
        self.name_entry = CTkEntry(master=self, textvariable=self.name_var, width=50)
        self.name_entry.grid(row=0, column=0, padx=10)
        self.name_entry.bind("<Return>", command=self.rename)
        self.value.grid(row=0, column=1, sticky="w")

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name
        self.name_var.set(name)

    def get_entry(self) -> str:
        return self.name_entry.get()

    def reset_entry(self):
        """Resets the entry to the name."""
        self.set_name(self.name)

    def set_value(self, value: Any):
        self.value.configure(text=str(value))

    def rename(self, _):
        temp = self.master
        while True:
            if hasattr(temp, "rename"):
                if isinstance(temp.rename, Callable):
                    temp.rename()
                    return
            temp = temp.master

