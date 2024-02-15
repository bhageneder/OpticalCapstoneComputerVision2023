from scapy.layers.inet import TCP

packet = TCP(flags="SA")
print(packet.flags)

if packet.flags == 'S' or packet.flags == 'SA':
    print('yes')
# if packet.flags & TCP.flags.S:
#     print("S flag is set")