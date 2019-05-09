#!/bin/bash

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set up python environment
/bin/bash $DIR/install-python.sh
alias python=python3

# Create Python runtime environment, install dependencies
if [[ $HOSTNAME == beaglebone ]]; then
    # Install production dependencies
    pip3 install -r requirements.prod.txt
    /bin/bash $DIR/install-packages.sh
else
    pip3 install virtualenv
	python3.7 -m virtualenv -p python3.7 p3_7env --no-site-packages

    if [[ $TRAVIS ]]; then
        # Install test dependencies
        . ./p3_7env/bin/activate; \
	    pip install -r requirements.test.txt
	else
	    # Install dev dependencies
	    . ./p3_7env/bin/activate; \
	    pip install -r requirements.dev.txt
    fi
fi

if mkdir logs; then
    # Do nothing
    echo "" > /dev/null
else
    # We don't care
    echo "" > /dev/null
fi


