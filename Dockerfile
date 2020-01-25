FROM balenalib/beaglebone-black-debian-python

ENV HOSTNAME beaglebone

COPY qemu-arm-static /usr/bin

RUN apt-get update && apt-get install make wget

COPY scripts /sailbot/scripts
COPY Makefile /sailbot/
COPY requirements.prod.txt /sailbot/
WORKDIR /sailbot

RUN make init

COPY src /sailbot/src
COPY tests /sailbot/tests
COPY main.py /sailbot/main.py
