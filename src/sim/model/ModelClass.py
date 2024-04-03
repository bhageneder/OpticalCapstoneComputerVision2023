from sim.controller.KillableThreadClass import KillableThread

class Model:
    def __init__(self):
        self.robots = list()

    def addRobot(self, robot):
        self.robots.append(robot)

    def removeRobot(self, robot):
        self.__robots.remove(robot)


class RobotModel:
    def __init__(self, ip, thread=None):
        self.ip = ip
        self.robotItem = None
        self.detections = list()
        self.thread = thread
