import threading
import ctypes

class KillableThread(threading.Thread):
    def __init__(self, target, args, name=""):
        threading.Thread.__init__(self)
        self.__target = target
        self.__args = args
        self.__name = name
             
    def run(self):
        self.__target(self.__args)

    def name(self):
        return self.__name
              
    def get_id(self):
        # Returns ID of the Thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def kill(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')