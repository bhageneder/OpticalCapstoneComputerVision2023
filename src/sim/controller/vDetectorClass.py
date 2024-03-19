
from src.interfaces.iDetectorClass import iDetector


class simDetector(iDetector):
    def __init__(self):
        super.__init__()
        self.detected = False
    print("Simulation Child Detector")

    def detect(self):
        print("Robot Detected") if self.detected else None
