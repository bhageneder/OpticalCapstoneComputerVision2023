
import threading
import binascii
#from functions import utilities
#from functions.analyze_packet import analyze_packet

def v_receive_manager(vg):
    thread_name = threading.current_thread().name
    while True:
        packet = vg.dataReceived.get()
        
        # Remove any starting bytes before 0xc0 (this should not happen) (bandaid-fix)
        # packet = packet[(packet.find(b'\xc0')):]

        vg.virtual_serial_port.write(packet)