import pandas as pd

from typing import Dict, List


def transform_dataframe_to_latex_ready(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """for every Column searches for another column that represents the error and then puts the together
    in a single column with rounded numbers. optionally renames the columns"""
    pass