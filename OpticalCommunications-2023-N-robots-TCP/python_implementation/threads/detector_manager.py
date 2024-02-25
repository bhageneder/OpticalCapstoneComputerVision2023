import string
import time
import globals
from threading import Thread
import sys
sys.path.append('/home/sa/Documents/OpticalCapstoneComputerVision2023/Computer-Vision')
from Detector import Detector

def detector_manager():
    # Only use the cameras in this set
    camSet1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method="2" ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! appsink'

    cameras = [1, 0]

    # Initialize Detector
    detector = Detector(1280, 360, "Robot_Model_Pan2", cameras, render = True, tracking = True)

    # Run Detector in a Thread
    globals.detector_thread = Thread(target = detector.detect, args = (), daemon=True, name="Detect")
    globals.detector_thread.start()

    # Wait Until Detection is Initialized
    #while detector.initializing:
    #    continue
    time.sleep(60)
    try:
        while True:
            print("transceiver " + str(detector.getTransceiver()))
            globals.best_transceiver = detector.getTransceiver()
            #print(transceiver)
            
            # Sleep
            time.sleep(0.01)  

    except KeyboardInterrupt:
        pass
    except:
        print("Get Transceiver or Send Error") 
