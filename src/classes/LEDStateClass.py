class LEDState:
    def __init__(self):
        # creates list containing 3 lists of 8 items each
        self.__LEDs = [[0 for x in range(8)] for y in range(3)]
    
    def getLEDs(self):
        return self.__LEDs

    def on(self, state, transceiver):
        if state == "finding":
            self.__LEDs[0][transceiver] += 1
        elif state == "connected":
            self.__LEDs[1][transceiver] += 1
        elif state == "lost":
            self.__LEDs[2][transceiver] += 1

    def off(self, state, transceiver):
        if state == "finding":
            self.__LEDs[0][transceiver] -= 1
        elif state == "connected":
            self.__LEDs[1][transceiver] -= 1
        elif state == "lost":
            self.__LEDs[2][transceiver] -= 1

    def reset():
        for i in range(3):
            for j in range(8):
                self.__LEDs[i][j] = 0