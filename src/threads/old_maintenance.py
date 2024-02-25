import time
import threading
import queue
from config.global_vars import global_vars
from src.functions import led_manager as lc
from src.functions.ping import ping

# 8 Mini_Maintenance Threads and 1 Maintenance Thread per Robot Link
def old_maintenance(robot_link):
    thread_name = threading.current_thread().name
    loss_percentages = queue.Queue()

    while True:
        # Creating Mini-Discovery Threads so threads can be started 
        # (needs to be done each time because threads cannot be restarted)
        mini_maintenance_threads = []
        for i in range(8):
            mini_maintenance_threads.append(threading.Thread(
                target=mini_maintenance,
                args=(
                    f'{robot_link.ip_address}',
                    i,
                    f'{global_vars.ROBOT_IP_ADDRESS}_Ping_Through_Transceiver{i}',
                    loss_percentages
                ),
                daemon=True,
                name=f"Mini_Maintenance_{i}"
            ))

        for i in range(8):
            mini_maintenance_threads[i].start()
        
        for i in range(8):
            mini_maintenance_threads[i].join()
        
        # Initializing These Values
        lowest_loss_percentage = 100
        current_loss_percentage = 100
        current_serial_port_number = global_vars.serial_ports.index(robot_link.serial_port)
        
        while not loss_percentages.empty():
            loss_percentage, transceiver_number = loss_percentages.get()
            #if globals.debug_maintenance: print(f'{thread_name}: Returned Tuple {(loss_percentage, transceiver_number)}')
            if int(transceiver_number) == current_serial_port_number:
                current_loss_percentage = loss_percentage
            
            if loss_percentage < lowest_loss_percentage:
                lowest_loss_percentage = loss_percentage
                best_transceiver_number = transceiver_number
                #if globals.debug_maintenance: print(f'{thread_name}: Best Transceiver # Set as {best_transceiver_number}')
        
        # one_packet_dropped_loss_percentage = round((1 - ((globals.PING_COUNT - 1) / globals.PING_COUNT)) * 100, 2)
        # if globals.debug_maintenance: print(f'{thread_name}: One Dropped Packet Loss Percentage: {one_packet_dropped_loss_percentage}')
        # # If we have dropped one packet or more, and something has dropped less than one packet, then we switch.
        # if current_loss_percentage > one_packet_dropped_loss_percentage and lowest_loss_percentage < one_packet_dropped_loss_percentage:

        if global_vars.debug_maintenance: print(f'{thread_name}: Current Loss Percentage: {current_loss_percentage}  Lowest Loss Percentage: {lowest_loss_percentage}')
        if current_loss_percentage > lowest_loss_percentage: 
            if global_vars.debug_maintenance: print(f'{thread_name}: Switching Robot Link Serial Port to {best_transceiver_number}')
            robot_link.serial_port = global_vars.serial_ports[best_transceiver_number]
    
            if global_vars.lights_enabled:
                    if global_vars.debug_maintenance: print(f'{thread_name}: Switching LED from {current_serial_port_number} to {best_transceiver_number}')
                    
                    # Do not turn off LED if the Transceiver is being used by other Robot Links
                    for i in range(len(global_vars.robot_links)):
                        if (global_vars.robot_links[i].serial_port == global_vars.serial_ports[current_serial_port_number]):
                            break
                    else:
                        lc.turn_off_for_robot_link(current_serial_port_number)
                    
                    # Turn on LED for the new Transceiver being used
                    lc.illuminate_for_robot_link(int(best_transceiver_number))

        time.sleep(global_vars.MAINTENANCE_INTERVAL_SLEEP)

        # Terminate if robot_link no longer exists
        if robot_link not in global_vars.robot_links:
            return


def mini_maintenance(dest_addr, identifier, payload, loss_percentages):
    loss_percentage = ping(
        dest_addr, 
        identifier, 
        global_vars.PING_COUNT, 
        global_vars.PING_INTERVAL,
        global_vars.PING_TIMEOUT,
        payload
        )
    
    # The Identifier also represents which Transceiver (or serial port)
    # was used to complete the ping test.
    transceiver_number = identifier
    # Enqueuing a tuple of both the loss_percentage, and which transceiver has it.
    loss_percentages.put((round(loss_percentage, 2), transceiver_number))