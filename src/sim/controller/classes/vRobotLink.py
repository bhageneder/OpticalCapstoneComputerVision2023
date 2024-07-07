from interfaces.BaseRobotLink import BaseRobotLink

class vRobotLink(BaseRobotLink):
    def __init__(self, name, socket, ip_address):
        BaseRobotLink.__init__(self, name, socket, ip_address)