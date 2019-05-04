#!/bin/bash

./install-packages.sh

if [ "$HOSTNAME" = beaglebone ]; then
	pip3 install -r requirements.txt
	pip3 install Adafruit_BBIO
else
	./install-python.sh
	pip install virtualenv
	virtualenv -p python3.7 p3_7env --system-site-packages

	./p3_7env/bin/activate; \
	pip install -r requirements.txt

	. ./p3_7env/bin/activate; \
	pip install Adafruit_BBIO || :
fi

mkdir logs || :


