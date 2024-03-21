import cv2
import datetime
import os
import time
import sys
sys.path.append("/home/orin/Documents/OpticalCapstoneComputerVision2023/src/classes")
from StreamClass import Stream


def main():
    # Open Camera Captures
    camSet1="v4l2src device=/dev/video0 ! image/jpeg,format=MJPG,width=1280,height=720,framerate=30/1 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
    camSet2="v4l2src device=/dev/video2 ! image/jpeg,format=MJPG,width=1280,height=720,framerate=30/1 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
    camSet3="v4l2src device=/dev/video4 ! image/jpeg,format=MJPG,width=1280,height=720,framerate=30/1 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"

    
    streams = [Stream(camSet1), Stream(camSet2), Stream(camSet3)]

    time.sleep(5)   

    # Default Path
    path = os.getcwd()
    print("Current Directory: {}".format(path))

    # Img Path
    imgPath = path + "/JPEGImages"

    # Make Directories if They Don't Exist
    if not os.path.isdir(imgPath):
        os.mkdir(imgPath)

    # Create a stop until key press so that the person can setup robots for image capturing.
    input("Press Enter to begin taking images...")

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

        time.sleep(2)

    # Release the streams 
    for stream in streams:
        stream.capture.release()
        print("released")

    # Destroy Windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
