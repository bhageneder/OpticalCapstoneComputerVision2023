from sim.model.ModelClass import RobotModel
from sim.controller.KillableThreadClass import KillableThread
from sim.controller.v_main import v_main
import time
import threading

class Controller:
    def __init__(self, model, globals):
        self.__model = model
        self.__view = None
        self.__IPs = [x for x in range(0,245)]
        self.__usableIPs = self.__IPs.copy()
        self.__globals = globals
        self.__threadList = []


    def setView(self, view):
        self.__view = view


    def updateRobotPositions(self, robotIP, x, y):
        # Update robot positions from view
        self.__globals.robot_positions.update({robotIP: (x, y)})


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
        self.__globals.robot_positions.update({robotModel.ip: (x, y)})

        # Start Threads for Robot (v_main for robot with ip)
        v_main_thread = KillableThread(v_main, (robotModel, self.__globals), name=robotModel.ip)
        self.__threadList.append(v_main_thread)
        v_main_thread.start()


    def deleteRobots(self, robotItems):
        for robotItem in robotItems:
            robotModel = next((x for x in self.__model.robots if x.robotItem is robotItem), None)

            if robotModel is None:
                raise "Error in deleteRobots(). Robot is not in list"
            
            for thread in self.__threadList:
                if (thread.name() == robotModel.ip):
                    # Stop the Threads
                    thread.kill()
                    thread.join()

            # Remove from Robot Positions
            self.__globals.robot_positions.pop(robotModel.ip)

            # Delete the Robot
            self.__model.robots.remove(robotModel)

            # Update Available IPs
            self.__usableIPs.append(robotModel.ip)

            # Remove from UI
            self.__view.eraseRobot(robotItem)
    

    def cleanupThreads(self):
        for thread in self.__threadList:
            thread.kill()
            thread.join()
