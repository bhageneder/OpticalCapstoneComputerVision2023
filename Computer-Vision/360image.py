import cv2

# Simplified Stream Definition
class Stream:
	def __init__(self, src):
		self.capture = cv2.VideoCapture(src)
		_,self.frame = self.capture.read()

	def getFrame(self):
		return self.frame

frames = list()

for i in range(3):
	cap = Stream(i)
	frames.append(cap.getFrame())
	cap.capture.release()

im_concat = cv2.hconcat([frames[0], frames[1], frames[2]])

im_resized = cv2.resize(im_concat, (int((1280*3)/2), int(720/2)))

while True:
	cv2.imshow('360 Degree Panorama', im_resized)

	if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			exit(1)
