import unittest
from unittest.mock import MagicMock
from tests.mock_adc import Adafruit_BBIO
from src.rc_input.rc_receiver import make_rc_receiver, RC_READ_INTERVAL, RCReceiverType
from src.rc_input.rc_broadcaster import make_broadcaster, RCInputBroadcasterType
from time import sleep


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit_BBIO.ADC.setup')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read')
        self.broadcaster = make_broadcaster(RCInputBroadcasterType.Testable)
        self.r = make_rc_receiver(RCReceiverType.ADC, broadcaster=self.broadcaster)

    def test_listen(self):
        """Tests that the listen method queries the ADC pins correctly"""
        self.r.listen()
        Adafruit_BBIO.ADC.setup.assert_called()
        sleep(RC_READ_INTERVAL * 1.1)  # Need to fudge it a little for it to work
        Adafruit_BBIO.ADC.read.assert_called()

    def test_scale_rudder(self):
        """Tests that the receiver reads and scales rudder input correctly"""
        test_voltages = [0, 0.25, 0.5, 0.75, 1]
        scaled_outputs = [-80, -20, 0, 20, 80]  # 80 * x^2
        for index, (test_voltage, scaled_output) in enumerate(zip(test_voltages, scaled_outputs)):
            Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read', return_value=test_voltage)
            self.r.listen()
            sleep(RC_READ_INTERVAL * 1.1)
            assert self.broadcaster.rudder_signals[index] == scaled_output


    def test_scale_trim(self):
        """Tests that the receiver reads and scales rudder input correctly"""
        assert False

    def test_detect_mode(self):
        """Tests that the receiver reads and scales rudder input correctly"""
        assert False


if __name__ == "__main__":
    unittest.main()
