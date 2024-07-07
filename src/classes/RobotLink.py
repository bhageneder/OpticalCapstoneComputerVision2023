from interfaces.BaseRobotLink import BaseRobotLink

class RobotLink(BaseRobotLink):
    def __init__(self, name, serial_port, socket, ip_address, port):
        BaseRobotLink.__init__(self, name, socket, ip_address)
        self.serial_port = serial_port
        self.socket = socket
        self.port = port
        self.lastPacketTime = -1
        self.active = True