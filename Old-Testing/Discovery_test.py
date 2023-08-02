import jetson_inference
import jetson_utils
import cv2
import math
from Stream import Stream

# Must be called in its own thread
class Detection:
        # Parameters: Width of Output Frame, Height of Output Frame, Object Detection Model Name, List of Camera Names [e.g., [0, 1, ...]), render (Boolean)
        def __init__(self, width, height, modelName, cameras, render = False, debug = False):
                self.initializing = True
                self.__width = width
                self.__height = height
                self.__render = render
                self.__current_transceiver = -1
                self.__debug = debug

                self.__starting_section = 3 # Section modified after first line is drawn
                self.__incrementer = 2 # Increment to control the increase at which sections are chosen (i.e. 1/10 -> 3/10 -> 5/10)
                self.__sections = math.ceil(2.5*len(cameras)) # Rounding up the sections to match the frames provided (2.5->3, 5->5, 7.5->8)
                self.__division = 2 * self.__sections # Create the width of the divison (width/2*section)) or half the width of a section

                # Set up detect net for the custom model
                self.__net = jetson_inference.detectNet(model=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/ssd-mobilenet.onnx", labels=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)
                
                # Intialize the display window
                if self.__render:
                        self.__display = jetson_utils.glDisplay()

                # Private list to hold captures
                self.__captures = list(map(lambda x: Stream(x), cameras))

                # Runs the detection method
                #self.__detect()

        # Deconstructor releases camera captures and destroys windows
        def __del__(self):
                for cap in self.__captures:
                        cap.capture.release()
                        print("Released")
                cv2.destroyAllWindows()
               
        # Detection code runs in thread created on init
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
                            
                            # Create the initial line segment ot use in the iterative loop
                            cv2.line(img_2, (int(self.__width/self.__division), 0), (int(self.__width/self.__division), self.__height), (0,0,0), 5)

                            # Loop to append previous frame with new segment line until entire frame is covered
                            while(self.__starting_section < self.__division):

                                    cv2.line(img_2, ((self.__starting_section*int(self.__width/self.__division)), 0), ((self.__starting_section*int(self.__width/self.__division)), self.__height), (0,0,0), 5)
                                    self.__starting_section = self.__starting_section + self.__incrementer

                            # Convert the image to correct color format
                            im_finalized = cv2.cvtColor(img_2, cv2.COLOR_RGBA2BGR)

                            # Output image to the display
                            cv2.imshow('Detection', im_finalized)

                            # Set the title of the window (Cannot do it above, it will render many windows)
                            cv2.setWindowTitle("Detection", "Object Detection | Network {:.0f} FPS".format(self.__net.GetNetworkFPS()))

                            # Close the display and break out of the loop if 'q' is pressed
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                cv2.destroyAllWindows()
                                break

                        #self.getTransceiver()
                        
                        self.initializing = False

        # Choose the transceiver number
        def getTransceiver(self):

                """
                Method_Name: indirect
                params_type: int j
                param_desc: j is the integer division from the center location of the object and the frame division
                return_type: int j
                return_desc: j is the modified integer that represents the transceiver number to use for each section from the range [0:7]
                """
                def indirect(j):
                        # Edge Cases when object enters 0~22.5 degrees of panoramic which would be the final half of the last transceivers 45 degree FOV
                        if (j == 0):
                                j = self.__sections
                        # Mathematics found in the ReadME for logic
                        else:
                                if (j%2 == 1):
                                        j = j/2 + 1
                                else:
                                        j = j/2
                        return (int(j)-1)

                """
                Method_Name: obtain_transceiver_number
                params_type: int Center_Of_Object, width_of_frame
                param_desc (Center_Of_Object): value of the center pixel location of the detect object
                param_desc (width_of_frame): value of the frame width determined from frame concat
                return_type: int normalized_x
                return_desc: normalized_x is the modified integer that represents the transceiver number to use for each section
                """
                def obtain_transceiver_number(Center_Of_Object, width_of_frame):
                        # Use integer division to obtain a section the object is detected in
                        normalized_x = int(int(Center_Of_Object) / int(width_of_frame/self.__division))
                        #print("normalized_x before indirect is {}".format(normalized_x)) # Helpful print statement
                        normalized_x = indirect(normalized_x)
                        normalized_x -= 1
                        return normalized_x                
               
                for detection in self.__detections:
                        if (detection.ClassID == 1):
                                transceiver_number = obtain_transceiver_number(detection.Center[0], self.__width)
                                self.__current_transceiver = transceiver_number
                                if (self.__debug):        
                                    print("The Ball is in Section {}, Using transceiver {}".format(self.__current_transceiver, self.__current_transceiver))
                                return transceiver_number                            
                if (self.__debug):
                    print("The Ball is in Section {}, Using transceiver {}".format(self.__current_transceiver, self.__current_transceiver))
                return self.__current_transceiver
