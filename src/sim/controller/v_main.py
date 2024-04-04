import time
import threading
from sim.controller.classes.vDetectorClass import vDetector

def v_main(params):

    robotModel = params[0]
    vg = params[1]
    model = params[2]

    # Initialize Detector
    detector = vDetector(robotModel, model)

    # Initialize Detector Thread
    detector_thread = threading.Thread(target = detector.detect, daemon=True, name="Detect")

    # Start Detector Thread
    detector_thread.start()