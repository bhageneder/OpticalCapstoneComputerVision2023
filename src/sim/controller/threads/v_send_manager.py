import threading
#from functions.analyze_packet import analyze_packet
import sim.sim_global_vars as sg

def v_send_manager(vg):
    thread_name = threading.current_thread().name
    while True:
        # Reading packet from Virtual Serial Port
        # packet = b""
        packet = ""
        complete_packet_read = False
        packet_started = False
        while not complete_packet_read:
            byte = vg.virtual_serial_port.read() # read(1)
            packet += str(byte)

            # The following is not implemented in simulated packets:
            # if byte == b'\xc0' and not packet_started:
            #     packet_started = True
            # elif byte == b'\xc0' and packet_started:
            #     complete_packet_read = True

            complete_packet_read = True
        
        if vg.debug_transceiver_send: print(f"{thread_name}:  {packet}")

        # Simulated packets are not formatted like the real ones
        # The following is not implemented in simulated packets:
        # packet_summary = analyze_packet(packet)

        if vg.debug_send_manager: print(f'{thread_name} Forwarding packet through dataQ {packet}')
        
        # Sending data is simplified in the simulator because transceivers are not implemented
        # Additionally, all packets are of the same type

        # Simulate the sending of data (queue it for the receiving robot)
        # Access receiving robots dataQ
        # Send data with tag
        sendingTo = packet.split("\x00")
        sg.listOfDataQ[int(sendingTo[1].split(".")[-1])-10].put(packet + " ", timeout=3)