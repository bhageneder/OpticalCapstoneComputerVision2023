import threading
import queue
import sim.sim_global_vars as sg

'''
Contains virtual global variables that will be used across sim files
Each robot maintains their own virtual globals state
'''
class vGlobals():
    def init(self, robotIP):
        self.detectionThreshold = sg.detectionThreshold
        self.commsThreshold     = sg.commsThreshold

        # Use this to enable to debug print statements within the program.
        # True = Debug Print Statements Active 
        self.debug_detector         = False
        self.debug_mini_discovery   = False
        self.debug_new_visible      = False
        self.debug_new_lost         = False
        self.debug_link_send        = False
        self.debug_link_receive     = True
        self.debug_node_discovery   = False


        self.ip = robotIP
        self.POSSIBLE_ROBOT_IP_ADDRESSES = [x for x in range(10,245)] 
        self.EXPECTED_NUMBER_OF_ROBOTS   = len(self.POSSIBLE_ROBOT_IP_ADDRESSES)

        self.DISCOVERY_INTERVAL_SLEEP = 0.05
        self.RECIEVE_INTERVAL_SLEEP   = 0.0
        self.PAYLOAD_INTERVAL_SLEEP   = 0.25

        self.trackIDs       = [x for x in range(1, 65535)] 
        self.trackingIDSet  = {}

        self.detector = None

        self.detector_thread    = None
        self.new_visible_thread = None
        self.new_lost_thread    = None

        self.visible    = []
        self.lost       = []

        self.visible_mutex  = threading.Lock()
        self.lost_mutex     = threading.Lock()

        self.newRobotQ = queue.Queue()
        
        self.dataReceived = {}
    