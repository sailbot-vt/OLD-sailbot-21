#!/bin/bash
# Installs OpenCV and Scipy

# Get needed packages
apt-get install python-devel cmake gcc gcc-c++ \
        libdc1394-devel libv4l-devel \
        ffmpeg-devel gstreamer-plugins-base-devel \
        eigen3-devel \
        libblas3 liblapack3 liblapack-dev libblas-dev gfortran

# Create temporary working directory
mkdir /tmp/packages-transient
cd /tmp/packages-transient

# Download OpenCV source
wget https://github.com/opencv/opencv/archive/4.1.0.tar.gz
tar xf 4.1.0.tar.gz
cd opencv-4.1.0

# Build OpenCV
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_EIGEN=ON
make
make install

# Clean up
rm -rf /tmp/packages-transient

# Create temporary working directory
mkdir /tmp/packages-transient
cd /tmp/packages-transient

# Download SciPy source
wget https://github.com/scipy/scipy/releases/download/v1.3.0/scipy-1.3.0.tar.xz
tar xf scipy-1.3.0.tar.xz
cd scipy-1.3.0

# Build SciPy
pip3 install .

# Clean up
rm -rf /tmp/packages-transient


