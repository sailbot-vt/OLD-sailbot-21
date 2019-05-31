import itertools
import unittest
from unittest.mock import MagicMock

from src.hardware.port import make_port
from tests.mock_port import serial


class PortTests(unittest.TestCase):
    """ Tests Port methods. """
    
    def setUp(self):
        """ Create testing fields """
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
        self.port.read = MagicMock(name="serial.Serial.read")
        # Simulates a buffer : 1, 2, 3 == one read
        # 4 == second read, 5 = third read
        # all other calls to read == null byte
        self.port.read.side_effect = itertools.chain(
            # Note, multi-lines and cut off line, last one not terminated
            [b"test\r\ntest2\r\ntest", b"3\r\ntest4\r\n", b"test5"], 
            itertools.repeat(b'')
        )
        # test1, 2, 3, 4
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test\r\n")
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test2\r\n")
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test3\r\n")
        self.assertEquals(self.port.read_line(terminator="\r\n"), "test4\r\n")
        # Unterminated line to buffer
        self.assertEquals(self.port.read_line(terminator="\r\n"), None)
        self.assertEquals(self.port.remaining_input, bytearray(b'test5'))
        # serial port not open
        serial.Serial.isOpen.return_value = False
        self.assertEquals(self.port.read_line(terminator="\r\n"), None)