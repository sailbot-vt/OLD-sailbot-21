import unittest

from src.utils.coord_conv import cartesian_to_polar, polar_to_cartesian

class CoordConvTests(unittest.TestCase):
    """Tests the coord conversion functions"""
    
    def test_cartesian_to_polar(self):
        """Test to check correctness of cartesian to polar conversion"""
        in_values = [(0,0), (5, 5), (5, 0), (-5, 0), (0, 8), (-10,-10), (6.23, -41)]
        out_values = [(0,0), (7.07107, 45), (5, 0), (5, 180), (8, 90), (14.1421, -135), (41.4706, -81.359929)]

        for ((x, y), (rOut, thetaOut)) in list(zip(in_values, out_values)):
            r, theta = cartesian_to_polar(x, y)
            self.assertAlmostEqual(rOut, r, places=4)
            self.assertAlmostEqual(thetaOut, theta, places=4)

    def test_polar_to_cartesian(self):
        """Test to check correctness of polar to cartesian conversion"""
        in_values = [(0,0), (7.07107, 45), (0, 5), (5, 180), (8, 90), (14.1421, 225), (41.4706, -81.359929)]
        out_values = [(0,0), (5, 5), (0, 0), (-5, 0), (0, 8), (-10,-10), (6.23, -41)]

        for ((r, theta), (xOut, yOut)) in list(zip(in_values, out_values)):
            x, y = polar_to_cartesian(r, theta)
            self.assertAlmostEqual(xOut, x, places = 4)
            self.assertAlmostEqual(yOut, y, places = 4)
