#!/bin/bash
# Installs Python
# Works for Debian 9 (Stretch)


export PATH=/usr/local/bin:$PATH

# If Python already exists, exit
if hash python3.7 2>/dev/null; then
    echo "Python 3.7 already installed"
    exit 0
fi

# Get Python build dependencies
apt-get install -y build-essential
apt-get install -y libbz2-dev libsqlite3-dev libreadline-dev zlib1g-dev libncurses5-dev libssl-dev libgdbm-dev libffi-dev python-pip
apt-get install -y make

# Get needed packages
./install-packages.sh

# Create temporary working directory
mkdir /tmp/py-transient
cd /tmp/py-transient

# Download Python source
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
tar xvf Python-3.7.2.tar.xz
cd Python-3.7.2

# Build python3.7 executable
./configure
make
make install

# Clean up
rm -rf /tmp/py-transient
