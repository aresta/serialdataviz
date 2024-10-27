from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import os
import sys
from src.window import MainWindow

app = QApplication([])

# set app icon
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'img/signal.png')
app.setWindowIcon( QIcon(path))

# init gui & data
window = MainWindow()
app.aboutToQuit.connect( window.cleanup)
app.exec()

