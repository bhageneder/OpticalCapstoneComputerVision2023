from threading import Thread
import cv2

# Define Stream class
class Stream:
    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        _,self.__frame = self.capture.read()							# Read frame on init, Prevent the code from running until one frame has been read
        self.__thread = Thread(target = self.__update, args = ())       # Instantiates a thread that runs the private update method
        self.__thread.daemon = True									    # Background threads. Destroys threads automatically when program exits
        self.__thread.start()                                           # Starts the thread

	# Update method is automatically called on initialization and run in a thread
    def __update(self):
        while True:
            _,self.__frame = self.capture.read()

    # Returns the current frame in the frame field
    def getFrame(self):
        return self.__frame
