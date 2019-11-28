import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.airmar.airmar_input_thread import AirmarInputThread
from src.broadcaster.broadcaster import BroadcasterType
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

class AirmarIntegrationTests(unittest.TestCase):
    """ Tests airmar program """

    def setUp(self):
        """ Initialize testing objects """
        self.thread = AirmarInputThread(
            mock_bbio=Adafruit_BBIO, 
            mock_port=serial)

        # Make mock of serial input + pubsub

    def test_update_true_wind(self):
        # WIVWT
        pass

    def test_update_rel_wind(self):
        # WIVWR
        pass

    def test_update_boat_gps(self):
        pass

    def test_update_boat_speed(self):
        pass