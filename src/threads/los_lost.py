import config.global_vars as g

def los_lost():
    while True:
        # Blocking Call to Detector's Lost Queue
        robot = g.detector.lostQ.get()

        # Check for Robot Link
        if (robot.robotLink != None):
            # Append to Global Lost List
            g.lost.append(robot) # Needs to have mutex lock

        # Remove from Global Visible List
        g.visible.append(robot) # Needs to have mutex lock