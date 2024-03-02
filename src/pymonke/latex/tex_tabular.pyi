import pandas as pd

from dataclasses import dataclass
from typing import List


@dataclass
class TexTabular:
    r"""This classes purpose is to create a string which can be used to create a LaTeX tabular environment out of
    a pandas DataFrame. Because of a separate table class for more complex use, the tabular environment will not be
    automatically put inside a table environment, but it will be if printed to a file with the `save` method.

    the string will have output in the following form:
    \caption{#caption}
    \label{#label}
    \begin{tabular}{#alignment}
        #data
    \end{tabular}

    Parameters
    ----------
    alignment: str
    Determines the alignment of the table. For a table with 3 columns with centered
    outputs and columns separated by lines, the alignment would be "c|c|c".
    data: DataFrame, optional
    contains the data of the table. If the data is given at initialization, for every
    column the corresponding errors will be searched inside the DataFrame. If this is not desired, the
    data should be inserted after initialization. For more complex operations to the data like renaming
    the columns, the method `add_data` should be used. This parameter is only optional at initialization.
    caption: str, optional
    The caption of the table. Is set to "default Caption" by default.
    label: str, optional
    The label of the table. Is set to "default Label" by default.
    h_lines: List[int], optional
    contains the indices of positions, where horizontal lines should be added to
    the table. The index 0 represents a horizontal line above the first line. If an index is inserted to the
    table multiple times, multiples lines will be inserted at that position. Is set to [1] by default.
    filler: str, optional
    Will be used to fill spaces in the table where no data exists. is set to "--" by default.
    booktabs: bool
    If set to `True`, the hlines will be replaced with macros from the booktabs package
    (midrule, toprule, bottomrule).

    """
    alignment: str
    data: pd.DataFrame = ...
    caption: str = ...
    label: str = ...
    caption_above: bool = ...
    h_lines: List[int] | None = ...
    filler: str = ...
    booktabs: bool = ...

    def add_data(self, data: pd.DataFrame, **kwargs) -> None:
        r"""Iterates through the column names and tries to find the corresponding error column.
    If it is found, both columns will be put together into a new column with the numbers separated by a plusminus
    sign. Other numbers in the DataFrame will be put inside the tablenum macro for proper alignment inside the
    table.

    Parameters
    ----------
    data: DataFrame
    Data to be transformed into other data that can be made into a string to work with LaTeX tables.

    Keyword Parameters
    ------------------
    error_marker: List[str], optional
    Defines a list of all string suffixes that mark a column of uncertainties. The default value
    is ["err", "error", "fehler", "Err", "Error", "Fehler"].
    columns: Dict[str, str], optional
    If a Key corresponds to a column of the data, that column will be renamed to the given value.
    ignore_rest: bool, optional
    If set to true, every column of the data that is not a key in the `columns` keyword argument will
    be dropped in the resulting DataFrame. The default value is `False`.
    is_table_num: bool, optional
    If false, numbers will not be inserted in the tablenum macro but the num macro instead. Default value is `True`.
    siunitx_column_option: Dict[str, str], optional
    For every column that is a key in the given dictionary, the value is inserted as an option for the tablenum
    macro.
    """
    ...

    def __data_to_str(self) -> str:
        """Creates a string out of the data that can be inserted inside a LaTeX table"""
        ...

    def save(self, file_path: str, method: str = "w", positioning: str = "htbp") -> None:
        r"""Save the string inside a table environment to a file specified by `file_path`. The `method` argument
        corresponds to the same parameter of the builtin `open()` function.

        `position` determines the positioning behavior of the table.
        """
        ...

