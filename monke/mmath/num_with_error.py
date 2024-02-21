import numpy as np

from typing import Tuple, Any, List


class NumWithError:
    """inputs two numbers and rounds them appropriately, treating x_error as an uncertainty.
    x and x_error could also be array_like objects."""
    def __init__(self, x, x_error):
        self.x = x
        self.x_error = x_error

    def get_values(self) -> Tuple[float | List[float], float | List[float]]:
        return self.x, self.x_error

    def __eq__(self, other):
        return self.x == other.x and self.x_error == other.x_error
