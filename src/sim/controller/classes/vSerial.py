from queue import Queue

# Virtual [Virtual] Serial Port
class vSerial:
    def __init__(self, vg):
        self.__vg = vg
        self.__sendQueue = Queue()

    def write(self, packet):
        # Grap the second IP (the from IP) to place it in the correct socket
        ip = packet.split("\x00")[2]
        self.__vg.socketQueues[int(ip.split(".")[-1])-10].put(packet)
        
    def writeFromSocket(self, packet):
        self.__sendQueue.put(packet)
    
    def read(self):
        return self.__sendQueue.get()