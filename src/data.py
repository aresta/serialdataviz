from dataclasses import dataclass
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

COLORS: list = []

