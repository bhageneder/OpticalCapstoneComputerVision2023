class LEDState:
    def __init__():
        # creates list containing 3 lists of 8 items each
        LEDs = [[0 for x in range(8)] for y in range(3)]
    
    def getLEDs():
        return LEDs

    def on(state, transceiver):
        if state == "finding":
            LEDs[0][transceiver] = 1
        elif state == "connected":
            LEDs[1][transceiver] = 1
        elif state == "lost":
            LEDs[2][transceiver] = 1

    def off(state, transceiver):
        if state == "finding":
            LEDs[0][transceiver] = 0
        elif state == "connected":
            LEDs[1][transceiver] = 0
        elif state == "lost":
            LEDs[2][transceiver] = 0
