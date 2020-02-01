import os

import yaml

def read_decision_config(path=None):
    """Reads the sensor decision configuration from config.yml and returns config dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        sensor_decision_config = conf["sensor_decision"]

    return sensor_decision_config
