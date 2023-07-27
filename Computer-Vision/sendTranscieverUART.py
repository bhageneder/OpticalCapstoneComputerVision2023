from Detection import Detection
from threading import Thread
from UART import UART 

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
    while True:
        if(not detection.initializing):
            break

    # Initialize UART
    connection = UART()

    # Infinite Loop to Send Data
    while(True):       
        try:	
            transceiver = detection.getTransceiver()
            connection.send(transceiver)
        except KeyboardInterrupt:
            break
        except:
            print("Detection Error") 

    # Close Serial Connection
    connection.close()

    exit(0)

if __name__ == "__main__":
    main()