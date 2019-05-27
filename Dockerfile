FROM balenalib/beaglebone-black-debian-python:3.7.2-build

ENV HOSTNAME beaglebone

COPY . /sailbot
WORKDIR /sailbot

RUN apt-get update && apt-get install -y make && make init

ENTRYPOINT make run