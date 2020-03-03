#!/bin/bash
# Installs Numpy, OpenCV, Scipy and Adafruit_BBIO

pip3 install --upgrade pip

apt-get install python3-numpy python3-opencv build-essential python3-dev python3-scipy

wget https://files.pythonhosted.org/packages/53/2b/b0e3dce6113225aae9beb886b2addd4fd5c140ba93c9503d7e4a97021bcc/Adafruit_BBIO-1.1.1.tar.gz
tar -xf Adafruit_BBIO-1.1.1.tar.gz
cd Adafruit_BBIO-1.1.1
python3.5 setup.py install
cd ..
rm -rf Adafruit_BBIO-1.1.1
