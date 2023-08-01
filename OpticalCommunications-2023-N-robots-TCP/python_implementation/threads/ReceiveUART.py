import serial, string

class ReceiveUART():
    def __init__(self, port):
        self.__connection = serial.Serial(port, 9600, 8, 'N', 1, timeout=1)
        self.__transceiver = -1

    def __del__(self):
        self.__connection.close()

    # Run this in a thread
    def readSerial(self):
        output = " "
        while output != "":
            self.__transceiver = int(self.__connection.readline().decode("ascii", "ignore"))

    def getTransceiver(self):
        return self.__transceiver