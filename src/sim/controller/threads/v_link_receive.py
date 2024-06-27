import time
import threading
import queue
import sim.sim_global_vars as sg

def v_link_receive(robot, vg):
    thread_name = threading.current_thread().name

    while True:
        data = None

        with vg.visible_mutex:
            if (robot in vg.visible):
                # Grab from queue 
                with sg.data_mutex:
                    dataQ = sg.listOfDataQ[int(vg.ip.split(".")[-1])-10]
                    # parse data with tag
                    try:
                        data, tag = dataQ.get(timeout=0.1).split(" ")
                        if vg.debug_link_receive: print(f'{thread_name} + {vg.ip} Received: "{data}" from {tag}')

                        # If the data is intended for a different recipient
                        if (data[:4] == "\XX\\"):
                            forwardAddress, data = data.split("\XX\\")
                            vg.forwarders[int(forwardAddress.split(".")[-1])-10].put(data)
                        
                        else:
                            # store data locally in virtual global variables
                            vg.dataReceived[tag].append(data + " ")
                            print(vg.dataReceived[tag])

                    except Exception as e:
                        pass
                        #if vg.debug_link_receive: print(f'No Data in Data Queue')
                
        # Terminate if robot no longer exists
        with vg.visible_mutex and vg.lost_mutex:
            if ((robot not in vg.visible) and (robot not in vg.lost)):
                if vg.debug_link_receive: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return
            
        # Sleep the Virtual Link Receive thread (Should be less than 100ms to allow for larger scale of robots all receiving)
        time.sleep(vg.RECIEVE_INTERVAL_SLEEP)
    