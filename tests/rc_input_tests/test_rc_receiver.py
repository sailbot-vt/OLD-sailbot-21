import unittest
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from src.hardware.pin import make_pin
from src.hardware.port import make_port
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

from src.navigation_mode import NavigationMode
from src.rc_input.rc_receiver import RCReceiver

class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        serial.Serial.write = MagicMock(name='serial.Serial.write')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        """Sets up a receiver for each test method"""
        self.r = RCReceiver({
            "UART_RX": make_pin({
                "pin_name": "UART_RX_test",
                "pin_type": "UART",
                "channel": "UART2"
            }, mock_lib=Adafruit_BBIO.UART),
            "UART_TX": make_pin({
                "pin_name": "UART_TX_test",
            })
        },
                            {
            "UART": make_port({
                "port_name": "serial_test",
                "port_type": "TESTABLE",
                "read_value": "0, 0, 0, 0"})
        })

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_get_rudder(self, mock_pub):
        """Tests that the receiver reads and scales rudder input correctly"""
        test_inputs = [-1, -0.25, 0, 0.25, 1]
        scaled_outputs = [-80, -20, 0, 20, 80]  # 80 * x^2

        ii = 0
        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            # Set the return value
#            self.r.pins["RUDDER"].value = test_input
            self.r.ports["UART"].value = str(test_input) + ', 0, 0, 0'

            self.r.send_inputs()

            self.assertAlmostEqual(scaled_output, mock_pub.method_calls[3*ii][2]["degrees_starboard"], 2)
            
            ii += 1

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_scale_trim(self, mock_pub):
        """Tests that the receiver reads and scales trim input correctly"""
        test_inputs = [-1, -0.25, 0, 0.25, 1]
        scaled_outputs = [-20, -5, 0, 5, 20]  # 20 * x^2

        ii = 0
        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            # Set the return value
#            self.r.pins["TRIM"].value = test_input
            self.r.ports["UART"].value = '0, ' + str(test_input) + ', 0, 0'

            self.r.send_inputs()

            self.assertAlmostEqual(scaled_output, mock_pub.method_calls[(3*ii) + 1][2]["degrees_in"], 2)

            ii += 1

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_detect_mode(self, mock_pub):
        """Tests that the receiver reads and transforms mode input correctly"""
        self.r.send_inputs()

        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)


if __name__ == "__main__":
    unittest.main()
