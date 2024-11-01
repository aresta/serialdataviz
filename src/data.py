from dataclasses import dataclass
from enum import Enum, auto


class Plot_Type( Enum):
    TIME_SERIES = auto()
    XY          = auto()
    SCATTER     = auto()
    BARS        = auto()
    HISTOGRAM   = auto()

class Data_Format( Enum):
    PLAIN       = auto()
    VAR_NAMES   = auto()

@dataclass
class Var:
    name: str = None
    vals: list[float | tuple[ float, float]] = None
    is_visible: bool = True

@dataclass
class Data:
    time: list[float] = None
    vars: list[Var] = None
    plot_type: Plot_Type = Plot_Type.TIME_SERIES
    data_format: Data_Format = Data_Format.PLAIN


COLORS: list = []

