import pathlib
import sys


this_directory = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(this_directory))

from error_style import *
from rounding import *
from statistics import *
from num_with_error import NumWithError

