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
    for i in range(1, 3):
        streams.append(Stream(i))

    time.sleep(5)

    # Object = TurtleBot, can parameterize the function later
    boxedObject = "TurtleBot"    

    # Default Path
    path = os.getcwd()

    # Current folder
    partialPaths = path.split("/")
    folder = partialPaths[len(partialPaths) - 1]

    # Img Path
    imgPath = path + "/JPEGImages"
    
    # Ann Path
    annPath = path + "/Annotations"

    # Sets Path
    setsPath = path + "/ImageSets"

    # Sets Path Main
    setsPathMain = setsPath + "/Main"

    # Make Directories if They Don't Exist
    if not os.path.isdir(imgPath):
        os.mkdir(imgPath)

    if not os.path.isdir(annPath):
        os.mkdir(annPath)

    if not os.path.isdir(setsPath):
        os.mkdir(setsPath)

    if not os.path.isdir(setsPathMain):
        os.mkdir(setsPathMain)
    
    
    # Keep going until the user quits
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
            ### Take Picture ###
            print("Taking picture...")

            # Set Directory
            os.chdir(imgPath)

            # Write the image
            name = str(datetime.datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-") + ".jpg"
            cv2.imwrite(name, img)

            print("Success!")

            # Destroy the imshow window
            cv2.destroyAllWindows()
            
            ### Draw Bounding Box ###
            # Select Region of Interest
            roi = cv2.selectROI(img)            
            print(roi)

            # Destroy the ROI window
            cv2.destroyAllWindows()

            ### Save Data into XML File (Make Annotations) ###
            # Change Directory
            os.chdir(annPath)

            # Need to remove .jpg from the name of the image first
            nameNoJPG = name.replace(".jpg", "")

            # Make the File
            xmlFile = open(nameNoJPG + ".xml", "x")   # Makes an XML file with name = name, permissions = x [create]
            
            # Write output to file
            xmlFile.write(f'''
<annotation>
    <filename>{name}</filename>
    <folder>{folder}</folder>
    <source>
        <database>{folder}</database>
        <annotation>custom</annotation>
        <image>custom</image>
    </source>
    <size>
        <width>{img.shape[1]}</width>
        <height>{img.shape[0]}</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>{boxedObject}</name>
        <pose>unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{roi[0]}</xmin>
            <ymin>{roi[1]}</ymin>
            <xmax>{roi[2]}</xmax>
            <ymax>{roi[3]}</ymax>
        </bndbox>
    </object>
</annotation>''')            
            
            # Close file
            xmlFile.close()

            ### Add the Image to the Train.txt Image Set
            # Change Directory
            os.chdir(setsPathMain)

            # Append Train.txt, Create it if it Doesn't Exist
            trainFile = open("Train.txt", "a")
            
            # Write to Train.txt
            trainFile.write(nameNoJPG + "\n")
            
            # Close Train.txt
            trainFile.close()
            
    
    # Release the streams 
    for stream in streams:
        stream.capture.release()
        print("released")

    # Destroy Windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
