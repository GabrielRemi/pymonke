from customtkinter import CTkFrame, StringVar, CTkEntry, CTkLabel

from typing import Callable, Any, Optional


class LimitsFrame(CTkFrame):
    def __init__(self, label: str = "", **kwargs: Any) -> None:
        CTkFrame.__init__(self, **kwargs)
        if label != "":
            self.label = CTkLabel(master=self, text=label)
            self.label.grid(row=0, column=0)

        self.min_var = StringVar(value="")
        self.max_var = StringVar(value="")
        self.__min: Optional[float] = None
        self.__max: Optional[float] = None
        self.set_limits(None, None)

        self.entry_bindings: list[Callable[[], None]] = []

        self.min_entry = CTkEntry(self, textvariable=self.min_var)
        self.min_entry.bind("<Return>", command=self.min_callback)
        self.max_entry = CTkEntry(self, textvariable=self.max_var)
        self.max_entry.bind("<Return>", command=self.max_callback)

        self.min_entry.grid(row=1, column=0)
        self.max_entry.grid(row=1, column=1)

    @property
    def min(self) -> Optional[float]:
        return self.__min

    @min.setter
    def min(self, value: Optional[float]) -> None:
        if value is None:
            self.__min = None
            self.min_var.set("")
        else:
            self.__min = value
            self.min_var.set(str(value))

    def get_min_var(self) -> Optional[float]:
        if (val := self.min_var.get()) == "":
            return None
        else:
            return float(val)

    def get_max_var(self) -> Optional[float]:
        if (val := self.max_var.get()) == "":
            return None
        else:
            return float(val)

    @property
    def max(self) -> Optional[float]:
        return self.__max

    @max.setter
    def max(self, value: Optional[float]) -> None:
        if value is None:
            self.__max = None
            self.max_var.set("")
        else:
            self.__max = value
            self.max_var.set(str(value))

    def set_limits(self, _min: Optional[float], _max: Optional[float]) -> None:
        self.min = _min
        self.max = _max

    def set_min(self, value: Optional[float]) -> None:
        if self.max is not None and value is not None:
            if value >= self.max:
                self.min = self.min
                return

        self.min = value

    def set_max(self, value: Optional[float]) -> None:
        if self.min is not None and value is not None:
            if value <= self.min:
                self.max = self.max
                return
        self.max = value

    def min_callback(self, _: Any) -> None:
        try:
            self.set_min(self.get_min_var())
            for binding in self.entry_bindings:
                binding()
        except ValueError:
            self.min = self.min

    def max_callback(self, _: Any) -> None:
        try:
            self.set_max(self.get_max_var())
            for binding in self.entry_bindings:
                binding()
        except ValueError:
            self.max = self.max
