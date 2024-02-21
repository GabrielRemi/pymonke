# ERROR STYLE ENUM
from enum import Enum


class ErrorStyle(Enum):
    PLUSMINUS = 1
    PARENTHESIS = 2
    SCIENTIFIC = 3

    def __eq__(self, other):
        return self.value == other.value
