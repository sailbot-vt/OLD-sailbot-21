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

    def _make_nmea_sentence(self, sentence):
        """ Helper function to create custom nmea sentences 
        
        Keyword Arguments:
        sentence -- The nmea sentence body to create nmea sentence from.

        Returns:
        A properly formatted NMEA sentence with checksum.
        """
        return "$" + sentence + "*{}\r\n".format(self.parser.checksum(sentence))

    def test_update_sentence_gpdtm(self):
        """ Tests format fields """
        data = {} # initialize raw data

        # Test GPDTM sentences
        sentence = "GPDTM,W84,,100.001,N,200.001,E,10,W84"
        sentence = self._make_nmea_sentence(sentence=sentence)

        fields = self.parser.parse(sentence=sentence)
        self.parser.update_data(data=data, fields=fields)

        self.assertEqual(data["GPDTM"]["local_datum_code"], "W84")
        self.assertEqual(data["GPDTM"]["subdivision_datum_code"], None)
        self.assertEqual(data["GPDTM"]["latitude_offset"], "100.001")
        self.assertEqual(data["GPDTM"]["latitiude_cardinality"], "N")
        self.assertEqual(data["GPDTM"]["longitude_offset"], "200.001")
        self.assertEqual(data["GPDTM"]["longitude_cardinality"], "E")
        self.assertEqual(data["GPDTM"]["altitude_offset"], "10")
        self.assertEqual(data["GPDTM"]["reference_datum_code"], "W84")

    def test_update_sentence_gpgga(self):
        # Test GPGGA sentences
        data = {}
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"

        fields = self.parser.parse(sentence=sentence)
        self.parser.update_data(data=data, fields=fields)

        self.assertEqual(data["GPGGA"]["utc_position"], "123519")
        self.assertEqual(data["GPGGA"]["latitude"], "4807.038")
        self.assertEqual(data["GPGGA"]["latitude_cardinality"], "N")
        self.assertEqual(data["GPGGA"]["longitude"], "01131.000")
        self.assertEqual(data["GPGGA"]["longitude_cardinality"], "E")
        self.assertEqual(data["GPGGA"]["gps_quality_indicator"], "1")
        self.assertEqual(data["GPGGA"]["number_satelites"], "08")
        self.assertEqual(data["GPGGA"]["hdop"], "0.9")
        self.assertEqual(data["GPGGA"]["geoid"], "545.4")
        self.assertEqual(data["GPGGA"]["geiodal_separation"], "46.9")
        self.assertEqual(data["GPGGA"]["age_of_differential_gps_data"], None)
        self.assertEqual(data["GPGGA"]["differential_reference_station_id"], None)

    def test_update_sentence_wimwd(self):
        data = {}
        sentence = "WIMWD,359.9,T,359.9,M,10.1,N,19.1,M"
        sentence = self._make_nmea_sentence(sentence=sentence)

        fields = self.parser.parse(sentence=sentence)
        self.parser.update_data(data=data, fields=fields)

        self.assertEqual(data["WIMWD"]["wind_direction_true"], "359.9")
        self.assertEqual(data["WIMWD"]["wind_direction_magnetic"], "359.9")
        self.assertEqual(data["WIMWD"]["wind_speed_knots"], "10.1")
        self.assertEqual(data["WIMWD"]["wind_speed_mps"], "19.1")

    def test_update_sentence_gpvtg(self):
        data = {}
        sentence = "GPVTG,054.7,T,034.4,M,005.5,N,010.2,K,A"
        sentence = self._make_nmea_sentence(sentence=sentence)

        fields = self.parser.parse(sentence=sentence)
        self.parser.update_data(data=data, fields=fields)

        self.assertEqual(data["GPVTG"]["course_over_ground_true"], "054.7")
        self.assertEqual(data["GPVTG"]["course_over_ground_magnetic"], "034.4")
        self.assertEqual(data["GPVTG"]["speed_over_ground_knots"], "005.5")
        self.assertEqual(data["GPVTG"]["speed_over_ground_kph"], "010.2")
        self.assertEqual(data["GPVTG"]["mode_indicator"], "A")

    def test_update_sentence_wivwr(self):
        data = {}
        sentence = "WIVWR,010.1,L,020.2,N,10.1,M,10.2,K"
        sentence = self._make_nmea_sentence(sentence=sentence)
        
        fields = self.parser.parse(sentence=sentence)
        self.parser.update_data(data=data, fields=fields)

        self.assertEqual(data["WIVWR"]["wind_angle_degree"], "010.1")
        self.assertEqual(data["WIVWR"]["wind_angle_direction"], "L")
        self.assertEqual(data["WIVWR"]["wind_speed_knots"], "020.2")
        self.assertEqual(data["WIVWR"]["wind_speed_mps"], "10.1")
        self.assertEqual(data["WIVWR"]["wind_speed_kph"], "10.2")

    def test_update_sentence_wivwt(self):
        data = {}
        sentence = "WIVWT,0,L,1,N,2,M,3,K"
        sentence = self._make_nmea_sentence(sentence=sentence)

        fields = self.parser.parse(sentence=sentence)
        self.parser.update_data(data=data, fields=fields)

        self.assertEqual(data["WIVWT"]["wind_angle_degree"], "0")
        self.assertEqual(data["WIVWT"]["wind_angle_direction"], "L")
        self.assertEqual(data["WIVWT"]["wind_speed_knots"], "1")
        self.assertEqual(data["WIVWT"]["wind_speed_mps"], "2")
        self.assertEqual(data["WIVWT"]["wind_speed_kph"], "3")