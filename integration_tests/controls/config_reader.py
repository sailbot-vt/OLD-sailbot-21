import os
import yaml

from integration_tests.controls.test_scheme_enum import TestScheme

def read_test_config(scheme, path=None):
    """Reads the test scheme configuration from config.yml and returns config dictionary"""
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/config.yml", "r") as yml:
        conf = yaml.full_load(yml)
        if scheme == TestScheme.ROTATE:
            test_config = conf["ROTATE"]

    return test_config
