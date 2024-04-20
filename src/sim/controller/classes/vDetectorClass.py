import time
import math
from shapely.geometry import LineString, Polygon
from interfaces.BaseDetectorClass import BaseDetector 

class vDetector(BaseDetector):
    def __init__(self, robotModel, systemModel):
        super.__init__
        self.__robotModel = robotModel # Current Robot Model
        self.__systemModel = systemModel # Complete MVC Model
        self.__threshold = 300  # Arbitrary threshold of 300 pixels


    def __distanceBetweenPoints(self, x1, y1, x2, y2):
        # Return the distance between points
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
        # Create a LineString representing the line segment between robots
        line = LineString([currentRobot, targetRobot])

        # Check if the line intersects with blocker
        return line.intersects(blocker)


    def detect(self, vg):
        # Start detection loop
        while True:
            # Stop detection loop if robot is deleted
            if not (self.__robotModel.robotItem.isActive()):
                break

            foundRobotindeces = list()
            
            # iterate through all known robots
            for robot in self.__systemModel.robots:
                
                # Don't care about current robot
                if (robot.ip == self.__robotModel.ip):
                    pass
                else:

                    # current robot's x,y position
                    currentRobotPos = self.__robotModel.robotItem.mapToScene(self.__robotModel.robotItem.boundingRect().center())
                    currentRobot = (currentRobotPos.x(),
                                    currentRobotPos.y())

                    # target robots x,y position
                    targetRobotPos = robot.robotItem.mapToScene(self.__robotModel.robotItem.boundingRect().center())
                    targetRobot = (targetRobotPos.x(),
                                   targetRobotPos.y())
                    
                    # obtain the distance between two robots
                    distance = self.__distanceBetweenPoints(
                                                            currentRobot[0],
                                                            currentRobot[1],
                                                            targetRobot[0],
                                                            targetRobot[1]
                                                            )
                    
                    # obtain the angle between two robots
                    angle = self.__angle(
                                        currentRobot[0],
                                        currentRobot[1],
                                        targetRobot[0],
                                        targetRobot[1]
                                        )

                    if (distance <= self.__threshold):
                        # if distance is within threshold; if blockers, not detectect : otherwise, detected
                        blocking = False
                        
                        # iterate through all known blockers
                        for blockerObj in self.__systemModel.blockers:

                            blockerItem = blockerObj.blockerItem
                            blockerRect = blockerItem.rect()

                            # Get updated positions of the four blocker corners
                            TL = blockerItem.mapToScene(blockerRect.topLeft())
                            TR = blockerItem.mapToScene(blockerRect.topRight())
                            BL = blockerItem.mapToScene(blockerRect.bottomLeft()) 
                            BR = blockerItem.mapToScene(blockerRect.bottomRight())

                            # Define the rectangle as a Polygon (bottom-left, bottom-right, top-right, top-left)
                            blocker = Polygon([(BL.x(), BL.y()), (BR.x(), BR.y()), (TR.x(), TR.y()), (TL.x(), TL.y())])

                            blocking = self.__blocking(currentRobot, targetRobot, blocker)

                            if blocking:
                                # blocker found, DNC if more than one blocker between two robots, end search
                                break

                        if blocking:
                            # Remove robot from detections list when blocked
                            self.__robotModel.detections.remove(robot.ip) if robot.ip in self.__robotModel.detections else None                                
                        else:
                            # Add robot to detections list of not blocked
                            self.__robotModel.detections.append(robot.ip) if robot.ip not in self.__robotModel.detections else None
                                
                        #print("INFO:    {} Detected {}".format(self.__robotModel.ip, robot.ip)) # Helpful print statement
                    else:
                        self.__robotModel.detections.remove(robot.ip) if robot.ip in self.__robotModel.detections else None
                
                if (self.__robotModel.ip == robot.ip):
                    # Helpful print statement
                    print("List of Detected Robots for {}:  {}".format(self.__robotModel.ip, self.__robotModel.detections))

            time.sleep(1)
