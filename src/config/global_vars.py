import queue
import threading
import configparser
import board

'''
Contains global variables that will be used across all files
'''
def init():
    global working_dir
    working_dir = None

    global lights_enabled
    lights_enabled = True

    global debug_discovery
    debug_discovery = True

    global debug_link_send
    debug_link_send = True

    global debug_link_receive
    debug_link_receive = True

    global debug_connection_manager
    debug_connection_manager = True

    global debug_listen_for_connection
    debug_listen_for_connection = True

    global debug_maintenance
    debug_maintenance = False

    global debug_mini_discovery
    debug_mini_discovery = False

    global debug_mini_maintenance
    debug_mini_maintenance = False

    global debug_receive_manager
    debug_receive_manager = True

    global debug_send_manager
    debug_send_manager = False

    global debug_transceiver_receive
    debug_transceiver_receive = False

    global debug_transceiver_send
    debug_transceiver_send = False

    global debug_packet_manager
    debug_packet_manager = False

    global debug_log_packets
    debug_log_packets = False

    global debug_logger
    debug_logger = False

    # From testing, duplicate maintenance packets are very useful
    # in determining the best transceiver. The more duplicate packets
    # received, the better the communication of that transceiver with the other robot.
    # In other words, if a transceiver can transmit data, and that data can be received
    # by 3 other transceivers on the other robot, then that is a good transceiver to use.
    # So ignoring duplicate maintenance packets should be set to False for the best results.
    global ignoring_duplicate_maintenance_packets
    ignoring_duplicate_maintenance_packets = False

    global robot_links
    robot_links = []
    
    # Prevent multiple threads modifying the robot_links list simultaneously
    global robot_links_mutex
    robot_links_mutex = threading.Lock()
    
    global transceiver_send_threads 
    transceiver_send_threads = []
    
    global transceiver_receive_threads 
    transceiver_receive_threads = []
    
    global listen_for_connection_threads
    listen_for_connection_threads = []
    
    global receive_manager_thread
    receive_manager_thread = None
    
    global send_manager_thread
    send_manager_thread = None
    
    global discovery_thread
    discovery_thread = None

    global detector_thread
    discovery_thread = None

    # Visible Robots List (Active LOS)
    global visible
    visible = []

    # Visible Robots List Mutex
    global visible_mutex
    visible_mutex = threading.Lock()

    # Lost Robots List (No Active LOS)
    global lost
    lost = []

    # Lost Robots List Mutex
    global lost_mutex
    lost_mutex = threading.Lock()

    global new_visible_thread
    new_visible_thread = None

    global new_lost_thread
    new_lost_thread = None

    # Queue for data that is received by all transceivers
    global data_received
    data_received = queue.Queue()
    
    # Queue for passing data to the maintenance thread
    global maintenance_data_received
    maintenance_data_received = queue.Queue()
    
    # Queue for passing data to the discovery thread
    global discovery_data_received
    discovery_data_received = queue.Queue()
    
    # Queue for other threads signify new robot links need to be maintained. Legacy version of newRobotQ
    global robot_links_new
    robot_links_new = queue.Queue()

    # Queue to create threads when new robots are created. 
    global newRobotQ
    newRobotQ = queue.Queue()
    
    # Queues for each of the Transceiver Send Threads (8 Transceivers)
    global transceiver_send_queues
    transceiver_send_queues = [
        queue.Queue(), queue.Queue(), queue.Queue(),queue.Queue(),
        queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()]
    
    # Mutex to prevent transceivers jamming eachother with simultaneous sends
    global transeiver_send_mutex
    transeiver_send_mutex = threading.Lock()
    
    # The name of the robot running the program
    global robot
    config = configparser.ConfigParser()
    config.read("./config/config.cfg")
    robot = config['Name']['robotName']

    # The cameras to use for vision
    global cameras
    cameras = list()
    numCameras = int(config['Cameras']['numCameras'])

    # Robot Mode Based on Camera Numbers Config
    global LEGACY_MODE
    if numCameras <= 0:
        LEGACY_MODE = True
    else:
        LEGACY_MODE = False

    # Camera Configurations
    if not LEGACY_MODE:
        camConfig = config['Cameras']['camConfig'].split(",")
        try:
            for i in range(0, numCameras):       
                if (camConfig[i] == "num"):
                    cameras.append(int(config['Cameras'][f'camera{i}']))
                else:
                    cameras.append(config['Cameras'][f'camera{i}'])
        except:
            raise Exception("Incorrect camera configuration!")

    global modelPath
    global model
    if not LEGACY_MODE:
        modelPath = config['Model']['modelPath']
        model = config['Model']['model']
    else:
        modelPath = None
        model = None

    # Detector Object - Runs CV Object Detection, Detects Robots
    global detector
    if not LEGACY_MODE:
        # Only can import this if running on CV Enabled System
        from classes.DetectorClass import Detector

        resolutionX = int(config['Model']['resolutionX'])
        resolutionY = int(config['Model']['resolutionY'])
        render = config['Model']['render'] == "True"

        # Initialize Detector
        detector = Detector(resolutionX, resolutionY, model, modelPath, cameras, render = render)
    
    else:
        detector = None

    global PING_COUNT
    PING_COUNT = 2

    global PING_INTERVAL
    PING_INTERVAL = 0

    # From our testing, it was determined 0.16 seconds was sufficient >99% of the time.
    global PING_TIMEOUT
    PING_TIMEOUT = 0.16
    
    global MAINTENANCE_INTERVAL_SLEEP
    MAINTENANCE_INTERVAL_SLEEP = 0
    
    global PAYLOAD_INTERVAL_SLEEP
    PAYLOAD_INTERVAL_SLEEP = 0.5
    
    global DISCOVERY_INTERVAL_SLEEP
    DISCOVERY_INTERVAL_SLEEP = 0
    
    global SOCKET_CONNECTION_TIMEOUT
    SOCKET_CONNECTION_TIMEOUT = 0.25

    global SOCKET_TRANSMISSION_TIMEOUT
    SOCKET_TRANSMISSION_TIMEOUT = 5
    
    # At the start of every packet, these bytes will appear - in Wireshark
    global START_OF_PACKET
    START_OF_PACKET = b'\x7E\x55\xAA\x7E'
    
    # At the end of every packet, these bytes will appear - in Wireshark
    global END_OF_PACKET
    END_OF_PACKET = b'\x7E\xAA\x55\x7E'
    
    # Escaping the data helps avoid conflicts by replacing special byte sequences 
    # (in this case, the Start of Packet, End of Packet, and Escape sequences) with 
    # alternative representations when they appear within the payload
    global ESCAPE
    ESCAPE = b'\x7D'
    
    # Set the expected number of robots 
    # (determines how many threads will be run, modifies discovery behavior greatly)
    global EXPECTED_NUMBER_OF_ROBOTS
    EXPECTED_NUMBER_OF_ROBOTS = 4
    
    global POSSIBLE_ROBOT_IP_ADDRESSES
    POSSIBLE_ROBOT_IP_ADDRESSES = []
    
    # Setting IP 
    starting_IP = 10
    for i in range(EXPECTED_NUMBER_OF_ROBOTS):
        POSSIBLE_ROBOT_IP_ADDRESSES.append(f'10.0.0.{starting_IP + i}')
        
    # The ROBOT_IP_ADDRESS is what is used for the SL0 interface
    global ROBOT_IP_ADDRESS
    if (robot == "pi"):
        ROBOT_IP_ADDRESS = POSSIBLE_ROBOT_IP_ADDRESSES[0]
    elif (robot == "orin"):
        ROBOT_IP_ADDRESS = POSSIBLE_ROBOT_IP_ADDRESSES[1]
    elif (robot == "nano"):
        ROBOT_IP_ADDRESS = POSSIBLE_ROBOT_IP_ADDRESSES[2]
    elif (robot == "orin2"):
        ROBOT_IP_ADDRESS = POSSIBLE_ROBOT_IP_ADDRESSES[3]

    global POSSIBLE_RECEIVING_ROBOT_PORTS
    POSSIBLE_RECEIVING_ROBOT_PORTS = []
    for i in range(8000, 8000 + EXPECTED_NUMBER_OF_ROBOTS):
        POSSIBLE_RECEIVING_ROBOT_PORTS.append(str(i))
    
    # Total # of sockets that can be openeed up simultaenously to attempt to connect - (we are only using 8)
    global POSSIBLE_SENDING_ROBOT_PORTS
    POSSIBLE_SENDING_ROBOT_PORTS = []
    for i in range(7000, 7000 + EXPECTED_NUMBER_OF_ROBOTS):
        POSSIBLE_SENDING_ROBOT_PORTS.append(str(i))
    
    global serial_ports
    global virtual_serial_port
    global robot_serial_port

    global pixels
    pixels = None
    
    global LEDs
    LEDs = None
    
    if robot == "pi":
        import neopixel # needed for neopixel
        pixels = neopixel.NeoPixel(
            board.D18,                      # Pixel Pin (Raspberry Pi's GPIO_18 pin)
            24,                             # Number of LEDs (Num of Pixels)
            brightness = 0.05,              # Scale from 0.00 to 1.00 (Higher = Brighter), CAUTION: 1.00 hurts your eyes
            pixel_order = neopixel.GRB      # G and R are reversed, so the colors are actually in order of RGB
        )
    elif robot == "orin" or robot == "orin2":
        import neopixel_spi as neopixel
        spi = board.SPI()   # MOSI pin 19
        
        # Board Setup
        pixels = neopixel.NeoPixel_SPI(
            spi,                            # SPI object
            24,                             # Number of LEDs (Num of Pixels)
            brightness = 0.05,              # Scale from 0.00 to 1.00 (Higher = Brighter), CAUTION: 1.00 hurts your eyes
            pixel_order = neopixel.GRB      # G and R are reversed, so the colors are actually in order of RGB
        )

