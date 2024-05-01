import threading

# Handles Newly Lost Robots
def v_new_lost(vg):
    thread_name = threading.current_thread().name
    if vg.debug_new_lost: print(f'{thread_name} Created')

    while True:
        # Blocking Call to Detector's Lost Queue
        robot = vg.detector.lostQ.get()  
        if vg.debug_new_lost: print(f'Dequeued')    

        # Check for Robot Link
        if (robot.robotLink != None):
            # Acquire Visible Robot List Mutex
            with vg.lost_mutex:
                # Append to Global Lost List
                vg.lost.append(robot)
                if vg.debug_new_lost: print(f'{robot.robotLink.ip_address} Lost') 
             

        # Acquire Visible Robot List Mutex
        with vg.visible_mutex:
            if robot in vg.visible:
                # Remove from Global Visible List
                vg.visible.remove(robot)
                if vg.debug_new_lost: print(f'removed from visible') 
