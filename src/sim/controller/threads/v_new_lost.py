import threading

# Handles Newly Lost Robots
def v_new_lost(vg):
    thread_name = threading.current_thread().name
    if vg.debug_new_lost: print(f'{thread_name} Created')

    while True:
        # Blocking Call to Detector's Lost Queue
        robot = vg.detector.lostQ.get()      

        # Check for Robot Link
        if (robot.robotLink != None):
            # Acquire Visible Robot List Mutex
            with vg.lost_mutex:
                # Append to Global Lost List
                vg.lost.append(robot)
             

        # Acquire Visible Robot List Mutex
        with vg.visible_mutex:
            if robot in vg.visible:
                # Remove from Global Visible List
                vg.visible.remove(robot)
