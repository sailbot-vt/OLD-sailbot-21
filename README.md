# sailbot-19

[![Build status](https://travis-ci.com/vt-sailbot/sailbot-19.svg?branch=master)](https://travis-ci.com/vt-sailbot/sailbot-19)
[![License information](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/vt-sailbot/sailbot-19/blob/master/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/)

> The VT SailBOT team repository for the 2018-2019 school year.

### Installation Instructions

1. Ensure that you have [Git](https://git-scm.com/downloads) and a version of [Python 3.7](https://www.python.org/downloads/) installed on your computer by running `git --version` and `python3.7 --version`. If either command does not give you a version number, you do not have the respective software.

2. Move to the directory where you would like to store your local copy of the code, and clone the repository by running `git clone git@github.com:vt-sailbot/sailbot-19.git`.

3. Install a Python 3.7 virtual environment in your local repository by running `virtualenv -p python3.7 p3_7env --no-site-packages`. The created directory `p3_7env` will be automatically excluded from source control. The name of the virtual environment is important if you want the `make` commands to work correctly.

4. On macOS or Linux, run `make init`. On Windows, open `Makefile` and run each command under `init` separately.

### Testing Instructions

Any code pushed to this repository will automatically be subject to all existing test methods as well as any newly added tests.

To run tests locally before pushing, run `make test` on macOS or Linux, or run each command under `test` in `Makefile` separately on Windows.

Test coverage should be as complete as is practical – for most classes, it should be 90% to 100%. Recall that robustness is our first design requirement.