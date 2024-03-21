class Model:
    def __init__(self):
        self.__robots = list()

    def addRobot(self, robot):
        self.__robots.append(robot)

    def removeRobot(self, robot):
        self.__robots.remove(robot)