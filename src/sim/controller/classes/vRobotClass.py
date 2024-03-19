from interfaces.iRobotClass import iRobot


class vRobot(iRobot):
    def __init__(self, trackingID, transceiver, losActive, RobotLink = None):
        super.__init__(trackingID, transceiver, losActive, RobotLink)

    def setTrackingID(self, inputTrackingID):
        self.trackingID = inputTrackingID
    
    def setTransceiver(self, inputTransceiver):
        self.transceiver = inputTransceiver

    def setRobotLink(self, inputRobotLink):
        self.RobotLink = inputRobotLink

    def setLosActive(self, inputLosActive):
        self.losActive = inputLosActive