import threading
import socket
import psutil
import config.global_vars as g
from classes.RobotLink import RobotLink
from classes.RobotClass import Robot
import time

# Listen for connection on all 8 possible ports (1 port per thread)
def listen_for_connection(port):
    thread_name = threading.current_thread().name
    # Open a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Listen on the socket, and terminate whatever process may have been using it before if needed
    try:
        server_socket.bind((g.ROBOT_IP_ADDRESS, int(port)))
    except OSError as e:
        if e.errno == socket.errno.EADDRINUSE: # Address already in use
            if g.debug_listen_for_connection: print(f'{thread_name} Address already in use error...')
            return
            # for proc in psutil.process_iter(['pid', 'name', 'connections']):
            #     for conn in proc.info['connections']:
            #         if conn.laddr.port == port:
            #             if g.debug_listen_for_connection: f"{thread_name} Terminating {proc.info['pid']} ({proc.info['name']})")
            #             os.kill(proc.info['pid'], 9)
            # time.sleep(1)
            # server_socket.bind((g.ROBOT_IP_ADDRESS, int(port)))
        else:
            raise e

    server_socket.listen()
    while True:
        client_socket, client_ip_address_and_port = server_socket.accept()
        robot_sending_ip_address = client_ip_address_and_port[0]
        robot_sending_port = client_ip_address_and_port[1]

        if g.debug_listen_for_connection: print(f'{thread_name} Connection Received')

        if g.LEGACY_MODE:
            # Check if the robot link already exists
            for robot_link in g.robot_links:
                if robot_link.ip_address == robot_sending_ip_address:
                    client_socket.close()
                    break
            else:
                # To make the socket never timed out now when sending or receiving data
                client_socket.settimeout(None) 

                # Default the serial port to transceiver 0, Maintenance will set the best one.
                link = RobotLink(None, g.serial_ports[0], client_socket, robot_sending_ip_address, robot_sending_port)
                link.lastPacketTime = time.time()
                with g.robot_links_mutex:
                    g.robot_links.append(link)
                if g.debug_listen_for_connection: print(f'{thread_name} New Robot Link Connected On: ', (robot_sending_ip_address, robot_sending_port))
                # Enqueue new robot link to be maintained
                g.robot_links_new.put(link)
        else:
            # Temporary variable to store combined lists (visible and lost)
            robotLists = list()

            # Get the lists
            with g.visible_mutex and g.lost_mutex:
                robotLists = g.visible + g.lost
            
            # Check if the robot link already exists
            for robot in robotLists:
                if (robot.robotLink is not None) and robot.robotLink.ip_address == robot_sending_ip_address:
                    client_socket.close()
                    break
            else:
                # To make the socket never timed out now when sending or receiving data
                client_socket.settimeout(None) 

                # Default the serial port to 0. Detector will set the best one when it finds it. Transceiver on robot object is used instead of port
                link = RobotLink(None, g.serial_ports[0], client_socket, robot_sending_ip_address, robot_sending_port)
                link.lastPacketTime = time.time()

                # Create Robot
                robot = Robot(-1, -1, link) # check if there is a way to get the transceiver here...

                # Append the Robot to the Global Lost Robot List
                with g.lost_mutex:
                    g.lost.append(robot)

                # Debug Statement
                if g.debug_listen_for_connection: print(f'{thread_name} New Robot Connected On: ', (robot_sending_ip_address, robot_sending_port))
                
                # Queue the New Robot
                g.newRobotQ.put(robot)