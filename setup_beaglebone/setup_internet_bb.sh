# Run this script to set up the BB to route internet
# requests through the host machine.

# Tells the BB the host machine (192.168.7.1) is
# the gateway. 
sudo route add default gw 192.168.7.1

# Tell the BB what server to use for DNS queries
# (i.e., figuring out what IP "www.google.com" is)
echo "nameserver 8.8.8.8" > /etc/resolv.conf
