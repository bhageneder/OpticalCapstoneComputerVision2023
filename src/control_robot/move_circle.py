import time
import os
import random
import serial
from calculate_checksum import calculate_checksum
from calculate_checksum import calculate_checksum_simple
from writeToRobot import writeToRobot
from move_straight_line import move_straight_line_for_distance_at_speed


def move_circle(robot_serial_port, speed):
    # Hex Number 0x3E8 is 1000mm = 1 Meter
    # Give it a byte array [0xE8 0x03] to make it turn with 1 Meter radius
    # 1 meter radius
    turning = bytearray([0xE8, 0x03])

    while True:
        writeToRobot(speed, turning, robot_serial_port)

        #move_straight_line_for_distance_at_speed(1, speed)

if __name__ == "__main__":
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
    move_circle(robot_serial_port, 0xC8)