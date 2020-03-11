import yaml
import os

def read_movement_config(path=None):
    """Reads the movement config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)

    return conf
