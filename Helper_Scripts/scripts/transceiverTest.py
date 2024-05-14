import serial
import subprocess

usbNumber = 7

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
