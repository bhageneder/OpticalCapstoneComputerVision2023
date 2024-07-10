
import threading
import binascii
#from functions import utilities
#from functions.analyze_packet import analyze_packet
import sim.sim_global_vars as sg

def v_receive_manager(vg):
    thread_name = threading.current_thread().name
    while True:
        # packet = vg.dataReceived.get()
        packet = sg.listOfDataQ[int(vg.ip.split(".")[-1])-10].get()
        
        # Remove any starting bytes before 0xc0 (this should not happen) (bandaid-fix)
        # packet = packet[(packet.find(b'\xc0')):]

        vg.virtual_serial_port.write(packet)