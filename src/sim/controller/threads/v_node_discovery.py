import threading
import time
from sim.controller.functions.v_ping import v_associate
from sim.controller.threads.v_mini_node_discovery import v_mini_node_discovery

# Attempt to Discover a TCP Connection (Robot Link) to a Newly Visible Robot
def v_node_discovery(robot, vg):
    
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
        for i in range(len(vg.POSSIBLE_ROBOT_IP_ADDRESSES)):
            # Skip over our own IP (we should really not have any used IPs in this list tbh, should change this)
            if vg.POSSIBLE_ROBOT_IP_ADDRESSES[i] == vg.ip:
                continue

            # Associative Ping:
            response = v_associate(vg.POSSIBLE_ROBOT_IP_ADDRESSES[i], vg)
            
            # If we get a response
            if response:
                robotIP = vg.POSSIBLE_ROBOT_IP_ADDRESSES[i]
                break

        # Only try to discover if we know the IP
        if robotIP is not None:
            # Set the IP - Checked by the Send Manager
            robot.IP = robotIP

            numThreads = vg.EXPECTED_NUMBER_OF_ROBOTS

            # Try to discovery on possible ports
            # Creating Mini Node Discovery Threads For Each Port
            mini_node_discovery_threads = []
            for i in range(numThreads):
                mini_node_discovery_threads.append(threading.Thread(
                    target=v_mini_node_discovery,
                    args=(
                        robotIP,
                        vg
                    ),
                    daemon=True,
                    name=f"Mini_Node_Discovery__{i}"
                ))

            for i in range(numThreads):
                mini_node_discovery_threads[i].start()

            for i in range(numThreads):
                mini_node_discovery_threads[i].join()

        # Sleep
        time.sleep(vg.DISCOVERY_INTERVAL_SLEEP)

        # Update Time
        t = time.time()

    if (robot.robotLink is None):
        # Failed to Discover Robot
        # Acquire Global Visible Robot List Mutex
            with vg.visible_mutex:
                # Remove Robot from Global Visible List
                try:
                    vg.visible.remove(robot)
                except ValueError:
                    # Robot is Already Considered Lost and Has Been Removed from List
                    pass
    else:
        # Queue to New Robot Queue
        vg.newRobotQ.put(robot)
