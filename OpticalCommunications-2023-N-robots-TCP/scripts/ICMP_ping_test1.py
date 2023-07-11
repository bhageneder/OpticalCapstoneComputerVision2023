import os
import struct
import time
import socket

def checksum(packet):
    if len(packet) % 2 == 1:
        packet += b'\0'
    s = sum(struct.unpack('!{}H'.format(len(packet)//2), packet))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

def create_icmp_packet(identifier, sequence, payload):
    header = struct.pack('!BBHHH', 8, 0, 0, identifier, sequence)
    data = payload.encode()
    chksum = checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, chksum, identifier, sequence)
    return header + data

def ping(dest_addr, count, interval, timeout, payload):
    icmp_proto = socket.getprotobyname('icmp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
    sock.settimeout(timeout)
    identifier = os.getpid() & 0xffff

    dest_ip = socket.gethostbyname(dest_addr)
    print(f'PING {dest_addr} ({dest_ip}): {len(payload)} data bytes')

    dropped_packets = 0
    total_rtt = 0

    for sequence in range(1, count + 1):
        packet = create_icmp_packet(identifier, sequence, payload)
        sock.sendto(packet, (dest_ip, 0))

        start_time = time.time()
        try:
            response, addr = sock.recvfrom(1024)
            elapsed_time = (time.time() - start_time) * 1000 # RTT in milliseconds
            total_rtt += elapsed_time
            # The IPv4 header has a fixed length of 20 bytes, and the ICMP header has a fixed length of 8 bytes. 
            # Therefore, the payload can be extracted starting from the 28th byte onwards.
            response_payload = response[28:].decode()
            if response_payload == payload:
                print(f'{len(response)} bytes from {addr[0]}: icmp_seq={sequence} ttl={response[8]} time={elapsed_time:.2f} ms')
            else:
                print(f'Unexpected payload in the response: {response_payload}')

        except socket.timeout:
            print(f'Request timed out.')
            dropped_packets += 1

        time.sleep(interval)

    loss_percentage = (dropped_packets / count) * 100
    avg_rtt = total_rtt / (count - dropped_packets) if (count - dropped_packets) > 0 else 0

    print(f'\n--- {dest_addr} ping statistics ---')
    print(f'{count} packets transmitted, {count - dropped_packets} received, {loss_percentage}% packet loss, time {(count * interval * 1000)}ms')
    print(f'RTT avg = {avg_rtt:.2f} ms')

    sock.close()

if __name__ == '__main__':
    # Default values for the ping
    dest_addr = "8.8.8.8"
    count = 10
    interval = 0.025
    timeout = 1
    payload = "Custom payload"

    ping(dest_addr, count, interval, timeout, payload)