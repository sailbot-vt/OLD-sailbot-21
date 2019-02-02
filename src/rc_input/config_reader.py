import yaml
import os

from src.hardware.pin import make_pin


def read_pin_config():
    """Reads the pin configuration from config.yml and returns a matching dictionary"""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        pins = {
            "RUDDER": make_pin(conf["pins"]["RUDDER"]),
            "TRIM": make_pin(conf["pins"]["TRIM"]),
            "MODE1": make_pin(conf["pins"]["MODE1"]),
            "MODE2": make_pin(conf["pins"]["MODE2"])
        }

    return pins


def read_interval():
    """Reads the read interval from config.yml."""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        interval = conf["read interval"]

    return interval
