import unittest
from unittest.mock import patch, MagicMock

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

from src.airmar.airmar_broadcaster import AirmarBroadcasterType

from src.airmar.airmar_input_thread import AirmarInputThread


class AirmarThreadTests(unittest.TestCase):
    """Integreation tests for AirmarInputThread"""

    def setUp(self):
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        serial.Serial.inWaiting = MagicMock(name='serial.Serial.inWaiting')
        serial.Serial.read = MagicMock(name='serial.Serial.read')
        serial.Serial.isOpen = MagicMock(name='serial.Serial.isOpen')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')

        self.airmar_input_thread = AirmarInputThread(
            mock_bbio=Adafruit_BBIO,
            mock_port=serial,
            broadcaster_type=AirmarBroadcasterType.Testable)

        self.broadcaster = self.airmar_input_thread.broadcaster

    def test_none(self):
        """ Tests that nothing is broadcasted when nothing is read. """
        self.airmar_input_thread.receiver.send_airmar_data()

        assert len(self.broadcaster.wind_speeds) == 0
        assert len(self.broadcaster.wind_heads) == 0
        assert len(self.broadcaster.boat_lats) == 0
        assert len(self.broadcaster.boat_longs) == 0
        assert len(self.broadcaster.boat_heads) == 0
        assert len(self.broadcaster.boat_speeds) == 0

    def test_wind(self):
        """ Tests that wind speed data was recorded """

        pass

    def test_boat_gps(self):
        """ Tests that boat latitudes and longitudes were recorded """
        sentence = "$GPGLL,3751.65,S,14507.36,E*77"
        # Lat: 49 deg. 16.45 min. South
        # Long 123 deg. 12.12 min. East
        serial.Serial.read = MagicMock(
            name='serial.Serial.read', return_value=sentence)

        self.airmar_input_thread.receiver.send_airmar_data()

        assert self.broadcaster.boat_lats[0] == 16.45
        assert self.broadcaster.boat_longs[0] == 12.12

    def test_boat_move(self):
        """ Tests that boat heading and speed were recorded """
        pass
