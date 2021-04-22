#!/bin/bash

# Check input arguments.
if [[ "$#" -ne 2 ]]; then
	echo "Usage: $0 bb_adapter out_adapter"
	exit 1
fi

# Flush old rules from iptables.
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -F
sudo iptables -X

# Add forwarding rules. 
iptables --table nat --append POSTROUTING --out-interface $2 -j MASQUERADE
iptables --append FORWARD --in-interface $1 -j ACCEPT
