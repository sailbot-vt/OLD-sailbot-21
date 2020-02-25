import os
import unittest

from src.tracking.config_reader import read_kalman_config, read_map_config

class TrackingConfigReaderTests(unittest.TestCase):
    """Tests methods in Tracking Config Reader"""
    def setUp(self):
        """Sets up the path of config.yml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_kalman_config(self):
        """Tests read kalman config method"""
        # create truth dict
        truth_dict = {'r_sigma': 1.0, 'theta_sigma': 1.0, 'r_hat_sigma': 3.0, 'theta_hat_sigma': 3.0}

        # check for correct behavior
        self.assertDictEqual(truth_dict, read_kalman_config(path=self.path))

    def test_read_map_config(self):
        """Tests read map config method"""
        # create truth dict
        truth_dict = {'update_interval': 0.5}

        # check for correct behavior
        self.assertDictEqual(truth_dict, read_map_config(path=self.path))
