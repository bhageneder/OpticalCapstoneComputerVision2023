import time
import threading
import config.global_vars as g
from threads.mini_discovery import mini_discovery

# THIS FUNCTION NEEDS TO BE IMPLEMENTED STILL
# Implementation is in progress

def node_discovery(robot):
    # 10 Second Timeout
    timeout = 10000

    # Store Initial Time
    t0 = time.time_ns() // 1_000_000
    t = t0

    # Try to Discover Until Robot Link is Established or Timeout Occurs
    while ((robot.robotLink is None) and (t - t0 < timeout)):

        # Creating Mini-Discovery Threads
        
        # Sleep
        time.sleep(g.DISCOVERY_INTERVAL_SLEEP)

        # Update Time
        t = time.time_ns() // 1_000_000

    if (robot.robotLink is None):
        # Failed to Discover Robot
        # Remove Robot from Visible List
        pass