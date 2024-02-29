import config.global_vars as g

def los_lost():
    while True:
        # Blocking Call to Detector's Lost Queue
        robot = g.detector.lostQ.get()

        # Check for Robot Link
        if (robot.robotLink != None):
            # Acquire Visible Robot List Mutex
            with g.lost_mutex:
                # Append to Global Lost List
                g.lost.append(robot)

        # Acquire Visible Robot List Mutex
        with g.visible_mutex:
            # Remove from Global Visible List
            g.visible.remove(robot)