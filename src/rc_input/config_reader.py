import os

import yaml

from src.hardware.pin import make_pin
from src.hardware.port import make_port


def read_pin_config(mock_bbio=None, path=None):
    """Reads the pin configuration from config.yml and returns a matching dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        if mock_bbio is None:
            pins = {
                "RUDDER": make_pin(conf["pins"]["RUDDER"]),
                "TRIM": make_pin(conf["pins"]["TRIM"]),
                "MODE1": make_pin(conf["pins"]["MODE1"]),
                "MODE2": make_pin(conf["pins"]["MODE2"]),
                "UART_RX": make_pin(conf["pins"]["UART_RX"]),
                "UART_TX": make_pin(conf["pins"]["UART_TX"])
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
                                  mock_lib=mock_bbio.GPIO),
                "UART_RX": make_pin(conf["pins"]["UART_RX"],
                                  mock_lib=mock_bbio.GPIO),
                "UART_TX": make_pin(conf["pins"]["UART_TX"],
                                  mock_lib=mock_bbio.GPIO)
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

def read_port_config(mock_port=None, path=None):
    """ Reads the settings for serial port communication from config.yml and 
    returns matching port dictionary"""

    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        if mock_port is None:
            ports = {
                    "UART": make_port(config=conf["port"])
            }
        else:
            ports = {
                    "UART": make_port(config=conf["port"], mock_port=mock_port)
            }
    return ports
