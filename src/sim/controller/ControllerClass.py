class Controller:
    def __init__(self, model):
        self.__model = model

    def addNewRobot(self):
        # Check if robot is valid

        # Add robot to model
        self.__model.addRobot("testRobot")
        
        # Start Threads for Robot
        
        # Update the View
        print("controller adding robot")