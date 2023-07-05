from threading import Thread
import cv2
from Stream import Stream

cam0 = Stream(0)
cam1 = Stream(1)

while True:
	frame0 = cam0.getFrame()
	frame1 = cam1.getFrame()

	im_concat = cv2.hconcat([frame0, frame1])
	im_resized = cv2.resize(im_concat, (1280, 360))   
	cv2.imshow('Combined Video', im_resized)

	print("Frame not available")
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cam0.capture.release()
		cam1.capture.release()
		cv2.destroyAllWindows()
		exit(1)
