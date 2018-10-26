import unittest
from tests.mock_adc import Adafruit_BBIO
from src.rc_input.rc_receiver import make_rc_receiver, RCReceiverType


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def test_listen(self):
        """Tests that the listen method queries the """
        r = make_rc_receiver(RCReceiverType.ADC)
        with r.listen():
            Adafruit_BBIO.ADC.setup.assert_called_with()


if __name__ == "__main__":
    unittest.main()
