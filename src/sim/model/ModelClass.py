from sim.model.v_main_test import v_main
from sim.controller.KillableThreadClass import KillableThread

class Model:
    def __init__(self):
        self.robots = list()

    def addRobot(self, robot):
        self.robots.append(robot)

    def removeRobot(self, robot):
        self.__robots.remove(robot)


class RobotModel:
    def __init__(self, ip):
        self.ip = ip
        self.robotItem = None
        self.thread = KillableThread(v_main, (ip))

        self.thread.start()