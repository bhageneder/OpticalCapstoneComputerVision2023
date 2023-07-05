import jetson_inference
import jetson_utils
import cv2
from Stream import Stream

# Define variables
height = 360					# Change for production code. Only set to 360 such that the images will fit on screen
width = 1280					# Change for production code. Only set to 1280 such that the images will fit on screen
modelName = "RobotModel2"		# Choose Model Name

# Set up detect net for the custom model
net = jetson_inference.detectNet(model=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/ssd-mobilenet.onnx", labels=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

# Initialize the display window
display = jetson_utils.glDisplay()

# Instantiate Stream objects for video0 and video1
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
	detections = net.Detect(img, width, height)		# List of objects detected
	display.RenderOnce(img, width, height)			# Renders the display
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

	# Print out the locations of detected robots
	# Using the location we can approximate a transceiver to use
	for detection in detections:
	    print ("class {} found at ({}, {}, {}, {})".format(detection.ClassID, detection.Left, detection.Top, detection.Right, detection.Bottom))
	
# Release when window is closed
cap0.capture.release()
cap1.capture.release()

# Threads are auto-killed on exit
exit(1)
