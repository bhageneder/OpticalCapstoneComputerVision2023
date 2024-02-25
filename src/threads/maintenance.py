import time
import threading
from config.global_vars import global_vars
from src.functions.ping import multi_ping
from src.functions import led_manager as lc

def maintenance(robot_link):
    thread_name = threading.current_thread().name
    transceiver_set = False
    while True:
        # Get the best transceiver number from the Jetson Nano        
        best_transceiver_number = global_vars.best_transceiver

        # Might want to ping for maintenance for backup

        # If the socket failed to open, multi_ping will return -1. 
        # In that case, try again.
        if best_transceiver_number == -1:
            continue

        current_transceiver_number = global_vars.serial_ports.index(robot_link.serial_port)
              
        if current_transceiver_number != best_transceiver_number or not transceiver_set:
            transceiver_set = True
            if global_vars.debug_maintenance: print(f'{thread_name}: Switching to use Transceiver {best_transceiver_number} for Robot Link')
            robot_link.serial_port = global_vars.serial_ports[best_transceiver_number]

            if global_vars.lights_enabled:
                if global_vars.debug_maintenance or global_vars.ROBOT_IP_ADDRESS == global_vars.POSSIBLE_ROBOT_IP_ADDRESSES[0]: print(f'{thread_name}: Switching LED from {current_transceiver_number} to {best_transceiver_number}')
                
                # Do not turn off LED if the Transceiver is being used by other Robot Links
                for i in range(len(global_vars.robot_links)):
                    if (global_vars.robot_links[i].serial_port == global_vars.serial_ports[current_transceiver_number]):
                        break
                else:
                    if global_vars.ROBOT_IP_ADDRESS == global_vars.POSSIBLE_ROBOT_IP_ADDRESSES[0]: print(f'Turning off LED {current_transceiver_number}')
                    lc.turn_off_for_robot_link(current_transceiver_number)
                
                # Turn on LED for the new Transceiver being used
                lc.illuminate_for_robot_link(best_transceiver_number)

        time.sleep(global_vars.MAINTENANCE_INTERVAL_SLEEP)

        # Terminate if robot_link no longer exists
        if robot_link not in global_vars.robot_links:
            return
