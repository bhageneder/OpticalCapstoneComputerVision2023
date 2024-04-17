#!/bin/bash

if [ "$1" == "-h" -o "$1" == "--h" ] ; then
    echo "Usage:"
    echo "create_serial_link [Local IP Address] [Destination IP Address]"
    echo "[Local IP Address] - The IP address of THIS machine (i.e. 10.0.0.0)"
    exit 0

fi

# Cleanup Serial Line Interfaces
for pid in $(ps -aux | grep root | grep 'slattach' | awk '{print($2)}'); do sudo kill -9 $pid; done

# Cleanup Socat Commands
for pid in $(ps -aux | grep root | grep 'socat' | awk '{print($2)}'); do sudo kill -9 $pid; done

# Get command parameter
local_ip=$1

# Create Virtual Serial Bridge --> /dev/ttyNetworkInterface <--> /dev/ttySoftwareEnd
sudo socat -d -d pty,raw,echo=0,link=/dev/ttyNetworkInterface pty,raw,echo=0,link=/dev/ttySoftwareEnd &
sleep 0.35

# Create the Serial Line Interface. Attach it to /dev/ttyNetworkInterface
sudo slattach -dvL -p slip -s 115200 /dev/ttyNetworkInterface &
sleep 0.35

# TODO: Determine the best MTU. 100 seems to work pretty well, but finding the best requires more testing.
# Configure and enable the Serial Line Interface 
sudo ifconfig sl0 ${local_ip}/24 up mtu 100
sleep 0.35

# Add the Serial Line Interface to the routing table
sudo route add ${local_ip} sl0 

stty sane
