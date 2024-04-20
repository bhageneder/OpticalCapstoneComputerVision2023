import socket
import threading
import time
from classes.RobotLink import RobotLink


def v_mini_node_discovery(robot_receiving_ip_address, dst_port, client_port, robot, vg):
    print("Virtualized v_mini_node_discovery")
    
    thread_name = threading.current_thread().name
    # Open a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(vg.SOCKET_CONNECTION_TIMEOUT)
    try:
        # Need to bind to the IP adress we want the server to see us as
        client_socket.bind((vg.ROBOT_IP_ADDRESS, int(client_port)))
        if vg.debug_mini_discovery: print(f'{thread_name} Binding On: ', (vg.ROBOT_IP_ADDRESS, int(client_port)))
    except socket.error:
        if vg.debug_mini_discovery: print(f'{thread_name} Socket Error - Failed to Bind On: ', (vg.ROBOT_IP_ADDRESS, int(client_port)))
        # Socket already in use, a previous thread already successfully connected
        return
    try:
        for robot in (vg.visible + vg.lost):
            if ((robot.robotLink is not None) and (robot.robotLink.ip_address == robot_receiving_ip_address)):
                break
        else:
            if vg.debug_mini_discovery: print(f'{thread_name} Attempting To Connect To: ', (robot_receiving_ip_address, int(dst_port)))
            # If there is no Robot Link that the robot_receiving_ip_address: 
            # Send SYN packets using send manager
            client_socket.connect((robot_receiving_ip_address, int(dst_port)))

    except socket.timeout:
        client_socket.close() # Close the socket to unbind it
        return
    
    if vg.debug_mini_discovery: print(f'{thread_name} Connected')

    for robot in (vg.visible + vg.lost):
            if ((robot.robotLink is not None) and (robot.robotLink.ip_address == robot_receiving_ip_address)):
                break
    else:
        # To make the socket never timed out now when sending or receiving data
        client_socket.settimeout(None) 

        # Default the serial port to transceiver 0, Maintenance will set the best one.
        link = RobotLink(None, vg.serial_ports[0], client_socket, robot_receiving_ip_address, dst_port)
        link.lastPacketTime = time.time()

        if vg.debug_mini_discovery: print(f'{thread_name} New Robot Link Found On: ', (robot_receiving_ip_address, int(dst_port)))
        robot.robotLink = link
