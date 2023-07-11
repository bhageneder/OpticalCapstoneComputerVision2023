import sliplib
from scapy.all import IP, ICMP, TCP
import globals
from utilities import nested_getattr
import binascii

class Packet:
    def __init__(self, source_port, dest_port, source_IP, dest_IP, length, sequence_number, payload, tcp_flags, icmp_code, icmp_type, icmp_identifier, original_data):
        self.source_port = source_port
        self.dest_port = dest_port
        self.source_IP = source_IP
        self.dest_IP = dest_IP
        self.length = length                # Length of the packet (taken from the IP header)
        self.sequence_number = sequence_number
        self.payload = payload              # The data that the packet is transporting
        self.tcp_flags = tcp_flags
        self.icmp_code = icmp_code
        self.icmp_type = icmp_type
        self.icmp_identifier = icmp_identifier
        self.data = original_data           # ALL of the original data from the packet. This is what is being sent through the transceivers

# Takes 'data' as an input. This is a single packet that is in byte format, an example is below...
# data = b'\xc0E\x00\x00D\xa6n@\x00@\x06\x80E\n\x00\x00\x01\n\x00\x00\x00\x84\x86\x17\xac\xd1\x9f\xa3\x06\xe1\xb5[\xf2\x80\x18\x01\xf6\xc8c\x00\x00\x01\x01\x08\n\xcf\x92\x10\xb1\x02\x05\xed\xb8\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x20\x74\x65\x73\x74\xc0'
def analyze_packet(packet):
    IP_packet = None
    TCP_packet = None
    ICMP_packet = None
    # Decode SLIP
    try:
        decoded_bytes = sliplib.decode(packet)

        if globals.debug_packet_manager == True: 
            hex_bytes = binascii.hexlify(decoded_bytes).decode('utf-8')
            print(f'Packet Hex Data: {hex_bytes}')

        # Decode IP Packet, and Get Fields If Present
        try:
            IP_packet = IP(decoded_bytes)
            #IP_packet.show()
            try:
                ICMP_packet = IP_packet[ICMP]
                if globals.debug_packet_manager == True: ICMP_packet.show()
            except:
                if globals.debug_packet_manager == True: print(f'Decoding ICMP Packet Error')
            try:
                TCP_packet = IP_packet[TCP]
                if globals.debug_packet_manager == True: TCP_packet.show()
            except:
                if globals.debug_packet_manager == True: print(f'Decoding TCP Packet Error')
        except:
            if globals.debug_packet_manager == True: print(f'Decoding IP Packet Error')

    except sliplib.ProtocolError:
        if globals.debug_packet_manager == True: print(f'SLIP Could Not Process Corrupt Packet: {packet}')
  
    # Create the packet object - if the field does not exist, it is set as None
    return Packet(
        nested_getattr(IP_packet, 'payload.sport'),
        nested_getattr(IP_packet, 'payload.dport'),
        nested_getattr(IP_packet, 'src'),
        nested_getattr(IP_packet, 'dst'),
        nested_getattr(IP_packet, 'len'),
        nested_getattr(IP_packet, 'payload.seq'),
        nested_getattr(IP_packet, 'payload.payload.load'),
        nested_getattr(TCP_packet, 'flags'),
        nested_getattr(ICMP_packet, 'code'),
        nested_getattr(ICMP_packet, 'type'),
        nested_getattr(ICMP_packet, 'id'),
        packet
        )

        
