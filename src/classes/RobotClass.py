from interfaces.iRobotClass import iRobot

class Robot(iRobot):
    def __init__(self, trackingID, transceiver, losActive, RobotLink = None):
        super().__init__(trackingID, transceiver, losActive, RobotLink)