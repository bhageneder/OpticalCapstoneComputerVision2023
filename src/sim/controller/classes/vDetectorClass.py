import time
import math
from interfaces.BaseDetectorClass import BaseDetector 

class vDetector(BaseDetector):
    def __init__(self, robotModel, model):
        super.__init__
        self.__robotModel = robotModel
        self.__model = model
        self.__threshold = 300  # Arbitrary threshold of 300 pixels


    def __distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    def detect(self):
        while True:
            for robot in self.__model.robots:
                if (robot.ip == self.__robotModel.ip):
                    pass
                else:
                    if not (self.__robotModel.robotItem.isActive()):
                        break
                    distance = self.__distance_between_points(
                                                            self.__robotModel.robotItem.pos().x(),
                                                            self.__robotModel.robotItem.pos().y(),
                                                            robot.robotItem.pos().x(),
                                                            robot.robotItem.pos().y()
                                                            )
                    if (distance <= self.__threshold):
                        if robot.ip not in self.__robotModel.detections:
                            self.__robotModel.detections.append(robot.ip)
                        print("INFO:    {} Detected {}".format(self.__robotModel.ip, robot.ip)) # Helpful print statement
                    else:
                        if robot.ip in self.__robotModel.detections:
                            self.__robotModel.detections.remove(robot.ip)

            time.sleep(1)
