from Detection import Detection
from threading import Thread
from UART import UART 
import time

##### Sends the Transceiver Assignment over UART to the Pi #####
def main():
    # Only use the cameras in this set
    cameras = [0]

    # Initialize Detection
    detection = Detection(1280, 720, "robots_only", cameras, True, False)

    # Run Detection in a Thread
    thread = Thread(target = detection.detect, args = (), daemon=True, name="Detect")
    thread.start()

    # Wait Until Detection is Initialized
    while detection.initializing:
        continue

    # Initialize UART
    connection = UART()
    
    try:
        # Infinite Loop to Send Data
        while(True):       
            	
            transceiver = detection.getTransceiver()
            if(connection.send(transceiver) != 0):
                print("UART Send Failed")
            
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
