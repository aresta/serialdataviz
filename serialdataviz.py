from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import tomllib
import os
import sys
from src.gui import init_app
from src.serial_data_worker import init_worker
from src.data import Data, process_data


conf = tomllib.load( open('serialdataviz.conf', mode='rb'))
app = QApplication([])

# set app icon
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'img/signal.png')
app.setWindowIcon( QIcon(path))

# init app gui
gui = init_app( conf)

# data
data = Data()

# thread
worker = init_worker()
worker.data_received.connect( lambda line: process_data( line, data, gui, conf))
gui.start_button.clicked.connect( lambda: worker.worker_start( gui))
gui.stop_button.clicked.connect( lambda: worker.worker_stop( gui))

gui.window.show()
app.exec()

