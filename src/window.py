import PyQt6.QtWidgets as Qtw
from PyQt6.QtCore import QThread, QTimer
import pyqtgraph as pg
from src import Gui, Cursors, Settings, Data, CONF
from src.dataproc import process_data
from src.data import Plot_Type
from src.serial_data_worker import Serial_data_worker


class MainWindow( Qtw.QMainWindow, Gui, Cursors, Settings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CONF = CONF
        self.data = Data()
        self.timer = QTimer( self)
        self.init_gui()
        self.init_workers()
        self.show()

    def cleanup( self):
        self.timer.stop()
        self.serial_worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        

    def data_received( self, line:str):
        process_data( self.data, line)
        while len( self.data.vars[0].y) > CONF['buffer_size']: 
            for var in self.data.vars: del var.y[0]
            if self.data.plot_type == Plot_Type.TIME_SERIES:
                del self.data.time[0]
            elif self.data.plot_type in (Plot_Type.XY, Plot_Type.SCATTER):
                for var in self.data.vars: del var.x[0]


    def init_workers( self):
        self.serial_worker = Serial_data_worker()
        self.worker_thread = QThread()
        self.serial_worker.moveToThread( self.worker_thread)

        self.serial_worker.data_received.connect( self.data_received)
        self.worker_thread.started.connect(self.serial_worker.work)
        self.worker_thread.finished.connect(self.serial_worker.finish)
        self.button_start.clicked.connect( self.worker_start)
        self.button_pause.clicked.connect( self.worker_stop)
        self.button_reset.clicked.connect( self.reset)
        self.legend_checkbox.clicked.connect( 
            lambda: self.legend.show() if self.legend_checkbox.isChecked() else self.legend.hide())
        self.autoscroll_chekbox.clicked.connect( self.autoscroll_chekbox_clicked)
        self.button_settings.clicked.connect( self.create_settings_dialog)
        self.cursors_h_checkbox.clicked.connect( self.add_cursors_h) 
        self.cursors_v_checkbox.clicked.connect( self.add_cursors_v) 

    def autoscroll_chekbox_clicked( self):
        if self.autoscroll_chekbox.isChecked():
            if self.data.plot_type == Plot_Type.TIME_SERIES:
                self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=False, y=True)
            self.cursors_h_checkbox.setChecked( False)
            self.cursors_v_checkbox.setChecked( False)
            self.cursors_h_checkbox.setEnabled( False)
            self.cursors_v_checkbox.setEnabled( False)
            if hasattr( self, 'cursors_h'):
                self.cursors_h.hide()
                self.cursors_h_deltalabel.hide()
            if hasattr( self, 'cursors_v'):
                self.cursors_v.hide()
                self.cursors_v_deltalabel.hide()
        else:
            self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=True, y=True)
            self.cursors_h_checkbox.setEnabled( True)
            self.cursors_v_checkbox.setEnabled( True)
            self.plot_widget.setXRange( 
                self.plot_widget.viewRect().left()-0.01,
                self.plot_widget.viewRect().right()+0.01)
            self.plot_widget.setYRange(         # workaround to avoid scale runaway
                self.plot_widget.viewRect().top()-0.01,
                self.plot_widget.viewRect().bottom()+0.01)
            
            

    def add_cursors_h( self):
        if not hasattr( self, 'cursors_h'):
            self.create_cursors()
        if self.cursors_h_checkbox.isChecked():
            self.cursors_h_set_region()
            self.cursors_h_deltalabel.show()
            self.cursors_deltalabels_update()
        else:
            self.cursors_h.hide()
            self.cursors_h_deltalabel.hide()

    def add_cursors_v( self):
        if not hasattr( self, 'cursors_v'):
            self.create_cursors()
        if self.cursors_v_checkbox.isChecked():
            self.cursors_v_set_region()
            self.cursors_v_deltalabel.show()
            self.cursors_deltalabels_update()
        else:
            self.cursors_v.hide()
            self.cursors_v_deltalabel.hide()


    def worker_start( self):
        self.button_pause.setEnabled( True)
        self.button_reset.setEnabled( False)
        self.button_start.setEnabled( False)
        self.port_dropdown.setEnabled( False)
        self.baudrate_dropdown.setEnabled( False)
        self.cursors_h_checkbox.setChecked( False)
        self.cursors_h_checkbox.setEnabled( False)
        self.cursors_v_checkbox.setChecked( False)
        self.cursors_v_checkbox.setEnabled( False)
        if hasattr( self, 'cursors_h'): 
            self.cursors_h.hide()
            self.cursors_h_deltalabel.hide()
        if hasattr( self, 'cursors_v'): 
            self.cursors_v.hide()
            self.cursors_v_deltalabel.hide()
        self.serial_worker.baudrate = int( self.baudrate_dropdown.currentText())
        self.serial_worker.serial_port = self.port_dropdown.currentText()
        if self.data.plot_type == Plot_Type.TIME_SERIES:
            self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=False, y=True)
        if self.data.vars:
            self.x_range = self.plot_widget.viewRect().width()
        self.worker_thread.start()

        # self.timer.timeout.connect( self.update_plot2)
        self.timer.timeout.connect( self.update_plot)
        self.timer.start(25)


    def worker_stop( self):
        self.serial_worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.button_pause.setEnabled( False)
        self.button_reset.setEnabled( True)
        self.button_start.setEnabled( True)
        self.port_dropdown.setEnabled( True)
        self.baudrate_dropdown.setEnabled( True)
        self.cursors_h_checkbox.setEnabled( True)
        self.cursors_v_checkbox.setEnabled( True)
        self.cursors_h_checkbox.setChecked( False)
        self.cursors_v_checkbox.setChecked( False)
        if hasattr( self, 'cursors_h'): 
            self.cursors_h.hide()
            self.cursors_h_deltalabel.hide()
        if hasattr( self, 'cursors_v'): 
            self.cursors_v.hide()
            self.cursors_v_deltalabel.hide()
        self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=True, y=True)
        self.timer.stop()
        self.plot_widget.setXRange( 
            self.plot_widget.viewRect().left()-0.01,
            self.plot_widget.viewRect().right()+0.01)
        self.plot_widget.setYRange(         # workaround to avoid scale runaway
            self.plot_widget.viewRect().top()-0.01,
            self.plot_widget.viewRect().bottom()+0.01)
        

    def reset( self):
        for data_item in self.plot_data_items:
            self.plot_widget.removeItem( data_item)
        self.plot_data_items = []
        self.data.vars = []
        self.button_reset.setEnabled( False)
        self.cursors_h_checkbox.setChecked( False)
        self.cursors_h_checkbox.setEnabled( False)
        self.cursors_v_checkbox.setChecked( False)
        self.cursors_v_checkbox.setEnabled( False)
        self.legend_checkbox.setEnabled( False)
        self.legend_checkbox.setChecked( False)
        self.legend.clear()
        self.legend.hide()
        self.autoscroll_chekbox.setEnabled( False)
        self.autoscroll_chekbox.setChecked( True)
        if hasattr( self, 'cursors_h'): 
            self.cursors_h.hide()
            self.cursors_h_deltalabel.hide()
        if hasattr( self, 'cursors_v'): 
            self.cursors_v.hide()
            self.cursors_v_deltalabel.hide()
        self.plot_widget.setXRange( 0, 1)
        self.plot_widget.setYRange( 0, 1)
        self.plot_widget.getPlotItem().getViewBox().enableAutoRange()
        
            

    def update_plot2( self):    #FIX
        try:
            self.update_plot()
        except Exception as e:
            print("Exception: ", e)
            print("Cleaning up...")
            self.worker_stop()
            lengths = [ len(var.y) for var in self.data.vars]
            lengths.append( len(self.data.time))
            minl = min( lengths)
            for var in self.data.vars:
                while len(var.y) >= minl:
                    var.y.pop()
            while len(self.data.time) >= minl:
                    self.data.time.pop()
            self.worker_start()
            print("Done\n")

    def update_plot( self):
        if not self.data.vars: return # no data yet
        if not self.plot_data_items:
            for var, color in zip( self.data.vars, self.COLORS):
                var.color = color
                data_item = pg.PlotDataItem( pen = pg.mkPen( color = color, width = 2))
                self.plot_widget.addItem( data_item)
                self.plot_data_items.append( data_item)
                self.legend.addItem( item = data_item, name = var.name)
            self.legend_checkbox.setEnabled( True)
                
            if len( self.data.vars) > 1:
                self.legend_checkbox.setChecked( True)
                self.legend.show()
            else:
                self.legend_checkbox.setChecked( False)
                self.legend.hide()
            self.autoscroll_chekbox.setEnabled( True)
        else:
            for data_item, var in zip( self.plot_data_items, self.data.vars):
                if var.is_visible:
                    if self.data.plot_type == Plot_Type.TIME_SERIES:
                        data_item.setData( self.data.time, var.y)
                    elif self.data.plot_type == Plot_Type.XY:
                        data_item.setData( var.x, var.y)
                    elif self.data.plot_type == Plot_Type.SCATTER:
                        data_item.setData( var.x, var.y, 
                            symbol='o', symbolPen=var.color, symbolBrush=var.color, symbolSize=5, pen=None)
        if self.data.plot_type == Plot_Type.TIME_SERIES: 
            if self.autoscroll_chekbox.isChecked():
                if len( self.data.time) > self.x_range: #FIX data range vs pixels
                    self.plot_widget.setXRange( self.data.time[-5] - self.x_range, self.data.time[-5])
            else:
                self.x_range = self.plot_widget.viewRect().width() #FIX move to event

            


        


