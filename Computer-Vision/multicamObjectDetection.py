import jetson_inference
import jetson_utils
import time
import cv2
from threading import Thread

# Define stream class
class Stream:
	def __init__(self, src):
		self.capture = cv2.VideoCapture(src)
		_,self.frame = self.capture.read()							# Prevent the code from running until one frame has been read
		self.thread = Thread(target = self.__update, args = ())
		self.thread.daemon = True									# Destroys threads automatically when program exits
		self.thread.start()

	# Update function is automatically called on initialization and run in a thread
	def __update(self):
		while True:
			_,self.frame = self.capture.read()

	def getFrame(self):
		return self.frame

# Define variables
height = 360		# Change for production code. Only set to 360 such that the images will fit on screen
width = 1280		# Change for production code. Only set to 1280 such that the images will fit on screen

# Set up detect net for the custom model
net = jetson_inference.detectNet(model="/home/sa/jetson-inference/python/training/detection/ssd/models/Balls_2/ssd-mobilenet.onnx", labels="/home/sa/jetson-inference/python/training/detection/ssd/models/Balls_2/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

# Initialize the display window
display = jetson_utils.glDisplay()

# Define Stream objects for video0 and video1
cap0 = Stream(0)
cap1 = Stream(1)

while (display.IsOpen()):
	# Read frames
	frame0 = cap0.getFrame()
	frame1 = cap1.getFrame()

	# Horizontally concats the images from frames 0 and 1
	im_concat = cv2.hconcat([frame0, frame1])

	# Resizes the images
	im_resized = cv2.resize(im_concat, (width, height))

	# Prep for object detection
	frame_rgba = cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGBA)
	img = jetson_utils.cudaFromNumpy(frame_rgba)

	# Object Detection
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

	# Print out the locations of detected robots
	# Using the location we can approximate a transceiver to use
	# Using size, we can approximate distance
	try:
		for detection in detections:
			#print("class {} found at ({}, {}, {}, {})".format(detection.ClassID, detection.Left, detection.Top, detection.Right, detection.Bottom))
			print("X Location is {}, Y Location is {}".format(detection.Center[0], detection.Center[1]))
	except SyntaxError as se:
		print("Error reading detection: {}".format(se))
		pass

# Release when window is closed
cap0.capture.release()
cap1.capture.release()
exit(1)
