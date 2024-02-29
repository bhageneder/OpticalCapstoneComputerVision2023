import time
import threading
import config.global_vars as g

def link_receive(robot_link):
    # This is really bad; it must be changed. I should not be using the datatype like this in the else case.
    if g.LEGACY_MODE:
        thread_name = threading.current_thread().name

        while True:
            # Receive Data From Socket
            # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
            # but it will block until it receives any data, or the connection is closed
            data = robot_link.socket.recv(65536)
            if g.debug_link_receive: print(f'{thread_name} Received: {data}')

            # Terminate if robot_link no longer exists
            if robot_link not in g.robot_links:
                return
    else:
        thread_name = threading.current_thread().name

        while True:
            # Receive Data From Socket
            # socket.recv(65536) will receive at most 65536 bytes from the socket at once,
            # but it will block until it receives any data, or the connection is closed

            # see how bad this is??? really bad
            data = robot_link.robotLink.socket.recv(65536)
            if g.debug_link_receive: print(f'{thread_name} Received: {data}')

            # Terminate if robot_link no longer exists
            with g.visible_mutex and g.lost_mutex:
                if ((robot_link.robotLink not in g.visible) or (robot_link.robotLink not in g.lost)):
                    return