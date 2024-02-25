import threading
import socket
import psutil
from config.global_vars import global_vars
from src.classes.RobotLink import RobotLink

# Listen for connection on all 8 possible ports (1 port per thread)
def listen_for_connection(port):
    thread_name = threading.current_thread().name
    # Open a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Listen on the socket, and terminate whatever process may have been using it before if needed
    try:
        server_socket.bind((global_vars.ROBOT_IP_ADDRESS, int(port)))
    except OSError as e:
        if e.errno == socket.errno.EADDRINUSE: # Address already in use
            if global_vars.debug_listen_for_connection: print(f'{thread_name} Address already in use error...')
            return
            # for proc in psutil.process_iter(['pid', 'name', 'connections']):
            #     for conn in proc.info['connections']:
            #         if conn.laddr.port == port:
            #             if global_vars.debug_listen_for_connection: f"{thread_name} Terminating {proc.info['pid']} ({proc.info['name']})")
            #             os.kill(proc.info['pid'], 9)
            # time.sleep(1)
            # server_socket.bind((global_vars.ROBOT_IP_ADDRESS, int(port)))
        else:
            raise e

    server_socket.listen()
    while True:
        client_socket, client_ip_address_and_port = server_socket.accept()
        robot_sending_ip_address = client_ip_address_and_port[0]
        robot_sending_port = client_ip_address_and_port[1]

        if global_vars.debug_listen_for_connection: print(f'{thread_name} Connection Received')

        for robot_link in global_vars.robot_links:
            if robot_link.ip_address == robot_sending_ip_address:
                client_socket.close()
                break
        else:
            # To make the socket never timed out now when sending or receiving data
            client_socket.settimeout(None) 

            # Default the serial port to transceiver 0, Maintenance will set the best one.
            link = RobotLink(None, global_vars.serial_ports[0], client_socket, robot_sending_ip_address, robot_sending_port)
            with global_vars.robot_links_mutex:
                global_vars.robot_links.append(link)
            if global_vars.debug_listen_for_connection: print(f'{thread_name} New Robot Link Connected On: ', (robot_sending_ip_address, robot_sending_port))
            # Enqueue new robot link to be maintained
            global_vars.robot_links_new.put(link)
