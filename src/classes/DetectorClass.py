import math
import cv2
import jetson_inference
import jetson_utils
from classes.StreamClass import Stream
from classes.RobotClass import Robot
import config.global_vars as g
import os
import queue
from interfaces.BaseDetectorClass import BaseDetector

class Detector(BaseDetector):
        # Constructor
        # Parameters: Width of Output Frame, Height of Output Frame, Object Detection Model Name, List of Camera Names [e.g., [0, 1, ...]), render (default false), debug (default false)
        def __init__(self, width, height, modelName, modelPath, cameras, render = False, debug = False):
                super.__init__
                self.initializing = True
                self.visibleQ = queue.Queue()
                self.lostQ = queue.Queue()
                self.__width = width
                self.__height = height
                self.__render = render
                self.__debug = debug
                #self.__stopFlag = False """ For Auto Deconstruct Purposes """
                self.__trackingMinFrames = 10
                self.__DropFramesFrames = 20
                self.__trackingOverlapThreshold = 0.5
                self.__sections = math.ceil(2.5*len(cameras))
                self.__division = 2 * self.__sections # Create the width of the divison (width/2*section)) or half the width of a section
                self.__current_transceiver = -1
                self.__robotList = list()
                self.__lostRobotList = list()
                
                # Set up detect net for the custom model
                self.__net = jetson_inference.detectNet(model=(modelPath + modelName + "/ssd-mobilenet.onnx"), labels=(modelPath + modelName + "/labels.txt"), input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

                self.__net.SetTrackingEnabled(True)
                self.__net.SetTrackingParams(self.__trackingMinFrames, self.__DropFramesFrames, self.__trackingOverlapThreshold)

                # Private list to hold captures
                self.__captures = list(map(lambda x: Stream(x), cameras))

        # Destructor
        # Releases camera captures and destroys windows
        def __del__(self):
                for cap in self.__captures:
                        cap.capture.release()
                        print("Released")
                cv2.destroyAllWindows()

        #### Public Methods ####

        """        
        # For Auto Deconstruct Purposes        
        def setStopFlag(self):
                self.__stopFlag = True
        """           
    
        # Detect Method: Call this method in its own thread
        def detect(self):
                # while not stopFlag
                while True:
                        # List of current frames
                        frames = list(map(lambda x: x.getFrame(), self.__captures))

                        # Horizontally concats the images from N number of frames and Resizes concatenated frames
                        im_resized = cv2.resize((cv2.hconcat(frames)), (self.__width, self.__height))

                        # Prep for object detection
                        frame_rgba = cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGBA)
                        img = jetson_utils.cudaFromNumpy(frame_rgba)

                        #Object Detection
                        self.__detections = self.__net.Detect(img, self.__width, self.__height)

                        # Only do this if we want a rendered output for debugging                        
                        if self.__render:                       
                            # Convert the image to Numpy format
                            img_2 = jetson_utils.cudaToNumpy(img)
                        
                            starting_section = 3 # Section modified after first line is drawn
                            incrementer = 2 # Increment to control the increase at which sections are chosen (i.e. 1/10 -> 3/10 -> 5/10)
                            
                            # Create the initial line segment ot use in the iterative loop
                            previous_line = cv2.line(img_2, (int(self.__width/self.__division), 0), (int(self.__width/self.__division), self.__height), (0,0,0), 5)

                            # Loop to append previous frame with new segment line until entire frame is covered
                            while(starting_section < self.__division):
                                    cv2.line(previous_line, ((starting_section*int(self.__width/self.__division)), 0), ((starting_section*int(self.__width/self.__division)), self.__height), (0,0,0), 5)
                                    starting_section = starting_section + incrementer

                            # Convert the image to correct color format
                            im_finalized = cv2.cvtColor(previous_line, cv2.COLOR_RGBA2BGR)

                            # Output image to the display
                            cv2.imshow('Detection', im_finalized)

                            # Set the title of the window (Cannot do it above, it will render many windows)
                            cv2.setWindowTitle("Detection", "Object Detection | Network {:.0f} FPS".format(self.__net.GetNetworkFPS()))

                            # Close the display and break out of the loop if 'q' is pressed
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                cv2.destroyAllWindows()
                                break

                        # Update the robotList
                        self.__updateRobotList()
                        
                        self.initializing = False

        #### Private Helper Methods ####

        # Helper method to update the robot list
        def __updateRobotList(self):
                def obtain_transceiver_number(Center_Of_Object, width_of_frame):
                        # Use integer division to obtain a section the object is detected in
                        #normalized_x = (Center_Of_Object // (width_of_frame // self.__division))            
                        normalized_x = (Center_Of_Object // (width_of_frame / self.__division))
                        
                        # Edge Cases
                        if (normalized_x == 0):
                                normalized_x = self.__sections
                        # Mathematics found in the ReadME for logic
                        else:
                                normalized_x = (normalized_x / 2 + 1) if normalized_x % 2 == 1 else (normalized_x / 2)                               

                        section = int(normalized_x) - 1
                        
                        # Offset the value to line up with numbers on physical transceivers
                        section = (section + 4) if section < 4 else (section - 4)

                        return section

                # Create a list to store found robot indeces
                foundRobotIndeces = list()

                # Acquire Visible Robot List Mutex
                with g.visible_mutex:
                        # Loop through all detections, create robots
                        for detection in self.__detections:
                                # If the detection is a robot and is tracked
                                if (detection.ClassID == 1 and detection.TrackID > -1):
                                        # Get the best transceiver for the robot and tracking information
                                        transceiver = obtain_transceiver_number(detection.Center[0], self.__width)
                                        # The trackID must be incremented by 1
                                        # Cannot start trackID at 0, or the associative ping will fail
                                        trackID = detection.TrackID + 1
                                        trackingStatus = detection.TrackStatus

                                        # Flag for when the loop identifies the robot
                                        foundRobotFlag = False

                                        # Find tracking ID in robot list
                                        for i in range(0, len(g.visible)):
                                                # If we are on the correct robot, update the tracking information
                                                if (g.visible[i].trackID == trackID):
                                                        foundRobotFlag = True
                                                        foundRobotIndeces.append(i)

                                                        # Update Transceiver
                                                        g.visible[i].transceiver = transceiver

                                                        # Exit inner loop
                                                        break

                                        # Check if the code in the loop executed
                                        # If not, create a new robot object and store in the visibleQ
                                        if not foundRobotFlag:
                                                self.visibleQ.put(Robot(trackID, transceiver))
                                        
                                        # Debug statement
                                        if (self.__debug):
                                                print("Current Tracking Status for ID {} is: {} using transceiver {}".format(trackID, trackingStatus, transceiver))

                        # Make a copy of the robot list
                        robotListCopy = g.visible[:]

                # Release Visible Robot Mutex

                # Remove all the found elements from the list
                for i in sorted(foundRobotIndeces, reverse=True):
                        robotListCopy.pop(i)

                # Queue up lost robots
                for robot in robotListCopy:
                        # Queue it to the lostQ
                        self.lostQ.put(robot)
