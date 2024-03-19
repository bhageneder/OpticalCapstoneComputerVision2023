import threading
import time
import config.global_vars as g
import classes.LEDClass
import functions.led_funcs

def led_manager():
    thread_name = threading.current_thread().name

    spi = board.SPI()   # MOSI pin 19
    
    # Board Setup
    g.pixels = neopixel.NeoPixel_SPI(
        spi,                            # SPI object
        24,                             # Number of LEDs (Num of Pixels)
        brightness = 0.05,              # Scale from 0.00 to 1.00 (Higher = Brighter), CAUTION: 1.00 hurts your eyes
        pixel_order = neopixel.GRB      # G and R are reversed, so the colors are actually in order of RGB
    )

    led_funcs.startup()
    while True:
        #background process to loop through LED arrays and set LEDs
        LEDs = LEDClass.getLEDs

        for transceiver in range(8):
            if LEDs[0][transceiver] == 1:
                led_funcs.illuminate_for_finding(transceiver)
            else:
                led_funcs.turn_off_for_finding(transceiver)
            if LEDs[1][transceiver] == 1:
                led_funcs.illuminate_for_connected(transceiver)
            else:
                led_funcs.turn_off_for_connected(transceiver)
            if LEDs[2][transceiver] == 1:
                led_funcs.illuminate_for_lost(transceiver)
            else:
                led_funcs.turn_off_for_lost(transceiver)

        time.sleep(0.25)