from Detector import Detector
from threading import Thread
from UART import UART 
import time

##### Sends the Transceiver Assignment over UART to the Pi #####
def main():
    # Only use the cameras in this set
    camSet1 = 'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method="2" ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! appsink'

    #cameras = [camSet1, 2, 1]

    # Initialize Detection    
    detector = Detector(1280, 240, "Robot_Model_Pan2", cameras, True, True, True)

    # Run Detection in a Thread
    thread = Thread(target = detector.detect, args = (), daemon=True, name="Detect")
    thread.start()

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
            
            # Sleep
            time.sleep(0.01)            

    except KeyboardInterrupt:
        pass
    except:
        print("Get Transceiver or Send Error") 

    # Close Serial Connection
    connection.close()

    exit(0)

if __name__ == "__main__":
    main()
