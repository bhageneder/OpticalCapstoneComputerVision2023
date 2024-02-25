import os
import struct
import time
import socket
import config.globals as globals
import errno
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

# Some Interesting Behavior to Note:
# Maintenance: Received Pings Array [18, 3, 0, 1, 5, 1, 0, 3]
# This robot had transceiver 0 pointing at the other, and the other had transceiver 4 pointing at this robot.
# As expected, Transceiver 0 had the most received pings for its replies
# because it is the transceiver facing the other robot.
# Also as expected, the adjacent transceivers 7 and 1 also had got some reply pings for their requests.
# However, the Transceiver on the opposite side of the robot (and its adjacents to a lesser extent), 
# Transceiver 4, somehow received replys for its request pings as well.
# I do not think Transceiver 4 actually got any replies for ITS request pings, because as previously 
# mentioned, the other robot had ITS transceiver 4 pointing at this robot. I believe the most likely 
# behavior that happened here is that the other robot sent its request pings for transceiver 4, and the local
# robot got those request pings, and sent replies. But somehow, due to light reflection or something else,
# we received our own reply pings that we sent, and we confused our sent reply pings as received reply pings
# for transceiver 4. To solve this issue, the payload of the request pings that are sent can be made unique 
# for every robot. So even if we somehow receive our own sent reply pings, they can be discarded because the
# payload will not match the expected payload of received reply pings for our robot.
# Note: This weird behavior does not happen anymore because the payload was made unique per robot,
# but this just goes to show how delicate things are here. Weird behavior happens very easily in this system.
def multi_ping(dest_addr, count, interval, timeout):
    thread_name = threading.current_thread().name
    maintenance_thread_number = int(thread_name.split('_')[-1])

    icmp_proto = socket.getprotobyname('icmp')
    try:
        ICMP_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
    except socket.error as e:
        if e.errno == errno.EPROTONOSUPPORT:
            # Sometimes, the OS fails to open a new ICMP socket...
            if globals.debug_maintenance == True: print(f'{thread_name}: ICMP Socket Failed to Open')
        else:
            if globals.debug_maintenance == True: print(f'{thread_name}: Unknown Socket Error')
        return -1
    
    ICMP_socket.settimeout(timeout)
    dest_ip = socket.gethostbyname(dest_addr)
    if globals.debug_maintenance == True: print(f'{thread_name}: PINGING {dest_addr}')

    # Create an array to hold the number of reply pings captured by each transceiver
    num_received_pings_per_transceiver = [0 for i in range(8)]
    total_rtt_time_per_transceiver = [0 for i in range(8)]
    received_packets = set()

    for sequence in range(count):
        for transceiver_number in range(8):
            # The identifier of the packet will be maintenance thread number making up the
            # first digit(s), and the transceiver number will be the last digit
            # The maintenance thread number must be in the identifier because Maintenance Ping Replies must 
            # distinguishable between eachother if more than one robot link is being maintained.
            # The payload here must be unique for every robot. Read the method's top comment for
            # more information why. (Strange behavior was happening due to light reflection or something else...)
            # The payload is used here for extra verification later on.
            payload = f'{globals.ROBOT_IP_ADDRESS}_T_{transceiver_number}'
            identifier = int(str(maintenance_thread_number) + str(transceiver_number))

            packet = create_icmp_packet(identifier, sequence, payload)
            ICMP_socket.sendto(packet, (dest_ip, 0))

        start_time = time.time()
        # After sending out all (8 * count) total ping packets, tally up the responses
        while True:
            try:
                response, addr = ICMP_socket.recvfrom(1024)
                received_identifier = struct.unpack('!H', response[24:26])[0]
                received_sequence = struct.unpack('!H', response[26:28])[0]
                source_ip = addr[0]

                # Since one reply packet transmission from the other robot
                # can potentially be received by multiple transceivers,
                # it is unclear whether these duplicate received packets should be
                # counted as additional received packets (indicating that it may be a
                # better transceiver to use for communication), or if they should be ignored.
                # If they are counted, then total number of received packets may be
                # multiplicative based on how many transceivers received the communication.
                if globals.ignoring_duplicate_maintenance_packets == True:
                    # Check if the packet is a duplicate
                    packet_tuple = (received_identifier, received_sequence, source_ip)
                    if packet_tuple in received_packets:
                        continue  # Ignore duplicate packet
                    else:
                        received_packets.add(packet_tuple)

                try:
                    response_payload = response[28:].decode()
                except UnicodeDecodeError:
                    # Decoding Error because the payload got messed up in transmission
                    continue

                elapsed_time = (time.time() - start_time) * 1000 # RTT in milliseconds

                # Confirming that the strings are not empty before converting them to an int
                if str(received_identifier)[:-1] and str(received_identifier)[-1]:
                    received_maintenance_thread_number = int(str(received_identifier)[:-1])
                    received_transceiver_number = int(str(received_identifier)[-1])
                else:
                    continue

                if received_transceiver_number >= 0 and received_transceiver_number <= 7 and received_maintenance_thread_number == maintenance_thread_number and received_sequence == sequence and response_payload == f'{globals.ROBOT_IP_ADDRESS}_T_{received_transceiver_number}':
                    num_received_pings_per_transceiver[received_transceiver_number] += 1
                    total_rtt_time_per_transceiver[received_transceiver_number] += elapsed_time
                    if globals.debug_maintenance == True: print(f'{thread_name}: Ping_{received_transceiver_number}, {len(response)} bytes from {addr[0]}: icmp_seq={received_sequence} ttl={response[8]} time={elapsed_time:.2f} ms')

            except socket.timeout:
                # When all pings have been sent, and no more data is received, any ping requests that did not
                # receive replies are considered timed out.
                if globals.debug_maintenance == True: print(f'{thread_name}: All Unresponsive Ping Requests Have Timed Out')
                break

    if globals.debug_maintenance == True: print(f'{thread_name}: Received Pings Array {num_received_pings_per_transceiver}')

    # Get highest number of received packets, and the transceiver number that received those packets
    highest_received_packets = max(num_received_pings_per_transceiver)
    if highest_received_packets == 0:
        # If no ping packets were received, return -1 to indicate not to switch the transceiver
        return -1
    best_transceiver_number = num_received_pings_per_transceiver.index(highest_received_packets)
    
    lowest_loss_percentage = (1 - (highest_received_packets / count)) * 100
    if globals.debug_maintenance: print(f'{thread_name}: Lowest Ping Loss Percentage: {lowest_loss_percentage}')

    if (highest_received_packets) > 0:
        avg_rtt = total_rtt_time_per_transceiver[best_transceiver_number] / (highest_received_packets)
    else:
        avg_rtt = -1 # If no packets were received, there is no average Round Trip Time (RTT)

    if globals.debug_maintenance == True: print(f'{thread_name}: Best Transceiver {best_transceiver_number}, --- {dest_addr} ping statistics ---')
    if globals.debug_maintenance == True: print(f'{thread_name}: Best Transceiver {best_transceiver_number}, {count} packets transmitted, {highest_received_packets} received, {lowest_loss_percentage:.2f}% packet loss, time {(count * interval * 1000)}ms')
    if globals.debug_maintenance == True: print(f'{thread_name}: Best Transceiver {best_transceiver_number}, RTT avg = {avg_rtt:.2f} ms')
    
    ICMP_socket.close()
    
    return best_transceiver_number

