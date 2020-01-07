import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from src.tracking.map import Map
from src.tracking.object import Object
from src.tracking.classification_types import ObjectType

from src.utils.time_in_millis import time_in_millis
from src.gps_point import GPSPoint

import numpy as np
from pubsub import pub
from datetime import datetime as dt
import time

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
        # set up objects to add to list (arbitrary values)
        rng_list = [12.512, 44]
        bearing_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]

        # add objects to object list 0.05s apart
        start_time = dt.now()
        for ii, (rng, bearing, obj_type) in enumerate(zip(rng_list, bearing_list, type_list)):
            while (abs((dt.now() - start_time).total_seconds()) < .05):     # while less than 0.05s since last object
                pass

            obj = Object(bearing, rng, time_in_millis(), objectType = obj_type)
            self.map.object_list.append(obj)
            start_time = dt.now()
        
        self.assertTrue(len(self.map.object_list) == 2)                 # assert that length of list is two 

        while (abs(dt.now() - start_time).total_seconds() < .05):     # while less than 0.05s since last object
            pass

        self.map.clear_objects(timeSinceLastSeen=75)       # should only clear 2nd object
        self.assertTrue(len(self.map.object_list) == 1)                 # assert that length of list is only one
        self.map.clear_objects(timeSinceLastSeen=0)         # should only clear all objects
        self.assertTrue(len(self.map.object_list) == 0)                 # assert that length of list is zero

    def test_return_objects(self):
        """Tests return objects method of map"""
        # set up objects to add to map
        timeRange = 5000                                       # time used to create rngRange 
        rngRange = (0, self.boat_speed * (timeRange/1000))     # range of ranges to return
        bearingRange = (-30, 30)                        # range of bearings to return
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY, 
                     ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY, ObjectType.NONE]    # object types

        # set up object 
        num_objects = 7
        correct_object_list = [0] * num_objects     # create empty object list 
        num_correct_objects = 0             # counter for correct objects

        # loop over objects to create
        for n in range(num_objects):
            rng = (n*6) + 3     # get range in range from 3 to 39
            bearing = (n*15) - 45   # get bearing in range from -45 to 45

            # add object to correct object list if with rngRange and bearingRange
            if (rngRange[0] <= rng <= rngRange[1]) and (bearingRange[0] <= bearing <= bearingRange[1]):
                correct_object_list[num_correct_objects] = [rng, bearing, type_list[n]]
                num_correct_objects += 1
        
            # add object to map
            obj = Object(bearing, rng, time_in_millis(), objectType = type_list[n])
            self.map.object_list.append(obj)

        # get list of objects meeting conditions
        returned_objects = self.map.return_objects(bearingRange, rngRange=rngRange)

        # check that objects match
        for jj, obj in enumerate(correct_object_list[0:num_correct_objects]):
            self.assertAlmostEqual(obj[0], returned_objects[jj].rng)
            self.assertAlmostEqual(obj[1], returned_objects[jj].bearing)
            self.assertEqual(obj[2], returned_objects[jj].objectType)

    @patch('src.tracking.map.Object.predict')
    def test_update_map(self, mock_predict):
        """Tests update map method"""
        # add objects to list 
        num_objects = 2
        rng_list = [12.512, 44]
        bearing_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        
        for ii, (rng, bearing, obj_type) in enumerate(zip(rng_list, bearing_list, type_list)):
            obj = Object(bearing, rng, time_in_millis(), objectType = obj_type)
            self.map.object_list.append(obj)

        # call update_map
        self.map.update_map()
        
        # check if predict was called for all objects in object_list
        self.assertEqual(mock_predict.call_count, num_objects)

    def test_smooth_frame(self):
        """Tests smooth frame method"""
        # create objects to add to map
        rng_list = [12.512, 44, 50]
        bearing_list = [-22, 81.5, 2]
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY]

        # loop through objects and add to map
        for rng, bearing, obj_type in zip(rng_list, bearing_list, type_list):
            obj = Object(bearing, rng, time_in_millis(), objectType = obj_type)
            self.map.object_list.append(obj)

        # create detections/observations to add to epoch frame
        num_detects = 3
        rng_list = [12, 44, 25]
        bearing_list = [-21.5, 81.5, 5]
        type_list = [ObjectType.BUOY, ObjectType.NONE, ObjectType.BUOY]
        dets_used = [1, 1, 0]

        epoch_frame = [0] * num_detects
        frame_bounds = ([0, 150], [-85, 85])        # excludes last object in object list from being included in update

        for ii, (rng, bearing, obj_type) in enumerate(zip(rng_list, bearing_list, type_list)):
            epoch_frame[ii] = [rng, bearing, obj_type]

        with patch('src.tracking.map.pdaf', return_value = ((0, 0), dets_used)) as mock_pdaf, \
             patch('src.tracking.map.Object.update') as mock_update, \
             patch('src.tracking.map.Map._generate_obj_gate', return_value = 0), \
             patch('src.tracking.map.Object.__init__', return_value = None) as mock_obj_init, \
             patch('src.tracking.map.time_in_millis', return_value = 1):
            # call smooth_frame
            self.map.smooth_frame(epoch_frame, frame_bounds)

            # check that update is called correct amount of times
            self.assertEqual(num_detects, mock_update.call_count)

            # check that new object is created for final detection
            new_obj_idx = 2
            self.assertEqual((bearing_list[new_obj_idx], rng_list[new_obj_idx], 1), mock_obj_init.call_args[0])
            self.assertEqual({'objectType': type_list[new_obj_idx]}, mock_obj_init.call_args[1])

    def test_generate_obj_gate(self):
        """Tests generate obj gate method"""
        # generate test object parameters 
        num_objects = 3
        rng_list, bearing_list, obj_type_list = [5, 12, 40], [45, 0, -20], [ObjectType.BOAT, ObjectType.NONE, ObjectType.BUOY]
        obj_list = [0] * num_objects

        # initialize truthed gates
        truth_rng_gates = [0] * num_objects
        truth_bearing_gates = [0] * num_objects
        truth_type_gates = [0] * num_objects

        # create objects and set up truth gates
        for ii in range(num_objects):
            obj_list[ii] = Object(bearing_list[ii], rng_list[ii], time_in_millis(), objectType=obj_type_list[ii])
            obj_list[ii].kalman.covar = np.eye(4)
            truth_rng_gates[ii] = (rng_list[ii] - 1, rng_list[ii] + 1)
            truth_bearing_gates[ii] = (bearing_list[ii] - 1, bearing_list[ii] + 1)
            truth_type_gates[ii] = (ObjectType.NONE, obj_type_list[ii])

        # compare truth gates to generated gates
        truth_gates = [*zip(truth_rng_gates, truth_bearing_gates, truth_type_gates)]
        for jj, obj in enumerate(obj_list):
            gate = self.map._generate_obj_gate(obj)
            self.assertEqual(truth_gates[jj], gate)

    def test_get_buoys(self):
        """Tests get buoys method"""
        # create objects to add to map
        rng_list = [12.512, 44, 50]
        bearing_list = [-22, 81.5, 2]
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY]

        # set up correct object list 
        correct_object_list = [0] * 2
        num_correct_objects = 0

        # loop through objects and add to map
        for rng, bearing, obj_type in zip(rng_list, bearing_list, type_list):
            obj = Object(bearing, rng, time_in_millis(), objectType = obj_type)
            self.map.object_list.append(obj)

            # add object to correct object list if is buoy
            if obj_type == ObjectType.BUOY:
                correct_object_list[num_correct_objects] = [rng, bearing, obj_type]
                num_correct_objects += 1

        # get list of objects from get_buoys
        returned_objects = self.map.get_buoys()

        # check if objects map correct object list
        for jj, obj in enumerate(correct_object_list):
            self.assertAlmostEqual(obj[0], returned_objects[jj].rng)
            self.assertAlmostEqual(obj[1], returned_objects[jj].bearing)
            self.assertEqual(obj[2], returned_objects[jj].objectType)
