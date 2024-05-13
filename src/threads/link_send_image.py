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

    # Send the Payload
    payload = utilities.deconstruct_file('/home/pi/repos/OpticalCommunications-2023/python_implementation/doge.png')

    # Ensure RobotLink is Established
    while robot.robotLink is None:
        continue

    # Send Payload through Socket 
    if g.debug_link_send: print(f'{thread_name} Sending Deconstrcuted File Payload Through TCP Socket')
    try:
        robot.robotLink.socket.sendall(payload)
    except OSError as e:
        if (str(e) == "[Errno 9] Bad file descriptor"):
            print(f"Handled Bad File Descriptor Error in {thread_name}")
            return
        else:
            print(f"Handled excpetion in {thread_name} on socket.sendall(...). Exception: {e}")
            return
        
    if g.debug_link_send: print(f'{thread_name} Finished Sending Deconstructed File Payload Through TCP Socket')


def link_send_legacy(robot_link):
    thread_name = threading.current_thread().name

    # Send the Payload
    payload = utilities.deconstruct_file('/home/pi/repos/OpticalCommunications-2023/python_implementation/doge.png')
    
    # Send Payload through Socket 
    if g.debug_link_send: print(f'{thread_name} Sending Deconstrcuted File Payload Through TCP Socket')
    try:
        robot_link.socket.sendall(payload)
    except OSError as e:
        if (str(e) == "[Errno 9] Bad file descriptor"):
            print(f"Handled Bad File Descriptor Error in {thread_name}")
            return
        else:
            print(f"Handled excpetion in {thread_name} on socket.sendall(...). Exception: {e}")
            return
        
    if g.debug_link_send: print(f'{thread_name} Finished Sending Deconstructed File Payload Through TCP Socket')