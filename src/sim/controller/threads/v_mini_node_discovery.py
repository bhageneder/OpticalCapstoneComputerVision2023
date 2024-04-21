import socket
import threading
import time
from controller.classes.vRobotLink import vRobotLink

def v_mini_node_discovery(robot_receiving_ip_address, vg):
    robot = None
    
    thread_name = threading.current_thread().name

    if vg.debug_mini_discovery: print(f'{thread_name} Connected')

    for r in (vg.visible + vg.lost):
            if ((r.robotLink is not None) and (r.robotLink.ip_address == robot_receiving_ip_address)):
                robot = r
                break
    else:
        # Default the serial port to transceiver 0, Maintenance will set the best one.
        link = vRobotLink(None, robot_receiving_ip_address)
        link.lastPacketTime = time.time()

        if vg.debug_mini_discovery: print(f'{thread_name} New Robot Link Found On: ', (robot_receiving_ip_address))
        robot.robotLink = link
