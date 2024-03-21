from customtkinter import *


class ListFrame(CTkFrame):
    def __init__(self, text: str, has_add_button: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.label = CTkLabel(self, text=text)
        self.label.grid(row=0, column=0)

        self.has_add_button = has_add_button
        if has_add_button:
            self.add_button = CTkButton(master=self, text="Add", command=self.add_parameter)
            self.add_button.grid(row=1, column=0)

        self.entries: list[Entry] = []

        self.text_list = []

        self.entry_bindings = []  # List of function that should be added to the return binding of the entries

    def add_parameter(self, val: str = ""):
        n = len(self.entries)
        entry = Entry(master=self, text=val)
        entry.grid(row=n+1, column=0)
        entry.bind("<Return>", self._update_list)
        for func in self.entry_bindings:
            entry.bind("<Return>", func)
        self.entries.append(entry)
        if self.has_add_button:
            self.add_button.grid(row=n+2, column=0)

    def set_parameters(self, parameters: list):
        self.delete_all()
        for param in parameters:
            self.add_parameter(param)

    def delete_all(self):
        for entry in self.entries:
            entry.destroy()
        self.entries = []

    def _update_list(self, _=None):
        ic(self.get_list())
        self.text_list = self.get_list()

    def get_list(self):
        return [i.string_var.get() for i in self.entries]


class Entry(CTkEntry):
    def __init__(self, text: str = "",  **kwargs):
        self.string_var = StringVar(value=text)
        super().__init__(textvariable=self.string_var, **kwargs)