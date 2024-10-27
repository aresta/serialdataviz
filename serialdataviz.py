from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import tomllib
import os
import sys
from src.window import MainWindow

conf = tomllib.load( open('serialdataviz.conf', mode='rb'))
app = QApplication([])

# set app icon
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'img/signal.png')
app.setWindowIcon( QIcon(path))

# init gui & data
window = MainWindow( conf)
app.exec()

