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

        self.ip = robotIP

        self.detector = None

        self.detector_thread = None
        self.new_visible_thread = None
        self.new_lost_thread = None

        self.visible = []
        self.lost = []

        self.visible_mutex = threading.Lock()
        self.lost_mutex = threading.Lock()

        self.newRobotQ = queue.Queue()

        
    