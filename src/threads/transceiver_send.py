import threading
from config.global_vars import global_vars
from src.functions import utilities
from src.functions import led_manager as lc

def transceiver_send(serial_port, send_queue):
    thread_name = threading.current_thread().name
    while True:
        packet = send_queue.get() # Block until item is available

        if global_vars.debug_transceiver_send: print(f'{thread_name} Items In Queue: {send_queue._qsize()}') 
        with global_vars.transeiver_send_mutex: # Block until mutex is acquired (to prevent jamming)
            serial_port.write(global_vars.START_OF_PACKET + utilities.escape(packet) + global_vars.END_OF_PACKET)
        