import cv2
from threading import Thread

# Define Stream class
class Stream:
	def __init__(self, src):
		self.capture = cv2.VideoCapture(src)
		_,self.frame = self.capture.read()							# Read frame on init, Prevent the code from running until one frame has been read
		self.thread = Thread(target = self.__update, args = ())     # Instantiates a thread that runs the private update method
		self.thread.daemon = True									# Destroys threads automatically when program exits
		self.thread.start()                                         # Starts the thread

	# Update method is automatically called on initialization and run in a thread
	def __update(self):
		while True:
			_,self.frame = self.capture.read()
			
    # Returns the current frame in the frame field
	def getFrame(self):
		return self.frame