class Robot:
    def __init__(self, trackingID, transceiver, RobotLink = None):
        self.trackingID = trackingID        # Integer - ID number associated with the robot in the detection loop
        self.transceiver = transceiver      # Integer - Best transceiver to use for communications
        self.RobotLink = RobotLink          # RobotLink (includes IP info) - set when a TCP socket is created
