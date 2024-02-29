import threading
import socket
import config.global_vars as g
from classes.RobotLink import RobotLink
from functions import led_manager as lc

# For n Robots:
# n - 1 possible IP addresses (not including our own), and 8 possible ports. (n - 1) * 8 threads need to be ran
def mini_discovery(robot_receiving_ip_address, dst_port, client_port, robot):
    thread_name = threading.current_thread().name
    # Open a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        for robot in g.visible:
            if robot.robotLink.ip_address == robot_receiving_ip_address:
                break
        else:
            if g.debug_mini_discovery: print(f'{thread_name} Attempting To Connect To: ', (robot_receiving_ip_address, int(dst_port)))
            # If there is no Robot Link that the robot_receiving_ip_address: 
            # Send SYN packets using send manager
            client_socket.connect((robot_receiving_ip_address, int(dst_port)))

            ''' ### NeoPixel Ring, Needs to be Updated. Use robot.transceiver
            # if no robot found, make all transceivers red
            if best_transceiver_number == -1:
                #for transceiver in g.best_transceiver:
                lc.illuminate_for_finding(best_transceiver_number)
            # if robot found, make that transceiver blue
            else:
                lc.illuminate_for_connecting(best_transceiver_number)
            '''
    except socket.timeout:
        ''' ### NeoPixel continued
        #if g.debug_mini_discovery: print(f'{thread_name} Socket Timeout')
        #for transceiver in g.best_transceiver:
        lc.turn_off_for_finding(g.best_transceiver)
        lc.turn_off_for_connecting(g.best_transceiver)
        '''
        client_socket.close() # Close the socket to unbind it
        return
    
    if g.debug_mini_discovery: print(f'{thread_name} Connected')
    
    for robot in g.visible:
            if robot.robotLink.ip_address == robot_receiving_ip_address:
                break
    else:
        # To make the socket never timed out now when sending or receiving data
        client_socket.settimeout(None) 

        ''' ### NeoPixel
        #for transceiver in g.best_transceiver:
        lc.turn_off_for_finding(g.best_transceiver)
        lc.turn_off_for_connecting(g.best_transceiver)
        '''

        # Default the serial port to transceiver 0, Maintenance will set the best one.
        link = RobotLink(None, g.serial_ports[0], client_socket, robot_receiving_ip_address, dst_port)
        if g.debug_mini_discovery: print(f'{thread_name} New Robot Link Found On: ', (robot_receiving_ip_address, int(dst_port)))
        robot.robotLink = link