from customtkinter import *


class DictFrame(CTkFrame):
    def __init__(self, text:str, **kwargs):
        super().__init__(**kwargs)
        self.label = CTkLabel(self, text=text)
        self.label.grid(row=0, column=0)

        self.add_button = CTkButton(master=self, text="Add", command=self.add_parameter)
        self.add_button.grid(row=1, column=0)

        self.entries: list[EntryPairFrame] = []

    def add_parameter(self):
        n = len(self.entries)
        entry = EntryPairFrame(master=self)
        entry.grid(row=n+1, column=0)
        self.entries.append(entry)
        self.add_button.grid(row=n+2, column=0)


class EntryPairFrame(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_var = StringVar()
        self.value_var = StringVar()
        self.key = CTkEntry(master=self, textvariable=self.key_var)
        self.value = CTkEntry(master=self, textvariable=self.value_var)
        self.key.grid(row=0, column=0)
        self.value.grid(row=0, column=1)
