import unittest
from unittest.mock import MagicMock

from src.airmar.airmar_receiver import AirmarReceiver
from src.broadcaster.broadcaster import BroadcasterType
from src.broadcaster.broadcaster import make_broadcaster
from src.hardware.pin import make_pin
from src.hardware.port import make_port
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial


class AirmarIntegrationTests(unittest.TestCase):
    """ Tests airmar program """

    def setUp(self):
        """ Initialize testing receiver """
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        serial.Serial.write = MagicMock(name='serial.Serial.write')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        pin = make_pin(config={
            "pin_name": "P0_0",
            "pin_type": "UART",
            "channel": "UART1"
        }, mock_lib=Adafruit_BBIO.UART)

        port = make_port(config={
            "port_name": "/dev/tty0",
            "port_type": "SERIAL",
            "baudrate": "4800",
            "encoding": "UTF-8",
            "timeout": 0 
        }, mock_port=serial.Serial)

        ids = ["VTG", "MWD", "GGA"]

        broadcaster = make_broadcaster(
            broadcaster_type=BroadcasterType.Testable)

        self.receiver = AirmarReceiver(
            broadcaster=broadcaster,
            ids=ids, pin=pin, port=port)

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
        self.receiver.processor.update_airmar_data.assert_called_once