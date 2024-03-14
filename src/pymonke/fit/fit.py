import numpy as np
from pandas import DataFrame
from scipy.optimize import curve_fit
from scipy import odr

from typing import List, Dict, Tuple, Iterable

from .parse import parse_function, replace_funcs
from .fit_result import FitResult
from ..misc.file_management import read_data_into_dataframe
from ..misc.dataframe import get_error_column_name


class Fit:
    def __init__(self, meta_data: dict, data: DataFrame | None = None):
        self.meta_data = meta_data
        if data is None:
            self.file: str = meta_data["file"]
            if (args := meta_data.get("read_data_args")) is not None:
                self.data: DataFrame = read_data_into_dataframe(self.file, **args)
            else:
                self.data = read_data_into_dataframe(self.file)
        else:
            self.data = data

        self.column_names = self.get_column_names(meta_data.get("error_marker"))

    def get_column_names(self, error_marker: List[str] | None = None) -> Dict[str, str]:
        if error_marker is None:
            error_marker = ["err", "error", "fehler", "Err", "Error", "Fehler"]
        names: Dict[str, str] = dict()
        names["x"] = self.meta_data["x"]
        names["y"] = self.meta_data["y"]
        x_error = get_error_column_name(self.data, names["x"], error_marker)
        y_error = get_error_column_name(self.data, names["y"], error_marker)
        if y_error is None:
            raise ValueError("Y Error values are missing")
        names["y error"] = y_error
        if x_error is not None:
            names["x error"] = x_error

        return names

    def run(self) -> dict[str, FitResult]:
        fits_meta: List[dict] = self.meta_data["fits"]
        result: dict[str, FitResult] = dict()
        for meta in fits_meta:
            result[meta["fit_name"]] = self.__do_fit(meta)

        return result

    def __do_fit(self, meta: dict) -> FitResult:
        if meta["fit_type"] == "optimize.curve_fit":
            return self.__do_optimize_curve_fit(meta)
        elif meta["fit_type"] == "odr":
            return self.__do_odr_fit(meta)
        else:
            raise ValueError(f"unknown fit type: {meta['fit_type']}")

    def __do_optimize_curve_fit(self, meta: dict) -> FitResult:
        p0: List[float | int] = meta["start_parameters"]
        x_min: float = self.data[self.column_names["x"]].min()
        x_max: float = self.data[self.column_names["x"]].max()
        if (val := meta.get("x_min_limit")) is not None:
            x_min = val
        if (val := meta.get("x_max_limit")) is not None:
            x_max = val

        query = f"{self.column_names['x']} >= {x_min} and {self.column_names['x']} <= {x_max}"
        data = self.data.query(query)

        function, params = parse_function(replace_funcs(meta["function"]))
        x = data[self.column_names["x"]]
        y = data[self.column_names["y"]]
        y_error = data[self.column_names["y error"]]
        if (b := meta.get("absolute_sigma")) is None:
            b = False
        if (check_finite := meta.get("check_finite")) is None:
            check_finite = False
        out: tuple = curve_fit(function, xdata=x, ydata=y, sigma=y_error, absolute_sigma=b,
                               check_finite=check_finite, p0=p0)
        popt, pcov = out
        fit_res = FitResult(function, params, popt, np.sqrt(pcov.diagonal()))
        fit_res.set_reduced_chi_squared(x, y, y_error)
        return fit_res

    def __do_odr_fit(self, meta: dict) -> FitResult:
        p0: List[float | int] = meta["start_parameters"]
        x_min: float = self.data[self.column_names["x"]].min()
        x_max: float = self.data[self.column_names["x"]].max()
        if (val := meta.get("x_min_limit")) is not None:
            x_min = val
        if (val := meta.get("x_max_limit")) is not None:
            x_max = val

        query = f"{self.column_names['x']} >= {x_min} and {self.column_names['x']} <= {x_max}"
        data = self.data.query(query)

        function, params = parse_function(replace_funcs(meta["function"]))
        x, y = data[self.column_names["x"]], data[self.column_names["y"]]
        sy = data[self.column_names["y error"]]
        sx = None
        if (name := self.column_names.get("x error")) is not None:
            sx = data[name]

        if (b := meta.get("absolute_sigma")) is None:
            b = False

        if b:
            odr_data = odr.RealData(x=x, y=y, sy=sy, sx=sx)
        else:
            wd = None
            if sx is not None:
                wd = 1 / sx**2
            odr_data = odr.Data(x=x, y=y, we=1/sy**2, wd=wd)

        def odr_func(_b: list, _x: float | int) -> float | int | Iterable[float | int]:
            return function(_x, *_b)

        odr_model = odr.Model(odr_func)
        odr_odr = odr.ODR(odr_data, odr_model, p0)
        odr_out: odr.Output = odr_odr.run()
        fit_res = FitResult(function, params, odr_out.beta, odr_out.sd_beta)
        fit_res.set_reduced_chi_squared(x, y, sy)
        return fit_res
