class BaseRobot:
    def __init__(self, trackID, robotLink=None):
        self.trackID = trackID        # Integer - ID number associated with the robot in the detection loop
        self.robotLink = robotLink          # RobotLink (includes IP info) - set when a TCP socket is created
        self.IP = None                      # IP - Needed for when an IP has been selected, but discovery has not completed (No RobotLink Exists Yet)
