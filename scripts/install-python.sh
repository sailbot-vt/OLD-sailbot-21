#!/bin/bash
# Installs Python 3.5
# Works for Debian 9 (Stretch)

export PATH=/usr/local/bin:$PATH

if [[ $HOSTNAME == beaglebone ]]; then
    # Docker img does not include by default.
    apt-get install -y python3-pip python3-setuptools python3-wheel
    pip3 install --upgrade pip
fi

# If Python already exists, exit
if hash python3.5 2>/dev/null; then
    echo "Python 3.5 already installed"
    exit 0
fi

# Get Python build dependencies
apt-get install -y build-essential
apt-get install -y libbz2-dev libsqlite3-dev libreadline-dev zlib1g-dev libncurses5-dev libssl-dev libgdbm-dev libffi-dev python3-pip openssl
apt-get install -y make

mkdir -p /tmp/py-transient
cd /tmp/py-transient

wget https://www.python.org/ftp/python/3.5.7/Python-3.5.7.tgz
tar -xzf Python-3.5.7.tgz
cd Python-3.5.7
./configure
make
make install

rm -r /tmp/py-transient
