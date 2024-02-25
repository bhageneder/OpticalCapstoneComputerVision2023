from threading import Thread
import time
from datetime import datetime
import matplotlib.pyplot as plt
from src.classes.DetectorClass import Detector

detection = Detector(1280, 360, "Balls_2", [1,0], True, True)


thread = Thread(target = detection.detect, args = (), daemon=True, name="Detect")

thread.start()

time.sleep(5)
time_difference = []
iterations = []
counter = 0
try:
    while(True):
        try:        
            start_time = datetime.now().timestamp()        
            transceiver = detection.getTransceiver()
            time_difference.append(float(datetime.now().timestamp() - start_time))
            iterations.append(counter) 
            counter = counter + 1
        except AttributeError as ae:
            time.sleep(0.5)
except KeyboardInterrupt:
    plt.plot(iterations, time_difference)
    plt.show()
