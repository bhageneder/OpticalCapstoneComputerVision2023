from threading import Thread
import time
from datetime import datetime
import matplotlib.pyplot as plt
import cv2
from src.classes.DetectorClass import Detector

# flip-method='2'

camSet1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! nvvidconv ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! appsink'

#cap = cv2.VideoCapture(camSet1, cv2.CAP_GSTREAMER)

#detection = Detection(3840, 720, "robots_only", [camSet1, 2, 1], True, False)
detection = Detector(1280, 720, "robots_only", [camSet1], True, False)

thread = Thread(target = detection.detect, args = (), daemon=True, name="Detect")

thread.start()

time.sleep(5)
while(True):       
    try:	
        transceiver = detection.getTransceiver()
    except KeyboardInterrupt:
        break

    except:
        print("err")    
#    ret, img = cap.read()
#    if(ret):
#        cv2.imshow("camera",img)
#    if cv2.waitKey(1)==ord('q'):
#        break

exit(0)

#cap.release()
#cv2.destroyAllWindows()
