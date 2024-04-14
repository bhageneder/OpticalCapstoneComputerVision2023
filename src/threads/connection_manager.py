import time
import config.global_vars as g
import socket
import threading

def connection_manager(robot):
    thread_name = threading.current_thread().name

    timeout = g.SOCKET_CONNECTION_TIMEOUT

    while True:
        # Calculate delta for last packet
        delta = time.time() - robot.tLastPacket

        # Check if the robot has received data within the timeout period
        if (delta > timeout):
            # Close connection
            robot.robotLink.socket.shutdown(socket.SHUT_RDWR)
            robot.robotLink.socket.close()

            # Remove from robot lists
            with g.visible_mutex and g.lost_mutex:
                if (robot in g.visible):
                    g.visible.remove(robot)
                elif (robot in g.lost):
                    g.lost.remove(robot)

            if g.debug_connection_manager: print(f'{thread_name} Exiting. Robot with IP {robot.IP} timed out')
            return

        # Terminate if Robot no longer exists
        with g.visible_mutex and g.lost_mutex:
            if ((robot not in g.visible) and (robot not in g.lost)):
                if g.debug_connection_manager: print(f'{thread_name} Exiting. Robot with ip {robot.IP} is Not in Visible or Lost List')
                return