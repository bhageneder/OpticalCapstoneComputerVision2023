import time
import threading
from classes.RobotLink import RobotLink
from classes.RobotClass import Robot
import config.global_vars as g

# Calls the correct link send version depending upon mode. Checks the type of the parameter to ensure type safety.
def link_send(generic):
    if g.LEGACY_MODE:
        if isinstance(generic, RobotLink):
            link_send_legacy(generic)
        else: 
            raise Exception("Type Error: link_send() takes generic parameter as type RobotLink in Legacy Mode")
    else:
        if isinstance(generic, Robot):
            robot_send(generic)
        else:
            raise Exception("Type Error: link_send() takes generic parameter as type Robot when not in Legacy Mode")

                
def robot_send(robot):
    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    while True:
        if robot.robotLink is not None:
            # Send Payload through Socket 
            if g.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
            try:
                robot.robotLink.socket.sendall(payload + send_num.to_bytes(4, byteorder="little"))
            except OSError as e:
                if (str(e) != "[Errno 9] Bad file descriptor"):
                    raise(e)

            send_num += 1

            # Update last packet time
            robot.robotLink.lastPacketTime = time.time()

        # Terminate if Robot no longer exists
        with g.visible_mutex and g.lost_mutex:
            if ((robot not in g.visible) and (robot not in g.lost)):
                if g.debug_link_send: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return

        # Sleep the Link Send Thread
        time.sleep(g.PAYLOAD_INTERVAL_SLEEP)

def link_send_legacy(robot_link):
    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    while True:
        # Send Payload through Socket 
        if g.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
        robot_link.socket.sendall(payload + send_num.to_bytes(4, byteorder="little"))

        # Update last packet time
        robot_link.lastPacketTime = time.time()

        send_num += 1
        time.sleep(g.PAYLOAD_INTERVAL_SLEEP)

        # Terminate if robot_link no longer exists
        if robot_link not in g.robot_links:
            return