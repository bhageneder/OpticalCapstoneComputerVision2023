import jetson.inference
import jetson.utils
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
net = jetson.inference.detectNet(model="/home/sa/jetson-inference/python/training/detection/ssd/models/RobotModel2/ssd-mobilenet.onnx", labels="/home/sa/jetson-inference/python/training/detection/ssd/models/RobotModel2/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

# Initialize the display window
display = jetson.utils.glDisplay()

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
	img = jetson.utils.cudaFromNumpy(frame_rgba)

	# Object Detection
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
	
	# Check for quit key, release camera captures, exit
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cam0.capture.release()
		cam1.capture.release()
		exit(1)
