import yaml

from definitions import ROOT_DIR
from src.pin import Pin


def read_pin_config():
    """Reads the pin configuration from pin_config.yml and returns a matching dictionary"""
    with open(ROOT_DIR + "/src/rc_input/pin_config.yml", "r") as yml:
        conf = yaml.load(yml)
        pins = {
            "RUDDER": Pin(conf["pins"]["RUDDER"]),
            "TRIM": Pin(conf["pins"]["TRIM"]),
            "MODE1": Pin(conf["pins"]["MODE1"]),
            "MODE2": Pin(conf["pins"]["MODE2"])
        }

    return pins
