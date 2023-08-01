import globals
import time
import threading
from threads.mini_discovery import mini_discovery

# There are (8 * (n - 1)) total threads to be run, but we are only running 7 at a time
# (n - 1) possible IP addresses (not including our own), and 8 possible ports. (n - 1) * 8 = 56
# Where n is the number of expected robots
def discovery():
    thread_name = threading.current_thread().name
    while True:
        # If all robots have been discovered, do not bother running discovery anymore.
        if len(globals.robot_links) >= globals.EXPECTED_NUMBER_OF_ROBOTS - 1:
            if globals.debug_discovery: print(f'{thread_name}: All robots have been discovered. Returning...')
            return

        # Creating Mini-Discovery Threads (n - 1 will run simultaneously at a time, not looking for own IP address)
        # (needs to be done each time because threads cannot be restarted)
        mini_discovery_threads = []
        for i in range(globals.EXPECTED_NUMBER_OF_ROBOTS):
            if globals.POSSIBLE_ROBOT_IP_ADDRESSES[i] == globals.ROBOT_IP_ADDRESS:
                continue
            for j in range(globals.EXPECTED_NUMBER_OF_ROBOTS):
                mini_discovery_threads.append(threading.Thread(
                    target=mini_discovery,
                    args=(
                        globals.POSSIBLE_ROBOT_IP_ADDRESSES[i],
                        globals.POSSIBLE_RECEIVING_ROBOT_PORTS[j],
                        globals.POSSIBLE_SENDING_ROBOT_PORTS[j],
                    ),
                    daemon=True,
                    name=f"Mini_Discovery_{i}_{j}"
                ))

        range_offset = 0
        for _ in range(globals.EXPECTED_NUMBER_OF_ROBOTS):
            for i in range(range_offset, range_offset + globals.EXPECTED_NUMBER_OF_ROBOTS - 1):
                mini_discovery_threads[i].start()
            
            for i in range(range_offset, range_offset + globals.EXPECTED_NUMBER_OF_ROBOTS - 1):
                mini_discovery_threads[i].join()
            
            range_offset += globals.EXPECTED_NUMBER_OF_ROBOTS - 1
        
        time.sleep(globals.DISCOVERY_INTERVAL_SLEEP)
