import os
import unittest

from src.autonomy.movement.config_reader import read_movement_config

class MovementConfigReaderTests(unittest.TestCase):
    """Tests methods in Movement Config Reader"""
    def setUp(self):
        """Sets up the path of config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_movement_config(self):
        """Tests read movement config method"""
        # expected values
        expected_vals = {"rudder_angles":
                            {"fast_turn"  : 15,
                             "medium_turn": 10,
                             "slow_turn"  : 5},
                         "default_turn_rate": 'medium_turn',
                         "update_interval": 0.5}

        self.assertDictEqual(expected_vals, read_movement_config(self.path))
