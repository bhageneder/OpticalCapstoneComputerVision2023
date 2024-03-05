# 4/15/23
# Optical Comm Capstone: Dynamic LED System
# Author: Kyle Bush

import time
import config.global_vars as g

# Colors
off = (0,0,0)
red = (255, 0, 0)
orange = (255, 70, 0)
yellow = (255, 150, 0)
lime = (170, 255, 0)
green = (0, 255, 0)
light_blue = (0, 255, 255)
blue = (0, 0, 255)
purple = (128, 0, 255)
pink = (255, 102, 178)
white = (255, 255, 255)

rainbow = (red,orange,yellow,lime,green,light_blue,blue,purple,pink)

# Functions
def colorAll(color, delay):
    for i in range(0,24):
        g.pixels[i] = color
        time.sleep(delay)
        pass

def illuminate(transceiver, color1, color2=None, color3=None):
    if(color2 is None or color3 is None):
        # If 3 colors are not specified, only use the first color
        g.pixels[transceiver*3] = color1
        g.pixels[transceiver*3+1] = color1
        g.pixels[transceiver*3+2] = color1
        pass
    else:
        # All 3 colors were entered
        g.pixels[transceiver*3] = color1
        g.pixels[transceiver*3+1] = color2
        g.pixels[transceiver*3+2] = color3
        pass

def illuminate_for_finding(transceiver_number):
        g.pixels[transceiver_number * 3] = red
        pass

def turn_off_for_finding(transceiver_number):
        g.pixels[transceiver_number * 3] = off
        pass

def illuminate_for_robot_link(transceiver_number):
        g.pixels[transceiver_number * 3 + 1] = green
        pass

def turn_off_for_robot_link(transceiver_number):
        g.pixels[transceiver_number * 3 + 1] = off
        pass

def illuminate_for_connecting(transceiver_number):
        g.pixels[transceiver_number * 3 + 2] = blue
        pass

def turn_off_for_connecting(transceiver_number):
        g.pixels[transceiver_number * 3 + 2] = off
        pass

def transmitting(transceiver):
    illuminate(transceiver, red, orange, red)

def receiving(transceiver):
    illuminate(transceiver, blue, light_blue, blue)

def startup():
    for i in range(8):
        illuminate(i, red)
        time.sleep(0.1)
        
# these are functions so that i do not have to redefine the colors in the startup program
def allGreen():
    colorAll(green, 0.05)
    
def turn_all_LEDs_off():
    colorAll(off, 0)

def test_LEDs():
    for j in range(0,24):
        for i in range(0,8):
            illuminate(i,random.choice(rainbow))
        time.sleep(0.075)
    turn_all_LEDs_off()