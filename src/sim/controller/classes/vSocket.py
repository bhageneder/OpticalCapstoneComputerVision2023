# Virtual TCP Socket

class vSocket:
    def __init__(self, ip, vg):
        self.__vg = vg
        self.__ip = ip

    def sendall(self, packet):
        self.__vg.virtual_serial_port.writeFromSocket(packet)
    
    def recv(self):
        return self.__vg.socketQueues[int(self.__ip(".")[-1])-10].get()

    def close(self):
        pass