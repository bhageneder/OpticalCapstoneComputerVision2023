import sim.controller.config.v_global_vars as vg
from sim.controller.functions.v_ping import v_associate
from sim.controller.threads.v_node_discovery import v_node_discovery
import threading
import queue

# Virtually Handles Newly Visible Robots
def v_new_visible(vg):
    thread_name = threading.current_thread().name
    if vg.debug_new_visible: print(f'{thread_name} Created')

    while True:
        # Blocking Call to the Visible Queue
        try:
            robot = vg.detector.visibleQ.get(timeout = 0.1)
        except queue.Empty:
            continue
        
        if vg.debug_new_visible: print(f'Pulled From Queue')

        # Aquire Visible Mutex
        with vg.visible_mutex:
            # Add Robot to the Visible List     
            vg.visible.append(robot)
            if vg.debug_new_visible: print(f'Appended Robot to Visible List')

        # Check if Robot is in Lost List
        foundRobot = findRobot(vg)
        if vg.debug_new_visible: print(f'Lost?: {foundRobot}')
        if (foundRobot is not None):
            # Update Robot Link
            robot.robotLink = foundRobot.robotLink

            # Acquire Global Lost List Mutex
            with vg.lost_mutex:
                # Remove from Global Lost List
                vg.lost.remove(foundRobot)

            # Queue to New Robot Queue
            vg.newRobotQ.put(robot)
            if vg.debug_new_visible: print(f'{robot} Added to New Robot Queue')

        # Robot is Not in Lost List
        else:
            # Launch Node Discovery Thread
            node_discovery_thread = threading.Thread(target=v_node_discovery, daemon=True, args=[robot, vg], name=f"V_Node_Discovery_For_Robot_{robot.trackID}")
            node_discovery_thread.start()

# Searchest Lost List for Parameter Robot
def findRobot(vg):
    # Acquire Lost Robot Mutex
    with vg.lost_mutex:
        if vg.debug_new_visible: print(f'Checking Lost')

        # Try to Communicate on Open Robot Links Using New Robot Transceiver
        for lostRobot in vg.lost:
            

            # Send a v_associate to Reassociate
            response = v_associate(lostRobot.robotLink.ip_address, vg)

            # If it Got a Response
            if response:
                # Return the Robot
                return lostRobot
            
    return None
