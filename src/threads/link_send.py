import time
import threading
import global_vars as global_vars

def link_send(robot_link):
    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    while True:
        # Send Payload through Socket 
        if global_vars.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
        robot_link.socket.sendall(payload + send_num.to_bytes(4, byteorder="little"))

        send_num += 1
        time.sleep(global_vars.PAYLOAD_INTERVAL_SLEEP)

        # Terminate if robot_link no longer exists
        if robot_link not in global_vars.robot_links:
            return
