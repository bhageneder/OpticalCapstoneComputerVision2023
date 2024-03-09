
import threading
import binascii
import config.global_vars as g
from functions import utilities
from functions import led_manager as lc
from functions.analyze_packet import analyze_packet

def receive_manager():
    thread_name = threading.current_thread().name
    while True:
        packet = g.data_received.get()
        # Remove any starting bytes before 0xc0 (this should not happen) (bandaid-fix)
        packet = packet[(packet.find(b'\xc0')):]
        if g.debug_log_packets:
            utilities.add_data_to_log_file(binascii.hexlify(packet).decode('utf-8'), "Raw")

        g.virtual_serial_port.write(packet)
