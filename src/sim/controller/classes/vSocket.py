# Virtual TCP Socket

class vSocket:
    def __init__(self, ip, vg):
        self.__vg = vg

    def sendall(self):
        self.__vg.socketQueues[int(self.__ip.split(".")[-1])-10]
    
    def recv(self):
        pass

    def close(self):
        pass