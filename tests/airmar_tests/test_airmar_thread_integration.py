import unittest
from unittest.mock import patch, MagicMock

from tests.mock_bbio import Adafruit_BBIO
from src.airmar.airmar_input_thread import AirmarInputThread


class AirmarThreadTests(unittest.TestCase):
    """Integreation tests for AirmarInputThread"""
    
    @patch('src.airmar.airmar_input_thread.serial', autospec=True)
    def setUp(self, mock_serial):
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')
        self.airmar_input_thread = AirmarInputThread(mock_bbio=Adafruit_BBIO)

    @patch('src.airmar.airmar_input_thread.serial', autospec=True)
    def test_run(self, mock_serial):
        pass