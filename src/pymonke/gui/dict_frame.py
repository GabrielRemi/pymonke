from customtkinter import *


from .misc import get_root


class EntryPairFrame(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_var = StringVar()
        self.value_var = StringVar()
        self.key = CTkEntry(master=self, textvariable=self.key_var)
        self.value = CTkEntry(master=self, textvariable=self.value_var)
        self.key.grid(row=0, column=0)
        self.value.grid(row=0, column=1)

        self.delete_button = CTkButton(master=self, text="-", width=30, command=self.destroy)
        self.delete_button.grid(row=0, column=2)


class DictFrame(CTkFrame):
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.label = CTkLabel(self, text=text)
        self.label.grid(row=0, column=0)

        self.add_button = CTkButton(master=self, text="Add", command=self.add_parameter)
        self.add_button.grid(row=1, column=0)

        self.entries: list[EntryPairFrame] = []

        self.return_bindings = []
        self.ignore_keys = []

    def add_parameter(self, key: str = "", value: str = ""):
        n = len(self.entries)
        entry = EntryPairFrame(master=self)
        entry.key.bind("<Return>", self.bindings)
        entry.key_var.set(key)
        entry.value.bind("<Return>", self.bindings)
        entry.value_var.set(value)
        entry.grid(row=n+1, column=0)
        entry.delete_button.configure(command=lambda: self.delete_on_button_click(entry))

        self.entries.append(entry)
        self.add_button.grid(row=n+2, column=0)

    def load_parameters(self, data: dict) -> None:
        self.delete_all()
        for key in data.keys():
            val = data[key]
            if key not in self.ignore_keys:
                self.add_parameter(key, val)

    def delete_entry(self, index) -> None:
        entry = self.entries.pop(index)
        entry.destroy()

    def delete_last(self) -> None:
        self.delete_entry(-1)

    def delete_all(self) -> None:
        for _ in range(len(self.entries)):
            self.delete_last()

    def delete_on_button_click(self, button: EntryPairFrame):
        """delete the Button and also remove the entry from meta"""
        ic.enable()
        ic()
        key = button.key_var.get()
        index = button.grid_info()["row"] - 1
        get_root(self).get_fit_meta()["plotting_style"].pop(key)
        self.delete_entry(index)
        ic(get_root(self).meta)
        ic.disable()

    def get_args(self):
        res = dict()
        for entry in self.entries:
            if (val := entry.value_var.get()) == "":
                val = None
            res[entry.key_var.get()] = self.parse(val)

        return res

    def bindings(self, _=None):
        for binding in self.return_bindings:
            binding()

    def parse(self, value: str):
        try:
            return float(value)
        except:
            return value


