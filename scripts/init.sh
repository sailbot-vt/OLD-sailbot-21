#!/bin/bash

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set up python environment
/bin/bash $DIR/install-python.sh
alias python=python3

# Create Python runtime environment, install dependencies
if [[ $HOSTNAME == beaglebone ]]; then
    # Install production dependencies
    echo "Building production version"
    export PYTHONPATH=/usr/local/lib/python3.5/site-packages/
    /bin/bash $DIR/install-packages.sh
    python3.5 -m pip install -r requirements.prod.txt
    /bin/bash $DIR/update-overlays.sh
else
    python3.5 -m pip install virtualenv
	python3.5 -m virtualenv -p python3.5 p3_5env --no-site-packages

    if [[ $TRAVIS ]]; then
        # Install test dependencies
        echo "Building test version"
        . ./p3_5env/bin/activate; \
	    pip install -r requirements.test.txt
	else
	    # Install dev dependencies
	    echo "Building production version"
	    . ./p3_5env/bin/activate; \
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

