import unittest
from unittest.mock import MagicMock

import os
from tests.mock_bbio import Adafruit_BBIO
from src.hardware.pin import make_pin

from src.airmar.config_reader import read_pin_config
from src.airmar.config_reader import read_interval


class AirmarConfigReaderTests(unittest.TestCase):
    """Tests methods in RC Config Reader"""

    def setUp(self):
        """Sets up path of test config.yaml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_pin_config(self):
        """Tests read_pin_config"""
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit.BBIO.UART.setup')

        pin = read_pin_config(mock_bbio=Adafruit_BBIO, path=self.path)

        assert pin.pin_name == "UART"
        Adafruit_BBIO.UART.setup.assert_called_with("UART1")

    def test_read_interval(self):
        """Tests read_interval"""
        assert read_interval(path=self.path) == "50 / 1000"
