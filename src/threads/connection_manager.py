import time
import socket
import threading
from classes.RobotLink import RobotLink
from classes.RobotClass import Robot
import config.global_vars as g

def connection_manager(generic):
    if g.LEGACY_MODE:
        if isinstance(generic, RobotLink):
            robot_link_manager(generic)
        else: 
            raise Exception("Type Error: connection_manager() takes generic parameter as type RobotLink in Legacy Mode")
    else:
        if isinstance(generic, Robot):
            robot_manager(generic)
        else:
            raise Exception("Type Error: connection_manager() takes generic parameter as type Robot when not in Legacy Mode")

def robot_manager(robot):
    thread_name = threading.current_thread().name

    timeout = g.SOCKET_TRANSMISSION_TIMEOUT

    while True:
        # Calculate delta for last packet
        delta = time.time() - robot.robotLink.lastPacketTime

        # Check if the robot has received data within the timeout period
        if (delta > timeout):
            # Check if link is active (ensures we don't try to close the socket twice)
            if robot.robotLink.active:
                # Make robotLink inactive
                robot.robotLink.active = False

                # Close connection
                robot.robotLink.socket.shutdown(socket.SHUT_RDWR)
                robot.robotLink.socket.close()

            # Remove from robot lists
            with g.visible_mutex and g.lost_mutex:
                if (robot in g.visible):
                    g.visible.remove(robot)
                elif (robot in g.lost):
                    g.lost.remove(robot)

            if g.debug_connection_manager: print(f'{thread_name} Exiting. Robot with IP {robot.IP} timed out')
            return
        
        # Sleep for remaining time in timeout
        time.sleep(timeout - delta)

        # Terminate if Robot no longer exists
        with g.visible_mutex and g.lost_mutex:
            if ((robot not in g.visible) and (robot not in g.lost)):
                if g.debug_connection_manager: print(f'{thread_name} Exiting. Robot with ip {robot.IP} is Not in Visible or Lost List')
                return

def robot_link_manager(robotLink):
    thread_name = threading.current_thread().name

    timeout = g.SOCKET_TRANSMISSION_TIMEOUT

    while True:
        # Calculate delta for last packet
        delta = time.time() - robotLink.lastPacketTime

        # Check if the robot has received data within the timeout period
        if (delta > timeout):
            # Check if link is active (ensures we don't try to close the socket twice)
            if robotLink.active:
                # Make robotLink inactive
                robotLink.active = False

                # Close connection
                robotLink.socket.shutdown(socket.SHUT_RDWR)
                robotLink.socket.close()

            # Remove from robot_links list
            if (robotLink in g.robot_links):
                g.robot_links.remove(robotLink)

            if g.debug_connection_manager: print(f'{thread_name} Exiting. Robot with IP {robotLink.ip_address} timed out')
            return
        
        # Sleep for remaining time in timeout
        time.sleep(timeout - delta)

        # Terminate if robot_link no longer exists
        if robotLink not in g.robot_links:
            return