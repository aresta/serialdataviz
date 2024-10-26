import PyQt6.QtWidgets as Qtw
import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
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
        self.autoscroll_chekbox.setChecked( True)
        top_layout.addWidget( self.autoscroll_chekbox)
        self.autoscroll_chekbox.setEnabled( False)
        
        self.legend_checkbox = Qtw.QCheckBox("Legend")
        self.legend_checkbox.setEnabled( False)
        top_layout.addWidget( self.legend_checkbox)
        
        # cursors
        self.cursors_h_checkbox = Qtw.QCheckBox("Cursors H")
        self.cursors_v_checkbox = Qtw.QCheckBox("Cursors V")
        self.cursors_h_checkbox.setChecked( False)
        self.cursors_h_checkbox.setEnabled( False)
        self.cursors_v_checkbox.setChecked( False)
        self.cursors_v_checkbox.setEnabled( False)
        top_layout.addWidget( self.cursors_h_checkbox)
        top_layout.addWidget( self.cursors_v_checkbox)
        cursor_pen = QPen( pg.mkColor("#EBB"))
        cursor_pen.setStyle( Qt.PenStyle.DotLine)
        cursor_pen.setWidth( 4)
        cursor_pen.setCosmetic( True)
        cursor_penhover = QPen( cursor_pen)
        cursor_penhover.setColor( pg.mkColor("#E88"))
        self.cursors_h = pg.LinearRegionItem(
            orientation = 'horizontal',
            pen = cursor_pen,
            hoverPen = cursor_penhover,
            brush = pg.mkBrush( pg.mkColor("#CCCCFF22")), 
            hoverBrush = pg.mkBrush( pg.mkColor("#CCCCFF55")))
        self.cursors_h.setZValue(-10)
        self.cursors_v = pg.LinearRegionItem(
            pen = cursor_pen,
            hoverPen = cursor_penhover,
            brush = pg.mkBrush( pg.mkColor("#CCCCFF22")), 
            hoverBrush = pg.mkBrush( pg.mkColor("#CCCCFF55")))
        self.cursors_v.setZValue(-10)
        pg.InfLineLabel( 
            self.cursors_v.lines[0],
            text = 'x1={value:0.2f}', 
            position=0.9, color="#C55",
            movable=True)
        self.lv2 = pg.InfLineLabel( 
            self.cursors_v.lines[1],
            text = 'x2={value:0.2f}', 
            position=0.9, color="#C55",
            movable=True)
        pg.InfLineLabel( 
            self.cursors_h.lines[0],
            text = 'x1={value:0.2f}', 
            position=0.9, color="#C55",
            movable=True)
        pg.InfLineLabel( 
            self.cursors_h.lines[1],
            text = 'x2={value:0.2f}', 
            position=0.9, color="#C55",
            movable=True)
        self.cursors_h.hide()
        self.cursors_v.hide()
        
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

        self.plot_widget.addItem( self.cursors_h)
        self.plot_widget.addItem( self.cursors_v)

        # main layout    
        main_layout.addLayout( top_layout)
        main_layout.addWidget( self.plot_widget)