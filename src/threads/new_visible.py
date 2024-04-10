import config.global_vars as g
from functions.ping import associate
from threads.node_discovery import node_discovery
import threading

# Handles Newly Visible Robots
def new_visible():
    while True:
        # Blocking Call to the Visible Queue
        robot = g.detector.visibleQ.get()

        #connecting/finding LEDs

        # Aquire Visible Mutex
        with g.visible_mutex:
            # Add Robot to the Visible List
            g.visible.append(robot)

        # Check if Robot is in Lost List
        foundRobot = findRobot(robot)
        if (foundRobot is not None):
            # Update Robot Link
            robot.robotLink = foundRobot.robotLink

            # Acquire Global Lost List Mutex
            with g.visible_mutex and g.lost_mutex:
                # Remove from Global Lost List
                g.lost.remove(foundRobot)

            # Queue to New Robot Queue
            g.newRobotQ.put(robot)

        # Robot is Not in Lost List
        else:
            # Launch Node Discovery Thread
            node_discovery_thread = threading.Thread(target=node_discovery, daemon=True, args=[robot], name=f"Node_Discovery_For_Robot_{robot.trackID}")
            node_discovery_thread.start()

# Searchest Lost List for Parameter Robot
def findRobot(robot):
    # Acquire Lost Robot Mutex
    with g.lost_mutex:
        # Try to Communicate on Open Robot Links Using New Robot Transceiver
        for lostRobot in g.lost:
            # Send an Associate Ping to Reassociate
            response = associate(robot.transceiver, lostRobot.robotLink.ip_address, robot.trackID)

            # If it Got a Response
            if response:
                # Return the Robot
                return lostRobot
            
    return None
