import threading
import time
import config.global_vars as g
from classes.LEDStateClass import LEDState
import functions.led_funcs as led_funcs

def led_manager():
    thread_name = threading.current_thread().name

    led_funcs.startup()

    g.LEDs = LEDState()
    
    while True:
        #background process to loop through LED arrays and set LEDs
        LEDs = g.LEDs.getLEDs()

        if g.LEGACY_MODE:
            for link in g.robot_links:
                g.LEDs.on("connected", g.serial_ports.index(link.serial_port))
        else:
            for robot in g.lost:
                if robot.transceiver > -1:
                    g.LEDs.on("lost", robot.transceiver)

            for robot in g.visible:
                if robot.robotLink is None:
                    g.LEDs.on("finding", robot.transceiver)
                else:
                    g.LEDs.on("connected", robot.transceiver)

        for transceiver in range(8):
            if LEDs[0][transceiver] > 0:
                led_funcs.illuminate_for_finding(transceiver)
            else:
                led_funcs.turn_off_for_finding(transceiver)
            if LEDs[1][transceiver] > 0:
                led_funcs.illuminate_for_connected(transceiver)
            else:
                led_funcs.turn_off_for_connected(transceiver)
            if LEDs[2][transceiver] > 0:
                led_funcs.illuminate_for_lost(transceiver)
            else:
                led_funcs.turn_off_for_lost(transceiver)
        
        g.LEDs.reset()        

        time.sleep(0.25)
