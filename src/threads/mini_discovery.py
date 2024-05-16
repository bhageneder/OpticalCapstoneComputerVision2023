import threading
import socket
import config.global_vars as g
from classes.RobotLink import RobotLink
import time

# For n Robots:
# n - 1 possible IP addresses (not including our own), and 8 possible ports. (n - 1) * 8 threads need to be ran
def mini_discovery(robot_receiving_ip_address, dst_port, client_port):
    thread_name = threading.current_thread().name
    # Open a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.settimeout(g.SOCKET_CONNECTION_TIMEOUT)
    try:
        # Need to bind to the IP adress we want the server to see us as
        client_socket.bind((g.ROBOT_IP_ADDRESS, int(client_port)))
        if g.debug_mini_discovery: print(f'{thread_name} Binding On: ', (g.ROBOT_IP_ADDRESS, int(client_port)))
    except socket.error:
        if g.debug_mini_discovery: print(f'{thread_name} Socket Error - Failed to Bind On: ', (g.ROBOT_IP_ADDRESS, int(client_port)))
        # Socket already in use, a previous thread already successfully connected
        return
    try:
        for robot_link in g.robot_links:
            if robot_link.ip_address == robot_receiving_ip_address:
                break
        else:
            if g.debug_mini_discovery: print(f'{thread_name} Attempting To Connect To: ', (robot_receiving_ip_address, int(dst_port)))
            # If there is no Robot Link that the robot_receiving_ip_address: 
            # Send SYN packets using send manager
            client_socket.connect((robot_receiving_ip_address, int(dst_port)))
    except socket.timeout:
        #if g.debug_mini_discovery: print(f'{thread_name} Socket Timeout')
        client_socket.close() # Close the socket to unbind it
        return
    
    if g.debug_mini_discovery: print(f'{thread_name} Connected')
    for robot_link in g.robot_links:
        if robot_link.ip_address == robot_receiving_ip_address:
            break
    else:
        # To make the socket never timed out now when sending or receiving data
        client_socket.settimeout(None) 

        # Default the serial port to transceiver 0, Maintenance will set the best one.
        link = RobotLink(None, g.serial_ports[0], client_socket, robot_receiving_ip_address, dst_port)
        link.lastPacketTime = time.time()

        if g.debug_mini_discovery: print(f'{thread_name} New Robot Link Found On: ', (robot_receiving_ip_address, int(dst_port)))
        with g.robot_links_mutex:
            g.robot_links.append(link)
        
        # Set the Discovery End Time (used for the discovery time calculations)
        g.discovery_end_time = time.time()

        # Mark Robot Object as the Discover-er (used for the discovery time calculations)
        link.discoverer = True

        # Enqueue new robot link to be 
        g.robot_links_new.put(link)