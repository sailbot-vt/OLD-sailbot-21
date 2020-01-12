import os
import unittest

from src.arduino.config_reader import read_arduino_config
from src.arduino.config_reader import read_port_config
from src.arduino.config_reader import read_pin_config

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

class ArduinoConfigReaderTests(unittest.TestCase):
    """Tests methods in Arduino Config Reader"""
    def setUp(self):
        """Sets up the path of config.yml for each test method"""
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_read_pin_config(self):
        """Tests read_pin_config method"""
        pin = read_pin_config(path = self.path)
        assert pin.pin_name == "Test"

    def test_read_arduino_config(self):
        """Tests read_arduino_config method"""
        arduino_config = read_arduino_config(path = self.path)
        expected_config = {'update_interval': 5}
        self.assertDictEqual(arduino_config, expected_config)

    def test_read_port_config(self):
        """ Tests read_port_config method"""
        port = read_port_config(path=self.path)
        mock_port = read_port_config(path=self.path, mock_port=serial.Serial)
    
        self.assertEqual(mock_port.port_name, "/dev/tty02")
        self.assertEqual(port.port_name, "/dev/tty02")
