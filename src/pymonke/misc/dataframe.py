from pandas import DataFrame

from typing import List


def get_error_column_name(data: DataFrame, column: str, error_marker: List[str] | None = None) -> str | None:
    """Get the columns name that is the uncertainty of the column argument. return None if not found.
    parameters
    ----------
    data: DataFrame
    The dataframe to analyze.
    column: str
    The name of the column which represents a series of values that have an uncertainty.
    error_marker: List[str]
    A list of words that indicate that a column represents a series of uncertainties.
    """
    columns = list(data.columns)
    if column not in columns:
        raise ValueError("column not in DataFrame")

    if error_marker is None:
        error_marker = ["error", "err", "fehler", "Error", "Err", "Fehler"]

    error_separator = ["_", "-", " ", ""]
    result: str | None = None
    for marker in error_marker:
        for separator in error_separator:
            if f"{column}{separator}{marker}" in columns:
                if result is None:
                    result = f"{column}{separator}{marker}"
                else:
                    text = f"""Error in DataFrame for the column {column} could not be determined because 
                    of ambivalence. Error marker are {error_marker}"""
                    raise ValueError(text)
    return result