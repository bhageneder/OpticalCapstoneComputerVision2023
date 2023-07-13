from Detection_mini import Detection
from threading import Thread

self.thread = Thread(target = Detection(1280, 360, "Balls_2", [0,1], True), args = (), daemon=True, name="Detect")
self.thread.start() 
while(True):
	continue
