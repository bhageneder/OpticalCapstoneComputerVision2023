import threading
import time
import config.global_vars as g
import classes.LEDStateClass
import functions.led_funcs

def led_manager():
    thread_name = threading.current_thread().name

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