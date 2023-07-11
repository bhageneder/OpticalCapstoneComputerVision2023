import jetson_inference
import jetson_utils
import cv2
from Stream import Stream

# Must be called in its own thread
class Detection:
        # Parameters: Width of Output Frame, Height of Output Frame, Object Detection Model Name, List of Camera Names [e.g., [0, 1, ...]), render (Boolean)
        def __init__(self, width, height, modelName, cameras, render):
                self.__width = width
                self.__height = height
                self.__render = render
                
                # Set up detect net for the custom model
                self.__net = jetson_inference.detectNet(model=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/ssd-mobilenet.onnx", labels=f"/home/sa/jetson-inference/python/training/detection/ssd/models/{modelName}/labels.txt", input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)
                
                # Intialize the display window
                if self.__render:
                        self.__display = jetson_utils.glDisplay()

                # Private list to hold captures
                self.__captures = list(map(lambda x: Stream(x), cameras))

                # Runs the detection method
                self.__detect()

        # Deconstructor releases camera captures
        def __del__(self):
                for capture in self.__captures:
                        capture.capture.release()

        # Detection code runs in thread created on init
        def __detect(self):
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

                        img_2 = jetson_utils.cudaToNumpy(img)
                        
                        starting_section = 3 # Section modified after first line is drawn
                        incrementer = 2 # Increment to control the increase at which sections are chosen (i.e. 1/10 -> 3/10 -> 5/10)
                        sections = 5
                        division = 2 * sections # Create the width of the divison (width/2*section)) or half the width of a section
                        
                        # Create the initial line segment ot use in the iterative loop
                        previous_line = cv2.line(img_2, (int(self.__width/division), 0), (int(self.__width/division), self.__height), (0,0,0), 5)

                        # Loop to append previous frame with new segment line until entire frame is covered
                        while(starting_section < division):
                                im_line = cv2.line(previous_line, ((starting_section*int(self.__width/division)), 0), ((starting_section*int(self.__width/division)), self.__height), (0,0,0), 5)
                                previous_line = im_line
                                starting_section = starting_section + incrementer
                        im_finalized = previous_line
                        
                        img_3 = jetson_utils.cudaFromNumpy(im_finalized)

                        if self.__render:
                                self.__display.RenderOnce(img, width = self.__width, height = self.__height, normalize=0, format='rgb8')
                                self.__display.SetTitle("Object Detection | Network {:.0f} FPS".format(self.__net.GetNetworkFPS()))
                        self.getTransceiver()

        # Choose the transceiver number
        def getTransceiver(self):

                """
                Method_Name: indirect
                params_type: int j
                param_desc: j is the integer division from the center location of the object and the frame division
                return_type: int j
                return_desc: j is the modified integer that represents the transceiver number to use for each section
                """
                def indirect(j):
                        # Edge Cases
                        if (j == 0):
                                j = 5
                        elif (j == 1):
                                j = 1 
                        # Mathematics found in the ReadME for logic
                        else:
                                if (j%2 == 1):
                                        j = j/2 + 1
                                else:
                                        j = j/2
                        return int(j)

                """
                Method_Name: object_transceiver_number
                params_type: int Center_Of_Object, width_of_frame
                param_desc (Center_Of_Object): value of the center pixel location of the detect object
                param_desc (width_of_frame): value of the frame width determined from frame concat
                return_type: int normalized_x
                return_desc: normalized_x is the modified integer that represents the transceiver number to use for each section
                """
                def obtain_transceiver_number(Center_Of_Object, width_of_frame):
                        # Use integer division to obtain a section the object is detected in
                        normalized_x = int(((int(Center_Of_Object) / int(width_of_frame/10))))
                        print("normalized_x before indirect is {}".format(normalized_x))
                        normalized_x = indirect(normalized_x)
                        print("The Ball is in Section {}, Using transceiver {}".format(normalized_x, normalized_x))
                        return normalized_x                
               
                # Placeholder code
                for detection in self.__detections:
                        if (detection.ClassID == 1):
                                transceiver_number = obtain_transceiver_number(detection.Center[0], self.__width)
                                return transceiver_number
                return -1
                        