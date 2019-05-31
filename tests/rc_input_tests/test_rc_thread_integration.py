import unittest
from unittest.mock import patch, MagicMock

from src.navigation_mode import NavigationMode
from src.rc_input.rc_input_thread import RCInputThread
from tests.mock_bbio import Adafruit_BBIO


class RCThreadTests(unittest.TestCase):
    """Integration tests for RCInputThread"""
    def setUp(self):
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit.BBIO.ADC.setup')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')

        self.rc_input_thread = RCInputThread(mock_bbio=Adafruit_BBIO)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_lows(self, mock_pub):
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input',
                                             return_value=False)
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=0.1)

        self.rc_input_thread.receiver.send_inputs()

        self.assertAlmostEqual(-80, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
        self.assertAlmostEqual(-20, mock_pub.method_calls[1][2]["degrees_in"], 2)
        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_zeros(self, mock_pub):
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input',
                                             return_value=False)
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=0.1472222222)

        self.rc_input_thread.receiver.send_inputs()

        self.assertAlmostEqual(0, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
        self.assertAlmostEqual(0, mock_pub.method_calls[1][2]["degrees_in"], 2)
        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_highs(self, mock_pub):
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input',
                                             return_value=False)
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit.BBIO.ADC.read',
                                           return_value=0.1944444444)

        self.rc_input_thread.receiver.send_inputs()

        self.assertAlmostEqual(80, mock_pub.method_calls[0][2]["degrees_starboard"], 2)
        self.assertAlmostEqual(20, mock_pub.method_calls[1][2]["degrees_in"], 2)
        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)


if __name__ == '__main__':
    unittest.main()
