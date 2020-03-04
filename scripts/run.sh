#!/bin/bash

if [[ $HOSTNAME == beaglebone ]]; then
	python3.5 main.py
else
	. ./p3_5env/bin/activate; \
	python main.py
fi
