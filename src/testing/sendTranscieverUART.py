from src.classes.DetectorClass import Detector
from threading import Thread
from UART import UART 
import time
import cv2

##### Sends the Transceiver Assignment over UART to the Pi #####
def main():
    # Only use the cameras in this set
    camSet1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method="2" ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! appsink'

    #cameras = [camSet1, 2, 1]
    cameras = [2,1]

    # Initialize Detection    240
    detector = Detector(1280, 360, "Robot_Model_Pan2", cameras, True, True, True)

    # Run Detection in a Thread
    detectionThread = Thread(target = detector.detect, args = (), daemon=True, name="Detect")
    detectionThread.start()

    # Wait Until Detection is Initialized
    while detector.initializing:
        continue

    # Initialize UART
    connection = UART()
    
    try:
        # Infinite Loop to Send Data
        while(True): 
            transceiver = detector.getTransceiver()
            if(connection.send(transceiver) != 0):
                print("UART Send Failed")
            #print(transceiver)
            """
            # For Auto Deconstructor Purposes
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Killing Detection Thread")
                detector.setStopFlag()
                time.sleep(1)
                detectionThread.join()
                cv2.destroyAllWindows()
                time.sleep(1.5) # If deconstructed too quickly, deconstructor tries to release camera before its done destroying window                
                del detector                
                break
            """                
         
            # Sleep
            time.sleep(0.05)            

    except KeyboardInterrupt:
        pass

    # Close Serial Connection
    connection.close()

    exit(0)

if __name__ == "__main__":
    main()
