from dataclasses import dataclass
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QComboBox, QPushButton, QCheckBox

@dataclass
class Var:
    name: str = None
    vals: list[float] = None
    is_visible: bool = True

@dataclass
class Data:
    time: list[float] = None
    vars: list[Var] = None
    is_nameval_format: bool = False

# @dataclass
# class Gui:
#     plot_data_items: list[pg.PlotDataItem] = None
#     plot_widget: pg.PlotWidget = None
#     baudrate_dropdown: QComboBox = None
#     port_dropdown: QComboBox = None
#     start_button: QPushButton = None
#     stop_button: QPushButton = None
#     settings_button: QPushButton = None
#     autoscroll: QCheckBox = None
#     legend_checkbox: QCheckBox = None
#     x_range: float = None
#     legend: pg.LegendItem = None

COLORS: list = []

