import threading
import os
import glob
import time
import subprocess
# import board    # needed for neopixel
# import neopixel_spi as neopixel # needed for neopixel
from threads.maintenance import maintenance
from threads.discovery import discovery
from threads.link_send import link_send
from threads.link_receive import link_receive
from threads.listen_for_connection import listen_for_connection
from threads.receive_manager import receive_manager
from threads.send_manager import send_manager
from threads.transceiver_send import transceiver_send
from threads.transceiver_receive import transceiver_receive
# from threads.new_visible import new_visible
# from threads.new_lost import new_lost
import config.global_vars as g
# import functions.led_manager as lc
# from control_robot.move_circle import move_circle
from functions.initialize_serial_ports import initialize_serial_ports
# from classes.DetectorClass import Detector
from sim.controller.classes.vDetectorClass import vDetector 


def v_main():
    # Clear robot_link_data directory
    link_files = glob.glob(os.getcwd() + 'robot_link_packets/*')
    for f in link_files:
        os.remove(f)

    # INITIALIZATION - setting all the global variables (including serial port initialization). Also sets up SLIP
    """ TODO: Create Simulation globals """
    g.init()
    
    g.working_dir = os.getcwd()
    
    """ SETUP SLIP NOT NEEDED IN SIMULATION """
    # Setup Serial Line Interface Protocol (SLIP), and create virtual serial ports
    # subprocess.run([g.working_dir + '/functions/create_serial_interface.sh', g.ROBOT_IP_ADDRESS])
    # time.sleep(1.5) # Wait for virtual serial ports to be fully created
    """ TODO: Create virtualized initialize serial port"""
    """ g.serial_ports, g.robot_serial_port, g.virtual_serial_port = initialize_serial_ports() """

    """ LEDS NOT NEEDED IN SIMULATION """
    # Nano does not support neopixel
    # if g.robot != "nano":
        # lc.test_LEDs()
    

    """ MOVING ROBOT NOT NEEDED IN SIMULATION """
    # Making One Robot Move in a 1 meter circle at speed 200 mm/s
    # if g.robot_serial_port is not None and g.ROBOT_IP_ADDRESS == g.POSSIBLE_ROBOT_IP_ADDRESSES[0]:
    #     moving_thread = threading.Thread(target=move_circle, args=(g.robot_serial_port, 0xC8,), daemon=True, name=f"Moving")
    #     moving_thread.start()

    
    """ TODO: Virtualize creating transceiver send and receive threads """
    # Creating Transceiver Receive and Transceiver Send Threads
    # print("Num Serial Ports: " + str(len(g.serial_ports))) FOR TESTING PURPOSES
    """
    for i in range(8):
        g.transceiver_receive_threads.append(threading.Thread(
            target=transceiver_receive, 
            args=(
                g.serial_ports[i],
                ), 
            daemon=True, 
            name=f"T_Receive_{i}"
        ))

        g.transceiver_send_threads.append(threading.Thread(
            target=transceiver_send, 
            args=(
                g.serial_ports[i], g.transceiver_send_queues[i],
                ), 
            daemon=True, 
            name=f"T_Send_{i}"
        ))

    for i in range(len(g.POSSIBLE_RECEIVING_ROBOT_PORTS)):
        # Creating Listen For Connection Thread
        g.listen_for_connection_threads.append(threading.Thread(
            target=listen_for_connection, 
            args=(
                g.POSSIBLE_RECEIVING_ROBOT_PORTS[i],
                ), 
            daemon=True, 
            name=f"Listen_{i}"
        ))
    """

    # Creating Discovery Thread
    """ TODO: Virtualize discovery """
    """ g.discovery_thread = threading.Thread(target=discovery, daemon=True, name=f"Discovery") """

    # Creating Send Manager Thread
    """ TODO: Virtualize maintenance """
    """ g.send_manager_thread = threading.Thread(target=send_manager, daemon=True, name=f"Send_Manager") """

    # Creating Receive Manager Thread
    """ TODO: Virtualize receive_manager """
    """ g.receive_manager_thread = threading.Thread(target=receive_manager, daemon=True, name=f"Receive_Manager") """

    # Create Threads Specific to CV Enabled Bots
    """ TODO: Virtualize CV specific threads """
    """
    if not g.LEGACY_MODE:
        # Calculate Resultion
        resolution = 720
        for i in range(len(g.cameras) - 1):
            resolution /= 2

        # Initialize Detector
        g.detector = Detector(1280, resolution, g.model, g.modelPath, g.cameras, render = True, tracking = True)

        # Initialize Detector Thread
        g.detector_thread = threading.Thread(target = g.detector.detect, daemon=True, name="Detect")
        
        # Initialize New Visible Thread
        g.new_visible_thread = threading.Thread(target=new_visible, daemon=True, name="New_Visible")

        # Initialize New Lost Thread
        g.new_lost_thread = threading.Thread(target=new_lost, daemon=True, name="New_Lost")
    """

    # Start the threads
    """ start_threads() """

def start_threads():
    # Running Transceiver Receive Threads
    for transceiver_receive_thread in g.transceiver_receive_threads:
        transceiver_receive_thread.start()

    # Running Transceiver Send Threads
    for transceiver_send_thread in g.transceiver_send_threads:
        transceiver_send_thread.start()

    # Running Listen For Connection Threads
    for listen_for_connection_thread in g.listen_for_connection_threads:
        listen_for_connection_thread.start()


    # TODO: Fix Current Bug: For Sending a Payload, If both Robots Run the Discovery Thread, then
    # the socket is closed / destroyed SOMETIMES by one of the robots, causing payload tranmsissions to fail.
    # A temporary fix is to have 1 robot run this discovery thread, until the bug is fixed.
    # Running Discovery Thread
    if g.LEGACY_MODE:
        g.discovery_thread.start()

    # Running Receive Manager Thread
    g.receive_manager_thread.start()

    # Running Send Manager Thread
    g.send_manager_thread.start()

    # On Computer Vision Enabled Bots Only...
    if not g.LEGACY_MODE:
        # Start the Detector Thread
        g.detector_thread.start()

        # Start the New Visible Thread
        g.new_visible_thread.start()

        # Start the New Lost Thread
        g.new_lost_thread.start()

    # Running New Threads based on new Robot Links
    if g.LEGACY_MODE:
        while True:
            robot_link = g.robot_links_new.get()

            thread_number = len(g.robot_links)
            link_send_thread = threading.Thread(target=link_send, args=(robot_link,), daemon=True, name=f"Link_Send_{thread_number}")
            link_send_thread.start()

            link_receive_thread = threading.Thread(target=link_receive, args=(robot_link,), daemon=True, name=f"Link_Receive_{thread_number}")
            link_receive_thread.start()

            maintenance_thread = threading.Thread(target=maintenance, args=(robot_link,), daemon=True, name=f"Maintenance_{thread_number}")
            maintenance_thread.start()
    else:
        # Store Thread Number
        thread_number = 0

        while True:
            # Blocking Call to Get New Robot
            robot = g.newRobotQ.get()

            # Create and Start Link Send Thread
            link_send_thread = threading.Thread(target=link_send, args=[robot], daemon=True, name=f"Link_Send_{thread_number}")
            link_send_thread.start()

            # Create and Start Link Receive Thread
            link_receive_thread = threading.Thread(target=link_receive, args=[robot], daemon=True, name=f"Link_Receive_{thread_number}")
            link_receive_thread.start()

            # Increase Thread Number
            thread_number += 1