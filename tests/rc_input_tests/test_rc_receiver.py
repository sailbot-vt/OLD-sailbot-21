import unittest

from src.hardware.pin import make_pin
from src.rc_input.rc_receiver import RCReceiver
from src.rc_input.rc_broadcaster import make_broadcaster, RCInputBroadcasterType
from src.navigation_mode import NavigationMode


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        """Sets up a receiver for each test method"""
        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Testable)
        self.r = RCReceiver(broadcaster=self.broadcaster, pins={
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

    def test_get_rudder(self):
        """Tests that the receiver reads and scales rudder input correctly"""
        test_inputs = [-1, -0.5, 0, 0.5, 1]
        scaled_outputs = [-80, -20, 0, 20, 80]  # 80 * x^2

        for index, (test_input, scaled_output) in enumerate(zip(test_inputs, scaled_outputs)):
            # Set the return value
            self.r.pins["RUDDER"].value = test_input

            self.r.send_inputs()

            # There should be one signal sent per iteration
            assert len(self.broadcaster.rudder_signals) == index + 1

            # The test outputs should match the expected values
            assert self.broadcaster.rudder_signals[index] == scaled_output

    def test_scale_trim(self):
        """Tests that the receiver reads and scales trim input correctly"""
        test_inputs = [-1, -0.5, 0, 0.5, 1]
        scaled_outputs = [-20, -5, 0, 5, 20]  # 20 * x^2

        for index, (test_input, scaled_output) in enumerate(zip(test_inputs, scaled_outputs)):
            # Set the return value
            self.r.pins["TRIM"].value = test_input

            self.r.send_inputs()

            # There should be one signal sent per iteration
            assert len(self.broadcaster.trim_signals) == index + 1

            # The test outputs should match the expected values
            assert self.broadcaster.trim_signals[index] == scaled_output

    def test_detect_mode(self):
        """Tests that the receiver reads and transforms mode input correctly"""
        self.r.send_inputs()

        # There should be one signal sent
        assert len(self.broadcaster.mode_signals) == 1

        # For now, the only mode is manual
        assert self.broadcaster.mode_signals[0] == NavigationMode.MANUAL


if __name__ == "__main__":
    unittest.main()
