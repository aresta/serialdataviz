from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import tomllib
import os
import sys
from src.gui import init_app, settings_button_clicked
from src.data import COLORS
from src.serial_data_worker import init_worker
from src.data_proc import Data, process_data


conf = tomllib.load( open('serialdataviz.conf', mode='rb'))
app = QApplication([])
COLORS += conf['COLORS']

# set app icon
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'img/signal.png')
app.setWindowIcon( QIcon(path))

# init app gui
window, gui = init_app( conf)

# data
data = Data()

# thread
worker = init_worker()
worker.data_received.connect( lambda line: process_data( line, data, gui, conf))
gui.start_button.clicked.connect( lambda: worker.worker_start( gui))
gui.stop_button.clicked.connect( lambda: worker.worker_stop( gui))

gui.legend_checkbox.clicked.connect( 
    lambda: gui.legend.show() if gui.legend_checkbox.isChecked() else gui.legend.hide())
gui.autoscroll.clicked.connect( 
    lambda: gui.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=(not gui.autoscroll.isChecked()), y=True))

gui.settings_button.clicked.connect( lambda: settings_button_clicked( gui, data))

window.show()
app.exec()

