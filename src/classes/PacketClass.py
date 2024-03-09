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
