import threading
import time

def led_manager():
    thread_name = threading.current_thread().name
    while True:
        #background process to loop through LED arrays and set LEDs
        time.sleep(1)