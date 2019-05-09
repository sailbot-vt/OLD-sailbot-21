#!/bin/bash

if [[ $HOSTNAME == beaglebone ]]; then
	export ENV test;
	unittest discover -vcs tests
else
	. ./p3_7env/bin/activate; \
	export ENV test; \
	coverage run --source src -m unittest discover -vcs tests
fi
