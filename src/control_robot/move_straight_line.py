import time
import os
import math
import random
import serial
from control_robot.calculate_checksum import calculate_checksum
from control_robot.calculate_checksum import calculate_checksum_simple
from control_robot.writeToRobot import writeToRobot

# Distance should be in meters
# Speed should be a byte (E.X. 0xFA speed = 250 mm/s) 
def move_straight_line_for_distance_at_speed(robot_serial_port, distance, speed):
    speed_in_meters = int(speed) / 1000
    time_needed = distance / speed_in_meters
    time_running = 0
    goStraight = bytearray([0x00, 0x00])

    while time_running <= time_needed:
            writeToRobot(speed, goStraight, robot_serial_port)
            time.sleep(0.025)
            time_running += 0.025
    
    # Write Speed of 0
    writeToRobot(0, goStraight, robot_serial_port)

# WIP - Not working...
def turn_degrees(robot_serial_port, degrees, speed):
    onlyClockwise = bytearray([0xFF, 0xFF])
    goStraight = bytearray([0x00, 0x00])
    radians = degrees * (math.pi / 180)


    speed_in_meters = int(speed) / 1000
    time_needed = degrees / speed_in_meters
    time_running = 0
    while time_running <= time_needed:
            writeToRobot(speed, onlyClockwise, robot_serial_port)
            time.sleep(0.025)
            time_running += 0.025
    
    writeToRobot(0, goStraight, robot_serial_port)


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

    # move 1 meter at speed 250 mm/s
    move_straight_line_for_distance_at_speed(robot_serial_port, 1, 0xFA)
