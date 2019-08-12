import os

import yaml

from src.hardware.pin import make_pin


def build_pin_from_config(path=None, logger=None):
    """Reads the pin configuration from config.yml and returns a matching Pin"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        pin = make_pin(conf["pins"]["RUDDER"], logger)

    return pin


def read_servo_config(path=None):
    """Reads the servo configuration from config.yml and returns a matching servo."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        servo_config = conf["servos"]["MAIN"]

    return servo_config


def read_rudder_config(path=None):
    """Reads the servo configuration from config.yml and returns a matching servo."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        rudder_config = conf["rudder"]

    return rudder_config
