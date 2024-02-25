
import threading
import binascii
from config.global_vars import global_vars
from src.functions import utilities
from functions import led_manager as lc
from src.functions.analyze_packet import analyze_packet

def receive_manager():
    thread_name = threading.current_thread().name
    while True:
        packet = global_vars.data_received.get()
        # Remove any starting bytes before 0xc0 (this should not happen) (bandaid-fix)
        packet = packet[(packet.find(b'\xc0')):]
        if global_vars.debug_log_packets:
            utilities.add_data_to_log_file(binascii.hexlify(packet).decode('utf-8'), "Raw")

        global_vars.virtual_serial_port.write(packet)
