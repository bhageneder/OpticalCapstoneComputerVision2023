import threading
import time
from sim.controller.classes.vRobotLink import vRobotLink
from sim.controller.classes.vSocket import vSocket

def v_mini_node_discovery(robot_receiving_ip_address, robot, vg):
    
    thread_name = threading.current_thread().name

    if vg.debug_mini_discovery: print(f'{thread_name} Connected')

    for r in (vg.visible + vg.lost):
        if ((r.robotLink is not None) and (r.robotLink.ip_address == robot_receiving_ip_address)):
            break
    else:
        # "Socket" can be established
        socket = vSocket(vg, robot_receiving_ip_address)

        # Default the serial port to transceiver 0, Maintenance will set the best one.
        link = vRobotLink(None, socket, robot_receiving_ip_address)

        if vg.debug_mini_discovery: print(f'{thread_name} New Robot Link Found On: ', (robot_receiving_ip_address))
        robot.robotLink = link
