import time
import threading
# import random
import sim.sim_global_vars as sg

def v_link_send(robot, vg):
    # thread_name = threading.current_thread().name
    # payload = "hello"
    # # payload = []
    
    # # for byte in payload_string.split(" "):
    # #     payload.append(byte)
    
    # send_num = 0
    # tag = vg.ip 

    thread_name = threading.current_thread().name
    payload = b'hello'
    send_num = 0

    while (True):
        if robot.robotLink is not None:

            # Send Payload through Socket 
            if vg.debug_link_send: print(f'{thread_name} Sending Payload through TCP Socket {payload}{send_num}')
            robot.robotLink.socket.sendall("\x00" + vg.ip + "\x00" + str(payload) + str(send_num.to_bytes(4, byteorder="little")))

            send_num += 1

        # Terminate if Robot no longer exists
        with vg.visible_mutex and vg.lost_mutex:
            if ((robot not in vg.visible) and (robot not in vg.lost)):
                if vg.debug_link_send: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return

        # Sleep the Link Send Thread
        time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)

            # # Send Payload
            # with vg.visible_mutex:
            #     sendingTo = robot.robotLink.ip_address
            #     if ((sendingTo in vg.detector.commsAvailable) and (robot in vg.visible)):

            #         # Check if a payload needs to be forwarded
            #         if (vg.forwarders[int(sendingTo.split(".")[-1])-10].qsize() > 0 and bool(random.getrandbits(1))):
            #             payload = vg.forwarders[int(sendingTo.split(".")[-1])-10].get()
                        
            #             if vg.debug_link_send: ("Sending Payload To: {}".format(tag))
            #             # Access receiving robots dataQ
            #             with sg.data_mutex:
            #                 dataQ = sg.listOfDataQ[int(sendingTo.split(".")[-1])-10]
            #                 # Send data with tag
            #                 if vg.debug_link_send: print(f'{thread_name} Forwarding payload through dataQ {payload}')
            #                 dataQ.put(payload + " " + tag, timeout=3)

            #         else:
            #             if vg.debug_link_send: ("Sending Payload To: {}".format(tag))
            #             # Access receiving robots dataQ
            #             with sg.data_mutex:
            #                 dataQ = sg.listOfDataQ[int(sendingTo.split(".")[-1])-10]
            #                 # Send data with tag
            #                 if vg.debug_link_send: print(f'{thread_name} Sending payload through dataQ {payload}, iteration {send_num}')
            #                 dataQ.put(payload + "_" + str(send_num) + " " + tag, timeout=3)
                            
            #                 # increment send number
            #                 send_num += 1

        # # Terminate if Robot no longer exists
        # with vg.visible_mutex and vg.lost_mutex:
        #     if ((robot not in vg.visible) and (robot not in vg.lost)):
        #         if vg.debug_link_send: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
        #         return

        # # Sleep the Virtual Link Send Thread
        # time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)