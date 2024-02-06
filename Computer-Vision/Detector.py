import jetson_inference
import jetson_utils
import cv2
import math
from Stream import Stream

class Detector:
        # Constructor
        # Parameters: Width of Output Frame, Height of Output Frame, Object Detection Model Name, List of Camera Names [e.g., [0, 1, ...]), render (Boolean)
        def __init__(self, width, height, modelName, cameras, render = False, debug = False):
                self.initializing = True
                self.__width = width
                self.__height = height
                self.__render = render
                self.__current_transceiver = 8
                self.__debug = debug
                self.__cameras = cameras
                self.__sections = math.ceil(2.5*len(cameras))
                self.__division = 2 * self.__sections # Create the width of the divison (width/2*section)) or half the width of a section
                
                # Set up detect net for the custom model
                self.__net = jetson_inference.detectNet(model=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/ssd-mobilenet.onnx", labels=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)
                
                # Intialize the display window
                if self.__render:
                        self.__display = jetson_utils.glDisplay()

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
               
        # Detect Method: Call this method in its own thread
        def detect(self):
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

                        self.__updateTransceiver()
                        
                        self.initializing = False

        #### Private Helper Methods ####

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
                        #normalized_x = int(int(Center_Of_Object) / int(width_of_frame / self.__division))
                        normalized_x = int(Center_Of_Object / (width_of_frame / self.__division))

                        
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
                                self.__current_transceiver = obtain_transceiver_number(detection.Center[0], self.__width)   
                
                if (self.__debug):        
                        print("The best transceiver is number {}".format(self.__current_transceiver))