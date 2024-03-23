from sim.model.ModelClass import RobotModel

class Controller:
    def __init__(self, model):
        self.__model = model
        self.__view = None
        self.__IPs = [x for x in range(0,245)]
        self.__usableIPs = self.__IPs.copy()

    def setView(self, view):
        self.__view = view

    def addNewRobot(self, x, y):
        # Check if robot is valid

        # Get next robot IP
        ip = f"10.0.0.1{self.__usableIPs[0]}"
        self.__usableIPs.remove(self.__usableIPs[0])

        # Make new RobotModel
        robotModel = RobotModel(x, y, ip)

        # Add robot to model
        self.__model.addRobot(robotModel)
        
        # Start Threads for Robot (v_main for robot with ip)
        
        # Update the View
        self.__view.drawRobot(robotModel)        

    def deleteRobots(self, robots):
        #for robot in robots:
            # if its a robot remove it from the model
        pass