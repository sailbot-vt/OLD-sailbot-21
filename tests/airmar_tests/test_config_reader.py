import os
import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.airmar.config_reader import read_interval
from src.airmar.config_reader import read_pin_config
from src.airmar.config_reader import read_port_config
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial


class ConfigReaderTests(unittest.TestCase):
    """ Tests Airmar Config reader methods """

    def setUp(self):
        """ Sets up path of test config.yml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_pin(self):
        """ Tests pin read from config.yml """
        Adafruit_BBIO.UART.setup = MagicMock(name="Adafruit.BBIO.UART.setup")

        mock_pin = read_pin_config(mock_bbio=Adafruit_BBIO, path=self.path)
        pin = read_pin_config(path=self.path)
        
        self.assertEqual(pin.pin_name, "P9_26")
        self.assertEqual(mock_pin.pin_name, "P9_26")


    def test_read_ids(self):
        """ Tests ids read from config.yml """
        pass

    def test_read_interval(self):
        """ Tests interval read from config.yml """
        self.assertEqual(read_interval(path=self.path), 50 / 1000)

    def test_read_port(self):
        """ Tests port read from config.yml """
        port = read_port_config(path=self.path)
        mock_port = read_port_config(path=self.path, mock_port=serial.Serial)
        
        self.assertEqual(mock_port.port_name, "/dev/tty01")
        self.assertEqual(port.port_name, "/dev/tty01")
