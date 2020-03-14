import yaml
import os

def read_start_gate_config(path=None):
    """Reads the read start gate config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        start_gate_conf = conf["start_gate"]

    return start_gate_conf

def read_round_buoy_config(path=None):
    """Reads the read round buoy config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        round_buoy_conf = conf["round_buoy"]

    return round_buoy_conf
