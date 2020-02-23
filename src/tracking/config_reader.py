import os

import yaml

def read_kalman_config(path=None):
    """Reads the kalman configuration from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        kalman_config = conf['kalman']

    return kalman_config

def read_map_config(path=None):
    """Reads the map configuration from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        map_config = conf['map']

    return map_config
