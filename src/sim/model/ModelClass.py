from sim.model.v_main_test import v_main
from sim.controller.KillableThreadClass import KillableThread

class Model:
    def __init__(self):
        self.robots = list()
        self.blockers = list()

    def addRobot(self, robot):
        self.robots.append(robot)

    def removeRobot(self, robot):
        self.__robots.remove(robot)

    def addBlocker(self, blocker):
        self.blockers.append(blocker)

    def removeBlocker(self, blocker):
        self.blockers.remove(blocker)


class RobotModel:
    def __init__(self, ip):
        self.ip = ip
        self.robotItem = None
        self.thread = KillableThread(v_main, (ip))

        self.thread.start()

class BlockerModel:
    def __init__(self, item):
        self.blockerItem = item