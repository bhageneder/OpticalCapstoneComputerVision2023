import global_vars as global_vars
import utilities
import threading
import led_manager as lc

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
            if not in_packet and data.endswith(global_vars.START_OF_PACKET):
                in_packet = True
                data = b'' # Clear the data buffer after finding the SOP delimiter
            elif in_packet and data.endswith(global_vars.START_OF_PACKET):
                # This should not happen, the packet did not end with the required bytes, so we are
                # getting data for a new packet. The data was corrupt, so do we give the messed 
                # up packet to TCP or just ignore it and let TCP retransmit?
                #raise Exception("Transceiver Receive Thread's data was corrupt")
                if global_vars.debug_transceiver_receive: print(f'{thread_name} Transceiver Receive Thread got corrupt data - Trashing that packet')
                data = b'' + byte
            elif in_packet and data.endswith(global_vars.END_OF_PACKET):
                # Packet is Pure now (nothing externally added to it)
                packet = utilities.unescape(data[:-len(global_vars.END_OF_PACKET)])
                break
        
        if global_vars.debug_transceiver_receive: print(f'{thread_name} Received Packet: {packet}')
        global_vars.data_received.put(packet) # Blocks until Queue is available
        
