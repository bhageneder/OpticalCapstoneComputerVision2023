import config.global_vars as g
from functions.ping import associate
from threads.node_discovery import node_discovery
import threading

# Handles Newly Visible Robots
def new_visible():
    while True:
        # Blocking Call to the Visible Queue
        robot = g.detector.visibleQ.get()

        # Aquire Visible Mutex
        with g.visible_mutex:
            # Add Robot to the Visible List     
            g.visible.append(robot)

        # Check if Robot is in Lost List
        foundRobot = findRobot(robot)
        if (foundRobot is not None):
            # Acquire Global Lost List Mutex
            with g.visible and g.lost_mutex: 
                # Copy Tracking ID and Transceiver Number
                foundRobot.trackID = robot.trackID
                foundRobot.transceiver = robot.transceiver

                # Remove from Lost List
                g.lost.remove(foundRobot)

                # Add to the visible list
                g.visible.append(foundRobot)

                # Remove the extra robot from the Visible List
                g.visible.remove(robot)

            # Queue to New Robot Queue
            # g.newRobotQ.put(robot) # delete this line

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
