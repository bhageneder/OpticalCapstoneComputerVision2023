import config.global_vars as g
import node_discovery
import threading

def los_found():
    while True:
        # Blocking Call to Detector's Lost Queue
        robot = g.detector.lostQ.get()

        # Check if Robot is in Global Lost List
        robotLink = findRobotLink()
        if (robotLink is not None):
            # Update Robot Link
            robot.robotLink = robotLink

            # Acquire Visible Robot List Mutex
            with g.visible_mutex:
                # Append to Global Visible List
                g.visible.append(robot)

            # Acquire Lost Robot List Mutex
            with g.lost_mutex:
                # Append to Global Lost List
                g.lost.remove(robot)

        # Robot is Not in Lost List
        else:
            # Acquire Visible Robot List Mutex
            with g.visible_mutex:
                # Append to Visible List
                g.visible.append(robot)

            # Launch Node Discovery Thread
            node_discovery_thread = threading.Thread(target=node_discovery, daemon=True, args=robot, name=f"Node_Discovery_For_Robot_{robot.trackingID}")
            node_discovery_thread.start()

def findRobotLink(robot):
    # Needs to be Implemented
    return None