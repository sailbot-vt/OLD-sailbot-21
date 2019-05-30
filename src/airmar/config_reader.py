import os

import yaml

from src.hardware.pin import make_pin
from src.hardware.port import make_port


def read_pin_config(mock_bbio=None, path=None):
    """Reads the pin configuration from config.yml and returns matching pin 
    dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_bbio is None:
            pin = make_pin(conf["pin"])
        else:
            pin = make_pin(conf["pin"], mock_lib=mock_bbio.UART)

    return pin


def read_ids(path=None):
    """ Reads the nmea sentence id's to enable from config.yml
    and returns list of ids."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        ids = conf["sentences"]
    return ids


def read_interval(path=None):
    """Reads the read interval from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        interval = conf["read interval"]

    return eval(interval)


def read_port_config(mock_port=None, path=None):
    """ Reads the settings for serial port communication from config.yml and 
    returns matching port dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_port is None:
            port = make_port(config=conf["port"])
        else:
            port = make_port(config=conf["port"], mock_port=mock_port)
    return port
