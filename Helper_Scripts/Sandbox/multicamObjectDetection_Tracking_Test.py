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

"""
Method_Name: indirect 
params_type: int j
param_desc: j is the integer division from the center location of the object and the frame division
return_type: int j
return_desc: j is the modified integer that represents the transceiver number to use for each section
"""
def indirect(j):
	#edge cases
	if (j == 0):
		j = 5
	elif (j == 1):
		j = 1
	#if the number is odd, divide by 2 and add 1 to represent the transceiver used. 
	#The mathematics for this can be found in the README.
	else:
		if (j%2 ==  1):
			j = j/2 + 1
		else:
			j = j/2  
	return j

"""
Method_Name: object_transceiver_number
params_type: int Center_Of_Object, width_of_frame 
param_desc (Center_Of_Object): value of the center pixel location of the detected object
param_desc (width_of_frame): value of the frame width determined from frame concat
return_type: int normalized_x
return_desc: normalized_x is the modified integer that represents the transceiver number to use for each section
"""
def obtain_transceiver_number(Center_Of_Object, width_of_frame):
	#print("class {} found at ({}, {}, {}, {})".format(detection.ClassID, detection.Left, detection.Top, detection.Right, detection.Bottom))
	#print("X Location is {}, Y Location is {}".format(detection.Center[0], detection.Center[1]))
	
	#Use integer division to obtain a section that the object is detected in.
	normalized_x = ((int(Center_Of_Object) / int(width_of_frame/10)))
	normalized_x = indirect(normalized_x)
	print("The Ball is in Section {}, Using transceiver {}".format(normalized_x, normalized_x))
	return normalized_x


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


i = 0			#abtract counter

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
	#frame_rgba_2 = cv2.cvtColor(im_finalized, cv2.COLOR_BGR2RGBA)
	img = jetson_utils.cudaFromNumpy(frame_rgba)

	# Object Detection
	detections = net.Detect(img, width, height)

	img_2 = jetson_utils.cudaToNumpy(img)

	starting_section = 3	#starting_section is the first section that will be modified after the initial frame is drawn on.
	incrementer = 2		#incrementer is used to increment to control the incrementation at which the sections are chosen (i.e. 1/10 -> 3/10 -> 5/10) 
	sections = 5		#number of sections to divide the frame into
	division = 2 * sections #math to create the width of the divisions (width/(2*section)) or half the width of a section

	#Create the initial line segment to use in the iterative loop
	previous_line = cv2.line(img_2, (int(width/division), 0), (int(width/division), height), (0,0,0), 5)

	#Loop that iteratively appends the previous frame with a new segment line until the entire frame has been covered
	while(starting_section < division): 
		im_line = cv2.line(previous_line, ((starting_section*int(width/division)), 0), ((starting_section*int(width/division)), height), (0,0,0), 5)
		previous_line = im_line
		starting_section = starting_section+incrementer
	im_finalized = previous_line	

	img_3 = jetson_utils.cudaFromNumpy(im_finalized)

	#Render the image to be displayed on the monitor
	display.RenderOnce(img_3, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
	# Print out the locations of detected robots
	# Using the location we can approximate a transceiver to use
	# Using size, we can approximate distance
	try:
		for detection in detections:
			#obtain trasnciever data every 100 iterations, an abstract value and can be modified depending on efficiency
			if (i % 100) == 0:
				obtain_transceiver_number(detection.Center[0], width)

	except SyntaxError as se:
		print("Error reading detection: {}".format(se))
		pass

# Release when window is closed
cap0.capture.release()
cap1.capture.release()
exit(1)




