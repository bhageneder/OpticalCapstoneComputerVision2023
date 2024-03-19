import threading
import config.global_vars as g
from functions import utilities

def transceiver_receive(serial_port):
    thread_name = threading.current_thread().name
    
    while True: 
        in_packet = False
        data = b''
        while True:
            byte = serial_port.read(1) # Blocks until data is available to be read
            if not byte:
                raise Exception('Transceiver Receive Thread serial port failed to read')
            data += byte
            if not in_packet and data.endswith(g.START_OF_PACKET):
                in_packet = True
                data = b'' # Clear the data buffer after finding the SOP delimiter
            elif in_packet and data.endswith(g.START_OF_PACKET):
                # This should not happen, the packet did not end with the required bytes, so we are
                # getting data for a new packet. The data was corrupt, so do we give the messed 
                # up packet to TCP or just ignore it and let TCP retransmit?
                #raise Exception("Transceiver Receive Thread's data was corrupt")
                if g.debug_transceiver_receive: print(f'{thread_name} Transceiver Receive Thread got corrupt data - Trashing that packet')
                data = b'' + byte
            elif in_packet and data.endswith(g.END_OF_PACKET):
                # Packet is Pure now (nothing externally added to it)
                packet = utilities.unescape(data[:-len(g.END_OF_PACKET)])
                break
        
        if g.debug_transceiver_receive: print(f'{thread_name} Received Packet: {packet}')
        g.data_received.put(packet) # Blocks until Queue is available
        if g.debug_transceiver_receive: print("Put packet in data received queue. Queue size: " + str(g.data_received.qsize()) + " Queue Empty? " + str(g.data_received.empty()))
