import globals
import utilities
import threading
import led_manager as lc

def transceiver_send(serial_port, send_queue):
    thread_name = threading.current_thread().name
    while True:
        packet = send_queue.get() # Block until item is available

        if globals.debug_transceiver_send: print(f'{thread_name} Items In Queue: {send_queue._qsize()}') 
        with globals.transeiver_send_mutex: # Block until mutex is acquired (to prevent jamming)
            serial_port.write(globals.START_OF_PACKET + utilities.escape(packet) + globals.END_OF_PACKET)
        