import yaml
import os

from src.hardware.pin import make_pin

def read_pin_config(mock_bbio=None, path=None):
    """Reads the pin configuration from config.yml and returns a matching pin"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        if mock_bbio is None:
            pin = make_pin(cong["pins"]["UART"])
        else:
            pin = make_pin(conf["pins"]["UART"], mock_lib=mock_bbio.UART)
    return pin

def read_interval(path=None):
    """Reads the read interval from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.load(yml)
        interval = conf("read interval")

    return interval
