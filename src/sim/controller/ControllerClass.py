from sim.model.ModelClass import RobotModel, BlockerModel

class Controller:
    def __init__(self, model):
        self.__model = model
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
        self.__model.addRobot(robotModel)
        
        # Start Threads for Robot (v_main for robot with ip)
        
        # Update the View
        robotItem = self.__view.drawRobot(robotModel, x, y)   

        # Update the robotItem Field
        robotModel.robotItem = robotItem

    def deleteItems(self, items):
        for item in items:
            robotModel = next((x for x in self.__model.robots if x.robotItem is item), None)

            if robotModel is None:
                # Blocker (Not a Robot)
                self.__view.eraseBlocker(item)
                continue

            #if robotModel is None:
            #    raise "Error in deleteRobots(). Robot is not in list"
            
            # Stop the Threads
            robotModel.thread.kill()
            robotModel.thread.join()

            # Delete the Robot
            self.__model.robots.remove(robotModel)

            # Update Available IPs
            self.__usableIPs.append(robotModel.ip)

            # Remove from UI
            self.__view.eraseRobot(item)
    
    def cleanupThreads(self):
        for robotModel in self.__model.robots:
            robotModel.thread.kill()
            robotModel.thread.join()

    def addNewBlocker(self, x, y, width, height):
        # Update the View
        blockerItem = self.__view.drawBlocker(x, y, width, height)   

        # Make new BlockerModel
        blockerModel = BlockerModel(blockerItem)

        # Add blocker to model
        self.__model.addBlocker(blockerModel)