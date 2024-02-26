import time
import neopixel
import board
import random

time.sleep(45) # Sleep for PI to be fully booted up

# Board Setup
pixels = neopixel.NeoPixel(
    board.D18,                      # Pixel Pin (Raspberry Pi's GPIO_18 pin)
    24,                             # Number of LEDs (Num of Pixels)
    brightness = 0.025,              # Scale from 0.00 to 1.00 (Higher = Brighter), CAUTION: 1.00 hurts your eyes
    pixel_order = neopixel.GRB      # G and R are reversed, so the colors are actually in order of RGB
)

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

# Functions
def colorAll(color, delay):
    for i in range(0,24):
        pixels[i] = color
        time.sleep(delay)

def colorAllReverse(color, delay):
    for i in range(23,-1,-1):
        pixels[i] = color
        time.sleep(delay)

def illuminate(transceiver, color1, color2=None, color3=None):
    if(color2 is None or color3 is None):
        # If 3 colors are not specified, only use the first color
        pixels[transceiver*3] = color1
        pixels[transceiver*3+1] = color1
        pixels[transceiver*3+2] = color1
    else:
        # All 3 colors were entered
        pixels[transceiver*3] = color1
        pixels[transceiver*3+1] = color2
        pixels[transceiver*3+2] = color3

def illuminate_for_receiving(transceiver_number):
        pixels[transceiver_number * 3] = red

def turn_off_for_receiving(transceiver_number):
        pixels[transceiver_number * 3] = off

def illuminate_for_robot_link(transceiver_number):
        pixels[transceiver_number * 3 + 1] = green

def turn_off_for_robot_link(transceiver_number):
        pixels[transceiver_number * 3 + 1] = off

def illuminate_for_sending(transceiver_number):
        pixels[transceiver_number * 3 + 2] = blue

def turn_off_for_sending(transceiver_number):
        pixels[transceiver_number * 3 + 2] = off

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

while True:
    # Do Light Show Stuff
    colorAllReverse(white, 0.01)
    time.sleep(1.5)
    colorAll(off, 0.01)

    for i in range(16):
        transmitting(i%8)
        time.sleep(0.5)
        illuminate(i%8,off)

    for i in range(0,8,2):
        receiving(i%8)
        time.sleep(0.5)
    for i in range(1,8,2):
        receiving(i%8)
        time.sleep(0.5)
    
    time.sleep(1)
    colorAll(off, 0.01)
    time.sleep(1)

    rainbow = (red,orange,yellow,lime,green,light_blue,blue,purple,pink)
    for j in range(0,24):
        for i in range(0,8):
            illuminate(i,random.choice(rainbow))
        time.sleep(0.075)

    tranlist = [0,1,2,3,4,5,6,7]
    for i in range(0,8):
        randnum = random.choice(tranlist)
        illuminate(randnum,off)
        tranlist.remove(randnum)
        time.sleep(0.075)

    time.sleep(1)