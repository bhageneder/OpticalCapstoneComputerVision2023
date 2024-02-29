import threading
import config.global_vars as g
from functions.analyze_packet import analyze_packet

def send_manager():
    thread_name = threading.current_thread().name
    while True:
        # Reading packet from Virtual Serial Port
        packet = b""
        complete_packet_read = False
        packet_started = False
        while not complete_packet_read:
            byte = g.virtual_serial_port.read(1)
            packet += byte
            if byte == b'\xc0' and not packet_started:
                packet_started = True
            elif byte == b'\xc0' and packet_started:
                complete_packet_read = True
        
        #if g.debug_transceiver_send: print(f"{thread_name}:  {packet}")

        packet_summary = analyze_packet(packet)

        # ICMP Request Ping Packets are of type 8, and Reply Ping Packets are of type 0
        if packet_summary.icmp_type == 8:
            # The Transceiver # to be used is the same as the ICMP packet's identifier
            requested_transceiver_number = int(str(packet_summary.icmp_identifier)[-1])
            if g.debug_send_manager: print(f'{thread_name}: Sending Ping Request Through Transceiver {requested_transceiver_number}, {packet_summary.payload.decode()}')
            g.transceiver_send_queues[requested_transceiver_number].put(packet)
            continue
        elif packet_summary.icmp_type == 0:
            if g.debug_send_manager: print(f'{thread_name}: Sending Ping Reply Through All Transceivers, {packet_summary.payload.decode()}')
            for i in range(len(g.serial_ports)):
                g.transceiver_send_queues[i].put(packet)
            continue
        
        # If the TCP Packet Contains the SYN (S) or SYN-ACK (SA) flags
        # then it is a mini_discovery or listen_for_connection packet.
        # Send it through all transceivers to find the other robots.
        if packet_summary.tcp_flags == 'S':
            if g.LEGACY_MODE:
                if g.debug_send_manager: print(f'{thread_name}: Sending SYN Through All Transceivers')
                for i in range(len(g.serial_ports)):
                    g.transceiver_send_queues[i].put(packet)
            
            # Send SYN Through Specific Transceiver
            else:
                transceiver = -1
                for robot in g.visible:
                    if (robot.robotLink.serial_port is not None and robot_link.ip_address == packet_summary.dest_IP):
                        transceiver = robot.transceiver
                        break

                if (transceiver != -1):
                    if g.debug_send_manager: print(f'{thread_name}: Sending SYN Through Through Transceiver {transceiver}"')
                    g.transceiver_send_queues[transceiver].put(packet)

            continue
        elif packet_summary.tcp_flags == 'SA':
            if g.LEGACY_MODE:
                if g.debug_send_manager: print(f'{thread_name}: Sending SYN-ACK Through All Transceivers')
                for i in range(len(g.serial_ports)):
                    g.transceiver_send_queues[i].put(packet)

            # Send SYN-ACK Through Specific Transceiver
            else:
                transceiver = -1
                for robot in g.visible:
                    if (robot.robotLink.serial_port is not None and robot_link.ip_address == packet_summary.dest_IP):
                        transceiver = robot.transceiver
                        break

                if (transceiver != -1):
                    if g.debug_send_manager: print(f'{thread_name}: Sending SYN-ACK Through Through Transceiver {transceiver}"')
                    g.transceiver_send_queues[transceiver].put(packet)

            continue
        
        # If the Packet is not an ICMP Ping Packet, send payload through specific transceiver 
        # if the packet's destination IP Address matches the Robot Link's IP Address 
        # (and the Robot Link has a serial port)       
        for robot_link in g.robot_links:
            if (robot_link.serial_port != None and robot_link.ip_address == packet_summary.dest_IP):
                if g.debug_send_manager: print(f"{thread_name}: Sending Payload Through Specific Transceiver {g.serial_ports.index(robot_link.serial_port)}: {packet_summary.payload}")
                g.transceiver_send_queues[g.serial_ports.index(robot_link.serial_port)].put(packet)
                break
        else:
            # Send through all transceivers if the destination IP Address is not a known Robot Link
            for i in range(len(g.serial_ports)):
                g.transceiver_send_queues[i].put(packet)


# Bug Showcase: The bug that was breaking everything...
# for i in range(len(g.robot_links)):
#     if (g.robot_links[i].serial_port != None and g.robot_links[i].ip_address == packet_summary.dest_IP):
#         if g.debug_send_manager: print(f"{thread_name}: Sending Payload Through Specific Transceiver {g.serial_ports.index(g.robot_links[i].serial_port)}: {packet_summary.payload}")
#         g.transceiver_send_queues[i].put(packet)