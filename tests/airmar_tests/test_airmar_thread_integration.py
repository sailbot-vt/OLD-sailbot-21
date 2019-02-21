import unittest
from unittest.mock import patch, MagicMock

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

from src.airmar.airmar_broadcaster import AirmarBroadcasterType

from src.airmar.airmar_input_thread import AirmarInputThread


class AirmarThreadTests(unittest.TestCase):
    """Integreation tests for AirmarInputThread"""

    def setUp(self):
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        self.airmar_input_thread = AirmarInputThread(
            mock_bbio=Adafruit_BBIO,
            mock_port=serial,
            broadcaster_type=AirmarBroadcasterType.Testable)

    def test_run(self):
        pass
