import threading
import globals
import socket
import sys
sys.path.append('./')
from robot_link import RobotLink

# For 8 Robots:
# 7 possible IP addresses (not including our own), and 8 possible ports. 7 * 8 = 56 threads need to be ran
def mini_discovery(robot_receiving_ip_address, dst_port, client_port):
    thread_name = threading.current_thread().name
    # Open a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(globals.SOCKET_CONNECTION_TIMEOUT)
    try:
        # Need to bind to the IP adress we want the server to see us as
        client_socket.bind((globals.ROBOT_IP_ADDRESS, int(client_port)))
        if globals.debug_mini_discovery: print(f'{thread_name} Binding On: ', (globals.ROBOT_IP_ADDRESS, int(client_port)))
    except socket.error:
        if globals.debug_mini_discovery: print(f'{thread_name} Socket Error - Failed to Bind On: ', (globals.ROBOT_IP_ADDRESS, int(client_port)))
        # Socket already in use, a previous thread already successfully connected
        return
    try:
        for robot_link in globals.robot_links:
            if robot_link.ip_address == robot_receiving_ip_address:
                break
        else:
            if globals.debug_mini_discovery: print(f'{thread_name} Attempting To Connect To: ', (robot_receiving_ip_address, int(dst_port)))
            # If there is no Robot Link that the robot_receiving_ip_address: 
            client_socket.connect((robot_receiving_ip_address, int(dst_port)))
    except socket.timeout:
        #if globals.debug_mini_discovery: print(f'{thread_name} Socket Timeout')
        client_socket.close() # Close the socket to unbind it
        return
    
    if globals.debug_mini_discovery: print(f'{thread_name} Connected')
    for robot_link in globals.robot_links:
        if robot_link.ip_address == robot_receiving_ip_address:
            break
    else:
        # To make the socket never timed out now when sending or receiving data
        client_socket.settimeout(None) 

        # Default the serial port to transceiver 0, Maintenance will set the best one.
        link = RobotLink(None, globals.serial_ports[0], client_socket, robot_receiving_ip_address, dst_port)
        if globals.debug_mini_discovery: print(f'{thread_name} New Robot Link Found On: ', (robot_receiving_ip_address, int(dst_port)))
        with globals.robot_links_mutex:
            globals.robot_links.append(link)
        # Enqueue new robot link to be maintained
        globals.robot_links_new.put(link)
            
            
       