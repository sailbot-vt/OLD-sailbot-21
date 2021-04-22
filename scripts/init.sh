#!/bin/bash

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set up python environment
/bin/bash $DIR/install-python.sh
alias python=python3

export PYTHONPATH=/usr/local/lib/python3.5/site-packages/
/bin/bash $DIR/install-packages.sh

# Create Python runtime environment, install dependencies
if [[ $HOSTNAME == beaglebone ]]; then
    # Install production dependencies
    echo "Building production version"
    pip3 install -r requirements.prod.txt
else
    echo "Building dev version"
    python3.5 -m pip install -r requirements.dev.txt
fi

if mkdir logs; then
    # Do nothing
    echo "" > /dev/null
else
    # We don't care
    echo "" > /dev/null
fi

