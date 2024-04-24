import time
import threading
import sim.sim_global_vars as sg

def v_link_send(robot, vg):
    thread_name = threading.current_thread().name
    payload_string = "hello this is a message"
    payload = []
    
    for byte in payload_string.split(" "):
        payload.append(byte)
    
    send_num = 0
    tag = vg.ip 

    while (len(payload) != 0):
        if robot.robotLink is not None:
            # Send Payload
            with vg.visible_mutex:
                sendingTo = robot.robotLink.ip_address
                if ((sendingTo in vg.detector.commsAvailable) and (robot in vg.visible)):
                    if vg.debug_link_send: ("Sending Payload To: {}".format(tag))
                    # Access receiving robots dataQ
                    with sg.data_mutex:
                        dataQ = sg.listOfDataQ[int(sendingTo.split(".")[-1])-10]
                        # Send data with tag
                        if vg.debug_link_send: print(f'{thread_name} Sending payload through dataQ {payload}, iteration {send_num}')
                        dataQ.put(payload[0] + " " + tag, timeout=3)    
                        payload.remove(payload[0])
                        
                        # increment send number
                        send_num += 1

        # Terminate if Robot no longer exists
        with vg.visible_mutex and vg.lost_mutex:
            if ((robot not in vg.visible) and (robot not in vg.lost)):
                if vg.debug_link_send: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return

        # Sleep the Virtual Link Send Thread
        time.sleep(vg.PAYLOAD_INTERVAL_SLEEP)
    return
