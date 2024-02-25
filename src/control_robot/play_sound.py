import random
import time
from calculate_checksum import calculate_checksum
from calculate_checksum import calculate_checksum_simple

"""
Documentation for serial communication format - http://yujinrobot.github.io/kobuki/enAppendixProtocolSpecification.html
"""
HEADER_0 = 0xAA
HEADER_1 = 0x55
SOUND_SEQUENCE_IDENTIFIER = 0x04
SOUND_SEQUENCE_LENGTH = 0x01
ZERO_BYTE = 0x00


def play_button_sound(robot_serial_port):
    payload = bytearray([SOUND_SEQUENCE_IDENTIFIER, SOUND_SEQUENCE_LENGTH, 0x03])
    payload_length = len(payload)
    message = bytearray([HEADER_0, HEADER_1, payload_length]) + payload
    checksum = calculate_checksum(message[2:]) # [2:] skips the first two bytes in the message, those are not used for checksum
    message += checksum.to_bytes(1, byteorder='little')
    robot_serial_port.write(message)
    

def play_sad_sound(robot_serial_port):
    payload = bytearray([SOUND_SEQUENCE_IDENTIFIER, SOUND_SEQUENCE_LENGTH, 0x04])
    payload_length = len(payload)
    message = bytearray([HEADER_0, HEADER_1, payload_length]) + payload
    checksum = calculate_checksum(message[2:]) # [2:] skips the first two bytes in the message, those are not used for checksum
    message += checksum.to_bytes(1, byteorder='little')
    robot_serial_port.write(message)

def play_connected_sound(robot_serial_port):
    payload = bytearray([SOUND_SEQUENCE_IDENTIFIER, SOUND_SEQUENCE_LENGTH, 0x02])
    payload_length = len(payload)
    message = bytearray([HEADER_0, HEADER_1, payload_length]) + payload
    checksum = calculate_checksum(message[2:]) # [2:] skips the first two bytes in the message, those are not used for checksum
    message += checksum.to_bytes(1, byteorder='little')
    robot_serial_port.write(message)