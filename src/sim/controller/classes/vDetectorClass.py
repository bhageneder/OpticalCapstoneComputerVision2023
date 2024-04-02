import time
import math
from classes.DetectorClass import Detector

class vDetector(Detector):
    def __init__(self, robotModel, model):
        self.detected = False
        self.__robotModel = robotModel
        self.__model = model
        self.__threshold = 300  # Arbitrary threshold of 300 pixels

    def __del__(self):
        # needed to overwrite deconstructor parent method
        pass


    def __distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    def detect(self):
        while True:
            for robot in self.__model.robots:
                if (robot.ip == self.__robotModel.ip):
                    pass
                else:
                    distance = self.__distance_between_points(
                                                            self.__robotModel.robotItem.pos().x(),
                                                            self.__robotModel.robotItem.pos().y(),
                                                            robot.robotItem.pos().x(),
                                                            robot.robotItem.pos().y()
                                                            )
                    if (distance <= self.__threshold):
                        self.detected = True
                        print("INFO:    {} Detected {}".format(self.__robotModel.ip, robot.ip)) # Helpful print statement
                    else:
                        self.detected = False

            time.sleep(1)
