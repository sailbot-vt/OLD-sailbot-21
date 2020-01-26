#!/bin/bash

#if [[ $HOSTNAME == beaglebone ]]; then
export ENV test;
python3.5 -m unittest discover -vcs tests
#else
#	. ./p3_5env/bin/activate; \
#	export ENV test; \
#	coverage run --source src -m unittest discover -vcs tests
#fi
