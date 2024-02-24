from dataclasses import dataclass, field
from typing import Any, List

from monke.latex.tex_tabular import TexTabular


@dataclass
class TexTable:
    positioning: str = "htbp"
    widths: List[float] = field(default_factory=list)
    spacing: List[float | str] = field(default_factory=list)
    tabular: List[TexTabular] = field(default_factory=list)

    def save(self, file_path: str, method: str = "w") -> None:
        with open(file_path, method) as file:
            file.write(str(self))

    def __str__(self) -> str:
        content = ""

        if len(self.tabular) == 0:
            raise ValueError("No tabular defined")
        elif len(self.tabular) == 1:
            content = self.tabular[0]
        else:
            if len(self.tabular) > len(self.widths):
                raise ValueError(r"you need to specify the width of each tabular")
            space: str = ""
            for (index, tab) in enumerate(self.tabular):
                text: str = space
                text += f"\n    \\parbox{{{self.widths[index]}\\linewidth}}{{\n        \\centering\n"
                text += str(tab)
                text += f"\n    }}"
                content += text
                try:
                    s = self.spacing[index]
                    if isinstance(s, float):
                        space = f"\\hspace{{{self.spacing[index]}cm}}"
                    elif isinstance(s, str):
                        space = s
                    else:
                        raise TypeError("the spacing parameter must be a float or a string")
                except IndexError:
                    space = r"\qquad"

        result = f"\\begin{{table}}[{self.positioning}]\n    \\centering\n{content}\n\\end{{table}}"
        return result

