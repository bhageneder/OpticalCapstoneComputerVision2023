import math
import cv2
import jetson_inference
import jetson_utils
from classes.StreamClass import Stream
from classes.RobotClass import Robot
from interfaces.iDetectorClass import iDetector
import config.global_vars as g
import os


class Detector(iDetector):
        # Constructor
        # Parameters: Width of Output Frame, Height of Output Frame, Object Detection Model Name, List of Camera Names [e.g., [0, 1, ...]), render (default false), debug (default false)
        def __init__(self, width, height, cameras, render = False, tracking=False, debug = False):
                super().init()
                self.initializing = True
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

                # Set up detect net for the custom model
                print(g.modelPath + g.model + "/ssd-mobilenet.onnx")
                self.__net = jetson_inference.detectNet(model=(g.modelPath + g.model + "/ssd-mobilenet.onnx"), labels=(g.modelPath + g.model + "/labels.txt"), input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)

                self.__net.SetTrackingEnabled(tracking)
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

        # Transceiver Getter
        def getTransceiver(self):
               return self.__current_transceiver
        
        # robotList Getter
        def getRobotLlist(self):
                return self.__robotList
        
        # lostRobotList Getter
        def getLostRobotLlist(self):
                return self.__lostRobotList

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

                        # Update the transceiver/robotList
                        self.__updateTransceiver()
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

                # Create a copy of the robotList
                robotListCopy = self.__robotList[:]

                # Create a list to store found robot indeces
                foundRobotIndeces = list()

                # Loop through all detections, create robots
                for detection in self.__detections:
                        # If the detection is a robot
                        if (detection.ClassID == 1 and detection.TrackID > -1):
                                # Get the best transceiver for the robot and tracking information
                                transceiver = obtain_transceiver_number(detection.Center[0], self.__width)
                                trackingID = detection.TrackID
                                trackingStatus = detection.TrackStatus

                                # Flag for when the loop identifies the robot
                                foundRobotFlag = False

                                # Find tracking ID in robot list
                                for i in range(0, len(self.__robotList)):
                                        # If we are on the correct robot, update the tracking information
                                        if (self.__robotList[i].trackingID == trackingID):
                                                foundRobotFlag = True
                                                foundRobotIndeces.append(i)

                                                # In theory, this is always true if the detection is in the list
                                                self.__robotList[i].losActive = False if trackingStatus == -1 else True

                                                # Only update the transceiver if the LOS is active. In theory this should always be true (see above)
                                                if (self.__robotList[i].losActive):
                                                        self.__robotList[i].transceiver = transceiver

                                                # Exit inner loop
                                                break

                                # Check if the code in the loop executed
                                # If so, remove from robotListCopy 
                                # If not, create a new robot object and store in the robotList
                                if not foundRobotFlag:
                                       newRobot = Robot(trackingID, transceiver, True)
                                       self.__robotList.append(newRobot)
                                       
                                # Debug statement
                                if (self.__debug):
                                        print("Current Tracking Status for ID {} is: {} using transceiver {}".format(trackingID, trackingStatus, transceiver))

                # Remove all the found elements from the list
                for i in sorted(foundRobotIndeces, reverse=True):
                        robotListCopy.pop(i)

                # Cleanup missing robots
                popList = list()
                for robot in robotListCopy:
                        for i in range(0, len(self.__robotList)):
                                if (robot == self.__robotList[i]):
                                        # Identified one of the missing robots in the robots list
                                        # Remove it and append to the Lost Robot List only if the robot has a link already
                                        if robot.RobotLink != None:
                                                self.__lostRobotList.append(self.__robotList[i])

                                        # Add the robot to the 'needs to be removed' from Robot List list
                                        popList.append(i)

                # Pop all lost robots out of robotList
                for i in reversed(popList):
                        self.__robotList.pop(i)

                # Debug Statements
                if self.__debug:
                    print("Robot List: " + str(self.__robotList) + "\n")
                    print("Lost Robot List: " + str(self.__lostRobotList) + "\n")


        #### Remove __updateTransceiver when __updateRobotList is officially working ####

        # Helper method to update the transceiver number
        def __updateTransceiver(self):
                """
                Function_Name: obtain_transceiver_number
                params_type: int Center_Of_Object, width_of_frame
                param_desc (Center_Of_Object): value of the center pixel location of the detect object
                param_desc (width_of_frame): value of the frame width determined from frame concat
                return_type: int normalized_x
                return_desc: normalized_x is the modified integer that represents the transceiver number to use for each section
                """
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
                
                # Loop through the detections, update the transceiver number when there is a robot detected
                # Note that this is a temporary implementation, we should, in the future attempt to communicate with all robots...
                # ...using all sections that a robot is found in, not just the last one in the list
                for detection in self.__detections:
                        if (detection.ClassID == 1):
                                if (self.__debug):
                                    print("Current Tracking Status for ID {} is: {}".format(detection.TrackID, detection.TrackStatus))
                                self.__current_transceiver = obtain_transceiver_number(detection.Center[0], self.__width)   
                
                if (self.__debug):        
                        print("The best transceiver is number {}".format(self.__current_transceiver))
