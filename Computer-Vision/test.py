from Detection import Detection
from threading import Thread
import time

detection = Detection(1280, 360, "Balls_2", [1,0], True)


thread = Thread(target = detection.detect, args = (), daemon=True, name="Detect")

thread.start()

time.sleep(3)
while(True):
    detection.getTransceiver()
    time.sleep(0.5)
