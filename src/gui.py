from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QWidget, QPushButton, QStyle
from dataclasses import dataclass
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import serial
from random import randrange
import serial.tools.list_ports


@dataclass
class Gui:
    plot_item: pg.PlotItem = None
    baudrate_dropdown: QComboBox = None
    port_dropdown: QComboBox = None
    window: QMainWindow = None
    start_button: QPushButton = None
    stop_button: QPushButton = None

def init_app( conf):
    gui = Gui()
    gui.window = QMainWindow()
    gui.window.setWindowTitle('SerialDataViz')
    gui.window.resize(1400, 800)

    # top layout
    top_layout = QHBoxLayout()
    gui.start_button = QPushButton("Start")
    gui.stop_button = QPushButton("Stop")
    gui.stop_button.setEnabled(False)
    top_layout.addWidget( gui.start_button)
    top_layout.addWidget( gui.stop_button)
    top_layout.addStretch() # push elements to the sides
    port_label = QLabel("Serial Ports")
    gui.port_dropdown = QComboBox()
    ports = [ port.device for port in serial.tools.list_ports.comports()] 
    gui.port_dropdown.addItems( ports)
    top_layout.addWidget( port_label)
    top_layout.addWidget( gui.port_dropdown)
    baudrate_label = QLabel("Baud rate")
    gui.baudrate_dropdown = QComboBox()
    gui.baudrate_dropdown.addItems( conf['bauds'])
    gui.baudrate_dropdown.setCurrentText("9600")
    top_layout.addSpacing(35)
    top_layout.addWidget( baudrate_label)
    top_layout.addWidget( gui.baudrate_dropdown)

    # plot
    plot_widget = pg.PlotWidget()
    plot_widget.setBackground( (0xE0, 0xE0, 0xE0))
    gui.plot_item = plot_widget.plot( 
        [], [], 
        pen = pg.mkPen(color = ( 0xCC, 0x88, 0x88), width = 4)
        )

    # main layout
    central_widget = QWidget( gui.window)
    gui.window.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)
    main_layout.addLayout( top_layout)
    main_layout.addWidget( plot_widget)

    return gui

def update_plot( data, gui):
    gui.plot_item.setData( data.time, data.val)


