import sim.controller.config.v_global_vars as vg

# Send ICMP Ping out of Single Transceiver Directed at a Single Robot
# Used for Associate (In Node Discovery) and Reassociate (in New Visible)
def v_associate(robotIP, robotTrackID):
    print("Virtualized associating")
    return False