import time
import threading
import queue
import sim.sim_global_vars as sg

def v_link_receive(robot, vg):
    thread_name = threading.current_thread().name

    # Flag for sleep when error reading from queue handling
    sleep = False

    while True:
        data = None
        
        if sleep:
            time.sleep(0.5)
            sleep = False
        
        with vg.visible_mutex:
            if (robot in vg.visible):
                # Receive Data From Socket
                # socket.recv() will block until it receives any data, or the connection is closed
                try:
                    data = robot.robotLink.socket.recv()
                except queue.Empty:
                    sleep = True
                    continue

                # Print the received data
                if vg.debug_link_receive: print(f'{thread_name} Received: {data}')

                # Update last packet time
                robot.robotLink.lastPacketTime = time.time()


                # Prototyping multi-hop communications code
                # Receiving the routing info from other robot
                checkForRouting = data.split('\x11')

                if (len(checkForRouting) == 2):
                    # Parse routing info from packet
                    routingInfo = checkForRouting[1][2:-2].translate(str.maketrans('', '', '(),')).replace("'","").split(" ")
                    # print(routingInfo)
                    formatRoutingInfo = list()

                    for i in range(0, len(routingInfo) - 1, 2):
                        formatRoutingInfo.append((routingInfo[i], routingInfo[i + 1]))
                        
                    # print(formatRoutingInfo)
                    vg.router.updateRoute(robot.IP, formatRoutingInfo)

                # Checking if the received packet is supposed to be forwarded
                elif (vg.ip != data.split("\x00")[1].replace(" ","")):
                    # Forward the data
                    print(f"{vg.ip} forwarding {data}")

                if(data == b''):
                    # Determine if the socket is in use by another robot
                    # This happens if the robot was deleted and a new one placed in its stead with same socket
                    with vg.visible_mutex:
                        otherInVisible = next((x for x in vg.visible if ((x.robotLink is robot.robotLink) and (x is not robot))), None) is not None
                    with vg.lost_mutex:
                        otherInLost = next((x for x in vg.lost if ((x.robotLink is robot.robotLink) and (x is not robot))), None) is not None

                    socketInUse = otherInVisible or otherInLost

                    # If the socket is not in use anymore
                    if not socketInUse:
                        # Check if link is active (ensures we don't try to close the socket twice)
                        if robot.robotLink.active:
                            # Make robotLink inactive
                            robot.robotLink.active = False

                            # Close socket
                            robot.robotLink.socket.close()

                        # Remove from robot lists
                        with vg.visible_mutex and vg.lost_mutex:
                            if (robot in vg.visible):
                                vg.visible.remove(robot)
                            elif (robot in vg.lost):
                                vg.lost.remove(robot)

                        if vg.debug_link_receive: print(f'{thread_name} Exiting. Socket was destroyed')
                        return
                
        # Terminate if robot no longer exists
        with vg.visible_mutex and vg.lost_mutex:
            if ((robot not in vg.visible) and (robot not in vg.lost)):
                if vg.debug_link_receive: print(f'{thread_name} Exiting. Robot is Not in Visible or Lost List')
                return
            
        # Sleep the Virtual Link Receive thread (Should be less than 100ms to allow for larger scale of robots all receiving)
        time.sleep(vg.RECIEVE_INTERVAL_SLEEP)
    