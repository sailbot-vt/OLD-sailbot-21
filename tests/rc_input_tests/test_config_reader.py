import os
import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.rc_input.config_reader import read_interval
from src.rc_input.config_reader import read_pin_config
from src.hardware.pin import ADCPin, GPIOPin
from tests.mock_bbio import Adafruit_BBIO


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
            if isinstance(pin, ADCPin):
                assert pin.min_v == 0
                assert pin.default_v == 0.90
                assert pin.max_v == 1.80
            elif isinstance(pin, GPIOPin):
                assert pin.io_type == Adafruit_BBIO.GPIO.IN

    def test_read_interval(self):
        assert read_interval(path=self.path) == 50 / 1000


if __name__ == "__main__":
    unittest.main()
