import yaml
import os

from src.hardware.pin import make_pin


def build_pin_from_config(path=None):
    """Reads the pin configuration from config.yml and returns a matching Pin"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        pin = make_pin(conf["pins"]["MAINSHEET"])

    return pin


def read_servo_config(path=None):
    """Reads the servo configuration from config.yml and returns a matching servo."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        servo_config = conf["servos"]["MAIN"]

    return servo_config


def read_mainsheet_config(path=None):
    """Reads the servo configuration from config.yml and returns a matching servo."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        rudder_config = conf["mainsheet"]

    return rudder_config
