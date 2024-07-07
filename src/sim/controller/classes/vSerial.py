# Virtual [Virtual] Serial Port
from queue import Queue

class vSerial:
    def __init__(self, ip, vg):
        self.__vg = vg
        self.__ip = ip
        self.__sendQueue = Queue()

    def write(self, packet):
        self.__vg.socketQueues[int(self.__ip.split(".")[-1])-10].put(packet)
        
    def writeFromSocket(self, packet):
        self.__sendQueue.put(packet)
    
    def read(self):
        return self.__sendQueue.get()