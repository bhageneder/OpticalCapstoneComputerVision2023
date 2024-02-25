import subprocess
import serial
import configparser

"""
Initializes all of the serial ports and stores them in a list
"""

def initialize_serial_ports():
    serial_ports = []
    static_serial_numbers = [] # The serial numbers of the converters, initially are not in the correct order to match transceiver numbers
    for i in range(8):
        serial_port = serial.Serial(
        port= f'/dev/ttyUSB{i}',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = None # A timeout of none to make the serial port block when reading if there is not enough bytes
        )
        serial_ports.append(serial_port)

        output = subprocess.check_output(f"udevadm info /dev/ttyUSB{i} | grep ID_SERIAL", shell=True).decode('utf-8')
        serial_number = output.split('\n')[0].split('=')[1]
        static_serial_numbers.append(serial_number)

    try:
        # opening serial port for robot controls
        robot_serial_port = serial.Serial(
                port='/dev/ttyUSB8',
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout = 1
            )
    except:
        robot_serial_port = None
        print('Robot Serial Port not opened because no connection was found')

    # The correct order to match the transceiver numbers
    serial_numbers = []
    config = configparser.ConfigParser()
    config.read("./config/config.cfg")
    for i in range(8):
        serial_numbers.append(config['SerialNumbers'][f'converterSerialNumber{i}'])
    # remove the first line which was just a comment
    #serial_numbers.pop(0) ### disabled to get it to run

    serial_ports_in_correct_order = []
    for i in range(8):
        for j in range(8):
            if (serial_numbers[i] == static_serial_numbers[j]):                
                serial_ports_in_correct_order.append(serial_ports[j])
                break
    
    # for testing purposes:   
    """
    for _ in static_serial_numbers:
        print("Static serial: {}".format(_))
    for _ in serial_numbers:    
        print("Serial Numbers: {}".format(_))
    for _ in serial_ports_in_correct_order:
        print("Serial Ports: {}".format(_))
    print("Length of serial ports: {}".format(len(serial_ports_in_correct_order)))
    """
    
    # We only want the /dev/ttySoftwareEnd of the connection (this is where we will write and receive data from SLIP)
    try:
        virtual_serial_port = serial.Serial(
        port= f'/dev/ttySoftwareEnd',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = None # A timeout of none to make the serial port block when reading if there is not enough bytes
        )
    except:
        virtual_serial_port = None
        print('No Virtual Serial Port')

    # The serial ports are in correct order such that index 0 of the list matches with transceiver 0
    return serial_ports_in_correct_order, robot_serial_port, virtual_serial_port
