import os

import yaml

from src.hardware.pin import make_pin


def build_pin_from_config(path=None):
    """Reads the pin configuration from config.yml and returns a matching Pin"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        pin = make_pin(conf["pins"]["MAINSHEET"])

    return pin


def read_servo_config(path=None):
    """Reads the servo configuration from config.yml and returns a matching servo."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        servo_config = conf["servos"]["MAIN"]

    return servo_config


def read_mainsheet_config(path=None):
    """Reads the servo configuration from config.yml and returns a matching servo."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        mainsheet_config = conf["mainsheet"]

    return mainsheet_config


def read_pin_config(mock_bbio=None, path=None):
    """Reads the pin configuration from config.yml and returns a matching dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_bbio is None:
            pins = [
                make_pin(conf["pins"]["Step"]),
                make_pin(conf["pins"]["Direction"]),
            ]
        else:
            pins = [
                make_pin(conf["pins"]["Step"],
                         mock_lib=mock_bbio.GPIO),
                make_pin(conf["pins"]["Direction"],
                         mock_lib=mock_bbio.GPIO),
            ]

    return pins


def read_center_stepper_angle(path=None):
    """Reads the read interval from config.yml."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        interval = conf["center stepper angle"]

    return interval
