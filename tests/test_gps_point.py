import unittest

from src.gps_point import GPSPoint


class GPSPointTests(unittest.TestCase):
    """Tests methods in GPS point"""
    def setUp(self):
        """Runs before each test case"""

    def test_bearing_from(self):
        """Tests the bearing_from method"""
        a = GPSPoint(lat=0, long=1)
        b = GPSPoint(1, 0)
        c = GPSPoint(0, -1)
        d = GPSPoint(-1, 0)
        o = GPSPoint(0, 0)
        self.assertAlmostEqual(90, a.bearing_from(o))
        self.assertAlmostEqual(0, b.bearing_from(o))
        self.assertAlmostEqual(270, c.bearing_from(o))
        self.assertAlmostEqual(180, d.bearing_from(o))

    def test_convert_to_bearing(self):
        """Tests the conversion from Cartesian angles to bearing"""
        self.assertAlmostEqual(0, GPSPoint.convert_to_bearing(90))
        self.assertAlmostEqual(90, GPSPoint.convert_to_bearing(0))
        self.assertAlmostEqual(180, GPSPoint.convert_to_bearing(-90))
        self.assertAlmostEqual(180, GPSPoint.convert_to_bearing(270))
        self.assertAlmostEqual(270, GPSPoint.convert_to_bearing(180))


if __name__ == "__main__":
    unittest.main()
