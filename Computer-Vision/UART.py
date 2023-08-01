import time
import serial

class UART:
    def __init__(self):
        # Initialize Serial Port
        self.__serial_port = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        # Wait for Serial Port to Initialize
        while(not self.__serial_port.is_open):
            continue
    
    # Send Data to the Pi
    def send(self, num):
        try:
            self.__serial_port.write((str(num)).encode("ascii", "ignore"))
            return 0
        except:
            return -1
        
    # Close Connection
    def close(self):
        self.__serial_port.close()
