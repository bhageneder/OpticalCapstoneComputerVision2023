from sim.model.ModelClass import RobotModel, BlockerModel
from sim.controller.KillableThreadClass import KillableThread
from sim.controller.v_main import v_main

class Controller:
    def __init__(self, systemModel):
        self.__systemModel = systemModel
        self.__view = None
        self.__IPs = [x for x in range(0,245)]
        self.__usableIPs = self.__IPs.copy()


    def setView(self, view):
        self.__view = view


    def addNewRobot(self, x, y):
        # Get next robot IP
        ip = f"10.0.0.1{self.__usableIPs[0]}"
        self.__usableIPs.remove(self.__usableIPs[0])

        # Make new RobotModel
        robotModel = RobotModel(ip)

        # Add robot to model
        self.__systemModel.addRobot(robotModel)
        
        # Update the View
        robotItem = self.__view.drawRobot(robotModel, x, y)   

        # Update the robotItem Field
        robotModel.robotItem = robotItem

        # Start Threads for Robot (v_main for robot with ip)
        robotModel.thread = KillableThread(v_main, (robotModel, self.__systemModel), name=robotModel.ip)
        robotModel.thread.start()


    def deleteItems(self, items):
        for item in items:
            robotModel = next((x for x in self.__systemModel.robots if x.robotItem is item), None)

            if robotModel is None:
                # Blocker (Not a Robot)
                blockerModel = next((x for x  in self.__systemModel.blockers if x.blockerItem is item), None)
                if blockerModel is None:
                    raise "Error in deleteItems(), neither Robot nor Blocker in list"
                self.__systemModel.blockers.remove(blockerModel)
                self.__view.eraseBlocker(item)
                continue

            #if robotModel is None:
            #    raise "Error in deleteRobots(). Robot is not in list"
            
            # Stop the Threads
            robotModel.thread.kill()
            robotModel.thread.join()

            # Clear robot from all detection lists
            for robot in self.__systemModel.robots:
                if robotModel.ip in robot.detections:
                    robot.detections.remove(robotModel.ip)

            # Delete the Robot
            self.__systemModel.robots.remove(robotModel)

            # Update Available IPs
            self.__usableIPs.append(robotModel.ip)

            # Remove from UI
            self.__view.eraseRobot(item)
    

    def cleanupThreads(self):
        for robotModel in self.__systemModel.robots:
            robotModel.thread.kill()
            robotModel.thread.join()

    def addNewBlocker(self, x, y, width, height):
        # Update the View
        blockerItem = self.__view.drawBlocker(x, y, width, height)   

        # Make new BlockerModel
        blockerModel = BlockerModel(blockerItem)

        # Add blocker to model
        self.__systemModel.addBlocker(blockerModel)