import time
import threading
from classes.RobotLink import RobotLink
from classes.RobotClass import Robot
import config.global_vars as g
import socket

def link_receive(generic):
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

    while True:
        if robot.robotLink is not None:
            # Receive Data From Socket
            # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
            # but it will block until it receives any data, or the connection is closed
            data = robot.robotLink.socket.recv(65536)
            if g.debug_link_receive: print(f'{thread_name} Received: {data}')

            # Update last packet time
            robot.robotLink.lastPacketTime = time.time()

            # Socket was destroyed
            if(data == b''):
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
                        robot.robotLink.socket.shutdown(socket.SHUT_RDWR)
                        robot.robotLink.socket.close()
                
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
                
def link_receive_legacy(robot_link):
    thread_name = threading.current_thread().name

    while True:
        # Receive Data From Socket
        # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
        # but it will block until it receives any data, or the connection is closed
        data = robot_link.socket.recv(65536)
        if g.debug_link_receive: print(f'{thread_name} Received: {data}')

        # Update last packet time
        robot_link.lastPacketTime = time.time()

        # Socket was destroyed
        if(data == b''):
            # Check if link is active (ensures we don't try to close the socket twice)
            if robot_link.active:
                # Make robotLink inactive
                robot_link.active = False
                
                # Close socket
                robot_link.socket.shutdown(socket.SHUT_RDWR)
                robot_link.socket.close()

            # Remove from the robot_links list
            if (robot_link in g.robot_links):
                g.robot_links.remove(robot_link)

            if g.debug_link_receive: print(f'{thread_name} Exiting. Socket was destroyed')
            return

        # Terminate if robot_link no longer exists
        if robot_link not in g.robot_links:
            return