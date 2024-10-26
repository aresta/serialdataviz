import PyQt6.QtWidgets as Qtw
import pyqtgraph as pg
from PyQt6.QtCore import Qt
import serial
import serial.tools.list_ports

class Gui:
    def init_gui( self):
        self.COLORS = self.conf['COLORS']
        self.setWindowTitle('SerialDataViz')
        self.resize(1400, 800)
        central_widget = Qtw.QWidget( self)
        self.setCentralWidget( central_widget)
        main_layout = Qtw.QVBoxLayout( central_widget)
        self.x_range = self.conf['x_range']

        # top layout
        top_layout = Qtw.QHBoxLayout()
        self.start_button = Qtw.QPushButton( icon = self.style().standardIcon( Qtw.QStyle.StandardPixmap.SP_MediaPlay))
        self.stop_button = Qtw.QPushButton( icon = self.style().standardIcon( Qtw.QStyle.StandardPixmap.SP_MediaStop))
        self.stop_button.setEnabled(False)
        top_layout.addWidget( self.start_button)
        top_layout.addWidget( self.stop_button)

        self.autoscroll_chekbox = Qtw.QCheckBox("Autoscroll")
        self.autoscroll_chekbox.setCheckState( Qt.CheckState.Checked)
        top_layout.addWidget( self.autoscroll_chekbox)
        self.autoscroll_chekbox.setEnabled( False)
        
        self.legend_checkbox = Qtw.QCheckBox("Legend")
        self.legend_checkbox.setEnabled( False)
        top_layout.addWidget( self.legend_checkbox)

        top_layout.addStretch() # push elements to the sides

        self.settings_button = Qtw.QPushButton("Settings", icon = self.style().standardIcon( Qtw.QStyle.StandardPixmap.SP_BrowserReload))
        top_layout.addWidget( self.settings_button)
        
        self.port_dropdown = Qtw.QComboBox()
        ports = [ port.device for port in serial.tools.list_ports.comports()] #FIX: refresh ports: port monitor worker
        port_index = next((x for x in ports if 'usb' in x)) #FIX dirty debug trick
        self.port_dropdown.addItems( ports)
        top_layout.addWidget( Qtw.QLabel("Serial Ports"))
        top_layout.addWidget( self.port_dropdown)
        self.port_dropdown.setCurrentText(port_index)    #FIX  dirty debug trick

        self.baudrate_dropdown = Qtw.QComboBox()
        self.baudrate_dropdown.addItems( self.conf['bauds'])
        self.baudrate_dropdown.setCurrentText("9600")
        top_layout.addSpacing(35)
        top_layout.addWidget( Qtw.QLabel("Baud rate"))
        top_layout.addWidget( self.baudrate_dropdown)

        # plot
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#E0E0E0")

        self.legend = self.plot_widget.getPlotItem().addLegend(offset=(-30,30))
        self.legend.hide()
        self.legend.setLabelTextColor("#223")
        self.legend.setPen( pg.mkPen( color = "#CCC", width = 3))
        self.legend.setLabelTextSize('12pt')

        # plot_data_items
        self.plot_data_items = []

        # main layout    
        main_layout.addLayout( top_layout)
        main_layout.addWidget( self.plot_widget)