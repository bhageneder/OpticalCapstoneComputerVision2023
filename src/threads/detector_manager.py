import time
from threading import Thread
from config.global_vars import global_vars
from src.classes.DetectorClass import Detector

def detector_manager():
    # Only use the cameras in this set
    camSet1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method="2" ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! appsink'

    cameras = [2, 1]

    # Initialize Detector
    detector = Detector(1280, 360, "Robot_Model_Pan2", cameras, render = True, tracking = True)

    # Run Detector in a Thread
    global_vars.detector_thread = Thread(target = detector.detect, args = (), daemon=True, name="Detect")
    global_vars.detector_thread.start()

    # Wait Until Detection is Initialized
    #while detector.initializing:
    #    continue
    time.sleep(60)
    try:
        while True:
            print("transceiver " + str(detector.getTransceiver()))
            global_vars.best_transceiver = 1
            #print(transceiver)

            # Sleep
            time.sleep(0.01)  

    except KeyboardInterrupt:
        pass
    except:
        print("Get Transceiver or Send Error")
