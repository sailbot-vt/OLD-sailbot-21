import unittest
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from src.tracking.map import Map
from src.tracking.classification_types import ObjectType

from pubsub import pub
from datetime import datetime as dt


class MapTests(unittest.TestCase):
    """Tests the methods in Map"""
    def setUp(self):
        """Sets up the objects needed for testing"""
        self.boat = MagicMock(name="boat")
        self.boat_speed = 5
        self.boat.current_speed = MagicMock(name="current_speed", return_value=5)
        self.map = Map(self.boat, False)

    @patch('src.tracking.map.Map._find_object_in_map', return_value = None)
    def test_clear_objects(self, mock_find_obj):
        """Tests clear objects method of map"""
        # set up objects to add to list (arbitrary values)
        rng_list = [5, 44]
        bearing_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]

        # add objects to object list 0.05s apart
        start_time = dt.now()
        for ii, (rng, bearing, obj_type) in enumerate(zip(rng_list, bearing_list, type_list)):
            while (abs((dt.now() - start_time).total_seconds()) < .05):     # while less than 0.05s since last object
                pass

            pub.sendMessage("object detected", rng=rng, bearing=bearing, objectType=obj_type)
            start_time = dt.now()

        self.assertTrue(len(self.map.object_list) == 2)                 # assert that length of list is two

        while (abs(dt.now() - start_time).total_seconds() < .05):     # while less than 0.05s since last object
            pass

        self.map.clear_objects(timeSinceLastSeen=75)       # should only clear 2nd object
        self.assertTrue(len(self.map.object_list) == 1)                 # assert that length of list is only one
        self.map.clear_objects(timeSinceLastSeen=0)         # should only clear all objects
        self.assertTrue(len(self.map.object_list) == 0)                 # assert that length of list is zero

    @patch('src.tracking.map.Object.predict')
    def test_add_object(self, mock_predict):
        """Tests add object method of map"""
        # set up objects to add to list (arbitrary values)
        rng_list = [5, 44]
        bearing_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]

        # loop through objects to add
        for ii, (rng, bearing, obj_type) in enumerate(zip(rng_list, bearing_list, type_list)):
            # add object
            pub.sendMessage("object detected", rng=rng, bearing=bearing, objectType=obj_type)

            # Compare to truthed data
            self.assertAlmostEqual(bearing, self.map.object_list[ii].bearing)
            self.assertAlmostEqual(rng, self.map.object_list[ii].rng)
            self.assertEqual(obj_type, self.map.object_list[ii].objectType)

        # check if new detections that match track in object list are handled correctly
        with patch('src.tracking.object.Object.update') as mock_update:
            # add object
            obj_idx = 0
            pub.sendMessage("object detected", rng=rng_list[obj_idx],
                            bearing=bearing_list[obj_idx], objectType=type_list[obj_idx])

            # get rng and bearing
            rng, bearing = rng_list[obj_idx], bearing_list[obj_idx]

            # assert that update is called and with correct parameters
            mock_update.assert_called_once_with(rng, bearing)

    @patch('src.tracking.map.Map._find_object_in_map', return_value = None)
    def test_return_objects(self, mock_find_obj):
        """Tests return objects method of map"""
        # set up objects to add to map
        timeRange = 5000                                       # time used to create rngRange
        rngRange = (0, self.boat_speed * (timeRange/1000))     # range of ranges to return
        bearingRange = (-30, 30)                        # range of bearings to return
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY,
                     ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY, ObjectType.NONE]    # object types

        # set up object lists 
        num_objects = 7
        rng_list = [0] * num_objects
        bearing_list = [0] * num_objects

        correct_object_list = [0] * num_objects     # create empty object list
        num_correct_objects = 0             # counter for correct objects

        # loop over objects to create
        for n in range(num_objects):
            rng = (n*6) + 3     # get range in range from 3 to 39
            bearing = (n*15) - 45   # get bearing in range from -45 to 45

            # add to list to be added to map
            rng_list[n] = rng
            bearing_list[n] = bearing

            # add object to correct object list if with rngRange and bearingRange
            if (rngRange[0] <= rng <= rngRange[1]) and (bearingRange[0] <= bearing <= bearingRange[1]):
                correct_object_list[num_correct_objects] = [rng, bearing, type_list[n]]
                num_correct_objects += 1

        # add objects to map
        for rng, bearing, obj_type in zip(rng_list, bearing_list, type_list):
            pub.sendMessage("object detected", rng=rng, bearing=bearing, objectType=obj_type)

        # get list of objects meeting conditions
        returned_objects = self.map.return_objects(bearingRange, rngRange=rngRange)

        # check that objects match
        for jj, obj in enumerate(correct_object_list[0:num_correct_objects]):
            self.assertAlmostEqual(obj[0], returned_objects[jj].rng)
            self.assertAlmostEqual(obj[1], returned_objects[jj].bearing)
            self.assertEqual(obj[2], returned_objects[jj].objectType)

    @patch('src.tracking.map.Object.predict')
    @patch('src.tracking.map.Map._find_object_in_map', return_value = None)
    def test_update_map(self, mock_find_obj, mock_predict):
        """Tests update map method"""
        # add objects to list 
        num_objects = 2
        rng_list = [5, 44]
        bearing_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]
        for rng, bearing, obj_type in zip(rng_list, bearing_list, type_list):
            pub.sendMessage("object detected", rng=rng, bearing=bearing, objectType=obj_type)

        # call update_map
        self.map.update_map()

        # check if predict was called for all objects in object_list
        self.assertEqual(mock_predict.call_count, num_objects)

    @patch('src.tracking.map.Map._find_object_in_map', return_value = None)
    def test_get_buoys(self, mock_find_obj):
        """Tests get buoys method"""
        # create objects to add to map
        rng_list = [5, 44, 60]
        bearing_list = [-22, 81.5, 60]
        type_list = [ObjectType.BUOY, ObjectType.BOAT, ObjectType.BUOY]

        # set up correct object list 
        correct_object_list = [0] * 2
        num_correct_objects = 0

        # loop through objects and add to map
        for rng, bearing, obj_type in zip(rng_list, bearing_list, type_list):
            pub.sendMessage("object detected", rng=rng, bearing=bearing, objectType=obj_type)

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

    @patch('src.tracking.map.Object.predict')
    def test_find_object_in_map(self, mock_predict):
        """Tests find object in map method"""

        # add objects to list
        rng_list = [5, 44]
        bearing_list = [-22, 81.5]
        type_list = [ObjectType.BUOY, ObjectType.BOAT]

        with patch('src.tracking.map.Map._find_object_in_map', return_value = None):
            for ii, (rng, bearing, obj_type) in enumerate(zip(rng_list, bearing_list, type_list)):
                pub.sendMessage("object detected", rng=rng, bearing=bearing, objectType=obj_type)

        # test case for object not in map
        rng, bearing, obj_type = (0, 0, ObjectType.NONE)               # not in uncertainty range of any object

        # call find object in map
        obj_idx = self.map._find_object_in_map(rng, bearing, obj_type)

        # check that value is None
        self.assertEqual(None, obj_idx)

        # test case for detection w/ exact same coordinates as object in map

        # set value of detection coordinates
        list_idx = 0

        # make arguments for find object in map
        rng, bearing, obj_type = (rng_list[list_idx], bearing_list[list_idx], ObjectType.BUOY)

        # call find object in map
        obj_idx = self.map._find_object_in_map(rng, bearing, obj_type)

        # check that value is correct
        self.assertEqual(list_idx, obj_idx)

        # test case for detection w/ coordinates in uncertainty range of object in map

        # pick object to use
        list_idx = 1

        # find uncertainty range for range and bearing
        rng_uncertainty = self.map.object_list[1].kalman.covar[0, 0]
        bearing_uncertainty = self.map.object_list[1].kalman.covar[1, 1]

        # set value of detection coordinates
        rng = rng_list[list_idx] - (0.5*rng_uncertainty)        # arbitrary value in uncertainty range
        bearing = bearing_list[list_idx] + (0.9*bearing_uncertainty)        # arbitrary value in uncertainty range

        # call find object in map
        obj_idx = self.map._find_object_in_map(rng, bearing, ObjectType.BOAT)

        # check that value is correct
        self.assertEqual(list_idx, obj_idx)


if __name__ == "__main__":
        unittest.main()
