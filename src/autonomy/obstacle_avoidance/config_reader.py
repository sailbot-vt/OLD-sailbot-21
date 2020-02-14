import yaml
import os


def read_object_field_config(path=None):
    """Reads the object field config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        object_field_config = conf['object_field']

    time_range = (object_field_config['time_range']['time_range_l'], object_field_config['time_range']['time_range_r'])
    bearing_range = (object_field_config['bearing_range']['bearing_range_l'], object_field_config['bearing_range']['bearing_range_r'])

    return_config = {'time_range': time_range, 'bearing_range': bearing_range}

    return return_config

def read_gap_config(path=None):
    """Reads the gap config from config.yml"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        gap_config = conf['gap_config']

    return gap_config
