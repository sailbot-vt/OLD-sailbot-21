import os

import yaml

from src.hardware.pin import make_pin


def read_pin_config(mock_bbio=None, path=None, logger=None):
    """Reads the pin configuration from config.yml and returns a matching dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        if mock_bbio is None:
            pins = {
                "RUDDER": make_pin(conf["pins"]["RUDDER"], logger=logger),
                "TRIM": make_pin(conf["pins"]["TRIM"], logger=logger),
                "MODE1": make_pin(conf["pins"]["MODE1"], logger=logger),
                "MODE2": make_pin(conf["pins"]["MODE2"], logger=logger)
            }
        else:
            pins = {
                "RUDDER": make_pin(conf["pins"]["RUDDER"],
                                   mock_lib=mock_bbio.ADC, logger=logger),
                "TRIM": make_pin(conf["pins"]["TRIM"],
                                 mock_lib=mock_bbio.ADC, logger=logger),
                "MODE1": make_pin(conf["pins"]["MODE1"],
                                  mock_lib=mock_bbio.GPIO, logger=logger),
                "MODE2": make_pin(conf["pins"]["MODE2"],
                                  mock_lib=mock_bbio.GPIO, logger=logger)
            }

    return pins


def read_interval(path=None):
    """Reads the read interval from config.yml."""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        interval = conf["read interval"]

    return eval(interval)
