# Virtual TCP Socket

class vSocket:
    def __init__(self, vg):
        self.__vg = vg

    def sendall(self, packet):
        self.__vg.virtual_serial_port.writeFromSocket(packet)
    
    def recv(self):
        return self.__vg.socketQueues[int(self.__vg.ip.split(".")[-1])-10].get()

    def close(self):
        pass