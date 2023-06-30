from threading import Thread
import cv2

#gst-launch-1.0 v4l2src device=/dev/video0 ! image/jpeg, width=640, height=480, framerate=30/1, format=MJPG ! nvv4l2decoder mjpeg=1 ! nvvidconv ! xvimagesink

class vStream:
	def __init__(self, src):
		self.capture = cv2.VideoCapture(src, cv2.CAP_GSTREAMER)
		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		self.capture.set(cv2.CAP_PROP_FPS, 30)
		self.thread = Thread(target = self.__update, args = ())
		self.thread.daemon = True
		self.thread.start()

	def __update(self):
		while True:
			_,self.frame = self.capture.read()

	def getFrame(self):
		return self.frame

cam0 = vStream(0)
cam1 = vStream(1)

while True:
	try:
		frame0 = cam0.getFrame()
		frame1 = cam1.getFrame()

		im_concat = cv2.hconcat([frame0, frame1])
		im_resized = cv2.resize(im_concat, (1280, 360))   
		cv2.imshow('Combined Video', im_resized)

	except:
		print("Frame not available")
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cam0.capture.release()
		cam1.capture.release()
		cv2.destroyAllWindows()
		exit(1)
