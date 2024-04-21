# Send ICMP Ping out of Single Transceiver Directed at a Single Robot
# Used for Associate (In Node Discovery) and Reassociate (in New Visible)
def v_associate(robotIP, vg):
    associate = True if robotIP in vg.detector.commsAvailable else False
    return associate