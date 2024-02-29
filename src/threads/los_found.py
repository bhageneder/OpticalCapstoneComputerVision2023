import config.global_vars as g

def los_found():
    while True:
        # Blocking Call to Detector's Lost Queue
        robot = g.detector.lostQ.get()

        # Check if Robot is in Global Lost List
        # Needs to be implemented. Will return value and the existing robot
        existingRobot = "insert robot here"
        if (True):
            # Update Tracking ID
            existingRobot.trackingID = robot.trackingID

            # Append to Global Visible List
            g.visible.append(existingRobot) # Needs to have mutex lock

            # Append to Global Lost List
            g.lost.remove(existingRobot) # Needs to have mutex lock

        # Robot is Not in Lost List
        else:
            # Append to Visible List
            g.visible.append(robot)

            # Launch Discovery Thread
            # Needs to be implemented