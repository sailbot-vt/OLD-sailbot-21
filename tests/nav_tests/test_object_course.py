import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.nav.course import ObjectCourse

from src.tracking.object import Object
from src.tracking.classification_types import ObjectType

class ObjectCourseTests(unittest.TestCase):
    """Tests the methods in ObjectCourse"""
    def setUp(self):
        self.obj_course = ObjectCourse()

    def test_add_obj(self):
        """Tests add object method of ObjectCourse"""
        # check that list is empty
        self.assertEqual(0, len(self.obj_course.objs))
        
        # generate list of objects
        rng_list = [50, 70, 70, 50]
        bearing_list = [5, 50, 140, 175]
        obj_type = ObjectType.BUOY

        obj_list = [0] * 4
        for ii, (rng, bearing) in enumerate(zip(rng_list, bearing_list)):
            obj_list[ii] = Object(bearing, rng, obj_type)

        # add objects to course (one by one) and check that course updates correctly

        # add first object
        self.obj_course.add_obj(obj_list[0])
        self.assertEqual(2, len(self.obj_course.objs))      # list length should be two
        self.assertEqual(obj_list[0], self.obj_course.objs[0])
        self.assertEqual(obj_list[0], self.obj_course.objs[1])

        # add 2nd object
        self.obj_course.add_obj(obj_list[1])
        self.assertEqual(3, len(self.obj_course.objs))      # list length should be three 
        self.assertEqual(obj_list[0], self.obj_course.objs[0])
        self.assertEqual(obj_list[1], self.obj_course.objs[1])
        self.assertEqual(obj_list[0], self.obj_course.objs[2])

        # add 3rd object
        self.obj_course.add_obj(obj_list[2])
        self.assertEqual(4, len(self.obj_course.objs))      # list length should be four 
        self.assertEqual(obj_list[0], self.obj_course.objs[0])
        self.assertEqual(obj_list[1], self.obj_course.objs[1])
        self.assertEqual(obj_list[2], self.obj_course.objs[2])
        self.assertEqual(obj_list[0], self.obj_course.objs[3])

        # add 4th object
        self.obj_course.add_obj(obj_list[3])
        self.assertEqual(5, len(self.obj_course.objs))      # list length should be five 
        self.assertEqual(obj_list[0], self.obj_course.objs[0])
        self.assertEqual(obj_list[1], self.obj_course.objs[1])
        self.assertEqual(obj_list[2], self.obj_course.objs[2])
        self.assertEqual(obj_list[3], self.obj_course.objs[3])
        self.assertEqual(obj_list[0], self.obj_course.objs[4])

    def test_clear(self):
        """Tests clear method of Object Course"""

        # add elements to objs in Object Course
        self.obj_course.objs = [x for x in range(5)]

        self.assertEqual(5, len(self.obj_course.objs))      # list length should be five 

        # clear list
        self.obj_course.clear()

        self.assertEqual(0, len(self.obj_course.objs))      # list length should be zero 
