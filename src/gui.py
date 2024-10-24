from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QWidget, QPushButton, QStyle, QCheckBox
from dataclasses import dataclass
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import serial
from random import randrange
from src.datastructs import Gui, Data, COLORS
import serial.tools.list_ports



def init_app( conf) -> Gui:
    gui = Gui()
    gui.window = QMainWindow()
    gui.window.setWindowTitle('SerialDataViz')
    gui.window.resize(1400, 800)
    central_widget = QWidget( gui.window)
    gui.window.setCentralWidget( central_widget)
    main_layout = QVBoxLayout( central_widget)
    gui.x_range = conf['x_range']

    # top layout
    top_layout = QHBoxLayout()
    gui.start_button = QPushButton("Start")
    gui.stop_button = QPushButton("Stop")
    gui.stop_button.setEnabled(False)
    top_layout.addWidget( gui.start_button)
    top_layout.addWidget( gui.stop_button)
    gui.autoscroll = QCheckBox("Autoscroll")
    gui.autoscroll.setCheckState( Qt.CheckState.Checked)
    top_layout.addWidget( gui.autoscroll)
    top_layout.addStretch() # push elements to the sides
    gui.port_dropdown = QComboBox()
    ports = [ port.device for port in serial.tools.list_ports.comports()] #FIX: refresh ports
    gui.port_dropdown.addItems( ports)
    top_layout.addWidget( QLabel("Serial Ports"))
    top_layout.addWidget( gui.port_dropdown)
    gui.baudrate_dropdown = QComboBox()
    gui.baudrate_dropdown.addItems( conf['bauds'])
    gui.baudrate_dropdown.setCurrentText("9600")
    top_layout.addSpacing(35)
    top_layout.addWidget( QLabel("Baud rate"))
    top_layout.addWidget( gui.baudrate_dropdown)

    # plot
    gui.plot_widget = pg.PlotWidget()
    gui.plot_widget.setBackground("#E0E0E0")

    # gui.plot_widget.setLimits( xMin=0, maxXRange=5000,
    #                     yMin=2000, yMax=4000, maxYRange=1000)

    # main layout    
    main_layout.addLayout( top_layout)
    main_layout.addWidget( gui.plot_widget)
    return gui

def update_plot( data:Data, gui:Gui):
    if not gui.plot_data_items:
        gui.plot_data_items = []
        for i in range( data.vars_num):    # reverse to paint 1st var on top
            data_item = pg.PlotDataItem( pen = pg.mkPen( color = COLORS[i], width = 2))
            gui.plot_widget.addItem( data_item)
            gui.plot_data_items.append( data_item)
            # gui.plot_item = gui.plot_widget.plot( 
            #     pen = pg.mkPen( color = "#CC8888", width = 4))
    else:
        i = 0
        for data_item in gui.plot_data_items:
            data_item.setData( data.vars[i])
            i += 1
    if gui.autoscroll.isChecked():
        if len( data.time) > gui.x_range:
            gui.plot_widget.setXRange( data.time[-1] - gui.x_range, data.time[-1])
        gui.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=False, y=True) #FIX move to event
        
    else:
        gui.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=True, y=True)
        gui.x_range = gui.plot_widget.viewRect().width() #FIX move to event


