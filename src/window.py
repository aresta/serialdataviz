import PyQt6.QtWidgets as Qtw
from PyQt6.QtCore import Qt, QThread
import pyqtgraph as pg
from src.data import Data, Var
from src.gui import Gui
from src.data_proc import DataProc
from src.serial_data_worker import Serial_data_worker


class MainWindow( Qtw.QMainWindow, DataProc, Gui):
    def __init__(self, conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conf = conf
        self.data = Data()
        self.init_gui()
        self.init_workers()
        self.show()


    def init_workers( self):
        self.serial_worker = Serial_data_worker()
        self.worker_thread = QThread()
        self.serial_worker.moveToThread( self.worker_thread)

        self.serial_worker.data_received.connect( self.process_data)
        self.worker_thread.started.connect(self.serial_worker.work)
        self.worker_thread.finished.connect(self.serial_worker.finish)
        self.start_button.clicked.connect( self.worker_start)
        self.stop_button.clicked.connect( self.worker_stop)
        self.legend_checkbox.clicked.connect( 
            lambda: self.legend.show() if self.legend_checkbox.isChecked() else self.legend.hide())
        self.autoscroll_chekbox.clicked.connect( 
            lambda: self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=(not self.autoscroll_chekbox.isChecked()), y=True))
        self.settings_button.clicked.connect( self.settings_button_clicked)


    def worker_start( self):
        self.stop_button.setEnabled( True)
        self.start_button.setEnabled( False)
        self.port_dropdown.setEnabled( False)
        self.baudrate_dropdown.setEnabled( False)
        self.serial_worker.baudrate = int( self.baudrate_dropdown.currentText())
        self.serial_worker.serial_port = self.port_dropdown.currentText()
        self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=False, y=True)
        self.worker_thread.start()


    def worker_stop( self):
        self.serial_worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.stop_button.setEnabled( False)
        self.start_button.setEnabled( True)
        self.port_dropdown.setEnabled( True)
        self.baudrate_dropdown.setEnabled( True)
        self.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=True, y=True)
        

    def update_plot( self):
        if not self.plot_data_items:
            for var, color in zip( self.data.vars, self.COLORS):
                data_item = pg.PlotDataItem( pen = pg.mkPen( color = color, width = 2))
                self.plot_widget.addItem( data_item)
                self.plot_data_items.append( data_item)
                self.legend.addItem( item = data_item, name = var.name)
            self.legend_checkbox.setEnabled( True)
                
            if len( self.data.vars) > 1:
                self.legend_checkbox.setCheckState( Qt.CheckState.Checked)
                self.legend.show()
            else:
                self.legend_checkbox.setCheckState( Qt.CheckState.Unchecked)
                self.legend.hide()
            self.autoscroll_chekbox.setEnabled( True)
        else:
            for data_item, var in zip( self.plot_data_items, self.data.vars):
                if var.is_visible:
                    data_item.setData( self.data.time, var.vals)
        if self.autoscroll_chekbox.isChecked():
            if len( self.data.time) > self.x_range: #FIX data range vs pixels
                self.plot_widget.setXRange( self.data.time[-1] - self.x_range, self.data.time[-1])
        
        else:
            self.x_range = self.plot_widget.viewRect().width() #FIX move to event


    def settings_button_clicked( self):
        dlg = Qtw.QDialog()
        def settings_save():
            if not self.data.vars: return
            for var, checkbox in zip( self.data.vars, checkboxes):
                var.is_visible = checkbox.isChecked()
            dlg.accept()

        dlg.setWindowTitle("Settings")
        layout = Qtw.QVBoxLayout()
        QBtn = Qtw.QDialogButtonBox.StandardButton.Save | Qtw.QDialogButtonBox.StandardButton.Cancel
        buttonBox = Qtw.QDialogButtonBox( QBtn)
        buttonBox.accepted.connect(settings_save)
        buttonBox.rejected.connect(dlg.reject)
        checkboxes:list[Qtw.QCheckBox] = []
        for var in self.data.vars or []:
            checkbox = Qtw.QCheckBox( var.name)
            checkbox.setChecked( var.is_visible)
            layout.addWidget( checkbox)
            checkboxes.append( checkbox)
        layout.addWidget( buttonBox)
        dlg.setLayout( layout)
        dlg.exec()


