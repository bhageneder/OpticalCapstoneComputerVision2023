class Robot:
    def __init__(self, trackID, transceiver, robotLink = None):
        self.trackID = trackID        # Integer - ID number associated with the robot in the detection loop
        self.transceiver = transceiver      # Integer - Best transceiver to use for communications
        self.robotLink = robotLink          # RobotLink (includes IP info) - set when a TCP socket is created
        self.IP = None                      # IP - Needed for when an IP has been selected, but discovery has not completed (No RobotLink Exists Yet)