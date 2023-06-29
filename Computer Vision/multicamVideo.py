import cv2
cap0 = cv2.VideoCapture(0)

cap1 = cv2.VideoCapture(1)

while(cap0.isOpened()):
	ret0, frame0 = cap0.read()
	ret1, frame1 = cap1.read()

	if ret0:
		im_concat = cv2.hconcat([frame0, frame1])

		im_resized = cv2.resize(im_concat, (1280, 360))   

		cv2.imshow('Combined Video', im_resized)

		if cv2.waitKey(1) & 0xFF == ord('q'):
            		break

	else: 
		break

cap0.release()
cap1.release()


cv2.waitKey(0)
cv2.destroyAllWindows()
