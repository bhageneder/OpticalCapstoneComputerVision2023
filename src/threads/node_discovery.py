import time
import threading
import config.global_vars as g
from functions.ping import associate
from threads.mini_node_discovery import mini_node_discovery

# Attempt to Discover a TCP Connection (Robot Link) to a Newly Visible Robot
def node_discovery(robot):
    # 1 Second Timeout
    timeout = 1

    # Store Initial Time
    t0 = time.time()
    t = 0

    # Try to Discover Until Robot Link is Established or Timeout Occurs
    while ((robot.robotLink is None) and (t - t0 < timeout)):

        # Define Empty Robot IP
        robotIP = None

        # Identify Which IP the Robot Has
        for i in range(len(g.POSSIBLE_ROBOT_IP_ADDRESSES)):
            # Skip over our own IP (we should really not have any used IPs in this list tbh, should change this)
            if g.POSSIBLE_ROBOT_IP_ADDRESSES[i] == g.ROBOT_IP_ADDRESS:
                continue

            # Associative Ping:
            response = associate(robot.transceiver, g.POSSIBLE_ROBOT_IP_ADDRESSES[i], robot.trackID)
            
            # If we get a response
            if response:
                robotIP = g.POSSIBLE_ROBOT_IP_ADDRESSES[i]
                break

        # Only try to discover if we know the IP
        if robotIP is not None:
            # Set the IP - Checked by the Send Manager
            robot.IP = robotIP

            numThreads = g.EXPECTED_NUMBER_OF_ROBOTS

            # Try to discovery on possible ports
            # Creating Mini Node Discovery Threads For Each Port
            mini_node_discovery_threads = []
            for i in range(numThreads):
                mini_node_discovery_threads.append(threading.Thread(
                    target=mini_node_discovery,
                    args=(
                        robotIP,
                        g.POSSIBLE_RECEIVING_ROBOT_PORTS[i],
                        g.POSSIBLE_SENDING_ROBOT_PORTS[i],
                        robot
                    ),
                    daemon=True,
                    name=f"Mini_Node_Discovery__{i}"
                ))

            for i in range(numThreads):
                mini_node_discovery_threads[i].start()

            for i in range(numThreads):
                mini_node_discovery_threads[i].join()

        # Sleep
        time.sleep(g.DISCOVERY_INTERVAL_SLEEP)

        # Update Time
        t = time.time()

    if (robot.robotLink is None):
        # Failed to Discover Robot
        # Acquire Global Visible Robot List Mutex
            with g.visible_mutex:
                # Remove Robot from Global Visible List
                try:
                    g.visible.remove(robot)
                except ValueError:
                    # Robot is Already Considered Lost and Has Been Removed from List
                    pass
    else:
        # Queue to New Robot Queue
        g.newRobotQ.put(robot)
