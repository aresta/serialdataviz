import serial
from PyQt6.QtCore import pyqtSignal, QObject

class Serial_data_worker( QObject):
    data_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.baudrate = None
        self.serial = None
        self.running = False

    def finish(self):
        self.running = False

    def work(self):
        try:
            self.serial = serial.Serial(self.serial_port, self.baudrate, timeout=2)
            self.running = True
            self.serial.reset_input_buffer()

            if self.serial.in_waiting > 0: # discard first line, maybe incomplete
                str = self.serial.read_until( size=128)

            while self.running:
                if self.serial.in_waiting > 0:
                    str = self.serial.read_until( size=128)
                    if not str: continue
                    try:
                        str = str.strip().decode('utf-8')
                    except Exception as e: 
                        print(e, str)
                        continue
                    self.data_received.emit( str)
        except serial.SerialException as e: print(e)
        except serial.SerialTimeoutException as e: print(e)
        except Exception as e: print(e)
        finally:
            if self.serial and self.serial.is_open: 
                self.serial.reset_input_buffer()
                self.serial.close()




