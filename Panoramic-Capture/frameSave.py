import cv2
import datetime
import os
import time
import sys
sys.path.append("/home/sa/Documents/OpticalCapstoneComputerVision2023/Computer-Vision")
from Stream import Stream

def main():
    # Open Camera Captures
    camSet1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method="2" ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! appsink'
    
    streams = [Stream(camSet1), Stream(2), Stream(1)]

    time.sleep(5)   

    # Default Path
    path = os.getcwd()
    print("Current Directory: {}".format(path))

    # Img Path
    imgPath = path + "/JPEGImages"

    # Make Directories if They Don't Exist
    if not os.path.isdir(imgPath):
        os.mkdir(imgPath)
    
    # Keep going until the user quits
    while(True):
        # Get frames from each camera
        frames = []
        for stream in streams:
            frames.append(stream.getFrame())

        # Concatenate into one frame
        img = cv2.hconcat(frames)

        # Output image to the display
        cv2.imshow('Panorama', cv2.resize(img, (1280, 240)))

        # Obtain and store current image
        os.chdir(imgPath)
        # Write the image
        name = str(datetime.datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-") + ".jpg"
        cv2.imwrite(name, img)
        print("Frame Captured!")

        # Close the display and break out of the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(5)

    # Release the streams 
    for stream in streams:
        stream.capture.release()
        print("released")

    # Destroy Windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
