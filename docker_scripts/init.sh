#!/bin/bash

# Get scripts directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Set up python environment
/bin/bash $DIR/install-python.sh
alias python=python3

# Create Python runtime environment, install dependencies
# Install production dependencies
echo "Building production version"
export PYTHONPATH=/usr/local/lib/python3.5/site-packages/
/bin/bash $DIR/install-packages.sh
python3.5 -m pip install -r requirements.prod.txt

if mkdir logs; then
    # Do nothing
    echo "" > /dev/null
else
    # We don't care
    echo "" > /dev/null
fi

