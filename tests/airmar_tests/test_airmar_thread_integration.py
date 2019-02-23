import unittest
from unittest.mock import patch, MagicMock

from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

from src.airmar.airmar_broadcaster import AirmarBroadcasterType

from src.airmar.airmar_input_thread import AirmarInputThread


class AirmarThreadTests(unittest.TestCase):
    """Integreation tests for AirmarInputThread"""

    def setUp(self):
        self.serial = serial.Serial
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
        serial.Serial.isOpen.return_value = False
        self.airmar_input_thread.receiver.send_airmar_data()

        serial.Serial.isOpen.return_value = True
        serial.Serial.read.return_value = "\r\n"
        self.airmar_input_thread.receiver.send_airmar_data()

        self.assertEquals(len(self.broadcaster.wind_speeds), 0)
        self.assertEquals(len(self.broadcaster.wind_heads), 0)
        self.assertEquals(len(self.broadcaster.boat_lats), 0)
        self.assertEquals(len(self.broadcaster.boat_longs), 0)
        self.assertEquals(len(self.broadcaster.boat_heads), 0)
        self.assertEquals(len(self.broadcaster.boat_speeds), 0)

    def test_wind(self):
        """ Tests that wind speed data was recorded """
        sentence = "$WIMWD,0.0,T,0.0,M,10.0,N,5.1,M\r\n"
        serial.Serial.read.return_value = sentence
        self.airmar_input_thread.receiver.send_airmar_data()
        
        xs = self.airmar_input_thread.receiver.processor.nmea_contents
        for x in xs:
            print(x)

        self.assertAlmostEqual(self.broadcaster.wind_heads[0], 0.0, 1)
        self.assertAlmostEqual(self.broadcaster.wind_speeds[0], 5.1, 1)

    def test_boat_gps(self):
        """ Tests that boat latitudes and longitudes were recorded """
        sentence = "$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76\r\n"
        serial.Serial.read.return_value = sentence
        self.airmar_input_thread.receiver.send_airmar_data()

        self.assertAlmostEqual(self.broadcaster.boat_lats[0], 53.36, 2)
        self.assertAlmostEqual(self.broadcaster.boat_longs[0], -6.5056, 2)

    def test_boat_move(self):
        """ Tests that boat heading and speed were recorded """
        sentence = "$GPVTG,360.0,T,348.7,M,000.0,N,000.0,K*43\r\n"
        serial.Serial.read.return_value = sentence
        self.airmar_input_thread.receiver.send_airmar_data()

        self.assertEqual(self.broadcaster.boat_heads[0], 0.0)
        self.assertEqual(self.broadcaster.boat_speeds[0], 0.0)
