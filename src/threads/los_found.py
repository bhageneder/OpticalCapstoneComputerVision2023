import config.global_vars as g
import node_discovery
import threading

def los_found():
    while True:
        # Blocking Call to Detector's Lost Queue
        robot = g.detector.lostQ.get()

        # Check if Robot is in Lost List
        foundRobot = findRobot(robot)
        if (foundRobot is not None):
            # Update Robot Link
            robot.robotLink = foundRobot.robotLink

            # Acquire Global Visible Robot List Mutex
            with g.visible_mutex:
                # Append to Global Visible List
                g.visible.append(robot)

            # Acquire Global Lost Robot List Mutex
            with g.lost_mutex:
                # Remove from Global Lost List
                g.lost.remove(foundRobot)

        # Robot is Not in Lost List
        else:
            # Acquire Global Visible Robot List Mutex
            with g.visible_mutex:
                # Append to Global Visible List
                g.visible.append(robot)

            # Launch Node Discovery Thread
            node_discovery_thread = threading.Thread(target=node_discovery, daemon=True, args=robot, name=f"Node_Discovery_For_Robot_{robot.trackingID}")
            node_discovery_thread.start()

# Searchest Lost List for Parameter Robot
def findRobot(robot):
    # Acquire Lost Robot Mutex
    with g.lost_mutex:
        # Try to Communicate on Open Robot Links Using New Robot Transceiver
        for lostRobot in g.lost:
            # Send Reassociate Ping
            response = reassociate(robot.transceiver, lostRobot) # Needs to be implemented

            # If it Got a Response
            if response:
                # Return the Robot
                return lostRobot
            
    return None