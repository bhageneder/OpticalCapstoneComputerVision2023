import config.globals as globals
import utilities
import threading
import binascii
import led_manager as lc
import sys
sys.path.append('./')
from packet_manager import analyze_packet

def receive_manager():
    thread_name = threading.current_thread().name
    while True:
        packet = globals.data_received.get()
        # Remove any starting bytes before 0xc0 (this should not happen) (bandaid-fix)
        packet = packet[(packet.find(b'\xc0')):]
        if globals.debug_log_packets:
            utilities.add_data_to_log_file(binascii.hexlify(packet).decode('utf-8'), "Raw")

        globals.virtual_serial_port.write(packet)
        
       