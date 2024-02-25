import time
import threading
from config.global_vars import global_vars

def link_receive(robot_link):
    thread_name = threading.current_thread().name

    while True:
        # Receive Data From Socket
        # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
        # but it will block until it receives any data, or the connection is closed
        data = robot_link.socket.recv(65536)
        if global_vars.debug_link_receive: print(f'{thread_name} Received: {data}')

        # Terminate if robot_link no longer exists
        if robot_link not in global_vars.robot_links:
            return
