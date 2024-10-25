import serial
from PyQt6 import QtCore, QtWidgets
from src.gui import Gui

class Serial_data_worker(QtCore.QThread):
    data_received = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.baudrate = None
        self.serial = None
        self.running = False

    def run(self):
        try:
            self.serial = serial.Serial(self.serial_port, self.baudrate, timeout=2)
            self.running = True
            while self.running:
                if self.serial.in_waiting > 0:
                    str = self.serial.read_until( size=128).strip().decode('utf-8')
                    if not str: continue
                    self.data_received.emit( str)
        except serial.SerialException as e: print(e)
        except serial.SerialTimeoutException as e: print(e)
        except IOError as e: print(e)
        except Exception as e: print(e)
        finally:
            self.worker_stop

    def worker_start( self, gui:Gui):
        gui.stop_button.setEnabled( True)
        gui.start_button.setEnabled( False)
        gui.port_dropdown.setEnabled( False)
        gui.baudrate_dropdown.setEnabled( False)
        self.baudrate = int( gui.baudrate_dropdown.currentText())
        self.serial_port = gui.port_dropdown.currentText()
        gui.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=False, y=True)
        self.start()

    def worker_stop( self, gui:Gui):
        self.running = False
        if self.isRunning():
            self.wait()
        if self.serial and self.serial.is_open:
            self.serial.close()
        gui.stop_button.setEnabled( False)
        gui.start_button.setEnabled( True)
        gui.port_dropdown.setEnabled( True)
        gui.baudrate_dropdown.setEnabled( True)
        gui.plot_widget.getPlotItem().getViewBox().setMouseEnabled( x=True, y=True)


def init_worker() -> Serial_data_worker:
    worker = Serial_data_worker()
    return worker

