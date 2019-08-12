import unittest
try:
    from unittest.mock import patch
except:
    from mock import patch

from src.hardware.pin import make_pin
from src.navigation_mode import NavigationMode
from src.rc_input.rc_receiver import RCReceiver


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        """Sets up a receiver for each test method"""
        self.r = RCReceiver({
            "RUDDER": make_pin({
                "pin_name": "rudder_test"
            }),
            "TRIM": make_pin({
                "pin_name": "trim_test"
            }),
            "MODE1": make_pin({
                "pin_name": "trim_test",
                "return_value": False
            }),
            "MODE2": make_pin({
                "pin_name": "trim_test",
                "return_value": False
            })
        })

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_get_rudder(self, mock_pub):
        """Tests that the receiver reads and scales rudder input correctly"""
        test_inputs = [-1, -0.5, 0, 0.5, 1]
        scaled_outputs = [-80, -20, 0, 20, 80]  # 80 * x^2

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            # Set the return value
            self.r.pins["RUDDER"].value = test_input

            self.r.send_inputs()

            mock_pub.sendMessage.assert_any_call("set rudder", degrees_starboard=scaled_output)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_scale_trim(self, mock_pub):
        """Tests that the receiver reads and scales trim input correctly"""
        test_inputs = [-1, -0.5, 0, 0.5, 1]
        scaled_outputs = [-20, -5, 0, 5, 20]  # 20 * x^2

        for test_input, scaled_output in zip(test_inputs, scaled_outputs):
            # Set the return value
            self.r.pins["TRIM"].value = test_input

            self.r.send_inputs()

            mock_pub.sendMessage.assert_any_call("set trim", degrees_in=scaled_output)

    @patch('src.rc_input.rc_receiver.pub', autospec=True)
    def test_detect_mode(self, mock_pub):
        """Tests that the receiver reads and transforms mode input correctly"""
        self.r.send_inputs()

        mock_pub.sendMessage.assert_any_call("set nav mode", mode=NavigationMode.MANUAL)


if __name__ == "__main__":
    unittest.main()
