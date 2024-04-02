from sim.model.ModelClass import RobotModel
from sim.controller.KillableThreadClass import KillableThread
from sim.controller.v_main import v_main

class Controller:
    def __init__(self, model, vg):
        self.__model = model
        self.__view = None
        self.__IPs = [x for x in range(0,245)]
        self.__usableIPs = self.__IPs.copy()
        self.__vg = vg


    def setView(self, view):
        self.__view = view


    def updateRobotPositions(self, robotIP, x, y):
        # Update robot positions from view
        self.__vg.robot_positions.update({robotIP: (x, y)})


    def addNewRobot(self, x, y):
        # Get next robot IP
        ip = f"10.0.0.1{self.__usableIPs[0]}"
        self.__usableIPs.remove(self.__usableIPs[0])

        # Make new RobotModel
        robotModel = RobotModel(ip)

        # Add robot to model
        self.__model.addRobot(robotModel)
        
        # Update the View
        robotItem = self.__view.drawRobot(robotModel, x, y)   

        # Update the robotItem Field
        robotModel.robotItem = robotItem

        # Add robot positions to known list of robot positions
        self.__vg.robot_positions.update({robotModel.ip: (x, y)})

        # Start Threads for Robot (v_main for robot with ip)
        robotModel.thread = KillableThread(v_main, (robotModel, self.__vg), name=robotModel.ip)
        robotModel.thread.start()


    def deleteRobots(self, robotItems):
        for robotItem in robotItems:
            robotModel = next((x for x in self.__model.robots if x.robotItem is robotItem), None)

            if robotModel is None:
                raise "Error in deleteRobots(). Robot is not in list"
            
            # Stop the Threads
            robotModel.thread.kill()
            robotModel.thread.join()

            # Remove from Robot Positions
            self.__vg.robot_positions.pop(robotModel.ip)

            # Delete the Robot
            self.__model.robots.remove(robotModel)

            # Update Available IPs
            self.__usableIPs.append(robotModel.ip)

            # Remove from UI
            self.__view.eraseRobot(robotItem)
    

    def cleanupThreads(self):
        for robotModel in self.__model.robots:
            robotModel.thread.kill()
            robotModel.thread.join()