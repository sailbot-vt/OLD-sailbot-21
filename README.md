# sailbot-20

[![Build status](https://travis-ci.com/vt-sailbot/sailbot-20.svg?branch=master)](https://travis-ci.com/vt-sailbot/sailbot-20)
[![Coverage Status](https://coveralls.io/repos/github/vt-sailbot/sailbot-20/badge.svg?branch=master)](https://coveralls.io/github/vt-sailbot/sailbot-20?branch=master)
[![License information](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/vt-sailbot/sailbot-20/blob/master/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/)

> The VT SailBOT team repository for the 2019-2020 school year.

### Architecture

The software design document detailing the system architecture can be found [here](https://docs.google.com/document/d/1JsAZn4CWerVZ45uQ7lLZehaZM9W0XL9Jg_lDHFKbvsM/edit?usp=sharing).

### Installation Instructions

1. Ensure that you have [Git](https://git-scm.com/downloads) and a version of [Docker](https://www.docker.com/get-started)installed on your computer by running `git --version` and `docker --version`. If either command does not give you a version number, you do not have the respective software.

2. Move to the directory where you would like to store your local copy of the code, and clone the repository by running `git clone git@github.com:vt-sailbot/sailbot-20.git`.

3. There is no longer a distinct initialization step. Initialization will occur upon first building an image through the commands `make test` or `make build_prod`. Note: the first time that you run these commands on your machine, the initialization will be very slow and take 15-20 minutes. After that first initialization, if there are no changes to the initialization instructions for the container, building the new docker image will be much faster.

4. A developmental environment is included in the sailbot-development docker image. We reccommend the use of this docker container rather than a typical python virtual environment, so our development environment remains consitent throughout the team. The image can be built and ran through the command `make dev`. This will allow you to enter a debian-stretch environment with python3 and our developmental packages installed. Note, this environment is not production ready, and code must be tested through `make test`.

### Testing Instructions

Any code pushed to this repository will automatically be subject to all existing test methods as well as any newly added tests.

To run tests locally before pushing, run `make test` on macOS or Linux, or run each command under `test` in `Makefile` separately on Windows. Running `make test` first builds a docker container with updated source files. Upon build completetion, unit tests are run.

Test coverage should be as complete as is practical – for most classes, it should be 90% to 100%. Recall that robustness is our first design requirement.

### Deployment Instructions

There are two options to deploy to the Beaglebone Black. 

#### Automated Deployment

Upon a successful pull request with master, a new Docker image will be built and pushed to the central Dockerhub. Once that occurs, running `make run` on the Beaglebone will (attempt to) pull that image and run it. This is the preferred option for stable, long-term deployment. Optionally, to access the command line interface the command `make run_cli` can be used instead.

#### Local Deployment

To use this command, you will need to set `experimental=True` in your docker-daemon configurations: [docker-daemon documentation](https://docs.docker.com/engine/reference/commandline/dockerd/). By running `make build_prod_tar`, a local docker image built for the Beaglebone is created and compressed on your local machine. Please note, the first time that this command is run after each change to initialization instructions will take 20-30 minutes. Then, with the Beaglebone either physically connected to your machine (via USB or Ethernet) or on the same network as your machine, you can sync the Docker image tarball to Beaglebone using rsync, scp, etc. Then, on the Beaglebone, use the command `docker load -i <path_to_tar_file>` and then use `make run`.
