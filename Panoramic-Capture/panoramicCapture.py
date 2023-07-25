import cv2
import datetime
import os
import time
import sys
sys.path.append("/home/sa/Documents/OpticalCapstoneComputerVision2023/Computer-Vision")
from Stream import Stream

def main():
    # Open Camera Captures
    streams = []
    for i in range(3):
        streams.append(Stream(i))

    time.sleep(5)

    # Set Directory
    dir = os.getcwd() + "/images"
    os.chdir(dir)

    while(True):
        # Get frames from each camera
        frames = []
        for stream in streams:
            frames.append(stream.getFrame())

        # Concatenate into one frame
        img = cv2.hconcat(frames)

        # Write the image
        cv2.imwrite(datetime.datetime.now().replace(" ", "_"), img)

        time.sleep(5)

if __name__ == "__main__":
    main()