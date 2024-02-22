import globals
import subprocess
import time
import utilities
import serial

# Setup Serial Line Interface Protocol (SLIP), and create virtual serial ports
#subprocess.run(['/home/sa/Documents/OpticalCapstoneComputerVision2023/OpticalCommunications-2023-N-robots-TCP/scripts/create_serial_interface.sh', 10.10.10.12])
#time.sleep(1.5) # Wait for virtual serial ports to be fully created

portNum = 1

serial_port = serial.Serial(
    port= f'/dev/ttyUSB{portNum}',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = None # A timeout of none to make the serial port block when reading if there is not enough bytes
    )

print("Connected to: " + serial_port.portstr)

output = subprocess.check_output(f"udevadm info /dev/ttyUSB{portNum} | grep ID_SERIAL", shell=True).decode('utf-8')
print(output)

while True:
    print("Read: " + str(serial_port.read()))
