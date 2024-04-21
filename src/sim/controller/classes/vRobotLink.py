from src.interfaces.BaseRobotLink import BaseRobotLink

class vRobotLink(BaseRobotLink):
    def __init__(self, name, ip_address):
        BaseRobotLink.__init__(self, name, ip_address)