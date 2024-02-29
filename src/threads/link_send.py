import time
import threading
import config.global_vars as g

def link_send(robot_link):
    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    # really bad as well

    if g.LEGACY_MODE:
        while True:
            # Send Payload through Socket 
            if g.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
            robot_link.socket.sendall(payload + send_num.to_bytes(4, byteorder="little"))

            send_num += 1
            time.sleep(g.PAYLOAD_INTERVAL_SLEEP)

            # Terminate if robot_link no longer exists
            if robot_link not in g.robot_links:
                return
    else:
        while True:
            # Send Payload through Socket 
            if g.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
            robot_link.robotLink.socket.sendall(payload + send_num.to_bytes(4, byteorder="little"))

            send_num += 1
            time.sleep(g.PAYLOAD_INTERVAL_SLEEP)

            # Terminate if robot_link no longer exists
            with g.visible_mutex and g.lost_mutex:
                if ((robot_link.robotLink not in g.visible) or (robot_link.robotLink not in g.lost)):
                    return
