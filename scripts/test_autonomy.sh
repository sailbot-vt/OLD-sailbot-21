#!/bin/bash

if [[ $HOSTNAME == beaglebone ]]; then
	python3.5 integration_test.py autonomy
else
	. ./p3_5env/bin/activate; \
	python integration_test.py autonomy 
fi
