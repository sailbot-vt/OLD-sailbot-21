import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.tracking.Map import Map
from src.tracking.Map import Object
from src.tracking.classification_types import ObjectType
from src.tracking.object_dtypes import buoy_array_dtype, object_array_dtype

from src.gps_point import GPSPoint
from pubsub import pub
from datetime import datetime as dt
import time

class MapTests(unittest.TestCase):
    """Tests the methods in Map"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.boat = MagicMock(name="boat")
        self.boat_speed = 5
        self.boat.current_speed = MagicMock(name="current_speed", returns=5)
        self.Map = Map(self.boat, False)

    def test_cartesian_to_polar(self):
        """Test to check correctness of cartesian to polar conversion"""
        in_values = [(0,0), (5, 5), (5, 0), (-5, 0), (0, 8), (-10,-10), (6.23, -41)]
        out_values = [(0,0), (7.07107, 45), (0, 5), (180, 5), (90, 8), (-135, 14.1421), (-81.3599, 41.4706)]

        for ((x, y), (rOut, thetaOut)) in list(zip(in_values, out_values)):
            r, theta = self.Map.cartesian_to_polar(x, y)
            unittest.TestCase.assertAlmostEqual(self, first=rOut, second=r, delta = 4)
            unittest.TestCase.assertAlmostEqual(self, first =thetaOut, second = theta, delta=.2)

    def test_polar_to_cartesian(self):
        """Test to check correctness of polar to cartesian conversion"""
        in_values = [(0,0), (7.07107, 45), (0, 5), (180, 5), (90, 8), (-135, 14.1421), (-81.3599, 41.4706)]
        out_values = [(0,0), (5, 5), (5, 0), (-5, 0), (0, 8), (-10,-10), (6.23, -41)]

        for ((r, theta), (xOut, yOut)) in list(zip(in_values, out_values)):
            x, y = self.Map.polar_to_cartesian(theta, r)
            unittest.TestCase.assertAlmostEqual(self, first = xOut, second = x, delta = .2)
            unittest.TestCase.assertAlmostEqual(self, first = yOut, second = y, delta = .2)

    def test_clear_objects(self):
        """Tests clear objects method of map"""
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        start_time = dt.now()
        ii = 0
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            #while (abs((dt.now() - start_time).total_seconds()) < .5):     # while less than 0.5s since last object
             #   pass
            #time.sleep(0.5)

            pub.sendMessage("buoy detected", delta_x = x, delta_y = y, objectType=obj_type)
            start_time = dt.now()
            ii += 1
        
        self.assertTrue(len(self.Map.objectList) == 2)                 # assert that length of list is two 
        while ((dt.now() - start_time) < 500):     # while less than 0.5s since last object
            pass
        self.Map.clear_objects(timeSinceLastSeen=750)       # should only clear 2nd object
        self.assertTrue(len(self.map.objectlist) == 1)                 # assert that length of list is only one
        self.Map.clear_objects(timeSinceLastSeen=0)         # should only clear all objects
        self.assertTrue(len(self.map.objectlist) == 0)                 # assert that length of list is zero

    def test_add_object(self):
        """Tests add object method of map"""
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        ii = 0
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):

            pub.sendMessage("buoy detected", delta_x = x, delta_y = y, objectType=obj_type)
            bearing, dist = self.Map.cartesian_to_polar(x, y)
            correctObject = Object(bearing, dist, None, None, None, objectType=obj_type)
            unittest.TestCase.assertAlmostEquals(self, first = correctObject.bearing, second = self.Map.objectList[ii].bearing, delta =.1)
            unittest.TestCase.assertEqual(self, first=correctObject, second=self.Map.objectList[ii])
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

        for n in range(num_objects):
            rng = (n*6) + 3     # get range of ranges from 3 to 39
            bearing = (n*15) - 45   # get range of bearings from -45 to 45
            d_x, d_y = self.Map.polar_to_cartesian(bearing, rng)
            delta_x_list[n] = d_x
            delta_y_list[n] = d_y
            if (rng < rngRange[1]) and (abs(bearing) < bearingRange[1]):
                num_correct_objects += 1

        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        correct_object_list = [0] * num_correct_objects
        ii = 0
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("buoy detected", delta_x = x, delta_y = y, objectType=obj_type)
            bearing, dist = self.Map.cartesian_to_polar(x, y)
            correctObject = Object(bearing, dist, None, None, None, objectType=obj_type)
            correct_object_list[ii] = correctObject
            ii += 1
        returned_objects = self.Map.return_objects()
        for ii, correct_obj in enumerate(correct_object_list):
            self.assertTrue([correct_obj.range, correct_obj.bearing, correct_obj.objectType] == returned_objects[ii])

    def test_update_map(self):
        """Tests update map method"""
        # add objects to list 
        delta_x_list = [12.512, 44]
        delta_y_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        correct_object_list = [0] * 2
        ii = 0
        for  x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("buoy detected", delta_x = x, delta_y = y, objectType=obj_type)
            bearing, dist = self.Map.cartesian_to_polar(x, y)
            correctObject = Object(bearing, dist, None, None, None, objectType=obj_type)
            correct_object_list[ii] = correctObject
            ii += 1

        # set boat's current position and old position
        cur_pos = GPSPoint(0, 0)
        delta_x = 5
        delta_y = 5
        self.Map.old_position = GPSPoint(0,0)
        cur_pos.lat += delta_x
        cur_pos.long += delta_y
        self.boat.current_position = MagicMock("self.boat.current_position", returns=cur_pos)
        
        # update map
        self.Map.updateMap()
        for ii, obj in enumerate(self.Map.objectList):
            obj_x, obj_y = self.polar_to_cartesian(obj.bearing, obj.range)
            self.assertTrue(delta_x_list[ii] - obj_x == delta_x)
            self.assertTrue(delta_y_list[ii] - obj_y == delta_y)

    def test_get_buoys(self):
        """Tests get buoys method"""
        delta_x_list = [12.512, 44, 60]
        delta_y_list = [-22, 81.5, 60]
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY]
        correct_object_list = []
        for x, y, obj_type in zip(delta_x_list, delta_y_list, type_list):
            pub.sendMessage("buoy detected", delta_x = x, delta_y = y, objectType=obj_type)
            bearing, rng = self.cartesian_to_polar(x, y)
            if obj_type == ObjectType.BUOY:
                correct_object_list = correct_object_list.append(Object(bearing=bearing, range=rng, objectType=obj_type))
        for obj in self.Map.objectList:
            self.assertTrue(obj in correct_obj_list)

if __name__ == "__main__":
        unittest.main()
