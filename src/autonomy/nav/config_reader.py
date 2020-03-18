import yaml
import os

def read_interval(path=None):
    """Reads the read interval from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        helm_interval = conf["nav interval"]

    return eval(str(helm_interval))

def read_nav_config(path=None):
    """Reads the nav config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        nav_config = conf["nav_config"]

    return nav_config

def read_tack_config(path=None):
    """Reads the tack config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        tack_config = conf["tack_config"]

    return tack_config
