import sliplib
from scapy.all import *

# Other Packet
#byte_array = b'\xc0E\x00\x00<\xa6j@\x00@\x06\x80Q\n\x00\x00\x01\n\x00\x00\x00\x84\x86\x17\xac\xd1\x9f\xa1Q\x00\x00\x00\x00\xa0\x02\xfa\xf0LM\x00\x00\x02\x04\x05\xb4\x04\x02\x08\n\xcf\x92\x0e\x0b\x00\x00\x00\x00\x01\x03\x03\x07\xc0'

# Payload Packet
byte_array = b'\xc0E\x00\x00D\xa6n@\x00@\x06\x80E\n\x00\x00\x01\n\x00\x00\x00\x84\x86\x17\xac\xd1\x9f\xa3\x06\xe1\xb5[\xf2\x80\x18\x01\xf6\xc8c\x00\x00\x01\x01\x08\n\xcf\x92\x10\xb1\x02\x05\xed\xb8\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x20\x74\x65\x73\x74\xc0'

# Decode SLIP
decoded_bytes = sliplib.decode(byte_array)
print(decoded_bytes)

# Analyze the TCP packet
try:
    packet = Ether(decoded_bytes)
    packet.show()
except:
    print('No Eth Layer')

try:
    packet = IP(decoded_bytes)
    packet.show()
except:
    print('No IP Layer')

# try:
#     packet = TCP(decoded_bytes)
#     packet.show()
# except:
#     print(f'{thread_name}No TCP Layer')




# Accessing packet layers
# eth_layer = packet[Ether]
# ip_layer = packet[IP]
# tcp_layer = packet[TCP]

# Ethernet layer information
# src_mac = eth_layer.src
# dst_mac = eth_layer.dst
# eth_type = eth_layer.type

# #IP layer information
# src_ip = ip_layer.src
# dst_ip = ip_layer.dst
# ip_version = ip_layer.version
# ip_ttl = ip_layer.ttl
# ip_proto = ip_layer.proto

# # TCP layer information
# src_port = tcp_layer.sport
# dst_port = tcp_layer.dport
# tcp_seq = tcp_layer.seq
# tcp_ack = tcp_layer.ack
# tcp_flags = tcp_layer.flags
# tcp_window = tcp_layer.window

# # Printing information
# # print(f"Source MAC: {src_mac}")
# # print(f"Destination MAC: {dst_mac}")
# # print(f"Ether Type: {eth_type}")

# print(f"Source IP: {src_ip}")
# print(f"Destination IP: {dst_ip}")
# print(f"IP Version: {ip_version}")
# print(f"IP TTL: {ip_ttl}")
# print(f"IP Protocol: {ip_proto}")

# print(f"Source Port: {src_port}")
# print(f"Destination Port: {dst_port}")
# print(f"TCP Sequence: {tcp_seq}")
# print(f"TCP Acknowledgment: {tcp_ack}")
# print(f"TCP Flags: {tcp_flags}")
# print(f"TCP Window Size: {tcp_window}")
