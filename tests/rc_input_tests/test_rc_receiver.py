import unittest
from unittest.mock import MagicMock
from tests.mock_adc import Adafruit_BBIO
from src.rc_input.rc_receiver import make_rc_receiver, RC_READ_INTERVAL
from src.rc_input.rc_broadcasting import make_broadcaster
from time import sleep


class RCReceiverTests(unittest.TestCase):
    """Tests methods in RCReceiver"""

    def setUp(self):
        Adafruit_BBIO.ADC.setup = MagicMock(name='Adafruit_BBIO.ADC.setup')
        Adafruit_BBIO.ADC.read = MagicMock(name='Adafruit_BBIO.ADC.read')

    def test_listen(self):
        """Tests that the listen method queries the """
        r = make_rc_receiver(broadcaster=make_broadcaster())
        with r.listen():
            Adafruit_BBIO.ADC.setup.assert_called_with()
            sleep(RC_READ_INTERVAL * 1.1)  # Need to fudge it a little for it to work
            Adafruit_BBIO.ADC.read.assert_called_with('P0_5')


if __name__ == "__main__":
    unittest.main()
