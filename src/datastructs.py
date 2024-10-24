from dataclasses import dataclass
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QComboBox, QPushButton, QCheckBox

@dataclass
class Data:
    time: list = None
    vars_num: int = 0
    vars: list = None

@dataclass
class Gui:
    plot_data_items: list = None
    plot_widget: pg.PlotWidget = None
    baudrate_dropdown: QComboBox = None
    port_dropdown: QComboBox = None
    window: QMainWindow = None
    start_button: QPushButton = None
    stop_button: QPushButton = None
    autoscroll: QCheckBox = None
    x_range = None

COLORS = ['#F8766D','#00B6EB','#53B400','#C49A00','#A58AFF','#00C094','#FB61D7']

