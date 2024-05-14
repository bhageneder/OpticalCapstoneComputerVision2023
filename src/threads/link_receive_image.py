import time
import threading
from classes.RobotLink import RobotLink
from classes.RobotClass import Robot
import config.global_vars as g
import functions.utilities as utilities
import socket

def link_receive_image(generic):
    if g.LEGACY_MODE:
        if isinstance(generic, RobotLink):
            link_receive_legacy(generic)
        else:
            raise Exception("Type Error: link_receive() takes generic parameter as type RobotLink in Legacy Mode") 
    else:
        if isinstance(generic, Robot):
            robot_receive(generic)
        else:
            raise Exception("Type Error: link_receive() takes generic parameter as type Robot when not in Legacy Mode")
            
        
def robot_receive(robot):
    thread_name = threading.current_thread().name

    # Init variables
    data = bytearray()
    received_data_length = 0
    expected_length = 215618

    # Ensure RobotLink is Established
    while robot.robotLink is None:
        continue

    # Get the Starting Time
    start_time = time.perf_counter()

    while received_data_length < expected_length:
        if robot.robotLink is not None:
            # Receive Data From Socket
            # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
            # but it will block until it receives any data, or the connection is closed
            try:
                buffer = robot.robotLink.socket.recv(65536)
                data += buffer
                received_data_length += len(buffer)
                if g.debug_link_receive: print(f"Progress: {round((received_data_length/expected_length) * 100, 1)} %     {round(time.perf_counter()-start_time,2)} s")
            except Exception as e:
                if g.debug_link_receive: print(f"{thread_name} Caught Error: {e}")
                return

            # Update last packet time
            robot.robotLink.lastPacketTime = time.time()

            # Socket was destroyed
            if(buffer == b''):
                # Determine if the socket is in use by another robot
                # This happens if the robot was deleted and a new one placed in its stead with same socket
                with g.visible_mutex:
                    otherInVisible = next((x for x in g.visible if ((x.robotLink is robot.robotLink) and (x is not robot))), None) is not None
                with g.lost_mutex:
                    otherInLost = next((x for x in g.lost if ((x.robotLink is robot.robotLink) and (x is not robot))), None) is not None
                
                socketInUse = otherInVisible or otherInLost

                # If the socket is not in use anymore
                if not socketInUse:
                    # Check if link is active (ensures we don't try to close the socket twice)
                    if robot.robotLink.active:
                        # Make robotLink inactive
                        robot.robotLink.active = False

                        # Close socket
                        try:
                            robot.robotLink.socket.shutdown(socket.SHUT_RDWR)
                            robot.robotLink.socket.close()
                        except Exception as e:
                            print(f"Handled excpetion in {thread_name} on socket shutdown/close. Exception: {e}")
                
                # Remove from robot lists
                with g.visible_mutex and g.lost_mutex:
                    if (robot in g.visible):
                        g.visible.remove(robot)
                    elif (robot in g.lost):
                        g.lost.remove(robot)

                if g.debug_link_receive: print(f'{thread_name} Exiting. Socket was destroyed')
                return

        # Terminate if Robot no longer exists
        with g.visible_mutex and g.lost_mutex:
            if ((robot not in g.visible) and (robot not in g.lost)):
                if g.debug_link_receive: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return

    utilities.construct_file(data, g.working_dir + f'received{str(time.time())}', ".png")
                
def link_receive_legacy(robot_link):
    thread_name = threading.current_thread().name

    # Initialize Variables
    data = bytearray()
    received_data_length = 0
    expected_length = 215618

    # Get the Starting Time
    start_time = time.perf_counter()

    while received_data_length < expected_length:
        if robot_link is not None:
            # Receive Data From Socket
            # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
            # but it will block until it receives any data, or the connection is closed
            try:
                buffer = robot_link.socket.recv(65536)
                data += buffer
                received_data_length += len(buffer)
                if g.debug_link_receive: print(f"Progress: {round((received_data_length/expected_length) * 100, 1)} %     {round(time.perf_counter()-start_time,2)} s")
            except Exception as e:
                if g.debug_link_receive: print(f"{thread_name} Caught Error: {e}")
                return

            # Update last packet time
            robot_link.lastPacketTime = time.time()

        # Socket was destroyed
        if(data == b''):
            # Check if link is active (ensures we don't try to close the socket twice)
            if robot_link.active:
                # Make robotLink inactive
                robot_link.active = False
                
                # Close socket
                try:
                    robot_link.socket.shutdown(socket.SHUT_RDWR)
                    robot_link.socket.close()
                except Exception as e:
                    print(f"Handled excpetion in {thread_name} on socket shutdown/close. Exception: {e}")

            # Remove from the robot_links list
            if (robot_link in g.robot_links):
                g.robot_links.remove(robot_link)

            if g.debug_link_receive: print(f'{thread_name} Exiting. Socket was destroyed')
            return

        # Terminate if robot_link no longer exists
        if robot_link not in g.robot_links:
            return

    utilities.construct_file(data, g.working_dir + f'received{str(time.time())}', ".png")