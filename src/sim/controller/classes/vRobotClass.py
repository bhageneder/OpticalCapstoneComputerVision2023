from src.interfaces.BaseRobotClass import BaseRobot

class vRobot(BaseRobot):
    def __init__(self, trackID, robotLink = None):
        BaseRobot.__init__(self, trackID, robotLink)
