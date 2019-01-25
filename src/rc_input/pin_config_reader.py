import yaml

from definitions import ROOT_DIR
from src.bb_interface.pin import make_pin


def read_pin_config():
    """Reads the pin configuration from pin_config.yml and returns a matching dictionary"""
    with open(ROOT_DIR + "/src/rc_input/pin_config.yml", "r") as yml:
        conf = yaml.load(yml)
        pins = {
            "RUDDER": make_pin(conf["pins"]["RUDDER"]),
            "TRIM": make_pin(conf["pins"]["TRIM"]),
            "MODE1": make_pin(conf["pins"]["MODE1"]),
            "MODE2": make_pin(conf["pins"]["MODE2"])
        }

    return pins
