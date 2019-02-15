import unittest
from unittest.mock import MagicMock

import os
from tests.mock_bbio import Adafruit_BBIO
from src.hardware.pin import make_pin

from src.rc_input.config_reader import read_pin_config
from src.rc_input.config_reader import read_interval

class RCConfigReaderTests(unittest.TestCase):
    """Tests methods in RC Config Reader"""
    def setUp(self):
        """Sets up the path of test config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_pin_config(self):
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adagruit.BBIO.ADC.setup')

        pins = read_pin_config(mock_bbio=Adafruit_BBIO, path=self.path)
        for pin in pins.values():
            if pin.pin_name == "ADC_PIN":
                assert pin.min_v == .18
                assert pin.default_v == .26
                assert pin.max_v == .35
            elif pin.pin_name == "GPIO_PIN":
                assert pin.io_type == Adafruit_BBIO.GPIO.IN

    def test_read_interval(self):
        assert read_interval(path=self.path) == "50 / 1000"

if __name__ == "__main__":
    unittest.main()
