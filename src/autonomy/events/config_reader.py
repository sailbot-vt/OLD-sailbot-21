import yaml
import os


def read_interval(event_type, path=None):
    """Reads the read interval from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        helm_interval = conf[event_type]["nav interval"]

    return eval(str(helm_interval))
