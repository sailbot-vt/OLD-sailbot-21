import yaml
import os

from src.hardware.pin import make_pin


def read_pin_config(mock_bbio=None, path=None):
    """Reads the pin configuration from config.yml and returns a matching dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_bbio is None:
            pins = {
                "RUDDER": make_pin(conf["pins"]["RUDDER"]),
                "TRIM": make_pin(conf["pins"]["TRIM"]),
                "MODE1": make_pin(conf["pins"]["MODE1"]),
                "MODE2": make_pin(conf["pins"]["MODE2"])
            }
        else:
            pins = {
                "RUDDER": make_pin(conf["pins"]["RUDDER"],
                                   mock_lib=mock_bbio.ADC),
                "TRIM": make_pin(conf["pins"]["TRIM"],
                                 mock_lib=mock_bbio.ADC),
                "MODE1": make_pin(conf["pins"]["MODE1"],
                                  mock_lib=mock_bbio.GPIO),
                "MODE2": make_pin(conf["pins"]["MODE2"],
                                  mock_lib=mock_bbio.GPIO)
            }

    return pins


def read_interval(path=None):
    """Reads the read interval from config.yml."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        interval = conf["read interval"]

    return eval(interval)
