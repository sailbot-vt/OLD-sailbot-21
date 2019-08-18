import unittest

from src.airmar.nmeaparser.nmea_parser import NmeaParser


class NmeaTests(unittest.TestCase):
    """ Tests nmea parser package. """

    def setUp(self):
        """ Create testing fields """
        self.parser = NmeaParser()
    
    def test_parse(self):
        """ Tests nmea sentence parser """
        self.assertEqual(self.parser.parse("$test*14\r\n"), None)
        self.assertEqual(self.parser.parse("$test*16\r\n")[0], "test")
        
        expected = ["test", "1", "2", "3", None, "4"]
        self.assertEqual(self.parser.parse("$test,1,2,3,,4*3E\r\n"), expected)

    def test_toggle(self):
        """ Tests sentence id toggles """
        self.assertEqual(self.parser.toggle(sentence_ids=[]), [])
        expected = "$PAMTC,EN,ALL,0,1,,*00\r\n"
        self.assertEqual(self.parser.toggle(enable=0)[0], expected)
        expected = [
            "$PAMTC,EN,GGA,1,1,,*01\r\n",
            "$PAMTC,EN,VTG,1,1,,*05\r\n",
            "$PAMTC,EN,MWD,1,1,,*1E\r\n",
        ]
        ids = ["GGA", "VTG", "MWD"]
        self.assertEqual(self.parser.toggle(sentence_ids=ids), expected)

    def test_settings(self):
        """ Tests power, post, factory_reset sentences """
        self.assertEqual(self.parser.power(resume=1), "$PAMTX,1*4D\r\n")
        self.assertEqual(self.parser.power(resume=0), "$PAMTX,0*4C\r\n")
        self.assertEqual(self.parser.factory_reset(), "$PAMTC,EN,ERST*50\r\n")
        self.assertEqual(self.parser.post(), "$PAMTC,POST*7F\r\n")

    def test_checksum(self):
        """ Tests checksum function """
        self.assertEqual(self.parser.checksum("test"), "16")
