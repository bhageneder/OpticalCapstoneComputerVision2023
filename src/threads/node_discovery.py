import time
import threading
import config.global_vars as g
from threads.mini_discovery import mini_discovery

# THIS FUNCTION NEEDS TO BE IMPLEMENTED STILL
# Implementation is in progress

def node_discovery(robot):
    # 1 Second Timeout
    timeout = 1000

    # Store Initial Time
    t0 = time.time_ns() // 1_000_000
    t = t0

    # Try to Discover Until Robot Link is Established or Timeout Occurs
    while ((robot.robotLink is None) and (t - t0 < timeout)):

        # Creating Mini-Discovery Threads
        mini_discovery_threads = []
        for i in range(g.EXPECTED_NUMBER_OF_ROBOTS):
            if g.POSSIBLE_ROBOT_IP_ADDRESSES[i] == g.ROBOT_IP_ADDRESS:
                continue
            for j in range(g.EXPECTED_NUMBER_OF_ROBOTS):
                mini_discovery_threads.append(threading.Thread(
                    target=mini_discovery,
                    args=(
                        g.POSSIBLE_ROBOT_IP_ADDRESSES[i],
                        g.POSSIBLE_RECEIVING_ROBOT_PORTS[j],
                        g.POSSIBLE_SENDING_ROBOT_PORTS[j],
                        robot.transceiver
                    ),
                    daemon=True,
                    name=f"Mini_Node_Discovery_{i}_{j}"
                ))

        range_offset = 0
        for _ in range(g.EXPECTED_NUMBER_OF_ROBOTS):
            for i in range(range_offset, range_offset + g.EXPECTED_NUMBER_OF_ROBOTS - 1):
                mini_discovery_threads[i].start()

            for i in range(range_offset, range_offset + g.EXPECTED_NUMBER_OF_ROBOTS - 1):
                mini_discovery_threads[i].join()

            range_offset += g.EXPECTED_NUMBER_OF_ROBOTS - 1

        # Sleep
        time.sleep(g.DISCOVERY_INTERVAL_SLEEP)

        # Update Time
        t = time.time_ns() // 1_000_000

    if (robot.robotLink is None):
        # Failed to Discover Robot
        # Acquire Global Visible Robot List Mutex
            with g.visible_mutex:
                # Remove Robot from Global Visible List
                g.visible.remove(robot)