import time
import math
from shapely.geometry import LineString, Polygon
from interfaces.BaseDetectorClass import BaseDetector 
import sim.sim_global_vars as sg

class vDetector(BaseDetector):
    def __init__(self, robotModel, systemModel):
        super.__init__
        self.__robotModel = robotModel # Current Robot Model
        self.__systemModel = systemModel # Complete MVC Model
        self.detections = list()
        self.commsAvailable = list()


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
    
    def __updateDetectionList(self, blocking, robot):
        print("update detection")
        if blocking:
            # Remove robot from detections list when blocked
            self.detections.remove(robot.ip) if robot.ip in self.detections else None
        else:
            # Robot not blocked, add to detections list
            self.detections.append(robot.ip) if robot.ip not in self.detections else None
        

    def __updateCommsAvailableList(self, blocking, robot):
        if blocking:
            # Remove robot from commsAvailable list when blocked
            self.commsAvailable.remove(robot.ip) if robot.ip in self.commsAvailable else None
        else:
            # Robot not blocked, add to commsAvailable list
            self.commsAvailable.append(robot.ip) if robot.ip not in self.commsAvailable else None


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

                    if distance <= vg.detectionThreshold:
                        # if distance is within the larger threshold; 
                        # if blockers, not detectect : otherwise, detected
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

                        # Update the state lists for detection and commsAvaiable
                        self.__updateDetectionList(blocking, robot)
                        if distance <= vg.commsThreshold:
                            self.__updateCommsAvailableList(blocking, robot)
                        else:
                            # robot outside comms threshold but inside detection threshold
                            self.commsAvailable.remove(robot.ip) if robot.ip in self.commsAvailable else None

                    else:
                        self.detections.remove(robot.ip) if robot.ip in self.detections else None
                        self.commsAvailable.remove(robot.ip) if robot.ip in self.commsAvailable else None
            
                if (self.__robotModel.ip == robot.ip):
                    # Helpful print statement
                    print("List of Detected Robots for {}:  {}".format(self.__robotModel.ip, self.detections))
                    print("List of Communicable Robots for {}: {}".format(self.__robotModel.ip, self.commsAvailable))
                    print("\n")
                

                # clean up state lists
                for ip in self.detections:
                    self.detections.remove(ip) if ip not in sg.usedIPs else None
                for ip in self.commsAvailable:
                    self.commsAvailable.remove(ip) if ip not in sg.usedIPs else None 

            
            time.sleep(1)
