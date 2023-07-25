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
        if(i >= 1):
            streams.append(Stream(i))

    time.sleep(5)

    # Set Directory
    dir = os.getcwd() + "/images"
    os.chdir(dir)
    
    i = 0

    while(True):
        # Get frames from each camera
        frames = []
        for stream in streams:
            frames.append(stream.getFrame())

        # Concatenate into one frame
        img = cv2.hconcat(frames)

        # Output image to the display
        cv2.imshow('Panorama', img)

        # Close the display and break out of the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('y'):
            print("Taking picture...")

            # Write the image
            name = str(datetime.datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-") + ".jpg"
            cv2.imwrite(name, img)

            print("Success!")

    for stream in streams:
        stream.capture.release()
        print("released")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
