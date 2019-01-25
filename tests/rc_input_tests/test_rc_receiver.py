import unittest
from unittest.mock import MagicMock
from tests.mock_bbio import Adafruit_BBIO

from src.rc_input.pin_config_reader import read_pin_config
from src.rc_input.rc_receiver import RCReceiver, BBB_MAX_INPUT_VOLTAGE
from src.rc_input.rc_broadcaster import make_broadcaster, RCInputBroadcasterType
from src.navigation_mode import NavigationMode


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit_BBIO.ADC.setup')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read')
        Adafruit_BBIO.GPIO.setup = MagicMock(name='Adafruit.BBIO.GPIO.setup')
        Adafruit_BBIO.GPIO.input = MagicMock(name='Adafruit.BBIO.GPIO.input')
        Adafruit_BBIO.GPIO.IN = MagicMock(name='Adafruit.BBIO.GPIO.IN')
        Adafruit_BBIO.GPIO.OUT = MagicMock(name='Adafruit.BBIO.GPIO.OUT')

        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Testable)
        self.r = RCReceiver(broadcaster=self.broadcaster, pins=read_pin_config())

    def tearDown(self):
        """Resets the receiver each test run"""
        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Testable)
        self.r = RCReceiver(broadcaster=self.broadcaster, pins=read_pin_config())

    def test_read_input(self):
        """Tests that the read_input method queries the ADC pins correctly.

        This test partially duplicates ones further down, but could help pinpoint issues."""
        self.r.read_input()

        Adafruit_BBIO.ADC.setup.assert_called()
        Adafruit_BBIO.ADC.read.assert_called()

        Adafruit_BBIO.GPIO.setup.assert_called()
        Adafruit_BBIO.GPIO.input.assert_called()

    def test_scale_rudder(self):
        """Tests that the receiver reads and scales rudder input correctly"""
        test_min = self.r.pins["RUDDER"].min_v
        test_max = self.r.pins["RUDDER"].max_v
        test_med = self.r.pins["RUDDER"].default_v
        test_voltages = [
            test_min,
            (test_med + test_min) * 0.5,
            test_med,
            (test_max + test_med) * 0.5,
            test_max
        ]  # Quintiles
        test_voltages = [v / BBB_MAX_INPUT_VOLTAGE for v in test_voltages]  # Scale to [0, 1]
        scaled_outputs = [
            -80,
            -20,
            0,
            20,
            80
        ]  # 80 * x^2

        for index, (test_voltage, scaled_output) in enumerate(zip(test_voltages, scaled_outputs)):
            # Mock Adafruit_BBIO.ADC.read() method with the correct return value
            Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read', return_value=test_voltage)

            self.r.read_input()

            # There should be one signal sent per iteration
            assert len(self.broadcaster.rudder_signals) == index + 1

            # The test outputs should match the expected values
            assert abs(self.broadcaster.rudder_signals[index] - scaled_output) < 3

    def test_scale_trim(self):
        """Tests that the receiver reads and scales trim input correctly"""
        test_min = self.r.pins["TRIM"].min_v
        test_max = self.r.pins["TRIM"].max_v
        test_med = self.r.pins["TRIM"].default_v
        test_voltages = [
            test_min,
            (test_med + test_min) * 0.5,
            test_med,
            (test_max + test_med) * 0.5,
            test_max
        ]  # Quintiles
        test_voltages = [v / BBB_MAX_INPUT_VOLTAGE for v in test_voltages]  # Scale to [0, 1]
        scaled_outputs = [
            -20,
            -5,
            0,
            5,
            20
        ]  # 80 * x^2

        for index, (test_voltage, scaled_output) in enumerate(zip(test_voltages, scaled_outputs)):
            # Mock Adafruit_BBIO.ADC.read() method with the correct return value
            Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read', return_value=test_voltage)

            self.r.read_input()

            # There should be one signal sent per iteration
            assert len(self.broadcaster.trim_signals) == index + 1

            # The test outputs should match the expected values
            assert abs(self.broadcaster.trim_signals[index] - scaled_output) < 1

    def test_detect_mode(self):
        """Tests that the receiver reads and transforms mode input correctly"""
        self.r.read_input()

        # There should be one signal sent per iteration
        assert len(self.broadcaster.mode_signals) == 1

        # The test outputs should match the expected values
        assert self.broadcaster.mode_signals[0] == NavigationMode.MANUAL


if __name__ == "__main__":
    unittest.main()
