import threading
import socket
import psutil
import config.global_vars as g
from classes.RobotLink import RobotLink

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

        for robot_link in g.robot_links:
            if robot_link.ip_address == robot_sending_ip_address:
                client_socket.close()
                break
        else:
            # To make the socket never timed out now when sending or receiving data
            client_socket.settimeout(None) 

            if g.LEGACY_MODE:
                # Default the serial port to transceiver 0, Maintenance will set the best one.
                link = RobotLink(None, g.serial_ports[0], client_socket, robot_sending_ip_address, robot_sending_port)
                with g.robot_links_mutex:
                    g.robot_links.append(link)
                if g.debug_listen_for_connection: print(f'{thread_name} New Robot Link Connected On: ', (robot_sending_ip_address, robot_sending_port))
                # Enqueue new robot link to be maintained
                g.robot_links_new.put(link)
            else:
                # Default the serial port to 0. Detector will set the best one when it finds it. Transceiver on robot object is used instead of port
                link = RobotLink(None, g.serial_ports[0], client_socket, robot_sending_ip_address, robot_sending_port)
                with g.lost_mutex:
                    g.lost.append(link)
                if g.debug_listen_for_connection: print(f'{thread_name} New Robot Link Connected On: ', (robot_sending_ip_address, robot_sending_port))