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

def ping(dest_addr, identifier, count=4, interval=1, timeout=1, payload=""):
    icmp_proto = socket.getprotobyname('icmp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
    sock.settimeout(timeout)

    dest_ip = socket.gethostbyname(dest_addr)
    print(f'Thread {identifier}: PING {dest_addr} ({dest_ip}): {len(payload)} data bytes')

    for sequence in range(1, count + 1):
        packet = create_icmp_packet(identifier, sequence, payload)
        sock.sendto(packet, (dest_ip, 0))

        start_time = time.time()
        try:
            response, addr = sock.recvfrom(1024)
            elapsed_time = (time.time() - start_time) * 1000  # RTT in milliseconds
            response_payload = response[28:].decode()
            received_identifier = struct.unpack('!H', response[24:26])[0]
            if received_identifier == identifier:
                # Process the packet
                print('matches')
            else:
                # Ignore the packet or handle it differently
                print('wtf')
                print('wtf')

            if response_payload == payload:
                print(f'Thread {identifier}: {len(response)} bytes from {addr[0]}: icmp_seq={sequence} ttl={response[8]} time={elapsed_time:.2f} ms')
            else:
                print(f'Thread {identifier}: Unexpected payload in the response: {response_payload}')

        except socket.timeout:
            print(f'Thread {identifier}: Request timed out.')

        time.sleep(interval)

    sock.close()

if __name__ == '__main__':
    dest_addr = "8.8.8.8"
    count = 4
    interval = 1
    timeout = 1
    payload = "Custom payload"

    num_threads = 4

    threads = []
    for i in range(num_threads):
        identifier = (os.getpid() + i) & 0xff
        t = threading.Thread(target=ping, args=(dest_addr, identifier, count, interval, timeout, payload))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()