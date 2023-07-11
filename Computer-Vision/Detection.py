import jetson_inference
import jetson_utils
import cv2
from Stream import Stream

# Must be called in its own thread
class Detection:
    # Parameters: Width of Output Frame, Height of Output Frame, Object Detection Model Name, List of Camera Names (e.g., [0, 1,...]), render (Boolean)
    def __init__(self, width, height, modelName, cameras, render):
        # Define private variables
        self.__width = width
        self.__height = height
        self.__render = render

        # Set up detect net for the custom model
        self.__net = jetson_inference.detectNet(model=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/ssd-mobilenet.onnx", labels=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

        # Initialize the display window
        if self.__render:
                self.__display = jetson_utils.glDisplay()

        # Private list to hold captures
        self.__captures = list(map(lambda x: Stream(x), cameras))

        # Runs a detection thread
        self.__detect()

    # Deconstructor releases camera captures
    def __del__(self):
        for capture in self.__captures:
            capture.capture.release()

    # Detection code runs in thread created on init
    def __detect(self):
        while True:
                # List of current frames
                frames = list(map(lambda x: x.getFrame(), self.__captures))

                # Horizontally concats the images from N number frames
                im_concat = cv2.hconcat(frames)

                # Resizes the images
                im_resized = cv2.resize(im_concat, (self.__width, self.__height))

                # Prep for object detection
                frame_rgba = cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGBA)
                img = jetson_utils.cudaFromNumpy(frame_rgba)

                # Object Detection
                self.__detections = self.__net.Detect(img, self.__width, self.__height)		# Detect objects, put them in a list
                if self.__render:
                        self.__display.RenderOnce(img, width = self.__width, height = self.__height, normalize=0, format='rgb8')			# Renders the display
                        self.__display.SetTitle("Object Detection | Network {:.0f} FPS".format(self.__net.GetNetworkFPS()))
                self.getTransceiver()

    # Choose the transceiver number
    def getTransceiver(self):
        # Placeholder code
        for detection in self.__detections:
              if (detection.ClassID == 1):
                print("TurtleBot found at ({})".format(detection.Center))
                return detection.Center
        return -1