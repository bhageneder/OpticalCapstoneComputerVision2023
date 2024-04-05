import time
import math
from shapely.geometry import LineString, Polygon
from interfaces.BaseDetectorClass import BaseDetector 

class vDetector(BaseDetector):
    def __init__(self, robotModel, model):
        super.__init__
        self.__robotModel = robotModel
        self.__model = model
        self.__threshold = 300  # Arbitrary threshold of 300 pixels


    def __distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def __angle(self, x1, y1, x2, y2):
        # Calculate the angle in radians using arctan2
        ang_rad = math.atan2(x2 - x1, y2 - y1)
        # Convert radians to degrees
        ang_deg = math.degrees(ang_rad)
        # Ensure the angle is between 0 and 360 degrees
        ang_deg %= 360
        return ang_deg

    def __blocking(self, currentRobot, targetRobot, blocker):
        # Create a LineString representing the line segment between obj1 and obj2
        line = LineString([currentRobot, targetRobot])

        # Convert obj3's shape to a Shapely geometry object
        blockerGeometry = blocker

        # Check if the line intersects with obj3's shape
        return line.intersects(blockerGeometry)


    def detect(self):
        while True:
            for robot in self.__model.robots:
                if (robot.ip == self.__robotModel.ip):
                    pass
                else:
                    if not (self.__robotModel.robotItem.isActive()):
                        break
                    blocking = False
                    for blockerObj in self.__model.blockers:
                        blockerItem = blockerObj.blockerItem
                        boundingRect = blockerItem.boundingRect()
                        # Get the positions of the four corners
                        TL = blockerItem.mapToScene(boundingRect.topLeft())
                        TR = blockerItem.mapToScene(boundingRect.topRight())
                        BL = blockerItem.mapToScene(boundingRect.bottomLeft()) 
                        BR = blockerItem.mapToScene(boundingRect.bottomRight())
                        # Define the rectangle as a Polygon (bottom-left, bottom-right, top-right, top-left)
                        blocker = Polygon([(BL.x(), BL.y()), (BR.x(), BR.y()), (TR.x(), TR.y()), (TL.x(), TL.y())])

                        blocking = self.__blocking(currentRobot, targetRobot, blocker)
                        if blocking:
                            break
                    if blocking:
                        if robot.ip in self.__robotModel.detections:
                            self.__robotModel.detections.remove(robot.ip)
                    else:
                        currentRobot = (self.__robotModel.robotItem.pos().x(), self.__robotModel.robotItem.pos().y())
                        targetRobot = (robot.robotItem.pos().x(), robot.robotItem.pos().y())
                        distance = self.__distance_between_points(
                                                                currentRobot[0],
                                                                currentRobot[1],
                                                                targetRobot[0],
                                                                targetRobot[1]
                                                                )
                        angle = self.__angle(
                                        currentRobot[0],
                                        currentRobot[1],
                                        targetRobot[0],
                                        targetRobot[1]
                        )
                        if (distance <= self.__threshold):
                            if robot.ip not in self.__robotModel.detections:
                                self.__robotModel.detections.append(robot.ip)
                            #print("INFO:    {} Detected {}".format(self.__robotModel.ip, robot.ip)) # Helpful print statement
                        else:
                            if robot.ip in self.__robotModel.detections:
                                self.__robotModel.detections.remove(robot.ip)
                if (self.__robotModel.ip == robot.ip):
                    print("List of Detected Robots for {}:  {}".format(self.__robotModel.ip, self.__robotModel.detections))

            time.sleep(1)