def ping(dest_addr, identifier, count, interval, timeout, payload):
    icmp_proto = socket.getprotobyname('icmp')
    try:
        ICMP_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
    except socket.error as e:
        if e.errno == errno.EPROTONOSUPPORT:
            # Sometimes, the OS fails to open a new ICMP socket...
            if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: ICMP Socket Failed to Open')
        else:
            if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: Unknown Socket Error')
        loss_percentage = 100
        return loss_percentage
    
    ICMP_socket.settimeout(timeout)
    dest_ip = socket.gethostbyname(dest_addr)
    if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: PING {dest_addr} ({dest_ip}): {len(payload)} data bytes')

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
        # If the other Robot is also pinging, those incoming pings will also be received
        while True:
            try:
                response, addr = ICMP_socket.recvfrom(1024)
                elapsed_time = (time.time() - start_time) * 1000 # RTT in milliseconds

                icmp_type = response[20]
                # Check if the received ICMP packet is an Echo Reply (type 0)
                if icmp_type != 0:
                    continue
                
                received_identifier = struct.unpack('!H', response[24:26])[0]
                received_sequence = struct.unpack('!H', response[26:28])[0]
                try:
                    response_payload = response[28:].decode()
                except UnicodeDecodeError:
                    # Decoding Error because the payload got messed up in transmission
                    continue

                # The IP is being included in the payload
                if (received_identifier == identifier and 
                    received_sequence == sequence and response_payload == payload):
                    received_packets += 1
                    if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: {len(response)} bytes from {addr[0]}: icmp_seq={sequence} ttl={response[8]} time={elapsed_time:.2f} ms')
                    total_rtt += elapsed_time
                    break

            except socket.timeout:
                if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: Ping Request Timed Out')
                break

        time.sleep(interval)

    loss_percentage = (1 - (received_packets / count)) * 100
    avg_rtt = total_rtt / (received_packets) if (received_packets) > 0 else 0

    if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: --- {dest_addr} ping statistics ---')
    if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: {count} packets transmitted, {received_packets} received, {loss_percentage:.2f}% packet loss, time {(count * interval * 1000)}ms')
    if globals.debug_mini_maintenance == True: print(f'Ping_{identifier}: RTT avg = {avg_rtt:.2f} ms')
    
    ICMP_socket.close()
    
    return loss_percentage