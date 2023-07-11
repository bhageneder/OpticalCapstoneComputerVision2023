import os
import struct
import time
import socket
import threading

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

def ping(dest_addr, identifier, count, interval, timeout, payload):
    icmp_proto = socket.getprotobyname('icmp')
    ICMP_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
    ICMP_socket.settimeout(timeout)
    dest_ip = socket.gethostbyname(dest_addr)
    print(f'Thread {identifier}: PING {dest_addr} ({dest_ip}): {len(payload)} data bytes')

    received_packets = 0
    total_rtt = 0

    for sequence in range(1, count + 1):
        packet = create_icmp_packet(identifier, sequence, payload)
        ICMP_socket.sendto(packet, (dest_ip, 0))
        start_time = time.time()

        # The operating system delivers all incoming ICMP packets to all open raw sockets 
        # listening for ICMP packets. If multiple threads are sending ICMP pings at the
        # same time they will receive eachother ICMP ping reply packets. Using a while True
        # loop insures that the socket will continue to be read (packets gotten) until it
        # looks at all of the packets actually intended for it.
        while True:
            try:
                response, addr = ICMP_socket.recvfrom(1024)
                elapsed_time = (time.time() - start_time) * 1000 # RTT in milliseconds
                total_rtt += elapsed_time
                
                received_identifier = struct.unpack('!H', response[24:26])[0]
                received_sequence = struct.unpack('!H', response[26:28])[0]

                if received_identifier == identifier and received_sequence == sequence:
                    response_payload = response[28:].decode()
                    if response_payload == payload:
                        received_packets += 1
                        print(f'Thread {identifier}: {len(response)} bytes from {addr[0]}: icmp_seq={sequence} ttl={response[8]} time={elapsed_time:.2f} ms')
                    else:
                        print(f'Thread {identifier}: Unexpected payload in the response: {response_payload}')
                    break

            except socket.timeout:
                print(f'Thread {identifier}: Request timed out.')
                break

        time.sleep(interval)

    loss_percentage = (1 - (received_packets / count)) * 100
    avg_rtt = total_rtt / (received_packets) if (received_packets) > 0 else 0

    print(f'\n--- {dest_addr} ping statistics ---')
    print(f'{count} packets transmitted, {received_packets} received, {loss_percentage}% packet loss, time {(count * interval * 1000)}ms')
    print(f'RTT avg = {avg_rtt:.2f} ms')

    ICMP_socket.close()

if __name__ == '__main__':
    dest_addr = "8.8.8.8"
    count = 5
    interval = 0.1
    timeout = 1
    payload = "Custom payload"

    num_threads = 2

    threads = []
    for i in range(num_threads):
        identifier = i
        t = threading.Thread(target=ping, args=(dest_addr, identifier, count, interval, timeout, payload))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()