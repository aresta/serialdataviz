from PyQt6.QtWidgets import QMainWindow,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QWidget,QPushButton,QCheckBox,QDialog,QDialogButtonBox,QStyle
from dataclasses import dataclass
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import serial
from src.data import COLORS, Gui, Data, Var
import serial.tools.list_ports


def init_app( conf) -> tuple[ QMainWindow, Gui]:
    gui = Gui()
    window = QMainWindow()
    window.setWindowTitle('SerialDataViz')
    window.resize(1400, 800)
    central_widget = QWidget( window)
    window.setCentralWidget( central_widget)
    main_layout = QVBoxLayout( central_widget)
    gui.x_range = conf['x_range']

    # top layout
    top_layout = QHBoxLayout()
    gui.start_button = QPushButton( icon = window.style().standardIcon( QStyle.StandardPixmap.SP_MediaPlay))
    gui.stop_button = QPushButton( icon = window.style().standardIcon( QStyle.StandardPixmap.SP_MediaStop))
    gui.stop_button.setEnabled(False)
    top_layout.addWidget( gui.start_button)
    top_layout.addWidget( gui.stop_button)

    gui.autoscroll = QCheckBox("Autoscroll")
    gui.autoscroll.setCheckState( Qt.CheckState.Checked)
    top_layout.addWidget( gui.autoscroll)
    gui.autoscroll.setEnabled( False)
    
    gui.legend_checkbox = QCheckBox("Legend")
    gui.legend_checkbox.setEnabled( False)
    top_layout.addWidget( gui.legend_checkbox)

    top_layout.addStretch() # push elements to the sides

    gui.settings_button = QPushButton("Settings", icon = window.style().standardIcon( QStyle.StandardPixmap.SP_BrowserReload))
    top_layout.addWidget( gui.settings_button)
    
    gui.port_dropdown = QComboBox()
    ports = [ port.device for port in serial.tools.list_ports.comports()] #FIX: refresh ports: port monitor worker
    port_index = next((x for x in ports if 'usb' in x)) #FIX dirty debug trick
    gui.port_dropdown.addItems( ports)
    top_layout.addWidget( QLabel("Serial Ports"))
    top_layout.addWidget( gui.port_dropdown)
    gui.port_dropdown.setCurrentText(port_index)    #FIX

    gui.baudrate_dropdown = QComboBox()
    gui.baudrate_dropdown.addItems( conf['bauds'])
    gui.baudrate_dropdown.setCurrentText("9600")
    top_layout.addSpacing(35)
    top_layout.addWidget( QLabel("Baud rate"))
    top_layout.addWidget( gui.baudrate_dropdown)

    # plot
    gui.plot_widget = pg.PlotWidget()
    gui.plot_widget.setBackground("#E0E0E0")

    # main layout    
    main_layout.addLayout( top_layout)
    main_layout.addWidget( gui.plot_widget)
    return window, gui

def update_plot( data:Data, gui:Gui):
    if not gui.plot_data_items:
        gui.plot_data_items = []
        gui.legend = gui.plot_widget.getPlotItem().addLegend(offset=(-30,30))
        gui.legend.setLabelTextColor("#223")
        gui.legend.setPen( pg.mkPen( color = "#CCC", width = 3))
        gui.legend.setLabelTextSize('12pt')
        for var, color in zip( data.vars, COLORS):
            data_item = pg.PlotDataItem( pen = pg.mkPen( color = color, width = 2))
            gui.plot_widget.addItem( data_item)
            gui.plot_data_items.append( data_item)
            gui.legend.addItem( item = data_item, name = var.name)
            
        gui.legend_checkbox.setEnabled( True)
        if len( data.vars) > 1:
            gui.legend_checkbox.setCheckState( Qt.CheckState.Checked)
            gui.legend.show()
        else:
            gui.legend_checkbox.setCheckState( Qt.CheckState.Unchecked)
            gui.legend.hide()
        gui.autoscroll.setEnabled( True)
    else:
        for data_item, var in zip( gui.plot_data_items, data.vars):
            if var.is_visible:
                data_item.setData( var.vals)
    if gui.autoscroll.isChecked():
        if len( data.time) > gui.x_range: #FIX data range vs pixels
            gui.plot_widget.setXRange( data.time[-1] - gui.x_range, data.time[-1])
    else:
        gui.x_range = gui.plot_widget.viewRect().width() #FIX move to event


def settings_button_clicked( gui:Gui, data:Data):
    dlg = QDialog()
    def settings_save():
        if not data.vars: return
        for var, checkbox in zip( data.vars, checkboxes):
            var.is_visible = checkbox.isChecked()
        dlg.accept()

    dlg.setWindowTitle("Settings")
    layout = QVBoxLayout()
    QBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
    buttonBox = QDialogButtonBox( QBtn)
    buttonBox.accepted.connect(settings_save)
    buttonBox.rejected.connect(dlg.reject)
    checkboxes:list[QCheckBox] = []
    for var in data.vars or []:
        checkbox = QCheckBox( var.name)
        checkbox.setChecked( var.is_visible)
        layout.addWidget( checkbox)
        checkboxes.append( checkbox)
    layout.addWidget( buttonBox)
    dlg.setLayout( layout)
    dlg.exec()


