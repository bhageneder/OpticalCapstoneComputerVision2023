import queue

class BaseDetector:
    def __init__(self):
        self.visibleQ = queue.Queue()
        self.lostQ = queue.Queue()

    def __del__(self):
        pass

    def detect(self):
        pass
