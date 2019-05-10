import os
import unittest

from src.sail.config_reader import build_pin_from_config
from src.sail.config_reader import read_mainsheet_config
from src.sail.config_reader import read_servo_config


class SailConfigReaderTest(unittest.TestCase):
    """Tests methods in Sail Config Reader"""
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_build_pin_from_config(self):
        pin = build_pin_from_config(self.path)
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

    def test_read_mainsheet_config(self):
        mainsheet_config = read_mainsheet_config(path=self.path)
        expected_config = {
            "sheeting_adv": 1,
            "max_boom_angle": 85
        }
        self.assertDictEqual(mainsheet_config, expected_config)
