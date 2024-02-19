import serial, string

class ReceiveUART():
    def __init__(self, port):
        self.__connection = serial.Serial(port, 9600, 8, 'N', 1, timeout=1)
        self.__transceiver = -1
        
        while (not self.__connection.isOpen()):
            print("connecting")

    def __del__(self):
        self.__connection.close()

    # Run this in a thread
    def readSerial(self):
        while True:
            self.__transceiver = int(self.__connection.read(1).decode("ascii", "ignore"))

    def getTransceiver(self):
        return self.__transceiver