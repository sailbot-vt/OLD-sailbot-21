import unittest

import os
from tests.mock_bbio import Adafruit_BBIO
from src.hardware.pin import make_pin

from src.rudder.config_reader import build_pin_from_config
from src.rudder.config_reader import read_servo_config
from src.rudder.config_reader import read_rudder_config

class RudderConfigReaderTests(unittest.TestCase):
    """Tests methods in Rudder Config Reader"""
    def setUp(self):
        """Sets up the path of config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_build_pin_from_config(self):
        pin = build_pin_from_config(path=self.path)
        # PWM mock_bbio param incomplete for config_reader?
        assert pin.pin_name == "Test"

    def test_read_servo_config(self):
        servo_config = read_servo_config(path=self.path)
        expected_config = {
            "full_left_duty": 1,
            "full_right_duty": 2,
            "full_left_angle": -180,
            "full_right_angle": 180
        }
        self.assertDictEqual(servo_config, expected_config)

    def test_read_rudder_config(self):
        rudder_config = read_rudder_config(path=self.path)
        expected_config = {
            "mechanical_adv": 1,
            "full_port_angle": -70,
            "full_starboard_angle": 70
        }
        self.assertDictEqual(rudder_config, expected_config)
