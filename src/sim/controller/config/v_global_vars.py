import threading
import queue

'''
Contains virtual global variables that will be used across sim files
Each robot maintains their own virtual globals state
'''
class VirtualGlobals():
    def init(self, robotIP):
        threshold = 300

        ip = robotIP

        detector = None

        detector_thread = None
        new_visible_thread = None
        new_lost_thread = None

        visible = []
        lost = []

        visible_mutex = threading.Lock()
        lost_mutex = threading.Lock()

        newRobotQ = queue.Queue()

        
    