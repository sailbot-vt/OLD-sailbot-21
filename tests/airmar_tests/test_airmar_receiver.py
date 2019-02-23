import unittest
from unittest.mock import patch, MagicMock

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

from src.airmar.airmar_broadcaster import make_broadcaster
from src.airmar.airmar_broadcaster import AirmarBroadcasterType

from src.hardware.pin import make_pin
from src.hardware.port import make_port

from src.airmar.airmar_receiver import AirmarReceiver


class AirmarReceiverTest(unittest.TestCase):
    """ Test cases for Airmar Receiver """

    def setUp(self):
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        port_conf = {
            "port_name": "/dev/tty0",
            "port_type": "SERIAL",
            "baudrate": 4800,
            "timeout": 0
        }

        pin_conf = {
            "pin_name": "P0_0",
            "pin_type": "UART",
            "channel": "UART1"
        }

        pin = make_pin(pin_conf, mock_lib=Adafruit_BBIO.UART)
        port = make_port(port_conf, mock_port=serial.Serial)
        broadcaster = make_broadcaster(
            broadcaster_type=AirmarBroadcasterType.Testable)

        self.receiver = AirmarReceiver(
            broadcaster=broadcaster, pin=pin, port=port)

    def test_split_messages(self):
        serial.Serial.isOpen.return_value = True
        self.receiver.remaining_input = "test0\r\n"
        serial.Serial.read.return_value = "test1\r\ntest2\r\n"

        string0 = self.receiver._read_msg()
        string1 = self.receiver._read_msg()
        string2 = self.receiver._read_msg()

        self.assertEqual(string0, "test0")
        self.assertEqual(string1, "test1")
        self.assertEqual(string2, "test2")