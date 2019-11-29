import itertools
import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.airmar.airmar_input_thread import AirmarInputThread
from src.airmar.nmeaparser.nmea_parser import NmeaParser
from src.broadcaster.broadcaster import BroadcasterType
from tests.mock_bbio import Adafruit_BBIO
from tests.mock_port import serial

class AirmarIntegrationTests(unittest.TestCase):
    """ Tests airmar program """

    def setUp(self):
        """ Initialize testing objects """
        self.thread = AirmarInputThread(
            mock_bbio=Adafruit_BBIO, 
            mock_port=serial.Serial,
            broadcaster_type=BroadcasterType.Testable)

        self.broadcaster = self.thread.broadcaster

        # Make mock of serial
        serial.Serial.isOpen = MagicMock(name="serial.Serial.isOpen",
                                    return_value=True)
        serial.Serial.open = MagicMock(name='serial.Serial.open')
        serial.Serial.close = MagicMock(name='serial.Serial.close')
        Adafruit_BBIO.UART.setup = MagicMock(name='Adafruit_BBIO.UART.setup')
        self.parser = NmeaParser()

    def _make_nmea_sentence(self, sentence):
        """ Helper function to create custom nmea sentences 
        
        Keyword Arguments:
        sentence -- The nmea sentence body to create nmea sentence from.

        Returns:
        A properly formatted NMEA sentence with checksum.
        """
        return "$" + sentence + "*{}\r\n".format(self.parser.checksum(sentence))

    def test_update_true_wind(self):
        """ Tests that airmar thread reads WIVWT sentences
            correctly. (WIVWT - True Wind) """
        # WIVWT,wind_angle, L, knots, N, mps, M, kmh, K
        test_inputs = []
        sentence = "WIVWT,0,L,,N,10,M,,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        sentence = "WIVWT,0,L,,N,10,M,,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        sentence = "WIVWT,2,R,,N,10,M,,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        serial.Serial.inWaiting = MagicMock(name="serial.Serial.inWaiting",
            return_value=len(b''.join(test_inputs)))
        serial.Serial.read = MagicMock(name="serial.Serial.read")
        serial.Serial.read.side_effect = itertools.chain(test_inputs, 
            itertools.repeat(b'')
        )

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(10, self.broadcaster.data["wind speed true"], 2)
        self.assertAlmostEqual(0, self.broadcaster.data["wind angle true"], 2)

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(10, self.broadcaster.data["wind speed true"], 2)
        self.assertAlmostEqual(0, self.broadcaster.data["wind angle true"], 2)

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(6.365, self.broadcaster.data["wind speed true"], 2)
        self.assertAlmostEqual(25.374, self.broadcaster.data["wind angle true"], 2)

    def test_update_rel_wind(self):
        # WIVWR
        test_inputs = []
        sentence = "WIVWR,0,L,,N,10,M,,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        sentence = "WIVWR,0,L,,N,10,M,,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        sentence = "WIVWR,2,R,,N,10,M,,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        serial.Serial.inWaiting = MagicMock(name="serial.Serial.inWaiting",
            return_value=len(b''.join(test_inputs)))
        serial.Serial.read = MagicMock(name="serial.Serial.read")
        serial.Serial.read.side_effect = itertools.chain(test_inputs, 
            itertools.repeat(b'')
        )

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(10, self.broadcaster.data["wind speed apparent"], 2)
        self.assertAlmostEqual(0, self.broadcaster.data["wind angle apparent"], 2)

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(10, self.broadcaster.data["wind speed apparent"], 2)
        self.assertAlmostEqual(0, self.broadcaster.data["wind angle apparent"], 2)

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(6.365, self.broadcaster.data["wind speed apparent"], 2)
        self.assertAlmostEqual(25.374, self.broadcaster.data["wind angle apparent"], 2)

    def test_update_boat_gps(self):
        # GPGGA
        test_inputs = []
        sentence = "GPGGA,,1,N,2,E,,,,,,,,,"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        serial.Serial.inWaiting = MagicMock(name="serial.Serial.inWaiting",
            return_value=len(b''.join(test_inputs)))
        serial.Serial.read = MagicMock(name="serial.Serial.read")
        serial.Serial.read.side_effect = itertools.chain(test_inputs, 
            itertools.repeat(b'')
        )

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(1, self.broadcaster.data["boat latitude"], 2)
        self.assertAlmostEqual(2, self.broadcaster.data["boat longitude"], 2)

    def test_update_boat_speed(self):
        # GPVTG
        test_inputs = []
        sentence = "GPVTG,1,T,2,M,,N,2,,"
        sentence = self._make_nmea_sentence(sentence=sentence)
        test_inputs.append(str.encode(sentence, encoding="UTF-8"))

        serial.Serial.inWaiting = MagicMock(name="serial.Serial.inWaiting",
            return_value=len(b''.join(test_inputs)))
        serial.Serial.read = MagicMock(name="serial.Serial.read")
        serial.Serial.read.side_effect = itertools.chain(test_inputs, 
            itertools.repeat(b'')
        )

        self.thread.receiver.send_airmar_data()
        self.assertAlmostEqual(1, self.broadcaster.data["boat heading"], 2)
        self.assertAlmostEqual(2, self.broadcaster.data["boat speed"], 2)
