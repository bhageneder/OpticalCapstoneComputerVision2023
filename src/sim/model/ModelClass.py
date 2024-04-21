class SystemModel:
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
    def __init__(self, ip, thread=None):
        self.ip = ip
        self.robotItem = None
        self.thread = thread
        

class BlockerModel:
    def __init__(self, item):
        self.blockerItem = item
        