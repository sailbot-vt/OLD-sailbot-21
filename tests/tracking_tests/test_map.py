import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from src.tracking.map import Map
from src.tracking.object import Object
from src.tracking.classification_types import ObjectType

from src.utils.coord_conv import polar_to_cartesian, cartesian_to_polar
from src.gps_point import GPSPoint

import numpy as np
from pubsub import pub
from datetime import datetime as dt
import time

#TODO REMOVE
import pdb

class MapTests(unittest.TestCase):
    """Tests the methods in Map"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.boat = MagicMock(name="boat")
        self.boat_speed = 5
        self.boat.current_speed = MagicMock(name="current_speed", return_value=5)
        self.map = Map(self.boat, False)

    def test_clear_objects(self):
        """Tests clear objects method of map"""
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        start_time = dt.now()
        ii = 0
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            while (abs((dt.now() - start_time).total_seconds()) < .5):     # while less than 0.5s since last object
                pass

            pub.sendMessage("object detected", delta_x = x, delta_y = y, objectType=obj_type)
            start_time = dt.now()
            ii += 1
        
        self.assertTrue(len(self.map.object_list) == 2)                 # assert that length of list is two 

        while (abs(dt.now() - start_time).total_seconds() < .5):     # while less than 0.5s since last object
            pass

        self.map.clear_objects(timeSinceLastSeen=750)       # should only clear 2nd object
        self.assertTrue(len(self.map.object_list) == 1)                 # assert that length of list is only one
        self.map.clear_objects(timeSinceLastSeen=0)         # should only clear all objects
        self.assertTrue(len(self.map.object_list) == 0)                 # assert that length of list is zero

    def test_add_object(self):
        """Tests add object method of map"""
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        ii = 0
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("object detected", delta_x = x, delta_y = y, objectType=obj_type)
            rng, bearing = cartesian_to_polar(x, y)
            correct_object = Object(bearing, rng, None, None, None, objectType=obj_type)
            self.assertAlmostEqual(correct_object.bearing, self.map.object_list[ii].bearing)
            self.assertAlmostEqual(correct_object.rng, self.map.object_list[ii].rng)
            self.assertEqual(correct_object.objectType, self.map.object_list[ii].objectType)
            ii += 1

    def test_return_objects(self):
        """Tests return objects method of map"""
        # add objects to list
        # sweep across bearing range
        num_objects = 7
        delta_x_list = [0] * num_objects 
        delta_y_list = [0] * num_objects
        num_correct_objects = 0             # counter for correct objects
        timeRange = 5
        rngRange = (0, self.boat_speed * timeRange)
        bearingRange = (-30, 30)
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY, ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY, ObjectType.BOAT]

        # set up correct_object_list
        correct_object_list = [0] * num_objects     # create empty object list 

        for n in range(num_objects):
            rng = (n*6) + 3     # get range of ranges from 3 to 39
            bearing = (n*15) - 45   # get range of bearings from -45 to 45
            d_x, d_y = polar_to_cartesian(rng, bearing)
            delta_x_list[n] = d_x
            delta_y_list[n] = d_y
            if (rngRange[0] <= rng <= rngRange[1]) and (bearingRange[0] <= bearing <= bearingRange[1]):
                correct_object_list[num_correct_objects] = [rng, bearing, type_list[n]]
                num_correct_objects += 1
        
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("object detected", delta_x = x, delta_y = y, objectType=obj_type)

        returned_objects = self.map.return_objects()
        for jj, obj in enumerate(correct_object_list[0:num_correct_objects]):
            self.assertAlmostEqual(obj[0], returned_objects[jj].rng)
            self.assertAlmostEqual(obj[1], returned_objects[jj].bearing)
            self.assertEqual(obj[2], returned_objects[jj].objectType)

    @patch('src.tracking.map.Object.predict')
    def test_update_map(self, mock_predict):
        """Tests update map method"""
        # add objects to list 
        num_objects = 2
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("object detected", delta_x = x, delta_y = y, objectType=obj_type)

        # call update_map
        self.map.update_map()
        
        # check if predict was called for all objects in object_list
        self.assertEqual(mock_predict.call_count, num_objects)

    def test_get_buoys(self):
        """Tests get buoys method"""
        delta_x_list = [12.512, 44, 60]
        delta_y_list = [-22, 81.5, 60]
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY]
        correct_object_list = [0] * 2
        ii = 0
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("object detected", delta_x = x, delta_y = y, objectType=obj_type)
            rng, bearing = cartesian_to_polar(x, y)
            if obj_type == ObjectType.BUOY:
                correct_object_list[ii] = [rng, bearing, obj_type]
                ii += 1

        returned_objects = self.map.get_buoys()
        for jj, obj in enumerate(correct_object_list):
            self.assertAlmostEqual(obj[0], returned_objects[jj].rng)
            self.assertAlmostEqual(obj[1], returned_objects[jj].bearing)
            self.assertEqual(obj[2], returned_objects[jj].objectType)

if __name__ == "__main__":
        unittest.main()
