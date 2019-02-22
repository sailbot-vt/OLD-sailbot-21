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
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        self.airmar_input_thread = AirmarInputThread(
            mock_bbio=Adafruit_BBIO,
            mock_port=serial,
            broadcaster_type=AirmarBroadcasterType.Testable)

    @patch('src.airmar.airmar_broadcaster.pub', autospec=True)
    def test_none(self, mock_pub):
        """ Tests that nothing is broadcasted when nothing is read. """
        serial.Serial.read = MagicMock(name='serial.Serial.read',
                                       return_value="")

        self.airmar_input_thread.receiver.send_airmar_data()

        mock_pub.sendMessage.assert_not_called()