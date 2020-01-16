""" buoy_detection/config_reader.py
Contains utility functions to read from the buoy_detection/config.yaml file for other
files to more easily use.
"""
import yaml

DEFAULT_PATH = "config.yaml"


def get_config(path=DEFAULT_PATH):
    with open(path, "r") as handle:
        return yaml.full_load(handle)


def get_calibration_config(path=DEFAULT_PATH):
    config = get_config(path)
    return config["calibration"]
