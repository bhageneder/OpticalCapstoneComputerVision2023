import time
import threading
import config.global_vars as g
from functions.ping import multi_ping
from functions import led_funcs as lc

def maintenance(robot_link):
    thread_name = threading.current_thread().name
    transceiver_set = False
    while True:
        # Get the best transceiver number      
        best_transceiver_number = multi_ping(
            robot_link.ip_address, 
            globals.PING_COUNT, 
            globals.PING_INTERVAL,
            globals.PING_TIMEOUT,
        )

        # If the socket failed to open, multi_ping will return -1. 
        # In that case, try again.
        if best_transceiver_number == -1:
            continue

        current_transceiver_number = g.serial_ports.index(robot_link.serial_port)
              
        if current_transceiver_number != best_transceiver_number or not transceiver_set:
            transceiver_set = True
            if g.debug_maintenance: print(f'{thread_name}: Switching to use Transceiver {best_transceiver_number} for Robot Link')
            robot_link.serial_port = g.serial_ports[best_transceiver_number]

            if g.lights_enabled:
                if g.debug_maintenance or g.ROBOT_IP_ADDRESS == g.POSSIBLE_ROBOT_IP_ADDRESSES[0]: print(f'{thread_name}: Switching LED from {current_transceiver_number} to {best_transceiver_number}')
                
                # Do not turn off LED if the Transceiver is being used by other Robot Links
                for i in range(len(g.robot_links)):
                    if (g.robot_links[i].serial_port == g.serial_ports[current_transceiver_number]):
                        break
                else:
                    if g.ROBOT_IP_ADDRESS == g.POSSIBLE_ROBOT_IP_ADDRESSES[0]: print(f'Turning off LED {current_transceiver_number}')
                    lc.turn_off_for_robot_link(current_transceiver_number)
                
                # Turn on LED for the new Transceiver being used
                lc.illuminate_for_robot_link(best_transceiver_number)

        time.sleep(g.MAINTENANCE_INTERVAL_SLEEP)

        # Terminate if robot_link no longer exists
        if robot_link not in g.robot_links:
            return
