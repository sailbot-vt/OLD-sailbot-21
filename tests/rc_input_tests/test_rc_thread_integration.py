import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.navigation_mode import NavigationMode
from src.rc_input.rc_input_thread import RCInputThread
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial
import src

import pdb

class RCThreadTests(unittest.TestCase):
    """Integration tests for RCInputThread"""
    def setUp(self):
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        serial.Serial.write = MagicMock(name='serial.Serial.write')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')
        src.hardware = MagicMock(name='src.hardware')
        src.hardware.port = MagicMock(name='src.hardware.port')
        src.hardware.port.SerialPort = MagicMock(name='src.hardware.port.SerialPort')

        self.rc_input_thread = RCInputThread(mock_bbio=Adafruit_BBIO, mock_port=serial.Serial)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_lows(self, mock_pub):

#        self.rc_input_thread.receiver.ports['UART'].value = "-1, -1, 0, 0\n"
        src.hardware.port.SerialPort.read_line = MagicMock(name='src.hardware.port.SerialPort.read_line',
                                                           return_value = "-1, -1, 0, 0\n")

        self.rc_input_thread.receiver.send_inputs()

        elf.assertAlmostEqual(-80, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
        self.assertAlmostEqual(-20, mock_pub.method_calls[1][2]["degrees_in"], 2)
        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_zeros(self, mock_pub):
        
#        self.rc_input_thread.receiver.ports['UART'].value = "0, 0, 0, 0\n"
        
        src.hardware.port.SerialPort.read_line = MagicMock(name='src.hardware.port.SerialPort.read_line',
                                                           return_value = "0, 0, 0, 0\n")

        self.rc_input_thread.receiver.send_inputs()

        self.assertAlmostEqual(0, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
        self.assertAlmostEqual(0, mock_pub.method_calls[1][2]["degrees_in"], 2)
        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_highs(self, mock_pub):
        
#        self.rc_input_thread.receiver.ports['UART'].value = "1, 1, 0, 0\n"
        src.hardware.port.SerialPort.read_line = MagicMock(name='src.hardware.port.SerialPort.read_line',
                                                           return_value = "1, 1, 0, 0\n")

        pdb.set_trace()

        self.rc_input_thread.receiver.send_inputs()

        self.assertAlmostEqual(80, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
        self.assertAlmostEqual(20, mock_pub.method_calls[1][2]["degrees_in"], 2)
        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)


if __name__ == '__main__':
    unittest.main()
