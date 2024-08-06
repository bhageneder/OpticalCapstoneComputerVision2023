import time

# Virtual TCP Socket

class vSocket:
    def __init__(self, vg, ip, robot):
        self.__vg = vg
        self.__conn_ip = ip
        self.robot = robot

    def sendall(self, packet):
        # Grap the first IP (sending to IP)
        ip = packet.split("\x00")[1]

        # Busy wait until sending can actually take place
        while not ((ip in self.__vg.detector.commsAvailable) and (self.robot in self.__vg.visible)):
            if ((self.robot not in self.__vg.visible) and (self.robot not in self.__vg.lost)):
                return
            time.sleep(0.5)
            continue

        self.__vg.virtual_serial_port.writeFromSocket(packet)
    
    def recv(self):
        return self.__vg.socketQueues[int(self.__conn_ip.split(".")[-1])-10].get(timeout=0.1)

    def close(self):
        pass