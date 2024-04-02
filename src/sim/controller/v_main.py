import time
import threading
from sim.controller.classes.vDetectorClass import vDetector

def v_main(params):

    robotModel = params[0]
    ip = robotModel.ip
    vg = params[1]

    # Initialize Detector
    detector = vDetector(ip, vg)

    # Initialize Detector Thread
    detector_thread = threading.Thread(target = detector.detect, daemon=True, name="Detect")
    detector_thread.start()