class BaseRobotLink:
    def __init__(self, name, socket, ip_address):
        self.name = name
        self.socket = socket
        self.ip_address = ip_address