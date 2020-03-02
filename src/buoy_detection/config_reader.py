""" buoy_detection/config_reader.py
Contains utility functions to read from the buoy_detection/config.yaml file for other
files to more easily use.
"""
import yaml


def get_config(path):
    """Gets the YAML configuration stored at the given path.

    Inputs:
        path -- The path to the YAML configuration file.

    Returns:
        The loaded YAML configuration object.
    """
    with open(path, "r") as handle:
        return yaml.full_load(handle)
