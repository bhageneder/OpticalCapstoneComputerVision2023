import time
import math
from classes.DetectorClass import Detector

class vDetector(Detector):
    def __init__(self, ip, globals):
        self.detected = False
        self.__ip = ip
        self.__globals = globals
        self.__threshold = 300  # Arbitrary threshold of 300 pixels

    def __del__(self):
        # needed to overwrite deconstructor parent method
        pass


    def __distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    def detect(self):
        while True:
            for robotIP in self.__globals.robot_positions.keys():
                # If only 1 robot, it will always be itself
                if (robotIP == self.__ip):
                    pass
                else:
                    pass
                    distance = self.__distance_between_points(self.__globals.robot_positions[self.__ip][0], 
                                                              self.__globals.robot_positions[self.__ip][1], 
                                                              self.__globals.robot_positions[robotIP][0], 
                                                              self.__globals.robot_positions[robotIP][1])
                    if (distance <= self.__threshold):
                        self.detected = True
                        print("INFO:    {} Detected {}".format(self.__ip, robotIP))
                    else:
                        self.detected = False

            #print("Robot Detected") if self.detected else print("Detecting")   # helpful print statement
            time.sleep(3)
