from src.interfaces.BaseRobotClass import BaseRobot

class Robot(BaseRobot):
    def __init__(self, trackID, transceiver, robotLink = None):
        BaseRobot.__init__(self, trackID, robotLink)
        self.transceiver = transceiver      # Integer - Best transceiver to use for communications