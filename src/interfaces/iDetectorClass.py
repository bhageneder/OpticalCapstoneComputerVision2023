class iDetector:
        # Constructor
        def __init__(self):
            self.__current_transceiver = -1
            
            # List of all robots currently being tracked
            self.__robotList = list()
            
            # List of all robots that we have lost tracking for
            self.__lostRobotList = list()


        # Destructor
        def __del__(self):
            print("Deconstructing Detector Object")

        #### Public Methods ####

        # Transceiver Getter
        def getTransceiver(self):
            return self.__current_transceiver
        
        # robotList Getter
        def getRobotLlist(self):
            return self.__robotList
        
        # lostRobotList Getter
        def getLostRobotLlist(self):
            return self.__lostRobotList     
    
        # Detect Method: Call this method in its own thread
        def detect(self):
            pass