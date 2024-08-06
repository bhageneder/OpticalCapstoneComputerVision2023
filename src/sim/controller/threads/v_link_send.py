import time
import threading
import sim.sim_global_vars as sg

def v_link_send(robot, vg):
    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    while (True):
        if robot.robotLink is not None:

            # Send Payload through Socket 
            if vg.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
            # packet = \x00 + IP_to + \x00 + IP_from + \x00 + Payload + Payload_Number
            robot.robotLink.socket.sendall("\x00" + str(robot.IP) + "\x00 " + vg.ip + "\x00 " + str(payload + send_num.to_bytes(4, byteorder="little")))

            # Prototyping sending routing info (1 extra hop only)
            if (send_num % 5 == 0):
                robots = list()
                
                for r in vg.visible:
                    robots.append((r.IP, 1))

                robot.robotLink.socket.sendall("\x00" + str(robot.IP) + "\x00 " + vg.ip + "\x00 " + "\x11 " + str(robots))
                
            send_num += 1

        # Terminate if Robot no longer exists
        with vg.visible_mutex and vg.lost_mutex:
            if ((robot not in vg.visible) and (robot not in vg.lost)):
                if vg.debug_link_send: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return

        # Sleep the Link Send Thread
        time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)