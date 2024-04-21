import time
import threading
from sim.controller.config.v_global_vars import VirtualGlobals
from sim.controller.classes.vDetectorClass import vDetector
from sim.controller.threads.v_new_visible import v_new_visible
from sim.controller.threads.v_new_lost import v_new_lost

def v_main(params):
    robotModel = params[0]
    systemModel = params[1]

    # initialize virtual globals
    vg = VirtualGlobals()
    vg.init(robotModel.ip)

    # Initialize Detector
    vg.detector = vDetector(robotModel, systemModel)

    # Initialize Detector Thread
    vg.detector_thread = threading.Thread(target = vg.detector.detect, args=[vg] ,daemon=True, name="Virtual_Detect")

    vg.new_visible_thread = threading.Thread(target=v_new_visible, args=[vg], daemon=True, name="Virtual_New_Visible")

    vg.new_lost_thread = threading.Thread(target=v_new_lost, args=[vg], daemon=True, name="Virtual_New_Lost")


    # Start Threads
    vg.detector_thread.start()
    vg.new_visible_thread.start()