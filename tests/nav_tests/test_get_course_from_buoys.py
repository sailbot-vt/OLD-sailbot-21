import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import numpy as np
from src.tracking.classification_types import ObjectType

from src.nav.get_course_from_buoys import get_course_from_buoys 

class BuoySortTests(unittest.TestCase):
    """Tests the method get_course_from_buoys"""
    def setUp(self):
        pass

    def test_get_course_from_buoys(self):
        # make buoy arrays
        test_arr_1 = np.array([(80., 60.), (50., 3.), (100., 135.), (60., 177.)])     # tests standard, 4 buoys, CCW navigation w/ boat outside of bounding box -- example of endurance race
        return_arr_1 = np.array([(50., 3.), (80., 60.), (100., 135.), (60., 177.)])

        test_arr_2 = np.array([(20., 165.), (20., 15.), (60., 90.)])     # tests standard, 3 buoys, CCW navigation w/ boat outside of bounding box -- example of fleet race
        return_arr_2 = np.array([(20., 15.), (60., 90.), (20., 165.)])

        test_arr_3 = np.array([(80., 60.), (50., 357.), (100., 135.), (60., 183.)])     # tests standard, 4 buoys, CCW navigation w/ boat INSIDE of bounding box -- example of endurance race if we screw up our path
        return_arr_3 = np.array([(50., 357.), (80., 60.), (100., 135.), (60., 183.)])
        
        self.assertTrue(np.array_equal(return_arr_1, get_course_from_buoys(test_arr_1, "CCW")))
        self.assertTrue(np.array_equal(return_arr_2, get_course_from_buoys(test_arr_2, "CCW")))
        self.assertTrue(np.array_equal(return_arr_3, get_course_from_buoys(test_arr_3, "CCW")))
