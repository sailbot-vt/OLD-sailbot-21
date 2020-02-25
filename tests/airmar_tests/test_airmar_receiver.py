import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.airmar.airmar_receiver import AirmarReceiver
from src.broadcaster.broadcaster import BroadcasterType
from src.broadcaster.broadcaster import make_broadcaster
from src.logging.logger import Logger

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial


class AirmarReceiverTests(unittest.TestCase):
    """ Tests airmar receiver """

    def setUp(self):
        """ Initialize testing receiver """
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        serial.Serial.write = MagicMock(name='serial.Serial.write')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        broadcaster = make_broadcaster(
            broadcaster_type=BroadcasterType.Testable)

        self.receiver = AirmarReceiver(
            logger=Logger(),
            broadcaster=broadcaster,
            mock_bbio=Adafruit_BBIO,
            mock_port=serial.Serial)

    def test_start_stop(self):
        """ 
        Tests start opens port, setup UART, flags is_running true
        Tests stop closes port, flags is_running false 
        """
        serial.Serial.isOpen.return_value = False
        self.receiver.start()
        assert self.receiver.is_running

        self.receiver.stop()
        assert not self.receiver.is_running

    def test_send_airmar_data(self):
        """ Tests update airmar data called """
        self.receiver.processor.update_airmar_data = MagicMock(
                name='receiver.processor.update_airmar_data')
        self.receiver.parser.parse = MagicMock(
            name='receiver.parser.parse', 
            return_value=None)
        self.receiver.send_airmar_data()
        self.receiver.parser.parse.return_value = ["test"] 
        self.receiver.send_airmar_data()
        self.assertEqual(2, self.receiver.processor.update_airmar_data.call_count)
