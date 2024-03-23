from sim.model.ModelClass import RobotModel

class Controller:
    def __init__(self, model):
        self.__model = model
        self.__view = None

    def setView(self, view):
        self.__view = view

    def addNewRobot(self, x, y):
        # Check if robot is valid

        # Get next robot IP
        ip = "10.0.0.10" # temp

        # Make new RobotModel
        robotModel = RobotModel(x, y, ip)

        # Add robot to model
        self.__model.addRobot(robotModel)
        
        # Start Threads for Robot (v_main for robot with ip)
        
        # Update the View
        self.__view.drawRobot(robotModel)        