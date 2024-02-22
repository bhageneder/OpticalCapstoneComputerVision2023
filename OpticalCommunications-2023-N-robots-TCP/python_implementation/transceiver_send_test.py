import globals
import subprocess
import time
import utilities
import serial

# Setup Serial Line Interface Protocol (SLIP), and create virtual serial ports
subprocess.run(['/home/sa/Documents/OpticalCapstoneComputerVision2023/OpticalCommunications-2023-N-robots-TCP/scripts/create_serial_interface.sh', ROBOT_IP_ADDRESS])
time.sleep(1.5) # Wait for virtual serial ports to be fully created

portNum = 0

serial_port = serial.Serial(
    port= f'/dev/ttyUSB{portNum}',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = None # A timeout of none to make the serial port block when reading if there is not enough bytes
    )

output = subprocess.check_output(f"udevadm info /dev/ttyUSB{portNum} | grep ID_SERIAL", shell=True).decode('utf-8')

while True:
    packet = b'\xc0E\x00\x00D\xa6n@\x00@\x06\x80E\n\x00\x00\x01\n\x00\x00\x00\x84\x86\x17\xac\xd1\x9f\xa3\x06\xe1\xb5[\xf2\x80\x18\x01\xf6\xc8c\x00\x00\x01\x01\x08\n\xcf\x92\x10\xb1\x02\x05\xed\xb8\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x20\x74\x65\x73\x74\xc0'
    serial_port.write(globals.START_OF_PACKET + utilities.escape(packet) + globals.END_OF_PACKET)