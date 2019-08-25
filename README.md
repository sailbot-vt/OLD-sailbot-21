# sailbot-20

[![Build status](https://travis-ci.com/vt-sailbot/sailbot-20.svg?branch=master)](https://travis-ci.com/vt-sailbot/sailbot-20)
[![Coverage Status](https://coveralls.io/repos/github/vt-sailbot/sailbot-20/badge.svg?branch=master)](https://coveralls.io/github/vt-sailbot/sailbot-20?branch=master)
[![License information](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/vt-sailbot/sailbot-20/blob/master/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/)

> The VT SailBOT team repository for the 2019-2020 school year.

### Architecture

The software design document detailing the system architecture can be found [here](https://docs.google.com/document/d/1JsAZn4CWerVZ45uQ7lLZehaZM9W0XL9Jg_lDHFKbvsM/edit?usp=sharing).

### Installation Instructions

1. Ensure that you have [Git](https://git-scm.com/downloads) and a version of [Python 3.5](https://www.python.org/downloads/) installed on your computer by running `git --version` and `python3.5 --version`. If either command does not give you a version number, you do not have the respective software.

2. Move to the directory where you would like to store your local copy of the code, and clone the repository by running `git clone git@github.com:vt-sailbot/sailbot-19.git`.

3. On macOS or Linux, run `make init`. On Windows, open `Makefile` and run each command under `init` separately. To compile with `clang` instead of `gcc` (for Mac users), run `make init CC=clang`.

### Testing Instructions

Any code pushed to this repository will automatically be subject to all existing test methods as well as any newly added tests.

To run tests locally before pushing, run `make test` on macOS or Linux, or run each command under `test` in `Makefile` separately on Windows.

Test coverage should be as complete as is practical – for most classes, it should be 90% to 100%. Recall that robustness is our first design requirement.

To view test coverage, run `coverage report` in the context of the `p3_5env` virtual environment.
