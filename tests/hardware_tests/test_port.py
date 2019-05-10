import unittest
from unittest.mock import MagicMock

from tests.mock_port import serial

from src.hardware.port import make_port


class PortTests(unittest.TestCase):
    """ Tests Port methods. """
    def setUp(self):
        serial.Serial.isOpen = MagicMock(name="serial.Serial.isOpen",
                                    return_value=True)
        self.port = make_port({
            "port_type" : "SERIAL",
            "port_name" : "mock serial",
            "baudrate" : "4800",
            "timeout" : 0,
            "encoding": "UTF-8"
        }, mock_port=serial.Serial)
        self.serial = serial.Serial

    def test_serial_read(self):
        """ Tests that serial port reads correctly."""
        msg = b"test"
        serial.Serial.inWaiting = MagicMock(name="serial.Serial.inWaiting", 
                                    return_value=len(msg))
        serial.Serial.read = MagicMock(name="serial.Serial.read", 
                                    return_value=msg)
        self.assertEquals(self.port.read(), msg)

    def test_serial_read_line(self):
        """ Tests that serial port reads line correctly. """
        msg = b"test\r\ntest2\r\ntest3\r\n"
                # Create port
        self.port.read = MagicMock(name="serial.Serial.read",
                                    return_value=msg)

        self.assertEquals(self.port.read_line(terminator="\r\n"), "test\r\n")
        self.port.read = MagicMock(name="serial.Serial.read",
                                    return_value=b"test4\r\n")
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test2\r\n")
        self.port.read = MagicMock(name="serial.Serial.read",
                                    return_value=b'')
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test3\r\n")
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test4\r\n")
        self.assertEquals(self.port.read_line(terminator="\r\n"), None)
        serial.Serial.isOpen.return_value = False
        self.assertEquals(self.port.read_line(terminator="\r\n"), None)