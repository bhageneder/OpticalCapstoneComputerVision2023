class RobotLink:
    def __init__(self, name, serial_port, socket, ip_address, port):
        self.name = name
        self.serial_port = serial_port
        self.socket = socket
        self.ip_address = ip_address
        self.port = port
        self.lastPacketTime = -1
        self.active = True