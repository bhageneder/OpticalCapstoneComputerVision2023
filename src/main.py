import threading
import os
import glob
import time
import subprocess
import board    # needed for neopixel
import neopixel # needed for neopixel
from threads.maintenance import maintenance
from threads.discovery import discovery
from threads.link_send import link_send
from threads.link_receive import link_receive
from threads.listen_for_connection import listen_for_connection
from threads.receive_manager import receive_manager
from threads.send_manager import send_manager
from threads.transceiver_send import transceiver_send
from threads.transceiver_receive import transceiver_receive
from threads.detector_manager import detector_manager
import global_vars as global_vars
import functions.led_manager as lc
from control_robot.move_circle import move_circle
from functions.initialize_serial_ports import initialize_serial_ports

def main():
    # Clear robot_link_data directory
    link_files = glob.glob(os.getcwd() + 'robot_link_packets/*')
    for f in link_files:
        os.remove(f)

    # INITIALIZATION - setting all the global variables (including serial port initialization). Also sets up SLIP
    global_vars.init()

    global_vars.working_dir = os.getcwd()

    # Setup Serial Line Interface Protocol (SLIP), and create virtual serial ports
    subprocess.run([global_vars.working_dir + 'scripts/create_serial_interface.sh', global_vars.ROBOT_IP_ADDRESS])
    time.sleep(1.5) # Wait for virtual serial ports to be fully created
    global_vars.serial_ports, global_vars.robot_serial_port, global_vars.virtual_serial_port = initialize_serial_ports()

    lc.turn_all_LEDs_off()

    # Making One Robot Move in a 1 meter circle at speed 200 mm/s
    if global_vars.robot_serial_port is not None and global_vars.ROBOT_IP_ADDRESS == global_vars.POSSIBLE_ROBOT_IP_ADDRESSES[0]:
        moving_thread = threading.Thread(target=move_circle, args=(global_vars.robot_serial_port, 0xC8,), daemon=True, name=f"Moving")
        moving_thread.start()

    # Creating Transceiver Receive and Transceiver Send Threads
    # print("Num Serial Ports: " + str(len(global_vars.serial_ports))) FOR TESTING PURPOSES
    for i in range(8):
        global_vars.transceiver_receive_threads.append(threading.Thread(
            target=transceiver_receive, 
            args=(
                global_vars.serial_ports[i],
                ), 
            daemon=True, 
            name=f"T_Receive_{i}"
        ))

        global_vars.transceiver_send_threads.append(threading.Thread(
            target=transceiver_send, 
            args=(
                global_vars.serial_ports[i], global_vars.transceiver_send_queues[i],
                ), 
            daemon=True, 
            name=f"T_Send_{i}"
        ))

    for i in range(len(global_vars.POSSIBLE_RECEIVING_ROBOT_PORTS)):
        # Creating Listen For Connection Thread
        global_vars.listen_for_connection_threads.append(threading.Thread(
            target=listen_for_connection, 
            args=(
                global_vars.POSSIBLE_RECEIVING_ROBOT_PORTS[i],
                ), 
            daemon=True, 
            name=f"Listen_{i}"
        ))

    # Creating Discovery Thread
    global_vars.discovery_thread = threading.Thread(target=discovery, daemon=True, name=f"Discovery")

    # Creating Send Manager Thread
    global_vars.send_manager_thread = threading.Thread(target=send_manager, daemon=True, name=f"Send_Manager")

    # Creating Receive Manager Thread
    global_vars.receive_manager_thread = threading.Thread(target=receive_manager, daemon=True, name=f"Receive_Manager")

    global_vars.detector_manager_thread = threading.Thread(target=detector_manager, daemon=True, name=f"Detector_Manager")

    start_threads()
    
def start_threads():
    # Running Transceiver Receive Threads
    for transceiver_receive_thread in global_vars.transceiver_receive_threads:
        transceiver_receive_thread.start()

    # Running Transceiver Send Threads
    for transceiver_send_thread in global_vars.transceiver_send_threads:
        transceiver_send_thread.start()

    # Running Listen For Connection Threads
    for listen_for_connection_thread in global_vars.listen_for_connection_threads:
        listen_for_connection_thread.start()


    # TODO: Fix Current Bug: For Sending a Payload, If both Robots Run the Discovery Thread, then
    # the socket is closed / destroyed SOMETIMES by one of the robots, causing payload tranmsissions to fail.
    # A temporary fix is to have 1 robot run this discovery thread, until the bug is fixed.
    # Running Discovery Thread
    global_vars.discovery_thread.start()

    # Running Receive Manager Thread
    global_vars.receive_manager_thread.start()

    # Running Send Manager Thread
    global_vars.send_manager_thread.start()

    global_vars.detector_manager_thread.start()

    # Running New Threads based on new Robot Links
    while True:
        robot_link = global_vars.robot_links_new.get()

        thread_number = len(global_vars.robot_links)
        link_send_thread = threading.Thread(target=link_send, args=(robot_link,), daemon=True, name=f"Link_Send_{thread_number}")
        link_send_thread.start()

        link_receive_thread = threading.Thread(target=link_receive, args=(robot_link,), daemon=True, name=f"Link_Receive_{thread_number}")
        link_receive_thread.start()

        maintenance_thread = threading.Thread(target=maintenance, args=(robot_link,), daemon=True, name=f"Maintenance_{thread_number}")
        maintenance_thread.start()

        
if __name__ == "__main__":
    main()
