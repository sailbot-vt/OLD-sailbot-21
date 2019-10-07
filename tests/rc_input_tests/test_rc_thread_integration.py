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
        
        self.rc_input_thread = RCInputThread(mock_bbio=Adafruit_BBIO, mock_port=serial.Serial)
        self.mock_data = {"RUDDER":0, "TRIM":0, "MODE1":0, "MODE2":0}

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_lows(self, mock_pub):

#        self.rc_input_thread.receiver.ports['UART'].value = "-1, -1, 0, 0\n"
        low_mock_data = self.mock_data
        low_mock_data["RUDDER"] = -1
        low_mock_data["TRIM"] = -1
        with patch('src.rc_input.rc_receiver.RCReceiver._decode_input', autospec=True):
            src.rc_input.rc_receiver.RCReceiver._decode_input = MagicMock(name="src.rc_input_thread.receiver.RCReceiver._decode_input", return_value=low_mock_data)                             
        
            self.rc_input_thread.receiver.send_inputs()

            self.assertAlmostEqual(-80, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
            self.assertAlmostEqual(-20, mock_pub.method_calls[1][2]["degrees_in"], 2)
            mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_zeros(self, mock_pub):
        
        zeros_mock_data = self.mock_data
        zeros_mock_data["RUDDER"] = 0
        zeros_mock_data["TRIM"] = 0
        with patch('src.rc_input.rc_receiver.RCReceiver._decode_input', autospec=True):
            src.rc_input.rc_receiver.RCReceiver._decode_input = MagicMock(name="src.rc_input_thread.receiver.RCReceiver._decode_input", return_value=zeros_mock_data)                             

            self.rc_input_thread.receiver.send_inputs()

            self.assertAlmostEqual(0, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
            self.assertAlmostEqual(0, mock_pub.method_calls[1][2]["degrees_in"], 2)
            mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_highs(self, mock_pub):
        
        highs_mock_data = self.mock_data
        highs_mock_data["RUDDER"] = 1
        highs_mock_data["TRIM"] = 1

        with patch('src.rc_input.rc_receiver.RCReceiver._decode_input', autospec=True):
            src.rc_input.rc_receiver.RCReceiver._decode_input = MagicMock(name="src.rc_input_thread.receiver.RCReceiver._decode_input", return_value=highs_mock_data)                             

            self.rc_input_thread.receiver.send_inputs()

            self.assertAlmostEqual(80, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
            self.assertAlmostEqual(20, mock_pub.method_calls[1][2]["degrees_in"], 2)
            mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

if __name__ == '__main__':
    unittest.main()
