# Send ICMP Ping out of Single Transceiver Directed at a Single Robot
# Used for Associate (In Node Discovery) and Reassociate (in New Visible)
def v_associate(robotIP, vg):
    associate = True if (robotIP in vg.detector.commsAvailable) else False

    # Prevent association with already associated robot
    # Though this can happen in the real system, it is removed for simplicity's sake
    for robot in vg.visible:
        if robot.IP == robotIP:
            associate = False
            break

    return associate