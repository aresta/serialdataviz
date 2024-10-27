import PyQt6.QtWidgets as Qtw
import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
import serial
import serial.tools.list_ports
from src.linearRegionItemFix import LinearRegionItemFix

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
               
        top_layout.addStretch() # push elements to the sides

        self.settings_button = Qtw.QPushButton("Settings", icon = self.style().standardIcon( Qtw.QStyle.StandardPixmap.SP_BrowserReload))
        top_layout.addWidget( self.settings_button)
        
        # port & bauds
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

        # legend
        self.legend = self.plot_widget.getPlotItem().addLegend(offset=(-30,30))
        self.legend.hide()
        self.legend.setLabelTextColor("#223")
        self.legend.setPen( pg.mkPen( color = "#CCC", width = 3))
        self.legend.setLabelTextSize('12pt')

        # plot_data_items
        self.plot_data_items:list[pg.PlotDataItem] = []

        # main layout    
        main_layout.addLayout( top_layout)
        main_layout.addWidget( self.plot_widget)


    # cursors
    def create_cursors( self):
        cursor_pen = QPen( pg.mkColor("#EBB"))
        cursor_pen.setStyle( Qt.PenStyle.DotLine)
        cursor_pen.setWidth( 4)
        cursor_pen.setCosmetic( True)
        cursor_penhover = QPen( cursor_pen)
        cursor_penhover.setColor( pg.mkColor("#E88"))
        self.cursors_h = LinearRegionItemFix(
            orientation = 'horizontal',
            swapMode = 'push',
            pen = cursor_pen,
            hoverPen = cursor_penhover,
            brush = pg.mkBrush( pg.mkColor("#CCCCFF20")), 
            hoverBrush = pg.mkBrush( pg.mkColor("#CCCCFF44")))
        self.cursors_h.setZValue(-10)
        self.cursors_v = LinearRegionItemFix(
            swapMode = 'push',
            pen = cursor_pen,
            hoverPen = cursor_penhover,
            brush = pg.mkBrush( pg.mkColor("#CCCCFF20")), 
            hoverBrush = pg.mkBrush( pg.mkColor("#CCCCFF44")))
        self.cursors_v.setZValue(-10)

        # cursor labels
        pg.InfLineLabel( 
            self.cursors_v.lines[0],
            text = 'x1={value:0.2f}', 
            position=0.9, color="#C55",
            movable=True)
        pg.InfLineLabel( 
            self.cursors_v.lines[1],
            text = 'x2={value:0.2f}', 
            position=0.87, color="#C55",
            movable=True)
        pg.InfLineLabel( 
            self.cursors_h.lines[1],
            text = 'x1={value:0.2f}', 
            position=0.06, color="#C55",
            movable=True)
        pg.InfLineLabel( 
            self.cursors_h.lines[0],
            text = 'x2={value:0.2f}', 
            position=0.05, color="#C55",
            movable=True)
        self.plot_widget.addItem( self.cursors_h)
        self.plot_widget.addItem( self.cursors_v)
        self.cursors_h.hide()
        self.cursors_v.hide()

        self.cursors_h_deltalabel = pg.TextItem("", color=pg.mkColor("#C55"))
        self.cursors_v_deltalabel = pg.TextItem("", color=pg.mkColor("#C55"), anchor=( 0.5,0))
        self.plot_widget.addItem( self.cursors_h_deltalabel)
        self.plot_widget.addItem( self.cursors_v_deltalabel)
        self.cursors_h_deltalabel.hide()
        self.cursors_v_deltalabel.hide()

        self.cursors_v.sigRegionChanged.connect( self.cursors_deltalabels_update)
        self.cursors_h.sigRegionChanged.connect( self.cursors_deltalabels_update)
        self.plot_widget.sigRangeChanged.connect( self.plot_range_changed)

    def cursors_h_set_region( self):
        self.cursors_h.show() # should be visible before setRegion
        self.cursors_h.setRegion([ 
            self.plot_widget.visibleRange().center().y() - self.plot_widget.visibleRange().height()/8,
            self.plot_widget.visibleRange().center().y() + self.plot_widget.visibleRange().height()/8 ])

    def cursors_v_set_region( self):
        self.cursors_v.show()
        self.cursors_v.setRegion([ 
            self.plot_widget.visibleRange().center().x() - self.plot_widget.visibleRange().width()/8,
            self.plot_widget.visibleRange().center().x() + self.plot_widget.visibleRange().width()/8 ])
        
    def plot_range_changed( self):
        self.cursors_deltalabels_update()
    
    def cursors_deltalabels_update( self):
        self.cursors_h_deltalabel.setText( "△: {:.2f}".format( self.cursors_h.boundingRect().height()))
        self.cursors_v_deltalabel.setText( "△: {:.2f}".format( self.cursors_v.boundingRect().width()))
        if self.cursors_h_checkbox.isChecked():
            self.cursors_h_deltalabel.setPos( 
                self.plot_widget.visibleRange().left(),
                self.cursors_h.boundingRect().center().y())
        if self.cursors_v_checkbox.isChecked():
            self.cursors_v_deltalabel.setPos( 
                self.cursors_v.boundingRect().center().x(),
                self.plot_widget.visibleRange().bottom()-5)


    # settings
    def settings_button_clicked( self):
        dlg = Qtw.QDialog()
        def settings_save():
            if not self.data.vars: return
            for var, checkbox in zip( self.data.vars, checkboxes):
                var.is_visible = checkbox.isChecked()
            dlg.accept()

        dlg.setWindowTitle("Settings")
        main_layout = Qtw.QVBoxLayout()
        QBtn = Qtw.QDialogButtonBox.StandardButton.Save | Qtw.QDialogButtonBox.StandardButton.Cancel
        buttonBox = Qtw.QDialogButtonBox( QBtn)
        buttonBox.accepted.connect(settings_save)
        buttonBox.rejected.connect(dlg.reject)
        checkboxes:list[Qtw.QCheckBox] = []
        vars_layout = Qtw.QVBoxLayout()
        for var in self.data.vars or []:
            checkbox = Qtw.QCheckBox( var.name)
            checkbox.setChecked( var.is_visible)
            vars_layout.addWidget( checkbox)
            checkboxes.append( checkbox)
        vars_group = Qtw.QGroupBox("Variables")
        vars_group.setLayout( vars_layout)
        main_layout.addWidget( vars_group)
        main_layout.addWidget( buttonBox)
        dlg.setLayout( main_layout)
        dlg.exec()