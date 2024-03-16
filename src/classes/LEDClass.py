class LEDClass:
    def __init__():
        # creates list containing 3 lists of 8 items each
        LEDs = [[0 for x in range(8)] for y in range(3)]
    
    def getLEDs():
        return LEDs

    def on(state, transceiver):
        if state == "finding":
            LEDs[0][transceiver] = 1
        if state == "connected":
            LEDs[1][transceiver] = 1
        if state == "lost":
            LEDs[2][transceiver] = 1

    def off(state, transceiver):
        if state == "finding":
            LEDs[0][transceiver] = 0
        if state == "connected":
            LEDs[1][transceiver] = 0
        if state == "lost":
            LEDs[2][transceiver] = 0
