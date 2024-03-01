import time
import threading
from classes.RobotLink import RobotLink
from classes.RobotClass import Robot
import config.global_vars as g

def link_receive(generic):
    if g.LEGACY_MODE:
        if type(generic) is not type(RobotLink):
            raise Exception("Type Error: link_receive() takes generic parameter as type RobotLink in Legacy Mode")
        else:
            link_receive_legacy(generic)
    else:
        if type(generic) is not type(Robot):
            raise Exception("Type Error: link_receive() takes generic parameter as type Robot when not in Legacy Mode")
        else:
            robot_receive(generic)
        
def robot_receive(robot):
    thread_name = threading.current_thread().name

    while True:
        # Receive Data From Socket
        # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
        # but it will block until it receives any data, or the connection is closed
        data = robot.robotLink.socket.recv(65536)
        if g.debug_link_receive: print(f'{thread_name} Received: {data}')

        # Terminate if robot_link no longer exists
        with g.visible_mutex and g.lost_mutex:
            if ((robot.robotLink not in g.visible) or (robot.robotLink not in g.lost)):
                return
                
def link_receive_legacy(robot_link):
    thread_name = threading.current_thread().name

    while True:
        # Receive Data From Socket
        # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
        # but it will block until it receives any data, or the connection is closed
        data = robot_link.socket.recv(65536)
        if g.debug_link_receive: print(f'{thread_name} Received: {data}')

        # Terminate if robot_link no longer exists
        if robot_link not in g.robot_links:
            return