import jetson.inference
import jetson.utils
import time
import cv2

# Define variables
height = 360 # Change for production code. Only set to 360 such that the images will fit on screen
width = 1280 # Change for production code. Only set to 1280 such that the images will fit on screen

# Set up detect net for the custom model
net = jetson.inference.detectNet(model="/home/sa/jetson-inference/python/training/detection/ssd/models/RobotModel2/ssd-mobilenet.onnx", labels="/home/sa/jetson-inference/python/training/detection/ssd/models/RobotModel2/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

# Initialize the display window
display = jetson.utils.glDisplay()

# Open Image Capture for video0 and video1
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

while (display.IsOpen() and cap0.isOpened()):
	# Read camera frames (poor way to do this - not synchronized and has terrible busy waiting)
	ret0, frame0 = cap0.read()
	ret1, frame1 = cap1.read()

	# If a frame was read...
	if ret0:
		# Horizontally concats the images from frames 0 and 1
		im_concat = cv2.hconcat([frame0, frame1])

		# Resizes the images
		im_resized = cv2.resize(im_concat, (width, height))   

		# Pressing q quits the loop
		if cv2.waitKey(1) & 0xFF == ord('q'):
            		break

	else: 
		print("Error: Frame could not be read")
		break

	# Prep for object detection
	frame_rgba = cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGBA)
	img = jetson.utils.cudaFromNumpy(frame_rgba)

	# Object Detection
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

# Release the video captures
cap0.release()
cap1.release()
