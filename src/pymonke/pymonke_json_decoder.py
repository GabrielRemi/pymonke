import json
from json import JSONDecoder
from typing import Any

import numpy as np

from .mmath.num_with_error import NumWithError
from .fit.fit_result import FitResult


def _object_hook(dct: dict[str, Any]) -> Any | None:
    keys = list(dct.keys())
    keys.sort()
    if keys == ["error", "value"]:
        return NumWithError(dct["value"], dct["error"])
    else:
        return dct



class PyMonkeJSONDecoder(JSONDecoder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        json.JSONDecoder.__init__(self, object_hook=_object_hook, *args, **kwargs)

