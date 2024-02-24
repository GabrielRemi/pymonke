import pandas as pd

from dataclasses import dataclass, field
from typing import Any, List
import os
import sys

from utils import transform_dataframe_to_latex_ready


@dataclass
class TexTabular:
    alignment: str
    caption: str = "default Caption"
    caption_above: bool = True
    label: str = "default Label"
    h_lines: List[int] | None = None
    filler: str = "--"
    booktabs: bool = False
    data: pd.DataFrame = field(default_factory=pd.DataFrame)

    def __post_init__(self):
        if self.h_lines is None:
            self.h_lines = [1]
        if not self.data.empty:
            self.data = transform_dataframe_to_latex_ready(self.data)

    def add_data(self, data: pd.DataFrame, **kwargs) -> None:
        """before setting the input to the tabular data, the function reformats the error arrays with the
        corresponding number arrays and then renames the columns"""
        self.data = transform_dataframe_to_latex_ready(data, **kwargs)

    def __data_to_str(self) -> str:
        result: str = ""
        data: list = [list(self.data.columns)]
        data.extend(list(i) for i in self.data.to_numpy())

        for (index, column) in enumerate(data):
            h_lines: int = len(list(filter(lambda x: x == index, self.h_lines)))
            if h_lines > 0:
                line_style = "hline"
                if index == 0 and self.booktabs:
                    line_style = "toprule"
                elif self.booktabs:
                    line_style = "midrule"

                result += "        " + f"\\{line_style}" * h_lines + "\n"
            result += "        "
            for elem in column:
                if str(elem) == "nan":
                    elem = self.filler
                result += str(elem) + " & "
            result = result.removesuffix(" & ")
            result += " \\\\\n"

        end_hlines: int = len(list(filter(lambda x: x == len(data), self.h_lines)))
        if end_hlines > 0:
            line_style = "hline"
            if self.booktabs:
                line_style = "bottomrule"

            result += "        " + f"\\{line_style}" * end_hlines + "\n"
        result = result.removesuffix("\n")
        return result

    def save(self, file_path: str, method: str = "w", positioning: str = "htbp") -> None:
        result = f"\n\\begin{{table}}[{positioning}]\n    \\centering\n{str(self)}\n\\end{{table}}\n"
        with open(file_path, method) as file:
            file.write(result)

    def __str__(self):
        caption_str = f"\\caption{{{self.caption}}}"
        label_str = f"\\label{{{self.label}}}"
        result: str = f"    \\begin{{tabular}}{{{self.alignment}}}\n"
        if self.caption_above:
            result = f"    {caption_str}\n    {label_str}\n{result}"
        result += f"{self.__data_to_str()}\n"
        result += f"    \\end{{tabular}}"
        if not self.caption_above:
            result += f"\n    {caption_str}\n    {label_str}"

        return result
