import threading
import config.global_vars as g
from functions import utilities
from functions import led_manager as lc

def transceiver_send(serial_port, send_queue):
    thread_name = threading.current_thread().name
    while True:
        packet = send_queue.get() # Block until item is available

        if g.debug_transceiver_send: print(f'{thread_name} Items In Queue: {send_queue._qsize()}') 
        with g.transeiver_send_mutex: # Block until mutex is acquired (to prevent jamming)
            serial_port.write(g.START_OF_PACKET + utilities.escape(packet) + g.END_OF_PACKET)