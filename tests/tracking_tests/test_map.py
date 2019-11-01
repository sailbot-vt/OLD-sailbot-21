import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.tracking.Map import Map
from src.tracking.Map import Object
from src.tracking.classification_types import ObjectType

class MapTests(unittest.TestCase):
    """Tests the methods in Map"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.boat = MagicMock(name="boat")
        self.Map = Map(self.boat)

    def test_cartesian_to_polar(self):
        """Test to check correctness of cartesian to polar conversion"""
        in_values = [(0,0), (5, 5), (5, 0), (-5, 0), (0, 8), (-10,-10), (6.23, -41)]
        out_values = [(0,0), (7.07107, 45), (0, 5), (180, 5), (90, 8), (-135, 14.1421), (-81.3599, 41.4706)]

        for ((x, y), (rOut, thetaOut)) in list(zip(in_values, out_values)):
            r, theta = self.Map.cartesian_to_polar(x, y)
            assertAlmostEqual(rOut, r, 4)
            assertAlmostEqual(thetaOut, theta, 4)

    def test_polar_to_cartesian(self):
        """Test to check correctness of polar to cartesian conversion"""
        in_values = [(0,0), (7.07107, 45), (0, 5), (180, 5), (90, 8), (-135, 14.1421), (-81.3599, 41.4706)]
        out_values = [(0,0), (5, 5), (5, 0), (-5, 0), (0, 8), (-10,-10), (6.23, -41)]

        for ((r, theta), (xOut, yOut)) in list(zip(in_values, out_values)):
            x, y = self.Map.cartesian_to_polar(r, theta)
            assertAlmostEqual(xOut, x, 4)
            assertAlmostEqual(yOut, y, 4)

    def test_add_object(self):
        """Tests add object method of map"""
        # clear object list to start with blank slate
        self.Map.clear_objects()
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        for ii, x, y, obj_type in enumerate(zip(delta_x_list, delta_y_list, type_list)):
            r, theta = self.Map.cartesian_to_polar(x, y)
            pub.sendMessage("buoy detected", delta_x = x, delta_y = y, objectType=obj_type)
            correctObject = Object(x, y, objectType=obj_type)
            assertEquals(correctObject, self.objectList[ii])



if __name__ == "__main__":
    unittest.main()
