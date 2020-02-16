import os
import unittest

from src.autonomy.obstacle_avoidance.config_reader import read_object_field_config, read_gap_config

class ObstacleAvoidanceConfigReaderTests(unittest.TestCase):
    """Tests methods in Obstacle Avoidance Config Reader"""
    def setUp(self):
        """Sets up the path of config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_object_field_config(self):
        """Tests read object field config method"""
        # expected values
        expected_vals = {'time_range': (0, 5), 'bearing_range': (-30, 30)}

        self.assertDictEqual(expected_vals, read_object_field_config(self.path))

    def test_read_gap_config(self):
        """Tests read gap config method"""
        # expected values
        expected_vals = {'t_step': 0.1, 'theta_step': 2}

        self.assertDictEqual(expected_vals, read_gap_config(self.path))
