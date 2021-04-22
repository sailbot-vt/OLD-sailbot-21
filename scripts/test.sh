#!/bin/bash

export ENV test;
python3.5 -m unittest discover -vcs tests
