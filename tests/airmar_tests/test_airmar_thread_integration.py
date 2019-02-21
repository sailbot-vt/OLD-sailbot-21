import unittest
from unittest.mock import patch, MagicMock

from tests.mock_bbio import Adafruit_BBIO
from src.airmar.airmar_input_thread import AirmarInputThread


class AirmarThreadTests(unittest.TestCase):
    """Integreation tests for AirmarInputThread"""
    
    def setUp(self):
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')
        self.airmar_input_thread = AirmarInputThread(mock_bbio=Adafruit_BBIO)

    def test_run(self):
        pass