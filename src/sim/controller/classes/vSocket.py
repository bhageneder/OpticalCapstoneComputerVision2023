# Virtual TCP Socket

class vSocket:
    def __init__(self, vg, ip):
        self.__vg = vg
        self.__conn_ip = ip

    def sendall(self, packet):
        #while not ((sendingTo in vg.detector.commsAvailable) and (robot in vg.visible)):
        # add a while loop that holds till da ip gets 
        self.__vg.virtual_serial_port.writeFromSocket(packet)
    
    def recv(self):
        # once its fixed in vSerial, this should get from the ip of where it came from
        return self.__vg.socketQueues[int(self.__conn_ip.split(".")[-1])-10].get()
        #self.__vg.ip or self.__ip.split ????
        # vg.ip.split ???? which IP am i trying to get from

    def close(self):
        pass