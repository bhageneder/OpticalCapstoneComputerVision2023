import time
import threading
import sim.sim_global_vars as sg


def v_test_single_hop(vg):
    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    while True:
        # We will target sending single hop data only to ...10
        ipForSingleHop = vg.router.findRoute("10.0.0.10")

        if ipForSingleHop == None:
            # Sleep the Link Send Thread
            # print(f"{vg.ip} none")
            time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)
            continue

        # Find robot with ip matching the best route
        robot = None
        
        with vg.visible_mutex:
            for r in vg.visible:
                if r.IP == ipForSingleHop:
                    robot = r
                    # print(f"{vg.ip} found robot with ip {r.IP}")

        if robot is None:
            # Sleep the Link Send Thread
            time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)
            continue

        if robot.robotLink is not None:
            # print(f"{vg.ip} sending to robot with ip {robot.IP}")
            # Send Payload through Socket 
            if vg.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
            # packet = \x00 + IP_to + \x00 + IP_from + \x00 + Payload + Payload_Number
            # robot.robotLink.socket.sendall("\x00" + str(robot.IP) + "\x00 " + vg.ip + "\x00 " + str(payload + send_num.to_bytes(4, byteorder="little")))
            # packet = \x00 + IP_to + \x00 + IP_from + \x00 + \x02 + \x00 + IP_forward + \x00 + Payload + Payload_Number
            # forward_flag = \x02
            robot.robotLink.socket.sendall("\x00" + str(robot.IP) + "\x00 " + vg.ip + "\x00 " + "\x02 " + "\x00 " + "10.0.0.10" + "\x00 " + str(payload + send_num.to_bytes(4, byteorder="little")))

        # Sleep the Link Send Thread
        time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)