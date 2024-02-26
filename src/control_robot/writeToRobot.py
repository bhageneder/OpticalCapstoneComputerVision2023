import random
import time
import serial
from control_robot.calculate_checksum import calculate_checksum
from control_robot.calculate_checksum import calculate_checksum_simple

"""
Documentation for serial communication format - http://yujinrobot.github.io/kobuki/enAppendixProtocolSpecification.html
"""
HEADER_0 = 0xAA
HEADER_1 = 0x55
BASE_CONTROL_IDENTIFIER = 0x01
BASE_CONTROL_LENGTH = 0x04
ZERO_BYTE = 0x00

def writeToRobot(speed, rotationByteArray, robot_serial_port):

    """
    Final Message Format: HEADER0, HEADER1, PAYLOAD_LENGTH, PAYLOAD, CHECKSUM
    
    For BASE_CONTROL, the payload is:
    BASE_CONTROL_IDENTIFIER, BASE_CONTROL_LENGTH, SPEED (2 bytes LSB first), RADIUS (2 bytes LSB first)
    
    RADIUS = 1 for pure rotation
    RADIUS = 0 for pure translation
    """
    payload = bytearray([BASE_CONTROL_IDENTIFIER, BASE_CONTROL_LENGTH, speed, ZERO_BYTE]) + rotationByteArray
    payload_length = len(payload)
    message = bytearray([HEADER_0, HEADER_1, payload_length]) + payload
    checksum = calculate_checksum(message[2:]) # [2:] skips the first two bytes in the message, those are not used for checksum
    message += checksum.to_bytes(1, byteorder='little')
    robot_serial_port.write(message)
