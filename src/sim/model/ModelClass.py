from threading import Thread
import threading
import ctypes
from sim.model.v_main_test import v_main

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
        self.thread = thread_with_exception(v_main, [ip])

        self.thread.start()

class thread_with_exception(Thread):
    def __init__(self, target, args):
        Thread.__init__(self)
        self.__target = target
        self.__args = args
             
    def run(self):
        # Target
        self.__target(self.__args[0])
          
    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')