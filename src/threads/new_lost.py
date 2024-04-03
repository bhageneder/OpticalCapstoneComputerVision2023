import config.global_vars as g

# Handles Newly Lost Robots
def new_lost():
    while True:
        # Blocking Call to Detector's Lost Queue
        robot = g.detector.lostQ.get()
        
        print("LED off")
        g.LEDs.off("finding", robot.transceiver)        

        # Check for Robot Link
        if (robot.robotLink != None):
            g.LEDs.on("lost", robot.transceiver)
            if robot.state == 1:    # finding state
                g.LEDs.off("connected", robot.transceiver)
            # Acquire Visible Robot List Mutex
            with g.lost_mutex:
                # Append to Global Lost List
                g.lost.append(robot)
             

        # Acquire Visible Robot List Mutex
        with g.visible_mutex:
            if robot in g.visible:
                # Remove from Global Visible List
                g.visible.remove(robot)
