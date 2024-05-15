import serial
import subprocess

###### USAGE ######
# This script assists with identifying which transceiver USB device corresponds with which 
# transceiver number around the edge of the PCB
# 1. Pick a USB device number (can be any)
# 2. Run the script ('sudo python3 transceiverTest.py')
# 3. Use phone camera to see which which transceiver number on the physical upper housing is activated
#       Aim camera at transceiver, you will see a purple light
#       Android is often better for this because they tend to filter less IR
#       For iPhone, put in video mode (don't need to start recording though)
# 4. Copy the serial number that is in the terminal to the config file for whichever transceiver
# number was physically being used, not the USB number

# USB Device Number (0-7)
usbNumber = 7 # ONLY NEED TO CHANGE THIS LINE

# Runs a subprocess that gets the serial number of the transceiver. Copy this to config file
subprocess.run(['./transceiverTest.sh', str(usbNumber)])

serial_port = serial.Serial(
        port= f'/dev/ttyUSB{usbNumber}',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = None # A timeout of none to make the serial port block when reading if there is not enough bytes
        )

while True:
    serial_port.write(b'test')
