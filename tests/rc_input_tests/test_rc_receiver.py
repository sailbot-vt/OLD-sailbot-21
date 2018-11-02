import unittest
from unittest.mock import MagicMock
from tests.mock_adc import Adafruit_BBIO
from src.rc_input.rc_receiver import make_rc_receiver, RCReceiverType
from src.rc_input.rc_broadcaster import make_broadcaster, RCInputBroadcasterType
from src.navigation_mode import NavigationMode


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit_BBIO.ADC.setup')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read')
        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Testable)
        self.r = make_rc_receiver(RCReceiverType.ADC, broadcaster=self.broadcaster)

    def tearDown(self):
        """Resets the receiver each test run"""
        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Testable)
        self.r = make_rc_receiver(RCReceiverType.ADC, broadcaster=self.broadcaster)

    def test_listen(self):
        """Tests that the listen method queries the ADC pins correctly"""
        self.r.read_input()
        Adafruit_BBIO.ADC.setup.assert_called()
        Adafruit_BBIO.ADC.read.assert_called()

    def test_scale_rudder(self):
        """Tests that the receiver reads and scales rudder input correctly"""
        test_voltages = [0, 0.25, 0.5, 0.75, 1]
        scaled_outputs = [-80, -20, 0, 20, 80]  # 80 * x^2
        for index, (test_voltage, scaled_output) in enumerate(zip(test_voltages, scaled_outputs)):
            Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read', return_value=test_voltage)
            self.r.read_input()
            assert len(self.broadcaster.rudder_signals) == index + 1
            assert self.broadcaster.rudder_signals[index] == scaled_output

    def test_scale_trim(self):
        """Tests that the receiver reads and scales trim input correctly"""
        test_voltages = [0, 0.25, 0.5, 0.75, 1]
        scaled_outputs = [-20, -5, 0, 5, 20]  # 20 * x^2
        for index, (test_voltage, scaled_output) in enumerate(zip(test_voltages, scaled_outputs)):
            Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read', return_value=test_voltage)
            self.r.read_input()
            assert len(self.broadcaster.trim_signals) == index + 1
            assert self.broadcaster.trim_signals[index] == scaled_output

    def test_detect_mode(self):
        """Tests that the receiver reads and transforms mode input correctly"""
        self.r.read_input()
        assert len(self.broadcaster.mode_signals) == 1
        assert self.broadcaster.mode_signals[0] == NavigationMode.MANUAL


if __name__ == "__main__":
    unittest.main()
