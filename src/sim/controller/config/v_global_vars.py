import threading
import queue

'''
Contains virtual global variables that will be used across sim files
Each robot maintains their own virtual globals state
'''
class VirtualGlobals():
    def init(self, robotIP):
        self.detectionThreshold = 500
        self.commsThreshold = 300

        self.debug_mini_discovery = True


        self.ip = robotIP
        self.POSSIBLE_ROBOT_IP_ADDRESSES = [x for x in range(10,245)] 
        self.EXPECTED_NUMBER_OF_ROBOTS = len(self.POSSIBLE_ROBOT_IP_ADDRESSES)
        self.DISCOVERY_INTERVAL_SLEEP = 0.1 

        self.trackIDs = [x for x in range(1, 65535)] 
        self.trackingIDSet = {}

        self.detector = None

        self.detector_thread = None
        self.new_visible_thread = None
        self.new_lost_thread = None

        self.visible = []
        self.lost = []

        self.visible_mutex = threading.Lock()
        self.lost_mutex = threading.Lock()

        self.newRobotQ = queue.Queue()

        
    