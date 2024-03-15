import matplotlib.pyplot as plt
from matplotlib.figure import Figure, SubFigure
from mypy_extensions import VarArg
import numpy as np
from pandas import DataFrame, Series
import scienceplots
from scipy import odr
from scipy.optimize import curve_fit

from typing import List, Dict, Tuple, Iterable, Callable, TypeAlias, Optional, Any

from .fit_result import FitResult
from ..misc.dataframe import get_error_column_name
from ..misc.file_management import read_data_into_dataframe
from .parse import parse_function, replace_funcs, numerical, scalar, array

func_type: TypeAlias = Callable[[numerical, VarArg(scalar)], numerical]


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

        self.result: Optional[dict[str, FitResult]] = None

        self.column_names = self.__get_column_names(meta_data.get("error_marker"))

    def __get_column_names(self, error_marker: List[str] | None = None) -> Dict[str, str]:
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

    def plot(self, figure_id: Optional[int | str | Figure | SubFigure] = None):
        if (style := self.meta_data.get("figure_style")) is None:
            style = "science"
        plt.style.use(style)
        if (size := self.meta_data.get("figure_size")) is None:
            size = (6, 4.7)
        if (dpi := self.meta_data.get("figure_dpi")) is None:
            dpi = 120
        plt.figure(num = figure_id, figsize=size, dpi=dpi)
        x, y = self.column_names["x"], self.column_names["y"]
        sx, sy = self.column_names.get("x error"), self.column_names["y error"]
        if sx is None:
            sx = 0
        else:
            sx = self.data[sx]

        plotting_style = {
            "linestyle": "",
            "ms": 3,
            "marker": "o",
            "capsize": 2.5,
            "zorder": 100
        }

        if (more_style := self.meta_data.get("plotting_style")) is not None:
            plotting_style.update(more_style)

        plt.xlim(self.__get_xlim(self.meta_data))
        plt.errorbar(self.data[x], self.data[y], yerr=self.data[sy], xerr=sx, **plotting_style)

        if self.result is not None:
            for fit_name in self.result.keys():
                self.__plot_fit(fit_name, self.result[fit_name])

    def __plot_fit(self, name: str, fit_res: FitResult) -> None:
        meta: dict = self.meta_data["fits"][name]
        if (points := meta.get("fit_points")) is None:
            points = 150

        plotting_style = {
            "linestyle": "--",
            "zorder": 0,
        }

        if (more_style := meta.get("plotting_style")) is not None:
            plotting_style.update(more_style)

        x = np.linspace(*self.__get_xlim(meta), points)
        plt.plot(x, fit_res.eval(x), **plotting_style)

    def __get_xlim(self, meta: dict) -> Tuple[float, float]:
        x = self.column_names["x"]
        if (x_min := meta.get("x_min_limit")) is None:
            x_min = self.data[x].min()
        if (x_max := meta.get("x_max_limit")) is None:
            x_max = self.data[x].max()

        return x_min, x_max

    def run(self) -> dict[str, FitResult]:
        fits_meta: dict[str, dict] = self.meta_data["fits"]
        result: dict[str, FitResult] = dict()
        for fit_name in fits_meta.keys():
            result[fit_name] = self.__do_fit(fits_meta[fit_name])

        self.result = result

        return result

    def __do_fit(self, meta: dict) -> FitResult:
        if meta["fit_type"] == "optimize.curve_fit":
            return self.__do_optimize_curve_fit(meta)
        elif meta["fit_type"] == "odr":
            return self.__do_odr_fit(meta)
        else:
            raise ValueError(f"unknown fit type: {meta['fit_type']}")

    def __do_optimize_curve_fit(self, meta: dict) -> FitResult:
        function, params, p0, lim, arrays = self.__get_fitting_data(meta)
        x, y, y_error = arrays["x"], arrays["y"], arrays["sy"]
        assert isinstance(x, Series) and isinstance(y, Series) and isinstance(y_error, Series)

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
        function, params, p0, lim, arrays = self.__get_fitting_data(meta)
        x, y, sy = arrays["x"], arrays["y"], arrays["sy"]
        sx = arrays.get("sx")
        assert isinstance(x, Series) and isinstance(y, Series) and isinstance(sy, Series)
        if (b := meta.get("absolute_sigma")) is None:
            b = False

        if b:
            odr_data = odr.RealData(x=x, y=y, sy=sy, sx=sx)
        else:
            wd = None
            if sx is not None:
                wd = 1 / sx ** 2
            odr_data = odr.Data(x=x, y=y, we=1 / sy ** 2, wd=wd)

        def odr_func(_b: list, _x: float | int) -> numerical:
            return function(_x, *_b)

        odr_model = odr.Model(odr_func)
        odr_odr = odr.ODR(odr_data, odr_model, p0)
        odr_out: odr.Output = odr_odr.run()
        fit_res = FitResult(function, params, odr_out.beta, odr_out.sd_beta)
        fit_res.set_reduced_chi_squared(x, y, sy)
        return fit_res

    def __get_fitting_data(self, meta: dict) -> Any:

        p0: List[float | int] = meta["start_parameters"]
        x_min, x_max = self.__get_xlim(meta)

        query = f"{self.column_names['x']} >= {x_min} and {self.column_names['x']} <= {x_max}"
        data = self.data.query(query)

        function, params = parse_function(replace_funcs(meta["function"]))
        x: Series = data[self.column_names["x"]]
        y: Series = data[self.column_names["y"]]
        sy: Series = data[self.column_names["y error"]]
        sx: Optional[Series] = None
        if (name := self.column_names.get("x error")) is not None:
            sx = data[name]

        fitting_data: Dict[str, array | Optional[array]] = {
            "x": x,
            "y": y,
            "sy": sy,
            "sx": sx,
        }

        lim: Tuple[float, float] = (x_min, x_max)

        return function, params, p0, lim, fitting_data
